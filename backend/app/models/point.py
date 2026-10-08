"""DisputePointSeed (fixtures) and DisputePoint (runtime).

Seed lat/lon may be null. Runtime lat/lon are numbers inside the Delhi bbox.
CONFLICT and UNKNOWN always keep responsible_agency null.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Agency(str, Enum):
    PWD = "PWD"
    MCD = "MCD"
    NDMC = "NDMC"
    IFC = "IFC"
    DDA = "DDA"
    DJB = "DJB"
    RAILWAYS = "RAILWAYS"
    CPWD = "CPWD"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class PointStatus(str, Enum):
    OPEN = "OPEN"
    ACKED = "ACKED"
    RESOLVED = "RESOLVED"


class OwnershipState(str, Enum):
    ASSIGNED = "ASSIGNED"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"


class Provenance(BaseModel):
    model_config = ConfigDict(extra="allow")

    source: str
    source_url: str | None = None
    retrieved_at: datetime
    source_date: str | None = None
    evidence_type: str | None = None
    confidence: float | None = None
    is_synthetic: bool
    is_derived: bool


class ReadinessSignal(BaseModel):
    model_config = ConfigDict(extra="allow")

    state: str = Field(pattern="^(OK|GAP|UNKNOWN)$")
    notes: str | None = None
    is_synthetic: bool


class Geometry(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str = Field(pattern="^(Point|LineString)$")
    coordinates: Any = None


class DisputePointSeed(BaseModel):
    """Fixture row. Null lat/lon is valid. evidence_ids may be empty."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(pattern=r"^dp-[a-z0-9-]+$")
    name: str = Field(min_length=1)
    lat: float | None = Field(ge=28.4, le=28.9)
    lon: float | None = Field(ge=76.8, le=77.5)
    agencies_claimed: list[Agency] = Field(min_length=1)
    evidence_ids: list[str] = Field(default_factory=list)
    recurrence_class: str | None = None
    status: PointStatus
    geo_source: str | None = None
    geo_query: str | None = None
    geo_osm_id: str | None = None
    geo_licence: str | None = None
    provenance: dict[str, Any] | None = None


class DisputePoint(BaseModel):
    """Runtime point. lat/lon are required numbers. evidence_ids min length 1."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(pattern=r"^dp-[a-z0-9-]+$")
    name: str = Field(min_length=1)
    lat: float = Field(ge=28.4, le=28.9)
    lon: float = Field(ge=76.8, le=77.5)
    geometry: Geometry | None = None
    agencies_claimed: list[Agency]
    evidence_ids: list[str] = Field(min_length=1)
    ownership_confidence: float = Field(ge=0, le=1)
    ownership_state: OwnershipState
    responsible_agency: Agency | None = None
    severity: float | None = Field(default=None, ge=0, le=1)
    recurrence_class: str | None = None
    is_underpass: bool | None = None
    is_arterial: bool | None = None
    readiness: ReadinessSignal | None = None
    priority_score: float
    priority_rank: int | None = None
    recommended_action: str | None = None
    sla_hours: float | None = None
    status: PointStatus
    provenance: Provenance

    @model_validator(mode="after")
    def null_agency_unless_assigned(self) -> DisputePoint:
        if self.ownership_state != OwnershipState.ASSIGNED and self.responsible_agency is not None:
            raise ValueError(f"{self.ownership_state.value} requires responsible_agency null")
        return self
