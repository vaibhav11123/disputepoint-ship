"""Live feeds must never assign agency or skip HITL on CONFLICT."""

from __future__ import annotations

import asyncio
import json

from backend.app.main import create_app
from backend.app.services.source_registry import SourceState


def call(app, method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
    payload = b"" if body is None else json.dumps(body).encode()
    messages: list[dict] = []
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [(b"content-type", b"application/json")],
        "client": ("127.0.0.1", 50000),
        "server": ("test", 80),
    }

    async def receive():
        return {"type": "http.request", "body": payload, "more_body": False}

    async def send(message):
        messages.append(message)

    asyncio.run(app(scope, receive, send))
    status = 500
    raw = b""
    for message in messages:
        if message["type"] == "http.response.start":
            status = message["status"]
        elif message["type"] == "http.response.body":
            raw += message.get("body", b"")
    return status, json.loads(raw.decode() or "{}")


def test_conflict_stays_null_after_scenario_rain() -> None:
    app = create_app(":memory:", enable_polling=False)
    status, _ = call(app, "POST", "/rain/scenario", {"precip_mm": 55})
    assert status == 200
    status, card = call(app, "GET", "/points/dp-purana-quila")
    assert status == 200
    assert card["ownership_state"] == "CONFLICT"
    assert card["responsible_agency"] is None


def test_river_source_context_only_never_priority_rule() -> None:
    app = create_app(":memory:", enable_polling=False)
    river = app.state.source_registry["nwdp-cwc-yamuna-wl"]
    assert "priority_rule" not in river.allowed_effects
    assert "context" in river.allowed_effects
    # Simulating a river update must not assign agency
    river.source_state = SourceState.LIVE
    river.value = 206.5
    status, card = call(app, "GET", "/points/dp-purana-quila")
    assert status == 200
    assert card["responsible_agency"] is None


def test_imd_and_google_have_no_priority_effect() -> None:
    app = create_app(":memory:", enable_polling=False)
    for sid in ("imd-district-rainfall", "imd-district-warning", "imd-aws", "google-flood-yamuna"):
        assert "priority_rule" not in app.state.source_registry[sid].allowed_effects
