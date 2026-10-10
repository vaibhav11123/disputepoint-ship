"""Seed demo HITL outcomes only through the same store rules as the HITL API."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from backend.app.db.store import add_audit, list_points, update_point


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
