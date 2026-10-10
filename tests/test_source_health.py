"""Source-state freshness contract."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from backend.app.services.source_health import apply_failure, apply_success, compute_freshness
from backend.app.services.source_registry import SourceState, new_registry, utcnow


def test_freshness_live_stale_unavailable_scenario() -> None:
    now = datetime.now(timezone.utc)
    fresh = (now - timedelta(minutes=10)).isoformat().replace("+00:00", "Z")
    old = (now - timedelta(hours=10)).isoformat().replace("+00:00", "Z")
    assert compute_freshness(fresh, freshness_limit_seconds=3600) == SourceState.LIVE
    assert compute_freshness(old, freshness_limit_seconds=3600) == SourceState.STALE
    assert compute_freshness(None, freshness_limit_seconds=3600, has_observation=False) == SourceState.UNAVAILABLE
    assert compute_freshness(fresh, freshness_limit_seconds=3600, is_synthetic=True) == SourceState.SCENARIO


def test_failure_preserves_last_good_as_stale() -> None:
    registry = new_registry()
    record = registry["open-meteo-rain"]
    apply_success(record, value=12.5, observation_time=utcnow(), units="mm")
    assert record.source_state in {SourceState.LIVE, SourceState.STALE}
    prior = record.value
    apply_failure(record, error_category="network")
    assert record.value == prior
    assert record.source_state == SourceState.STALE
    assert record.last_error_category == "network"
    assert record.retrieval_ok is False
