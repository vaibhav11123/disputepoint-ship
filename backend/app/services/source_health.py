"""Freshness and retrieval status updates for the source registry."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.app.services.source_registry import (
    ObservationProvenance,
    SourceRecord,
    SourceState,
    parse_iso,
    utcnow,
)


def compute_freshness(
    observation_time: str | None,
    *,
    freshness_limit_seconds: int | None,
    is_synthetic: bool = False,
    has_observation: bool = True,
) -> SourceState:
    if is_synthetic:
        return SourceState.SCENARIO
    if not has_observation or observation_time is None:
        return SourceState.UNAVAILABLE
    limit = freshness_limit_seconds
    if limit is None:
        return SourceState.LIVE
    observed = parse_iso(observation_time)
    if observed is None:
        return SourceState.UNAVAILABLE
    now = datetime.now(timezone.utc)
    if observed.tzinfo is None:
        observed = observed.replace(tzinfo=timezone.utc)
    age = (now - observed).total_seconds()
    if age <= limit:
        return SourceState.LIVE
    return SourceState.STALE


def apply_success(
    record: SourceRecord,
    *,
    value: Any,
    observation_time: str | None,
    retrieved_at: str | None = None,
    is_synthetic: bool = False,
    units: str | None = None,
    location_or_station_id: str | None = None,
    validation_result: str = "ok",
) -> ObservationProvenance:
    retrieved = retrieved_at or utcnow()
    observed = observation_time or retrieved
    record.last_attempt_at = retrieved
    record.last_success_at = retrieved
    record.retrieved_at = retrieved
    record.observation_time = observed
    record.value = value
    record.retrieval_ok = True
    record.last_error_category = None
    if units is not None:
        record.units = units
    if location_or_station_id is not None:
        record.location_or_station_id = location_or_station_id
    state = compute_freshness(
        observed,
        freshness_limit_seconds=record.freshness_limit_seconds,
        is_synthetic=is_synthetic,
        has_observation=True,
    )
    record.source_state = state
    return ObservationProvenance(
        source_id=record.source_id,
        location_or_station_id=record.location_or_station_id,
        observation_time=observed,
        retrieved_at=retrieved,
        value=value,
        units=record.units,
        source_reference=record.source_reference,
        validation_result=validation_result,
        freshness_state=state,
    )


def apply_failure(
    record: SourceRecord,
    *,
    error_category: str,
    keep_last_good: bool = True,
) -> None:
    """Record a failed retrieval. Preserve last usable observation when present."""
    record.last_attempt_at = utcnow()
    record.retrieval_ok = False
    record.last_error_category = error_category
    has_value = record.value is not None or record.observation_time is not None
    if keep_last_good and has_value and record.source_state != SourceState.SCENARIO:
        # Recompute freshness on cached observation; do not wipe value.
        if record.source_state != SourceState.SCENARIO:
            record.source_state = compute_freshness(
                record.observation_time,
                freshness_limit_seconds=record.freshness_limit_seconds,
                is_synthetic=False,
                has_observation=True,
            )
            if record.source_state == SourceState.LIVE:
                # Observation still within limit but retrieval failed → STALE presentation
                # only if we want retrieval failure to surface; plan: STALE when refresh fails
                # but usable cache remains.
                record.source_state = SourceState.STALE
        return
    if not has_value:
        record.source_state = SourceState.UNAVAILABLE


def sync_rain_record(record: SourceRecord, rain: dict[str, Any] | None) -> None:
    """Seed or refresh open-meteo-rain from rain_cache without a network call."""
    if rain is None:
        record.value = None
        record.observation_time = None
        record.source_state = SourceState.UNAVAILABLE
        return
    # Fixture dry seed is not a live Open-Meteo observation and not an operator scenario.
    if rain.get("source") == "fixture":
        record.value = rain.get("precip_mm")
        record.observation_time = rain.get("observation_time") or rain.get("retrieved_at")
        record.retrieved_at = rain.get("retrieved_at")
        record.source_state = SourceState.UNAVAILABLE
        record.access_status = "active"
        return
    # Historical replay uses stored station totals — not Open-Meteo LIVE.
    if rain.get("source") == "historical_replay":
        record.value = rain.get("precip_mm")
        record.observation_time = rain.get("observation_time") or rain.get("retrieved_at")
        record.retrieved_at = rain.get("retrieved_at")
        record.source_state = SourceState.SCENARIO
        record.access_status = "active"
        record.retrieval_ok = None
        record.last_error_category = None
        return
    synthetic = rain.get("source") == "scenario_slider" or (
        bool(rain.get("is_synthetic")) and rain.get("source") != "open-meteo"
    )
    observed = rain.get("observation_time") or rain.get("retrieved_at")
    # Cache re-seed must not erase a failed live refresh (STALE / last observation).
    if (
        not synthetic
        and rain.get("source") == "open-meteo"
        and record.retrieval_ok is False
        and record.last_error_category
    ):
        record.value = rain.get("precip_mm")
        record.observation_time = observed
        record.retrieved_at = rain.get("retrieved_at")
        record.source_state = SourceState.STALE
        return
    apply_success(
        record,
        value=rain.get("precip_mm"),
        observation_time=observed,
        retrieved_at=rain.get("retrieved_at"),
        is_synthetic=synthetic,
        units="mm",
        location_or_station_id="delhi-centroid",
        validation_result="ok",
    )


def rain_observation_time(payload: dict[str, Any]) -> str | None:
    """Prefer explicit observation_time; else last hourly slot; else retrieved_at."""
    if payload.get("observation_time"):
        return str(payload["observation_time"])
    hourly = (payload.get("hourly") or {}).get("time") or []
    if hourly:
        # Open-Meteo returns local Asia/Kolkata times without Z — treat as IST wall clock → store as retrieved.
        return str(hourly[-1])
    return payload.get("retrieved_at")
