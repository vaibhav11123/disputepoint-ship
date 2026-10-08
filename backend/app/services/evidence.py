"""Load Evidence rows and check quote ⊆ source.

Type weights match LLD §13. This module does not read gitignored L0 bodies.
Callers pass source text when they have it.
"""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

TYPE_WEIGHTS = {
    "COURT_ORDER": 1.0,
    "GOV_ORDER": 0.85,
    "AGENCY_QUOTE": 0.7,
    "PRESS_REPORT": 0.55,
    "SPATIAL_HEURISTIC": 0.35,
}

AGENCIES = {
    "PWD",
    "MCD",
    "NDMC",
    "IFC",
    "DDA",
    "DJB",
    "RAILWAYS",
    "CPWD",
    "OTHER",
    "UNKNOWN",
}


class EvidenceType(str, Enum):
    COURT_ORDER = "COURT_ORDER"
    GOV_ORDER = "GOV_ORDER"
    AGENCY_QUOTE = "AGENCY_QUOTE"
    PRESS_REPORT = "PRESS_REPORT"
    SPATIAL_HEURISTIC = "SPATIAL_HEURISTIC"


class QuoteNotInSource(ValueError):
    pass


class EvidenceRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str = Field(min_length=1)
    type: EvidenceType
    url: str = Field(min_length=1)
    quote: str = Field(min_length=10)
    agency: str | None
    location_span: str | None = None
    source_date: str | None = None
    retrieved_at: datetime
    weight: float = Field(ge=0, le=1)
    needs_review: bool = False
    is_synthetic: bool

    @field_validator("agency")
    @classmethod
    def agency_allowlist(cls, value: str | None) -> str | None:
        if value is not None and value not in AGENCIES:
            raise ValueError("agency must be null or an allowlisted name")
        return value


def quote_subseteq_source(quote: str, source: str) -> bool:
    return len(quote) >= 10 and quote in source


def require_quote_subseteq_source(record: EvidenceRecord, source: str) -> None:
    if not quote_subseteq_source(record.quote, source):
        raise QuoteNotInSource(record.id)


def load_evidence(path: Path) -> list[EvidenceRecord]:
    document = json.loads(path.read_text())
    return [EvidenceRecord.model_validate(row) for row in document["evidence"]]


def evidence_for_ids(records: list[EvidenceRecord], evidence_ids: list[str]) -> list[EvidenceRecord]:
    by_id = {record.id: record for record in records}
    missing = [evidence_id for evidence_id in evidence_ids if evidence_id not in by_id]
    if missing:
        raise KeyError(missing[0])
    return [by_id[evidence_id] for evidence_id in evidence_ids]
