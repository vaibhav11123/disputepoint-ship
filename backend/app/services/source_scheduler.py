"""Bounded background polling via FastAPI lifespan. Disabled in tests by default."""

from __future__ import annotations

import asyncio
import logging
import os
import random
from typing import Any, Callable

from fastapi import FastAPI

from backend.app.db.store import get_rain, list_evidence, list_points, save_rain, update_evidence, update_point
from backend.app.services.evidence_live import verify_corpus
from backend.app.services.geocode import fill_missing
from backend.app.services.ingest import rescore
from backend.app.services.rain import RainUnavailable, refresh
from backend.app.services.source_health import apply_failure, apply_success, sync_rain_record
from backend.app.services.source_registry import SourceRecord, SourceState, utcnow
from backend.app.services.sources import google_flood, imd, nwdp_cwc

log = logging.getLogger("disputepoint.sources")


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    return int(_env_float(name, float(default)))


def polling_enabled(app: FastAPI | None = None) -> bool:
    """Background loops off unless explicitly enabled (or live fetch on)."""
    if app is not None and getattr(app.state, "enable_polling", True) is False:
        return False
    if os.environ.get("DP_SOURCE_POLLING", "").lower() in {"0", "false", "no"}:
        return False
    if os.environ.get("DP_SOURCE_POLLING", "").lower() in {"1", "true", "yes"}:
        return True
    # Default: poll when live fetch requested; tests leave both unset → no pollers
    return os.environ.get("DP_LIVE_FETCH", "").lower() in {"1", "true", "yes"}


def rain_poll_seconds() -> float:
    return max(60.0, _env_float("RAIN_POLL_MINUTES", 15) * 60.0)


def evidence_poll_seconds() -> float:
    return max(60.0, _env_float("DP_EVIDENCE_POLL_MINUTES", 60) * 60.0)


def flood_poll_seconds() -> float:
    return max(60.0, _env_float("DP_FLOOD_POLL_MINUTES", 30) * 60.0)


def source_timeout() -> float:
    return max(1.0, _env_float("DP_SOURCE_TIMEOUT_SECONDS", 10))


def max_backoff() -> float:
    return max(30.0, _env_float("DP_SOURCE_MAX_BACKOFF_SECONDS", 900))


