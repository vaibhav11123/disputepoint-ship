"""Read routes: health, points, point, honesty, rain refresh, rain scenario."""

from __future__ import annotations

import json
import logging
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend.app.db.store import clear_rain, get_rain, list_evidence, save_rain
from backend.app.services.ingest import list_points as stored_points
from backend.app.services.ingest import load_point, rescore
from backend.app.services.ownership import THETA, W_NORM
from backend.app.services.priority import U_SEMANTICS, WEIGHTS
from backend.app.services.rain import RainUnavailable, refresh, scenario
from backend.app.services.source_health import apply_failure, apply_success, sync_rain_record
from backend.app.services.source_registry import SourceState, snapshot

router = APIRouter()
log = logging.getLogger("disputepoint.api")

_FETCH_FAIL = frozenset({"fetch_failed", "fetch_forbidden", "fetch_rate_limited"})


class ScenarioBody(BaseModel):
    precip_mm: float = Field(ge=0)


def rain_mode(source: str | None) -> str:
    if source == "open-meteo":
        return "live"
    if source == "scenario_slider":
        return "slider"
    if source == "historical_replay":
        return "replay"
    if source is None:
        return "none"
    return "cache"


def _is_live_observation(rain: dict | None) -> bool:
    if not rain:
        return False
    if rain.get("source") == "open-meteo" and not rain.get("is_synthetic"):
        return True
    return False


def _strip_last_live(rain: dict) -> dict:
    return {key: value for key, value in rain.items() if key != "last_live"}


def _stash_last_live(cache: dict | None) -> dict | None:
    if not cache:
        return None
    if _is_live_observation(cache):
        return _strip_last_live(cache)
    prior = cache.get("last_live")
    return dict(prior) if isinstance(prior, dict) else None


def evidence_counts(rows: list[dict]) -> dict[str, int]:
    counts = {
        "stored": len(rows),
        "verified": 0,
        "unavailable": 0,
        "verification_failed": 0,
        "not_reverified": 0,
        "volunteer": 0,
    }
    for row in rows:
        if row.get("channel") == "VOLUNTEER_REPORTED":
            counts["volunteer"] += 1
        status = row.get("live_status")
        if status is None or status == "":
            counts["not_reverified"] += 1
        elif status == "ok":
            counts["verified"] += 1
        elif status == "quote_miss":
            counts["verification_failed"] += 1
        elif status in _FETCH_FAIL:
            counts["unavailable"] += 1
        else:
            # skipped_* etc. — stored but not a live verification success
            counts["not_reverified"] += 1
    return counts


def _live_stats(request: Request) -> dict:
    return getattr(request.app.state, "live_stats", None) or {
        "live_fetch": False,
        "evidence_live_ok": 0,
        "evidence_live_fail": 0,
        "evidence_live_skipped": 0,
        "geo_fill": "none",
    }


def _registry(request: Request):
    return getattr(request.app.state, "source_registry", None)


@router.get("/health")
def health(request: Request) -> dict:
    rain = get_rain(request.app.state.conn)
    source = None if rain is None else rain.get("source")
    stats = _live_stats(request)
    registry = _registry(request)
    if registry is not None:
        sync_rain_record(registry["open-meteo-rain"], rain)
    rain_record = None if registry is None else registry.get("open-meteo-rain")
    rain_state = None if rain_record is None else rain_record.source_state.value
    scenario_active = source == "scenario_slider"
    replay_state = getattr(request.app.state, "replay_state", None) or {}
    # Authoritative session flag only — rain.source alone must not disagree after exit.
    replay_active = bool(replay_state.get("active"))
    raw_precip = None if rain is None else rain.get("precip_mm")
    precip = None if raw_precip is None else float(raw_precip)
    evidence_rows = list_evidence(request.app.state.conn)
    # When replay session is active, prefer replay mode even if parked with null precip.
    mode = "replay" if replay_active else rain_mode(source)
    return {
        "ok": True,
        "rain_mode": mode,
        "precip_mm": precip,
        "rain_retrieved_at": None if rain is None else rain.get("retrieved_at"),
        "rain_observation_time": None if rain is None else rain.get("observation_time") or rain.get("retrieved_at"),
        "rain_source_state": rain_state,
        "rain_station": None if rain is None else rain.get("station") or rain.get("priority_station"),
        "rain_period_start": None if rain is None else rain.get("period_start"),
        "rain_period_end": None if rain is None else rain.get("period_end"),
        "rain_window_hours": None if rain is None else rain.get("window_hours"),
        "rain_priority_uses": None if rain is None else rain.get("priority_uses"),
        "scenario_active": scenario_active,
        "replay_active": replay_active,
        "replay_id": replay_state.get("replay_id") if replay_active else None,
        "replay_clock": replay_state.get("clock") if replay_active else None,
        "replay_activated_point_ids": list(replay_state.get("activated_point_ids") or []) if replay_active else [],
        "has_last_live": bool(rain and isinstance(rain.get("last_live"), dict)),
        "live_fetch": bool(stats.get("live_fetch")),
        "geo_fill": stats.get("geo_fill") or "none",
        "evidence_live_ok": int(stats.get("evidence_live_ok") or 0),
        "evidence_live_fail": int(stats.get("evidence_live_fail") or 0),
        "evidence_live_skipped": int(stats.get("evidence_live_skipped") or 0),
        "evidence_counts": evidence_counts(evidence_rows),
        "sources": [] if registry is None else snapshot(registry),
    }


