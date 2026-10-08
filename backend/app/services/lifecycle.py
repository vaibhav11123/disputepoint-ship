"""Shared lifecycle transition contract (mirrors frontend/src/lib/lifecycle.ts)."""

from __future__ import annotations

from typing import Final

LIFECYCLE_TRANSITIONS: Final[dict[str, dict[str, list[str]]]] = {
    "INCIDENT_RECEIVED": {"TRIAGED": ["EOC_OPERATOR", "INCIDENT_COMMANDER"]},
    "TRIAGED": {
        "RESPONSIBILITY_CLEAR": ["SYSTEM"],
        "RESPONSIBILITY_DISPUTED": ["SYSTEM"],
    },
    "RESPONSIBILITY_CLEAR": {"ASSIGNED": ["SYSTEM"]},
    "RESPONSIBILITY_DISPUTED": {
        "EVIDENCE_REVIEW": ["EOC_OPERATOR", "INCIDENT_COMMANDER", "AGENCY_COORDINATOR"],
    },
    "EVIDENCE_REVIEW": {
        "HUMAN_REVIEW": ["EOC_OPERATOR", "INCIDENT_COMMANDER", "AGENCY_COORDINATOR"],
    },
    "HUMAN_REVIEW": {"OFFICER_CONFIRMED": ["INCIDENT_COMMANDER"]},
    "OFFICER_CONFIRMED": {"ASSIGNED": ["SYSTEM"]},
    "ASSIGNED": {
        "ACTION_PENDING": ["INCIDENT_COMMANDER", "AGENCY_COORDINATOR"],
        "RESOLVED": ["INCIDENT_COMMANDER", "AGENCY_COORDINATOR"],
    },
    "ACTION_PENDING": {"RESOLVED": ["INCIDENT_COMMANDER", "AGENCY_COORDINATOR"]},
    "RESOLVED": {"AUDITED": ["SYSTEM", "AUDITOR"]},
}

DISPUTE_LIFECYCLES = frozenset(
    {"RESPONSIBILITY_DISPUTED", "EVIDENCE_REVIEW", "HUMAN_REVIEW"},
)

IC = "INCIDENT_COMMANDER"
AGENCIES = {"MCD", "PWD", "NDMC", "DJB", "PWD_FLOOD", "NHAI", "DMRC", "OTHER"}


def can_transition(from_state: str, to_state: str, actor: str) -> bool:
    edges = LIFECYCLE_TRANSITIONS.get(from_state, {})
    allowed = edges.get(to_state)
    if not allowed:
        return False
    return actor in allowed


def is_forbidden_conflict_to_assigned(from_lifecycle: str, to_lifecycle: str) -> bool:
    return from_lifecycle in DISPUTE_LIFECYCLES and to_lifecycle == "ASSIGNED"


def lifecycle_from_point(point: dict) -> str:
    if point.get("officer_confirmed"):
        return "OFFICER_CONFIRMED"
    if point.get("escalated"):
        return "HUMAN_REVIEW"
    ownership = point.get("ownership_state")
    if ownership == "CONFLICT":
        return "RESPONSIBILITY_DISPUTED"
    if ownership == "ASSIGNED":
        return "ASSIGNED"
    return "TRIAGED"


def agency_combo_legal(ownership: str, lifecycle: str, agency: str | None) -> bool:
    if ownership == "CONFLICT":
        if lifecycle in DISPUTE_LIFECYCLES:
            return agency is None
        if lifecycle in {
            "OFFICER_CONFIRMED",
            "ASSIGNED",
            "ACTION_PENDING",
            "RESOLVED",
            "AUDITED",
        }:
            return agency is not None
    if ownership == "ASSIGNED":
        if lifecycle in DISPUTE_LIFECYCLES:
            return False
        return agency is not None
    if ownership == "UNKNOWN":
        if lifecycle == "RESPONSIBILITY_CLEAR":
            return False
        return agency is None
    return True