class SourceScheduler:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self._tasks: list[asyncio.Task[Any]] = []
        self._locks: dict[str, asyncio.Lock] = {}
        self._failures: dict[str, int] = {}

    def _lock(self, key: str) -> asyncio.Lock:
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    def _registry(self) -> dict[str, SourceRecord]:
        return self.app.state.source_registry

    def _live_stats(self) -> dict[str, Any]:
        return self.app.state.live_stats

    async def _backoff_sleep(self, key: str, base: float) -> None:
        n = self._failures.get(key, 0)
        delay = min(max_backoff(), base * (2 ** min(n, 6)))
        delay *= 0.5 + random.random()
        await asyncio.sleep(delay)

    def _mark_fail(self, key: str) -> None:
        self._failures[key] = self._failures.get(key, 0) + 1

    def _mark_ok(self, key: str) -> None:
        self._failures[key] = 0

    async def poll_rain_once(self) -> None:
        async with self._lock("open-meteo-rain"):
            conn = self.app.state.conn
            registry = self._registry()
            record = registry["open-meteo-rain"]
            cache = get_rain(conn)
            prev_mm = None if cache is None else cache.get("precip_mm")
            # Do not overwrite active operator scenario or historical replay with live fetch.
            # Still allow refreshing last_live under scenario (handled in API refresh path).
            if cache and cache.get("source") in {"scenario_slider", "historical_replay"}:
                # Stash live under scenario/historical display — never overwrite active mm.
                try:
                    timeout = source_timeout()

                    def _fetch_stash():
                        return refresh(cache=None)

                    obs = await asyncio.wait_for(asyncio.to_thread(_fetch_stash), timeout=timeout + 2)
                except (RainUnavailable, TimeoutError, OSError, ValueError) as exc:
                    apply_failure(record, error_category="network")
                    self._mark_fail("open-meteo-rain")
                    log.info(
                        "rain poll (%s stash) failed: %s",
                        cache.get("source"),
                        type(exc).__name__,
                    )
                    return
                if not obs.get("observation_time"):
                    obs["observation_time"] = obs.get("retrieved_at")
                body = dict(cache)
                body["last_live"] = {k: v for k, v in obs.items() if k != "last_live"}
                save_rain(conn, body)
                apply_success(
                    record,
                    value=obs.get("precip_mm"),
                    observation_time=obs.get("observation_time") or obs.get("retrieved_at"),
                    retrieved_at=obs.get("retrieved_at"),
                    is_synthetic=False,
                    units="mm",
                )
                # Restore display classification after apply_success marked LIVE.
                if cache.get("source") == "historical_replay":
                    sync_rain_record(record, body)
                else:
                    record.source_state = SourceState.LIVE
                self._mark_ok("open-meteo-rain")
                return
            try:
                timeout = source_timeout()

                def _fetch():
                    return refresh(cache=None)

                obs = await asyncio.wait_for(asyncio.to_thread(_fetch), timeout=timeout + 2)
            except (RainUnavailable, TimeoutError, OSError, ValueError) as exc:
                apply_failure(record, error_category="network")
                self._mark_fail("open-meteo-rain")
                log.info("rain poll failed: %s", type(exc).__name__)
                return
            # stamp observation_time if missing
            if not obs.get("observation_time"):
                obs["observation_time"] = obs.get("retrieved_at")
            save_rain(conn, obs)
            apply_success(
                record,
                value=obs.get("precip_mm"),
                observation_time=obs.get("observation_time") or obs.get("retrieved_at"),
                retrieved_at=obs.get("retrieved_at"),
                is_synthetic=bool(obs.get("is_synthetic")),
                units="mm",
            )
            self._mark_ok("open-meteo-rain")
            if obs.get("precip_mm") != prev_mm and "priority_rule" in record.allowed_effects:
                if record.source_state in {SourceState.LIVE, SourceState.STALE, SourceState.SCENARIO}:
                    rescore(conn, float(obs["precip_mm"]))

    async def poll_evidence_once(self) -> None:
        async with self._lock("evidence-live"):
            conn = self.app.state.conn
            registry = self._registry()
            record = registry["evidence-live"]
            try:
                rows = list_evidence(conn)
                updated, stats = await asyncio.to_thread(verify_corpus, rows)
                for row in updated:
                    update_evidence(conn, row["id"], row)
                live = dict(self._live_stats())
                live.update(
                    {
                        "evidence_live_ok": stats["ok"],
                        "evidence_live_fail": stats["fail"],
                        "evidence_live_skipped": stats["skipped"],
                        "live_fetch": True,
                    }
                )
                self.app.state.live_stats = live
                apply_success(
                    record,
                    value={"ok": stats["ok"], "fail": stats["fail"], "skipped": stats["skipped"]},
                    observation_time=utcnow(),
                    retrieved_at=utcnow(),
                    validation_result="ok" if stats["fail"] == 0 else "partial",
                )
                self._mark_ok("evidence-live")
            except Exception as exc:  # noqa: BLE001 — isolate poller
                apply_failure(record, error_category="network")
                self._mark_fail("evidence-live")
                log.info("evidence poll failed: %s", type(exc).__name__)

    async def poll_geo_once(self) -> None:
        """One-shot Nominatim fill in background — never blocks startup."""
        async with self._lock("nominatim-geo"):
            conn = self.app.state.conn
            try:
                before = {(p["id"], p.get("lat"), p.get("lon")) for p in list_points(conn)}
                filled = await asyncio.to_thread(fill_missing, list_points(conn))
                for point in filled:
                    update_point(conn, point)
                after = {(p["id"], p.get("lat"), p.get("lon")) for p in list_points(conn)}
                live = dict(self._live_stats())
                live["geo_fill"] = "nominatim" if before != after else live.get("geo_fill") or "fixture"
                self.app.state.live_stats = live
            except Exception as exc:  # noqa: BLE001
                log.info("geo fill failed: %s", type(exc).__name__)

    async def poll_river_once(self) -> None:
        async with self._lock("nwdp-cwc-yamuna-wl"):
            registry = self._registry()
            record = registry["nwdp-cwc-yamuna-wl"]
            result = await asyncio.to_thread(nwdp_cwc.fetch_observation)
            if result.get("ok"):
                apply_success(
                    record,
                    value=result.get("value"),
                    observation_time=result.get("observation_time"),
                    units=result.get("units"),
                    location_or_station_id=result.get("station_id"),
                )
                record.access_status = "active"
                self._mark_ok("nwdp-cwc-yamuna-wl")
            else:
                apply_failure(record, error_category=str(result.get("error_category") or "unknown"))
                self._mark_fail("nwdp-cwc-yamuna-wl")

    async def poll_imd_once(self) -> None:
        registry = self._registry()
        for source_id, fetcher in (
            ("imd-district-rainfall", imd.fetch_district_rainfall),
            ("imd-district-warning", imd.fetch_district_warning),
            ("imd-aws", imd.fetch_aws),
        ):
            async with self._lock(source_id):
                record = registry[source_id]
                result = await asyncio.to_thread(fetcher)
                if result.get("ok"):
                    apply_success(
                        record,
                        value=result.get("value"),
                        observation_time=result.get("observation_time"),
                        units=result.get("units"),
                        location_or_station_id=result.get("station_id"),
                    )
                    record.access_status = "active"
                    self._mark_ok(source_id)
                else:
                    cat = str(result.get("error_category") or "auth")
                    apply_failure(record, error_category=cat)
                    if cat == "auth":
                        record.source_state = SourceState.UNKNOWN
                        record.access_status = "key_required"
                    self._mark_fail(source_id)

    async def poll_google_once(self) -> None:
        async with self._lock("google-flood-yamuna"):
            record = self._registry()["google-flood-yamuna"]
            result = await asyncio.to_thread(google_flood.fetch_forecast)
            if result.get("ok"):
                apply_success(
                    record,
                    value=result.get("value"),
                    observation_time=result.get("observation_time"),
                    location_or_station_id=result.get("station_id"),
                )
                record.access_status = "active"
            else:
                apply_failure(record, error_category=str(result.get("error_category") or "waitlist"))
                record.source_state = SourceState.UNKNOWN
                record.access_status = "waitlist"

    async def _loop(self, key: str, interval: float, fn: Callable[[], Any]) -> None:
        # Stagger first run slightly so startup stays snappy
        await asyncio.sleep(0.05 + random.random() * 0.2)
        while True:
            try:
                await fn()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001
                log.info("poller %s error: %s", key, type(exc).__name__)
                self._mark_fail(key)
            failures = self._failures.get(key, 0)
            if failures:
                await self._backoff_sleep(key, min(interval, 30.0))
            else:
                await asyncio.sleep(interval)

    def start(self) -> None:
        if not polling_enabled(self.app):
            return
        live = bool(self._live_stats().get("live_fetch"))
        self._tasks.append(asyncio.create_task(self._loop("rain", rain_poll_seconds(), self.poll_rain_once), name="dp-rain-poll"))
        if live:
            self._tasks.append(
                asyncio.create_task(self.poll_geo_once(), name="dp-geo-once"),
            )
            self._tasks.append(
                asyncio.create_task(self._loop("evidence", evidence_poll_seconds(), self.poll_evidence_once), name="dp-evidence-poll"),
            )
        if os.environ.get("DP_FLOOD_CONTEXT_ENABLED", "").lower() in {"1", "true", "yes"}:
            self._tasks.append(
                asyncio.create_task(self._loop("river", flood_poll_seconds(), self.poll_river_once), name="dp-river-poll"),
            )
        if os.environ.get("IMD_API_KEY"):
            self._tasks.append(
                asyncio.create_task(self._loop("imd", rain_poll_seconds(), self.poll_imd_once), name="dp-imd-poll"),
            )
        # Google: only poll if explicitly enabled (access granted)
        if os.environ.get("DP_GOOGLE_FLOOD_ENABLED", "").lower() in {"1", "true", "yes"}:
            self._tasks.append(
                asyncio.create_task(self._loop("google", flood_poll_seconds(), self.poll_google_once), name="dp-google-poll"),
            )

    async def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
        for task in self._tasks:
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._tasks.clear()

