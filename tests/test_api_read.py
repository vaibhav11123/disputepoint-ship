"""Read API. Numeric lat stays null until a human verifies geocodes."""

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


def test_health_points_point_and_honesty() -> None:
    app = create_app(":memory:")
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health["ok"] is True
    started = time.perf_counter()
    status, listing = call(app, "GET", "/points")
    elapsed = time.perf_counter() - started
    assert status == 200
    assert len(listing["items"]) >= 32
    assert elapsed < 0.3
    with_coords = [item for item in listing["items"] if item["lat"] is not None and item["lon"] is not None]
    without = [item for item in listing["items"] if item["lat"] is None or item["lon"] is None]
    assert len(with_coords) == 14  # Gate A VERIFIED
    assert len(without) >= 18  # Expansion B null until VERIFIED
    assert listing["items"][0]["priority_rank"] == 1
    assert "precip_mm" in health
    assert health["live_fetch"] is False
    assert "evidence_live_ok" in health
    assert "evidence_live_fail" in health
    assert "evidence_live_skipped" in health
    status, denied = call(app, "POST", "/evidence/refresh", {})
    assert status == 503
    assert denied["detail"]["code"] == "DP-503-LIVE"
    status, missing = call(app, "GET", "/points/dp-not-a-point")
    assert status == 404
    assert missing["detail"]["code"] == "DP-404-POINT"
    status, card = call(app, "GET", "/points/dp-purana-quila")
    assert status == 200
    assert card["lat"] == 28.61497
    assert card["lon"] == 77.2362208
    assert set(card["components"]) == {"R", "S", "C", "Q", "U", "G"}
    assert card["counterfactuals"]
    assert card["responsible_agency"] is None
    assert card["ownership_state"] == "CONFLICT"
    status, minto = call(app, "GET", "/points/dp-minto-bridge")
    assert status == 200
    assert minto["ownership_state"] == "CONFLICT"
    assert minto["responsible_agency"] is None
    status, meta = call(app, "GET", "/meta/honesty")
    assert status == 200
    assert meta["theta_assign"] == 0.65
    assert meta["bedrock_enabled"] is False
    assert "physical severity" in meta["u_semantics"]


def test_rain_scenario_reranks_and_rejects_bad_body() -> None:
    app = create_app(":memory:")
    status, bad = call(app, "POST", "/rain/scenario", {})
    assert status == 400
    assert bad["code"] == "DP-400-SCHEMA"
    status, rain = call(app, "POST", "/rain/scenario", {"precip_mm": 40})
    assert status == 200
    assert rain["source"] == "scenario_slider"
    assert rain["is_synthetic"] is True
    assert rain["precip_mm"] == 40
    status, listing = call(app, "GET", "/points")
    assert status == 200
    assert listing["items"][0]["components"]["R"] == 0.8
