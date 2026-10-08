"""T-RANK-01. U is coordination uncertainty. Hide-synthetic zeros G."""

from types import SimpleNamespace

import pytest

from backend.app.services.priority import U_SEMANTICS, WEIGHTS, priority


def _point(**overrides: object) -> SimpleNamespace:
    base = dict(
        severity=0.4,
        is_arterial=False,
        is_underpass=False,
        recurrence_class="chronic",
        ownership_confidence=0.2,
        ownership_state="UNKNOWN",
        readiness={"state": "GAP", "is_synthetic": True},
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def test_t_rank_01_components_include_u_as_coordination() -> None:
    result = priority(_point(), precip_mm=40)
    assert set(result.components) == {"R", "S", "C", "Q", "U", "G"}
    assert "flood" not in U_SEMANTICS.lower()
    assert any(U_SEMANTICS in line for line in result.explanation)
    assert result.components["U"] == 0.8
    assert abs(result.score - sum(WEIGHTS[key] * result.components[key] for key in WEIGHTS)) < 1e-9


def test_conflict_raises_coordination_uncertainty_floor() -> None:
    calm = priority(_point(ownership_confidence=0.9, ownership_state="ASSIGNED"), precip_mm=0)
    conflict = priority(_point(ownership_confidence=0.9, ownership_state="CONFLICT"), precip_mm=0)
    assert calm.components["U"] == pytest.approx(0.1)
    assert conflict.components["U"] == 0.8
    assert conflict.score > calm.score


def test_hide_synthetic_zeros_g() -> None:
    shown = priority(_point(), precip_mm=0, hide_synthetic=False)
    hidden = priority(_point(), precip_mm=0, hide_synthetic=True)
    assert shown.components["G"] == 1.0
    assert hidden.components["G"] == 0.0
    assert hidden.score < shown.score


def test_counterfactuals_present_and_zero_rain_drops_score() -> None:
    result = priority(_point(), precip_mm=40)
    factors = {row["factor"] for row in result.counterfactuals}
    assert factors == {"zero_R", "resolve_U", "zero_Q", "zero_G"}
    zero_r = next(row for row in result.counterfactuals if row["factor"] == "zero_R")
    assert zero_r["score_after"] < zero_r["score_before"]
    assert "flood risk" not in zero_r["copy"]
