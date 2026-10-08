"""Seed validates. A runtime point with null lat does not."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from backend.app.models import DisputePoint, DisputePointSeed

ROOT = Path(__file__).resolve().parents[1]
POINTS = ROOT / "data" / "fixtures" / "points.json"
SEED_SCHEMA = ROOT / "docs" / "schemas" / "DisputePointSeed.schema.json"
RUNTIME_SCHEMA = ROOT / "docs" / "schemas" / "DisputePoint.schema.json"


def _runtime(**overrides: object) -> dict:
    payload = {
        "id": "dp-schema-bound",
        "name": "Schema bound double",
        "lat": 28.4,
        "lon": 76.8,
        "agencies_claimed": ["PWD"],
        "evidence_ids": ["ev-schema-bound"],
        "ownership_confidence": 0.9,
        "ownership_state": "ASSIGNED",
        "responsible_agency": "PWD",
        "priority_score": 0.5,
        "status": "OPEN",
        "provenance": {
            "source": "unit",
            "retrieved_at": "2026-10-08T08:00:00Z",
            "is_synthetic": True,
            "is_derived": True,
        },
    }
    payload.update(overrides)
    return payload


def test_seed_fixture_validates_and_covers_twelve_points() -> None:
    document = json.loads(POINTS.read_text())
    points = document["points"]
    assert len(points) >= 12
    for raw in points:
        seed = DisputePointSeed.model_validate(raw)
        assert seed.id.startswith("dp-")
        if seed.lat is not None:
            assert 28.4 <= seed.lat <= 28.9
        if seed.lon is not None:
            assert 76.8 <= seed.lon <= 77.5


def test_seed_schema_allows_null_geo_runtime_schema_does_not() -> None:
    seed_schema = json.loads(SEED_SCHEMA.read_text())
    runtime_schema = json.loads(RUNTIME_SCHEMA.read_text())
    assert "null" in seed_schema["properties"]["lat"]["type"]
    assert runtime_schema["properties"]["lat"]["type"] == "number"
    assert runtime_schema["properties"]["evidence_ids"]["minItems"] == 1


def test_runtime_null_lat_fails() -> None:
    with pytest.raises(ValidationError):
        DisputePoint.model_validate(_runtime(lat=None))


def test_runtime_null_lon_fails() -> None:
    with pytest.raises(ValidationError):
        DisputePoint.model_validate(_runtime(lon=None))


def test_runtime_outside_bbox_fails() -> None:
    with pytest.raises(ValidationError):
        DisputePoint.model_validate(_runtime(lat=0))


def test_runtime_empty_evidence_fails() -> None:
    with pytest.raises(ValidationError):
        DisputePoint.model_validate(_runtime(evidence_ids=[]))


def test_conflict_rejects_agency() -> None:
    with pytest.raises(ValidationError):
        DisputePoint.model_validate(
            _runtime(ownership_state="CONFLICT", responsible_agency="MCD", ownership_confidence=0.9)
        )


def test_conflict_with_null_agency_validates() -> None:
    point = DisputePoint.model_validate(
        _runtime(ownership_state="CONFLICT", responsible_agency=None, ownership_confidence=0.9)
    )
    assert point.responsible_agency is None


def test_seed_numeric_outside_bbox_fails() -> None:
    raw = json.loads(POINTS.read_text())["points"][0]
    raw["lat"] = 0
    raw["lon"] = 0
    with pytest.raises(ValidationError):
        DisputePointSeed.model_validate(raw)
