"""T-PROV-01. Fixture rows keep url, quote, and provenance fields. Quotes must sit inside a source string."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.app.services.evidence import (
    TYPE_WEIGHTS,
    EvidenceRecord,
    QuoteNotInSource,
    evidence_for_ids,
    load_evidence,
    quote_subseteq_source,
    require_quote_subseteq_source,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "data" / "fixtures" / "evidence.json"
POINTS_PATH = ROOT / "data" / "fixtures" / "points.json"


def test_t_prov_01_fixture_rows_have_provenance_fields() -> None:
    records = load_evidence(EVIDENCE_PATH)
    assert records
    for record in records:
        assert record.url
        assert len(record.quote) >= 10
        assert record.retrieved_at is not None
        assert isinstance(record.is_synthetic, bool)
        assert record.weight == TYPE_WEIGHTS[record.type.value]


def test_each_seed_point_has_evidence_with_url_and_quote() -> None:
    records = load_evidence(EVIDENCE_PATH)
    points = json.loads(POINTS_PATH.read_text())["points"]
    assert len(points) >= 12
    for point in points:
        attached = evidence_for_ids(records, point["evidence_ids"])
        assert attached
        assert all(item.url and len(item.quote) >= 10 for item in attached)


def test_quote_must_be_substring_of_source() -> None:
    source = "the storm water drain from India Gate to Yamuna River is sectioned in six jurisdictions"
    quote = "six jurisdictions"
    assert quote_subseteq_source(quote, source)
    record = EvidenceRecord.model_validate(
        {
            "id": "ev-subset",
            "type": "PRESS_REPORT",
            "url": "https://example.invalid/source",
            "quote": quote,
            "agency": None,
            "retrieved_at": "2026-10-08T08:00:00Z",
            "weight": 0.55,
            "is_synthetic": True,
        }
    )
    require_quote_subseteq_source(record, source)
    with pytest.raises(QuoteNotInSource):
        require_quote_subseteq_source(record, "a different paragraph that does not contain the quote")


def test_quote_shorter_than_ten_characters_is_rejected() -> None:
    with pytest.raises(ValueError):
        EvidenceRecord.model_validate(
            {
                "id": "ev-short",
                "type": "PRESS_REPORT",
                "url": "https://example.invalid/source",
                "quote": "too short",
                "agency": None,
                "retrieved_at": "2026-10-08T08:00:00Z",
                "weight": 0.55,
                "is_synthetic": True,
            }
        )