@router.get("/points")
def list_points(request: Request) -> dict:
    items = stored_points(request.app.state.conn)
    items.sort(key=lambda point: point["priority_rank"])
    return {"items": items}


@router.get("/points/{point_id}")
def get_point(point_id: str, request: Request) -> dict:
    point = load_point(request.app.state.conn, point_id)
    if point is None:
        raise HTTPException(status_code=404, detail={"code": "DP-404-POINT", "message": "Unknown point"})
    point["advisory"] = True
    return point


@router.post("/rain/refresh")
def rain_refresh(request: Request) -> dict:
    conn = request.app.state.conn
    cache = get_rain(conn)
    registry = _registry(request)
    record = None if registry is None else registry.get("open-meteo-rain")
    replay_state = getattr(request.app.state, "replay_state", None) or {}
    replay_active = bool(replay_state.get("active")) or (cache is not None and cache.get("source") == "historical_replay")
    try:
        from backend.app.services.rain import fetch_open_meteo

        obs = fetch_open_meteo()
    except RainUnavailable as exc:
        if record is not None:
            if cache is not None and cache.get("source") == "open-meteo" and not cache.get("is_synthetic"):
                record.value = cache.get("precip_mm")
                record.observation_time = cache.get("observation_time") or cache.get("retrieved_at")
                record.retrieved_at = cache.get("retrieved_at")
            elif cache is not None and isinstance(cache.get("last_live"), dict):
                prior = cache["last_live"]
                record.value = prior.get("precip_mm")
                record.observation_time = prior.get("observation_time") or prior.get("retrieved_at")
                record.retrieved_at = prior.get("retrieved_at")
            apply_failure(record, error_category="network")
        # Preserve cache; mark STALE via apply_failure when usable observation exists
        raise HTTPException(status_code=503, detail={"code": "DP-503-RAIN", "message": str(exc)}) from exc
    live_body = _strip_last_live(obs)
    if replay_active and cache is not None:
        # Update stash only — keep historical display intact.
        body = dict(cache)
        body["last_live"] = live_body
        save_rain(conn, body)
        if record is not None:
            apply_success(
                record,
                value=obs.get("precip_mm"),
                observation_time=obs.get("observation_time") or obs.get("retrieved_at"),
                retrieved_at=obs.get("retrieved_at"),
                is_synthetic=False,
                units="mm",
            )
            # Display mode remains historical via rain.source / replay_active.
            sync_rain_record(record, body)
        return {**body, "last_live_updated": True, "display_unchanged": True}
    obs["last_live"] = live_body
    save_rain(conn, obs)
    if record is not None:
        apply_success(
            record,
            value=obs.get("precip_mm"),
            observation_time=obs.get("observation_time") or obs.get("retrieved_at"),
            retrieved_at=obs.get("retrieved_at"),
            is_synthetic=False,
            units="mm",
        )
    rescore(conn, obs["precip_mm"])
    return obs


