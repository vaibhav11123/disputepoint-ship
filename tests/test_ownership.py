"""T-OWN-θ and T-OWN-CF-NULL. CONFLICT overrides a score that would otherwise assign."""

from backend.app.models.point import Agency, OwnershipState
from backend.app.services.ownership import THETA, EvidenceScore, decide


def test_t_own_theta_below_threshold_forces_null_agency() -> None:
    # One court order is weight 1.0; confidence = 1.0 / 2.0 = 0.5 < 0.65.
    decision = decide([EvidenceScore(type="COURT_ORDER", agency="PWD")])
    assert decision.ownership_confidence < THETA
    assert decision.ownership_state is OwnershipState.UNKNOWN
    assert decision.responsible_agency is None


def test_t_own_theta_at_threshold_assigns() -> None:
    # 1.0 + 0.35 = 1.35; 1.35 / 2.0 = 0.675 >= 0.65. No close second agency.
    decision = decide(
        [
            EvidenceScore(type="COURT_ORDER", agency="PWD"),
            EvidenceScore(type="SPATIAL_HEURISTIC", agency="PWD"),
        ]
    )
    assert decision.ownership_confidence >= THETA
    assert decision.ownership_state is OwnershipState.ASSIGNED
    assert decision.responsible_agency is Agency.PWD


def test_t_own_cf_null_conflict_overrides_assignment() -> None:
    # Each side sums to 1.55 (court + press). Confidence of the top is 0.775 >= θ,
    # and the two sums are within 0.1 and both above 0.4, so the result is CONFLICT.
    items = [
        EvidenceScore(type="COURT_ORDER", agency="PWD"),
        EvidenceScore(type="PRESS_REPORT", agency="PWD"),
        EvidenceScore(type="COURT_ORDER", agency="MCD"),
        EvidenceScore(type="PRESS_REPORT", agency="MCD"),
    ]
    decision = decide(items)
    assert decision.ownership_confidence >= THETA
    assert decision.ownership_state is OwnershipState.CONFLICT
    assert decision.responsible_agency is None


def test_states_are_only_assigned_conflict_or_unknown() -> None:
    samples = [
        decide([]),
        decide([EvidenceScore(type="PRESS_REPORT", agency="NDMC")]),
        decide(
            [
                EvidenceScore(type="COURT_ORDER", agency="DJB"),
                EvidenceScore(type="GOV_ORDER", agency="DJB"),
            ]
        ),
        decide(
            [
                EvidenceScore(type="GOV_ORDER", agency="IFC"),
                EvidenceScore(type="GOV_ORDER", agency="DDA"),
            ]
        ),
    ]
    allowed = {OwnershipState.ASSIGNED, OwnershipState.CONFLICT, OwnershipState.UNKNOWN}
    for decision in samples:
        assert decision.ownership_state in allowed
        if decision.responsible_agency is not None:
            assert decision.ownership_state is OwnershipState.ASSIGNED
            assert decision.ownership_confidence >= THETA


def test_null_agency_evidence_does_not_assign() -> None:
    decision = decide([EvidenceScore(type="COURT_ORDER", agency=None)])
    assert decision.responsible_agency is None
    assert decision.ownership_state is OwnershipState.UNKNOWN
