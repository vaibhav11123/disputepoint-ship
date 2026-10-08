import asyncio
import json

from backend.app.db.store import update_point
from backend.app.main import create_app
from backend.app.services.ingest import load_point


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


def test_ack_requires_assigned_open_and_writes_feedback() -> None:
    app = create_app(":memory:")
    status, denied = call(app, "POST", "/points/dp-purana-quila/ack", {"reviewer": "cell-1"})
    assert status == 409
    assert denied["detail"]["code"] == "DP-409-ACK"

    point = load_point(app.state.conn, "dp-minto-bridge")
    assert point is not None
    point["ownership_state"] = "ASSIGNED"
    point["responsible_agency"] = "PWD"
    point["status"] = "OPEN"
    update_point(app.state.conn, point)

    status, ok = call(app, "POST", "/points/dp-minto-bridge/ack", {"reviewer": "cell-1"})
    assert status == 200
    assert ok["status"] == "ACKED"
    stored = load_point(app.state.conn, "dp-minto-bridge")
    assert stored is not None
    assert stored["status"] == "ACKED"
    assert stored["audit"][-1]["action"] == "ACK"
    assert stored["status"] != "RESOLVED"


def test_override_and_escalate_stay_open() -> None:
    app = create_app(":memory:")
    status, row = call(
        app,
        "POST",
        "/points/dp-purana-quila/override",
        {"agency": "PWD", "reason": "cell assigns PWD for this window", "reviewer": "cell-1"},
    )
    assert status == 200
    assert row["action"] == "OVERRIDE"
    stored = load_point(app.state.conn, "dp-purana-quila")
    assert stored is not None
    assert stored["status"] == "OPEN"
    assert stored["human_selected_agency"] == "PWD"

    status, escalated = call(
        app,
        "POST",
        "/points/dp-purana-quila/escalate",
        {"reason": "two agencies still claimed", "reviewer": "cell-1"},
    )
    assert status == 200
    stored = load_point(app.state.conn, "dp-purana-quila")
    assert stored is not None
    assert stored["status"] == "OPEN"
    assert stored["escalated"] is True
