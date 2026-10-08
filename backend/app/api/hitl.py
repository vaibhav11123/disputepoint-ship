"""ACK, OVERRIDE, and ESCALATE. No path sets RESOLVED."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from backend.app.db.store import add_audit, update_point
from backend.app.services.ingest import load_point

router = APIRouter()
AGENCIES = {"MCD", "PWD", "NDMC", "DJB", "PWD_FLOOD", "NHAI", "DMRC", "OTHER"}


class AckBody(BaseModel):
    reviewer: str = Field(min_length=1)


class OverrideBody(BaseModel):
    agency: str
    reason: str = Field(min_length=1)
    reviewer: str = Field(min_length=1)


class EscalateBody(BaseModel):
    reason: str = Field(min_length=1)
    reviewer: str = Field(min_length=1)


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
    update_point(conn, point)
    row = _stamp("ACK", body.reviewer, point, {"status": "ACKED"})
    add_audit(conn, row)
    return {"point_id": point_id, "status": "ACKED", "action": "ACK"}


@router.post("/points/{point_id}/override")
def override(point_id: str, body: OverrideBody, request: Request) -> dict[str, Any]:
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
    update_point(conn, point)
    row = _stamp(
        "OVERRIDE",
        body.reviewer,
        point,
        {"human_selected_agency": body.agency, "override_reason": body.reason},
    )
    add_audit(conn, row)
    return row


@router.post("/points/{point_id}/escalate")
def escalate(point_id: str, body: EscalateBody, request: Request) -> dict[str, Any]:
    conn = request.app.state.conn
    point = load_point(conn, point_id)
    if point is None:
        raise _missing(point_id)
    point["escalated"] = True
    point["escalate_reason"] = body.reason
    if point.get("status") != "ACKED":
        point["status"] = "OPEN"
    update_point(conn, point)
    row = _stamp("ESCALATE", body.reviewer, point, {"reason": body.reason, "status": point["status"]})
    add_audit(conn, row)
    return row
