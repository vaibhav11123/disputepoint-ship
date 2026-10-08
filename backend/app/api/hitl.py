"""ACK, OVERRIDE, ESCALATE, and IC officer confirm. No silent RESOLVED."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from backend.app.db.store import add_audit, update_point
from backend.app.services.ingest import load_point
from backend.app.services.lifecycle import AGENCIES, IC, can_transition, lifecycle_from_point

router = APIRouter()


class AckBody(BaseModel):
    reviewer: str = Field(min_length=1)


class OverrideBody(BaseModel):
    agency: str
    reason: str = Field(min_length=1)
    reviewer: str = Field(min_length=1)
    actor_role: str = "INCIDENT_COMMANDER"


class EscalateBody(BaseModel):
    reason: str = Field(min_length=1)
    reviewer: str = Field(min_length=1)
    actor_role: str = "EOC_OPERATOR"


class ConfirmBody(BaseModel):
    agency: str
    reason: str = Field(min_length=1)
    reviewer: str = Field(min_length=1)
    actor_role: str = IC
    evidence_ids: list[str] = Field(default_factory=list)


def _missing(point_id: str) -> HTTPException:
    return HTTPException(
        status_code=404,
        detail={"code": "DP-404-POINT", "message": f"Unknown point {point_id}"},
    )


def _stamp(action: str, reviewer: str, point: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    return {
        "point_id": point["id"],
        "action": action,
        "reviewer": reviewer,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "previous_recommendation": point.get("recommended_action"),
        "final_decision": extra,
    }


def install_hitl(app: Any) -> None:
    app.include_router(router)


@router.post("/points/{point_id}/ack")
def ack(point_id: str, body: AckBody, request: Request) -> dict[str, Any]:
    conn = request.app.state.conn
    point = load_point(conn, point_id)
    if point is None:
        raise _missing(point_id)
    if point.get("status") != "OPEN" or point.get("ownership_state") != "ASSIGNED":
        raise HTTPException(
            status_code=409,
            detail={"code": "DP-409-ACK", "message": "ACK only when ASSIGNED and OPEN"},
        )
    point["status"] = "ACKED"
    point.pop("evidence", None)
    point.pop("audit", None)
    update_point(conn, point)
    row = _stamp("ACK", body.reviewer, point, {"status": "ACKED"})
    add_audit(conn, row)
    return {"point_id": point_id, "status": "ACKED", "action": "ACK"}


@router.post("/points/{point_id}/override")
def override(point_id: str, body: OverrideBody, request: Request) -> dict[str, Any]:
    if body.actor_role != IC:
        raise HTTPException(
            status_code=403,
            detail={"code": "DP-403-ROLE", "message": "OVERRIDE requires INCIDENT_COMMANDER"},
        )
    if body.agency not in AGENCIES:
        raise HTTPException(
            status_code=422,
            detail={"code": "DP-422-THETA", "message": "Agency is not in the allowed set"},
        )
    conn = request.app.state.conn
    point = load_point(conn, point_id)
    if point is None:
        raise _missing(point_id)
    if point.get("status") != "OPEN":
        raise HTTPException(
            status_code=409,
            detail={"code": "DP-409-ACK", "message": "OVERRIDE only from OPEN"},
        )
    point["recommended_agency"] = point.get("responsible_agency")
    point["human_selected_agency"] = body.agency
    point["override_reason"] = body.reason
    point.pop("evidence", None)
    point.pop("audit", None)
    update_point(conn, point)
    row = _stamp(
        "OVERRIDE",
        body.reviewer,
        point,
        {"human_selected_agency": body.agency, "override_reason": body.reason, "actor_role": body.actor_role},
    )
    add_audit(conn, row)
    return row


@router.post("/points/{point_id}/escalate")
def escalate(point_id: str, body: EscalateBody, request: Request) -> dict[str, Any]:
    conn = request.app.state.conn
    point = load_point(conn, point_id)
    if point is None:
        raise _missing(point_id)
    from_state = lifecycle_from_point(point)
    # Allow escalate into HUMAN_REVIEW from disputed / evidence / already open conflict
    if from_state not in {"RESPONSIBILITY_DISPUTED", "EVIDENCE_REVIEW", "TRIAGED", "ASSIGNED", "HUMAN_REVIEW"}:
        if not can_transition(from_state, "HUMAN_REVIEW", body.actor_role):
            # CONFLICT points report RESPONSIBILITY_DISPUTED — always allow escalate for ops
            if point.get("ownership_state") != "CONFLICT":
                raise HTTPException(
                    status_code=409,
                    detail={"code": "DP-409-LIFECYCLE", "message": f"Cannot escalate from {from_state}"},
                )
    point["escalated"] = True
    point["escalate_reason"] = body.reason
    point["lifecycle_state"] = "HUMAN_REVIEW"
    if point.get("status") != "ACKED":
        point["status"] = "OPEN"
    point.pop("evidence", None)
    point.pop("audit", None)
    update_point(conn, point)
    row = _stamp(
        "ESCALATE",
        body.reviewer,
        point,
        {"reason": body.reason, "status": point["status"], "lifecycle_state": "HUMAN_REVIEW"},
    )
    add_audit(conn, row)
    return row


@router.post("/points/{point_id}/confirm")
def confirm_responsibility(point_id: str, body: ConfirmBody, request: Request) -> dict[str, Any]:
    """IC-only: HUMAN_REVIEW → OFFICER_CONFIRMED → ASSIGNED with DecisionRecord."""
    if body.actor_role != IC:
        raise HTTPException(
            status_code=403,
            detail={"code": "DP-403-ROLE", "message": "Confirm requires INCIDENT_COMMANDER"},
        )
    if body.agency not in AGENCIES:
        raise HTTPException(
            status_code=422,
            detail={"code": "DP-422-THETA", "message": "Agency is not in the allowed set"},
        )
    if not body.evidence_ids:
        raise HTTPException(
            status_code=422,
            detail={"code": "DP-422-EVIDENCE", "message": "At least one evidence id required"},
        )
    conn = request.app.state.conn
    point = load_point(conn, point_id)
    if point is None:
        raise _missing(point_id)
    if not point.get("escalated") and point.get("ownership_state") != "CONFLICT":
        raise HTTPException(
            status_code=409,
            detail={"code": "DP-409-LIFECYCLE", "message": "Confirm only after escalate / dispute"},
        )
    previous_ownership = point.get("ownership_state")
    previous_lifecycle = lifecycle_from_point(point)
    if previous_lifecycle not in {"HUMAN_REVIEW", "RESPONSIBILITY_DISPUTED", "EVIDENCE_REVIEW"}:
        if previous_lifecycle != "HUMAN_REVIEW" and not point.get("escalated"):
            raise HTTPException(
                status_code=409,
                detail={"code": "DP-409-LIFECYCLE", "message": f"Cannot confirm from {previous_lifecycle}"},
            )
    audit_id = f"AUD-{secrets.token_hex(3).upper()}"
    decision = {
        "actorRole": IC,
        "agency": body.agency,
        "reason": body.reason,
        "evidenceIds": body.evidence_ids,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "previousOwnershipState": previous_ownership,
        "previousLifecycleState": previous_lifecycle,
        "decisionType": "OPERATIONAL_RESPONSIBILITY_CONFIRMATION",
        "auditId": audit_id,
    }
    # Human confirmation sets operational agency without rewriting ownership_state to invent clarity:
    # store human_selected + officer_confirmed; keep CONFLICT visible until assigned via human path.
    point["officer_confirmed"] = True
    point["lifecycle_state"] = "ASSIGNED"
    point["human_selected_agency"] = body.agency
    point["responsible_agency"] = body.agency
    point["ownership_state"] = "ASSIGNED"
    point["decision_record"] = decision
    point.pop("evidence", None)
    point.pop("audit", None)
    update_point(conn, point)
    row = _stamp("OFFICER_CONFIRMED", body.reviewer, point, decision)
    add_audit(conn, row)
    return {"point_id": point_id, "action": "OFFICER_CONFIRMED", "decision": decision, **row}
