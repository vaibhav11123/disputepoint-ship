"""A-SM / A-OX — lifecycle transitions and ownership×lifecycle legality."""

from backend.app.services.lifecycle import (
    agency_combo_legal,
    can_transition,
    is_forbidden_conflict_to_assigned,
    lifecycle_from_point,
)


def test_forbidden_conflict_path_cannot_jump_to_assigned():
    assert is_forbidden_conflict_to_assigned("RESPONSIBILITY_DISPUTED", "ASSIGNED")
    assert is_forbidden_conflict_to_assigned("HUMAN_REVIEW", "ASSIGNED")
    assert not can_transition("RESPONSIBILITY_DISPUTED", "ASSIGNED", "SYSTEM")
    assert not can_transition("HUMAN_REVIEW", "ASSIGNED", "INCIDENT_COMMANDER")


def test_only_ic_can_officer_confirm():
    assert can_transition("HUMAN_REVIEW", "OFFICER_CONFIRMED", "INCIDENT_COMMANDER")
    assert not can_transition("HUMAN_REVIEW", "OFFICER_CONFIRMED", "EOC_OPERATOR")
    assert not can_transition("HUMAN_REVIEW", "OFFICER_CONFIRMED", "AGENCY_COORDINATOR")


def test_officer_confirmed_then_system_assigns():
    assert can_transition("OFFICER_CONFIRMED", "ASSIGNED", "SYSTEM")


def test_conflict_disputed_requires_null_agency():
    assert agency_combo_legal("CONFLICT", "RESPONSIBILITY_DISPUTED", None)
    assert not agency_combo_legal("CONFLICT", "RESPONSIBILITY_DISPUTED", "MCD")
    assert agency_combo_legal("CONFLICT", "OFFICER_CONFIRMED", "MCD")
    assert not agency_combo_legal("CONFLICT", "OFFICER_CONFIRMED", None)


def test_unknown_clear_illegal():
    assert not agency_combo_legal("UNKNOWN", "RESPONSIBILITY_CLEAR", None)


def test_lifecycle_from_point_escalated_conflict():
    assert (
        lifecycle_from_point({"ownership_state": "CONFLICT", "escalated": True})
        == "HUMAN_REVIEW"
    )
    assert (
        lifecycle_from_point(
            {"ownership_state": "CONFLICT", "escalated": True, "officer_confirmed": True}
        )
        == "OFFICER_CONFIRMED"
    )
