"""Failure subset: live rain timeout, unknown id, ACK on CONFLICT, bad scenario body."""

import asyncio
import json

from backend.app.db.store import update_point
from backend.app.main import create_app
from backend.app.services.ingest import load_point
from backend.app.services.rain import RainUnavailable, refresh, scenario


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


def test_open_meteo_timeout_keeps_slider_path() -> None:
    def opener(*_args, **_kwargs):
        raise TimeoutError("open-meteo timed out")

    try:
        refresh(opener=opener, cache=None)
        raised = False
    except RainUnavailable:
        raised = True
    assert raised
    fallback = scenario(40)
    assert fallback["source"] == "scenario_slider"
    assert fallback["is_synthetic"] is True


def test_unknown_id_ack_conflict_and_bad_scenario() -> None:
    app = create_app(":memory:")
    status, missing = call(app, "GET", "/points/dp-does-not-exist")
    assert status == 404
    assert missing["detail"]["code"] == "DP-404-POINT"

    point = load_point(app.state.conn, "dp-purana-quila")
    assert point is not None
    point["ownership_state"] = "CONFLICT"
    point["responsible_agency"] = None
    point["status"] = "OPEN"
    update_point(app.state.conn, point)
    status, denied = call(app, "POST", "/points/dp-purana-quila/ack", {"reviewer": "cell-1"})
    assert status == 409
    assert denied["detail"]["code"] == "DP-409-ACK"

    status, bad = call(app, "POST", "/rain/scenario", {})
    assert status == 400
    assert bad["code"] == "DP-400-SCHEMA"