@router.post("/rain/scenario")
def rain_scenario(body: ScenarioBody, request: Request) -> dict:
    conn = request.app.state.conn
    cache = get_rain(conn)
    obs = scenario(body.precip_mm)
    last_live = _stash_last_live(cache)
    if last_live is not None:
        obs["last_live"] = last_live
    save_rain(conn, obs)
    # Scenario is distinct from historical replay — clear session.
    request.app.state.replay_state = {
        "replay_id": (getattr(request.app.state, "replay_state", None) or {}).get("replay_id"),
        "active": False,
        "clock": None,
        "activated_point_ids": [],
    }
    registry = _registry(request)
    if registry is not None:
        apply_success(
            registry["open-meteo-rain"],
            value=obs.get("precip_mm"),
            observation_time=obs.get("observation_time") or obs.get("retrieved_at"),
            retrieved_at=obs.get("retrieved_at"),
            is_synthetic=True,
            units="mm",
        )
    rescore(conn, obs["precip_mm"])
    return get_rain(conn)


@router.post("/rain/clear-scenario")
def rain_clear_scenario(request: Request) -> dict:
    """Restore last live observation, or clear rain entirely — never invent 0.0 mm."""
    conn = request.app.state.conn
    cache = get_rain(conn)
    registry = _registry(request)
    record = None if registry is None else registry.get("open-meteo-rain")
    # Clearing scenario/historical operator state ends replay session.
    prior_replay = getattr(request.app.state, "replay_state", None) or {}
    request.app.state.replay_state = {
        "replay_id": prior_replay.get("replay_id"),
        "active": False,
        "clock": None,
        "activated_point_ids": [],
    }
    last_live = _stash_last_live(cache) if cache and cache.get("source") == "scenario_slider" else None
    if last_live is None and cache and isinstance(cache.get("last_live"), dict):
        last_live = dict(cache["last_live"])
    if last_live is not None:
        restored = dict(last_live)
        restored["last_live"] = _strip_last_live(restored)
        save_rain(conn, restored)
        if record is not None:
            sync_rain_record(record, restored)
        rescore(conn, float(restored.get("precip_mm") or 0))
        return restored
    clear_rain(conn)
    if record is not None:
        sync_rain_record(record, None)
        record.source_state = SourceState.UNAVAILABLE
    # Priority uses 0 input when no observation; health precip stays null
    rescore(conn, 0.0)
    return {"cleared": True, "precip_mm": None, "source": None, "is_synthetic": False}


@router.post("/evidence/refresh")
def evidence_refresh(request: Request) -> dict:
    from backend.app.db.store import list_evidence, update_evidence
    from backend.app.main import live_fetch_enabled
    from backend.app.services.evidence_live import verify_corpus

    stats_state = _live_stats(request)
    if not live_fetch_enabled() and not stats_state.get("live_fetch") and not getattr(request.app.state, "allow_evidence_refresh", False):
        raise HTTPException(
            status_code=503,
            detail={"code": "DP-503-LIVE", "message": "Live evidence refresh requires DP_LIVE_FETCH=1"},
        )
    rows = list_evidence(request.app.state.conn)
    updated, counts = verify_corpus(rows)
    for row in updated:
        update_evidence(request.app.state.conn, row["id"], row)
    stats = {
        "evidence_live_ok": counts["ok"],
        "evidence_live_fail": counts["fail"],
        "evidence_live_skipped": counts["skipped"],
    }
    live = dict(stats_state)
    live.update(stats)
    live["live_fetch"] = True
    request.app.state.live_stats = live
    registry = _registry(request)
    if registry is not None:
        apply_success(
            registry["evidence-live"],
            value=stats,
            observation_time=None,
            validation_result="ok" if counts["fail"] == 0 else "partial",
        )
    return {"ok": True, **stats}


@router.get("/meta/honesty")
def honesty() -> dict:
    return {
        "advisory": True,
        "theta_assign": THETA,
        "w_norm": W_NORM,
        "weights": WEIGHTS,
        "u_semantics": U_SEMANTICS,
        "bedrock_enabled": False,
        "policy_strings": [
            "CONFLICT sets responsible_agency null",
            "U is coordination_uncertainty, not physical severity",
            "No ML runtime in the MVP",
        ],
    }


def install_read_api(app: FastAPI) -> None:
    app.include_router(router)

    @app.middleware("http")
    async def request_log(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid4())
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        log.info(json.dumps({"request_id": request_id, "stage": "api", "path": request.url.path, "status": response.status_code}))
        return response

    @app.exception_handler(RequestValidationError)
    async def bad_schema(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=400, content={"code": "DP-400-SCHEMA", "message": "Request body failed validation"})
