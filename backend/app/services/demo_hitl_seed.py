"""Seed demo HITL outcomes only through the same store rules as the HITL API."""

from __future__ import annotations

import os
import secrets
from datetime import datetime, timezone
from typing import Any

from backend.app.db.store import add_audit, list_points, update_point

# Distinct IC confirms for HUMAN VERIFIED seal on the demo board (allowed AGENCIES only).
_DEMO_CONFIRMS: tuple[tuple[str, str, str, str], ...] = (
    (
        "dp-minto-bridge",
        "NDMC",
        "demo-ic-minto",
        "IC review of NDMC/MCD/PWD/rail narratives; operational responsibility confirmed to NDMC for Minto underpass response.",
    ),
    (
        "dp-azadpur-underpass",
        "MCD",
        "demo-ic-azadpur",
        "IC review of PWD pump vs MCD drain claims; operational responsibility confirmed to MCD for Azadpur underpass follow-up.",
    ),
    (
        "dp-ashram-underpass",
        "PWD",
        "demo-ic-ashram",
        "IC review of arterial underpass evidence; operational responsibility confirmed to PWD for Ashram underpass.",
    ),
    (
        "dp-mehrauli-badarpur-saket",
        "DMRC",
        "demo-ic-saket",
        "IC review of MB Road / Saket metro corridor evidence; operational responsibility confirmed to DMRC for station-approach coordination.",
    ),
)


def seed_demo_acks(conn, *, reviewer: str = "demo-ic") -> list[str]:
    """ACK selected ASSIGNED+OPEN points (same contract as POST /points/{id}/ack).

    Enabled when DP_SEED_DEMO_ACK=1 (default on for local/Ship It demo boards).
    Idempotent: skips points that are no longer OPEN.
    """
    if os.environ.get("DP_SEED_DEMO_ACK", "1").lower() in {"0", "false", "no"}:
        return []
    # Prefer clear PWD assignments already in the curated mix.
    prefer = ("dp-mathura-rd-hc", "dp-bharat-mandapam-tunnel")
    by_id = {p["id"]: p for p in list_points(conn)}
    seeded: list[str] = []
    now = datetime.now(timezone.utc).isoformat()
    for point_id in prefer:
        point = by_id.get(point_id)
        if point is None:
            continue
        if point.get("status") != "OPEN" or point.get("ownership_state") != "ASSIGNED":
            continue
        point = dict(point)
        point["status"] = "ACKED"
        point.pop("evidence", None)
        point.pop("audit", None)
        update_point(conn, point)
        row: dict[str, Any] = {
            "point_id": point_id,
            "action": "ACK",
            "reviewer": reviewer,
            "timestamp": now,
            "previous_recommendation": point.get("recommended_action"),
            "final_decision": {"status": "ACKED", "seed": "demo_hitl_seed"},
        }
        add_audit(conn, row)
        seeded.append(point_id)
    return seeded


def seed_demo_officer_confirms(conn) -> list[str]:
    """Seed OFFICER_CONFIRMED (HUMAN VERIFIED) for curated demo points.

    Same field mutations as POST /points/{id}/confirm. Enabled when
    DP_SEED_DEMO_CONFIRM=1 (default on). Idempotent if already officer_confirmed.
    """
    if os.environ.get("DP_SEED_DEMO_CONFIRM", "1").lower() in {"0", "false", "no"}:
        return []
    by_id = {p["id"]: p for p in list_points(conn)}
    seeded: list[str] = []
    now = datetime.now(timezone.utc).isoformat()
    for point_id, agency, reviewer, reason in _DEMO_CONFIRMS:
        point = by_id.get(point_id)
        if point is None:
            continue
        if point.get("officer_confirmed"):
            continue
        evidence_ids = [eid for eid in (point.get("evidence_ids") or []) if eid][:2]
        if not evidence_ids:
            continue
        previous_ownership = point.get("ownership_state")
        previous_lifecycle = "HUMAN_REVIEW" if point.get("escalated") else previous_ownership
        audit_id = f"AUD-{secrets.token_hex(3).upper()}"
        decision = {
            "actorRole": "INCIDENT_COMMANDER",
            "agency": agency,
            "reason": reason,
            "evidenceIds": evidence_ids,
            "timestamp": now,
            "previousOwnershipState": previous_ownership,
            "previousLifecycleState": previous_lifecycle,
            "decisionType": "OPERATIONAL_RESPONSIBILITY_CONFIRMATION",
            "auditId": audit_id,
            "seed": "demo_hitl_seed",
        }
        point = dict(point)
        point["officer_confirmed"] = True
        point["escalated"] = False
        point["lifecycle_state"] = "ASSIGNED"
        point["human_selected_agency"] = agency
        point["responsible_agency"] = agency
        point["ownership_state"] = "ASSIGNED"
        point["decision_record"] = decision
        if point.get("status") != "ACKED":
            point["status"] = "OPEN"
        point.pop("evidence", None)
        point.pop("audit", None)
        update_point(conn, point)
        row: dict[str, Any] = {
            "point_id": point_id,
            "action": "OFFICER_CONFIRMED",
            "reviewer": reviewer,
            "timestamp": now,
            "previous_recommendation": point.get("recommended_action"),
            "final_decision": decision,
        }
        add_audit(conn, row)
        seeded.append(point_id)
    return seeded
