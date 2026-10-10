"""Non-blocking startup with DP_LIVE_FETCH=1 when externals are unreachable."""

from __future__ import annotations

import asyncio
import json
import time

from backend.app.main import create_app


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

    async def run():
        await app(scope, receive, send)

    asyncio.run(run())
    status = 500
    raw = b""
    for message in messages:
        if message["type"] == "http.response.start":
            status = message["status"]
        elif message["type"] == "http.response.body":
            raw += message.get("body", b"")
    return status, json.loads(raw.decode() or "{}")


def test_create_app_live_fetch_does_not_block_on_externals() -> None:
    """Startup must remain fast even when live_fetch=True (no sync network)."""
    started = time.perf_counter()
    app = create_app(":memory:", live_fetch=True, enable_polling=False)
    elapsed = time.perf_counter() - started
    assert elapsed < 2.0
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health["ok"] is True
    assert health["live_fetch"] is True
    assert "sources" in health
    assert any(s["source_id"] == "open-meteo-rain" for s in health["sources"])
    status, listing = call(app, "GET", "/points")
    assert status == 200
    assert len(listing["items"]) >= 32


def test_health_exposes_gated_sources_as_unknown() -> None:
    app = create_app(":memory:", live_fetch=False, enable_polling=False)
    status, health = call(app, "GET", "/health")
    assert status == 200
    by_id = {s["source_id"]: s for s in health["sources"]}
    assert by_id["imd-district-rainfall"]["access_status"] == "key_required"
    assert by_id["nwdp-cwc-yamuna-wl"]["access_status"] == "investigating"
    assert by_id["google-flood-yamuna"]["access_status"] == "waitlist"
    assert by_id["imd-district-rainfall"]["source_state"] == "UNKNOWN"
