"""Source registry — states, permitted effects, and in-memory health records."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SourceState(str, Enum):
    LIVE = "LIVE"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"
    SCENARIO = "SCENARIO"


class AccessStatus(str, Enum):
    ACTIVE = "active"
    INVESTIGATING = "investigating"
    WAITLIST = "waitlist"
    KEY_REQUIRED = "key_required"
    BLOCKED = "blocked"


class SourceRecord(BaseModel):
    source_id: str
    source_name: str
    access_status: str
    source_state: SourceState = SourceState.UNKNOWN
    observation_time: str | None = None
    retrieved_at: str | None = None
    last_attempt_at: str | None = None
    last_success_at: str | None = None
    units: str | None = None
    freshness_limit_seconds: int | None = None
    last_error_category: str | None = None
    allowed_effects: list[str] = Field(default_factory=list)
    value: Any = None
    location_or_station_id: str | None = None
    source_reference: str | None = None
    retrieval_ok: bool | None = None


class ObservationProvenance(BaseModel):
    source_id: str
    location_or_station_id: str | None = None
    observation_time: str | None = None
    retrieved_at: str | None = None
    value: Any = None
    units: str | None = None
    source_reference: str | None = None
    validation_result: str = "ok"
    freshness_state: SourceState = SourceState.UNKNOWN


# Freshness defaults (observation age, not poll interval)
OPEN_METEO_FRESHNESS_S = 6 * 3600  # matches 6h precip window
EVIDENCE_FRESHNESS_S = 24 * 3600
DEFAULT_CONTEXT_FRESHNESS_S = 6 * 3600

_SEED: list[dict[str, Any]] = [
    {
        "source_id": "open-meteo-rain",
        "source_name": "Open-Meteo rainfall",
        "access_status": AccessStatus.ACTIVE.value,
        "source_state": SourceState.UNKNOWN,
        "units": "mm",
        "freshness_limit_seconds": OPEN_METEO_FRESHNESS_S,
        "allowed_effects": ["priority_rule"],
        "location_or_station_id": "delhi-centroid",
        "source_reference": "https://api.open-meteo.com",
    },
    {
        "source_id": "evidence-live",
        "source_name": "Evidence URL verify",
        "access_status": AccessStatus.ACTIVE.value,
        "source_state": SourceState.UNKNOWN,
        "freshness_limit_seconds": EVIDENCE_FRESHNESS_S,
        "allowed_effects": ["context"],
        "source_reference": "fixture URLs",
    },
    {
        "source_id": "imd-district-rainfall",
        "source_name": "IMD district rainfall",
        "access_status": AccessStatus.KEY_REQUIRED.value,
        "source_state": SourceState.UNKNOWN,
        "units": "mm",
        "freshness_limit_seconds": 24 * 3600,
        "allowed_effects": ["context"],
        "source_reference": "https://api.imd.gov.in/api/v1/districtrainfall",
    },
    {
        "source_id": "imd-district-warning",
        "source_name": "IMD district warnings",
        "access_status": AccessStatus.KEY_REQUIRED.value,
        "source_state": SourceState.UNKNOWN,
        "freshness_limit_seconds": 12 * 3600,
        "allowed_effects": ["context"],
        "source_reference": "https://api.imd.gov.in/api/v1/districtwarning",
    },
    {
        "source_id": "imd-aws",
        "source_name": "IMD AWS/ARG",
        "access_status": AccessStatus.KEY_REQUIRED.value,
        "source_state": SourceState.UNKNOWN,
        "units": "varies",
        "freshness_limit_seconds": 3600,
        "allowed_effects": ["context"],
        "source_reference": "https://api.imd.gov.in/api/v1/aws_data",
    },
    {
        "source_id": "nwdp-cwc-yamuna-wl",
        "source_name": "NWDP/CWC Yamuna water level",
        "access_status": AccessStatus.INVESTIGATING.value,
        "source_state": SourceState.UNKNOWN,
        "units": "m",
        "freshness_limit_seconds": DEFAULT_CONTEXT_FRESHNESS_S,
        "allowed_effects": ["context"],
        "source_reference": "https://nwdp.nwic.gov.in/",
    },
    {
        "source_id": "google-flood-yamuna",
        "source_name": "Google Flood Forecasting",
        "access_status": AccessStatus.WAITLIST.value,
        "source_state": SourceState.UNKNOWN,
        "freshness_limit_seconds": DEFAULT_CONTEXT_FRESHNESS_S,
        "allowed_effects": ["context"],
        "source_reference": "https://floodforecasting.googleapis.com",
    },
]


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def new_registry() -> dict[str, SourceRecord]:
    return {row["source_id"]: SourceRecord.model_validate(deepcopy(row)) for row in _SEED}


def snapshot(registry: dict[str, SourceRecord]) -> list[dict[str, Any]]:
    return [record.model_dump(mode="json") for record in registry.values()]
