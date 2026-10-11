"""A-F4 / A-F9 — IC confirm creates DecisionRecord and assignment."""

import asyncio
import json

from backend.app.main import create_app


def call(app, method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
    payload = json.dumps(body).encode() if body is not None else b""
    captured: dict = {}

    async def run() -> None:
        sent: list[dict] = []

        async def receive():
            return {"type": "http.request", "body": payload, "more_body": False}

        async def send(message):
            sent.append(message)

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": method,
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [(b"content-type", b"application/json")] if body is not None else [],
            "scheme": "http",
            "server": ("127.0.0.1", 8000),
            "client": ("127.0.0.1", 1234),
        }
        await app(scope, receive, send)
        raw = b"".join(part.get("body", b"") for part in sent if part["type"] == "http.response.body")
        captured["status"] = next(part["status"] for part in sent if part["type"] == "http.response.start")
        captured["body"] = json.loads(raw) if raw else {}

    asyncio.run(run())
    return captured["status"], captured["body"]


def test_confirm_requires_ic_role():
    app = create_app()
    status, listing = call(app, "GET", "/points")
    assert status == 200
    conflict = next(p for p in listing["items"] if p["ownership_state"] == "CONFLICT")
    status, detail = call(app, "GET", f"/points/{conflict['id']}")
    assert status == 200
    evidence_ids = [e["id"] for e in detail.get("evidence", [])][:1] or ["ev-missing"]
    call(
        app,
        "POST",
        f"/points/{conflict['id']}/escalate",
        {"reason": "Competing agency claims", "reviewer": "op-1", "actor_role": "EOC_OPERATOR"},
    )
    denied, body = call(
        app,
        "POST",
        f"/points/{conflict['id']}/confirm",
        {
            "agency": "MCD",
            "reason": "Reviewed jurisdiction",
            "reviewer": "op-1",
            "actor_role": "EOC_OPERATOR",
            "evidence_ids": evidence_ids,
        },
    )
    assert denied == 403
    assert body["detail"]["code"] == "DP-403-ROLE"


def test_confirm_creates_assignment_and_audit():
    app = create_app()
    status, listing = call(app, "GET", "/points")
    assert status == 200
    conflict = next(p for p in listing["items"] if p["id"] == "dp-purana-quila" or p["ownership_state"] == "CONFLICT")
    status, detail = call(app, "GET", f"/points/{conflict['id']}")
    evidence_ids = [e["id"] for e in detail.get("evidence", [])][:2]
    assert evidence_ids, "fixture must have evidence for confirm"
    call(
        app,
        "POST",
        f"/points/{conflict['id']}/escalate",
        {"reason": "Competing agency claims", "reviewer": "ic-1"},
    )
    ok, body = call(
        app,
        "POST",
        f"/points/{conflict['id']}/confirm",
        {
            "agency": "MCD",
            "reason": "Jurisdiction record reviewed and confirmed",
            "reviewer": "ic-1",
            "actor_role": "INCIDENT_COMMANDER",
            "evidence_ids": evidence_ids,
        },
    )
    assert ok == 200, body
    assert body["action"] == "OFFICER_CONFIRMED"
    assert body["decision"]["agency"] == "MCD"
    assert body["decision"]["decisionType"] == "OPERATIONAL_RESPONSIBILITY_CONFIRMATION"
    assert body["decision"]["auditId"].startswith("AUD-")
    status, after = call(app, "GET", f"/points/{conflict['id']}")
    assert status == 200
    assert after["ownership_state"] == "ASSIGNED"
    assert after["responsible_agency"] == "MCD"
    assert after["officer_confirmed"] is True
    assert not after.get("escalated")
    assert any(a["action"] == "OFFICER_CONFIRMED" for a in after.get("audit", []))
