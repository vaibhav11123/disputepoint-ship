"""Source-state honesty — rain availability and evidence chips independent of fixture board."""

from __future__ import annotations

import asyncio
import json
from unittest.mock import patch

from backend.app.db.store import clear_rain, get_rain, list_evidence, save_rain, update_evidence
from backend.app.main import create_app
from backend.app.services.rain import RainUnavailable, observation


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


def test_live_zero_mm_is_live_and_points_list() -> None:
    app = create_app(":memory:", enable_polling=False)
    obs = observation(0.0, source="open-meteo", is_synthetic=False)
    save_rain(app.state.conn, obs)
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health["precip_mm"] == 0.0
    assert health["scenario_active"] is False
    assert health["rain_source_state"] == "LIVE"
    assert health["rain_mode"] == "live"
    status, listing = call(app, "GET", "/points")
    assert status == 200
    assert len(listing["items"]) >= 32


def test_live_nonzero_is_live() -> None:
    app = create_app(":memory:", enable_polling=False)
    save_rain(app.state.conn, observation(12.5, source="open-meteo", is_synthetic=False))
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health["precip_mm"] == 12.5
    assert health["rain_source_state"] == "LIVE"
    assert health["scenario_active"] is False


def test_refresh_timeout_with_cache_marks_stale_points_remain() -> None:
    app = create_app(":memory:", enable_polling=False)
    live = observation(7.5, source="open-meteo", is_synthetic=False)
    save_rain(app.state.conn, live)

    def boom(*_a, **_k):
        raise RainUnavailable("timeout")

    with patch("backend.app.services.rain.fetch_open_meteo", boom):
        status, body = call(app, "POST", "/rain/refresh", {})
    assert status == 503
    cached = get_rain(app.state.conn)
    assert cached is not None
    assert float(cached["precip_mm"]) == 7.5
    status, health = call(app, "GET", "/health")
    assert health["rain_source_state"] == "STALE"
    assert health["precip_mm"] == 7.5
    status, listing = call(app, "GET", "/points")
    assert status == 200
    assert len(listing["items"]) >= 32


def test_timeout_no_cache_precip_null_points_remain() -> None:
    app = create_app(":memory:", enable_polling=False)
    clear_rain(app.state.conn)

    def boom(*_a, **_k):
        raise RainUnavailable("timeout")

    with patch("backend.app.services.rain.fetch_open_meteo", boom):
        status, _ = call(app, "POST", "/rain/refresh", {})
    assert status == 503
    assert get_rain(app.state.conn) is None
    status, health = call(app, "GET", "/health")
    assert health["precip_mm"] is None
    assert health["rain_source_state"] == "UNAVAILABLE"
    assert health["scenario_active"] is False
    status, listing = call(app, "GET", "/points")
    assert status == 200
    assert len(listing["items"]) >= 32


def test_scenario_stashes_last_live() -> None:
    app = create_app(":memory:", enable_polling=False)
    save_rain(app.state.conn, observation(9.0, source="open-meteo", is_synthetic=False))
    status, obs = call(app, "POST", "/rain/scenario", {"precip_mm": 42})
    assert status == 200
    assert obs["source"] == "scenario_slider"
    assert obs["last_live"]["precip_mm"] == 9.0
    assert obs["last_live"]["source"] == "open-meteo"
    status, health = call(app, "GET", "/health")
    assert health["scenario_active"] is True
    assert health["rain_source_state"] == "SCENARIO"
    assert health["has_last_live"] is True
    assert health["precip_mm"] == 42


def test_clear_scenario_restores_last_live() -> None:
    app = create_app(":memory:", enable_polling=False)
    save_rain(app.state.conn, observation(9.0, source="open-meteo", is_synthetic=False))
    call(app, "POST", "/rain/scenario", {"precip_mm": 42})
    status, restored = call(app, "POST", "/rain/clear-scenario", {})
    assert status == 200
    assert restored["source"] == "open-meteo"
    assert float(restored["precip_mm"]) == 9.0
    status, health = call(app, "GET", "/health")
    assert health["scenario_active"] is False
    assert health["precip_mm"] == 9.0
    assert health["rain_source_state"] == "LIVE"


def test_clear_scenario_without_last_live_never_invents_zero() -> None:
    app = create_app(":memory:", enable_polling=False)
    clear_rain(app.state.conn)
    call(app, "POST", "/rain/scenario", {"precip_mm": 42})
    # Scenario over empty/fixture-less path: no last_live
    rain = get_rain(app.state.conn)
    assert rain is not None
    rain.pop("last_live", None)
    save_rain(app.state.conn, rain)
    status, cleared = call(app, "POST", "/rain/clear-scenario", {})
    assert status == 200
    assert cleared.get("cleared") is True
    assert cleared.get("precip_mm") is None
    assert get_rain(app.state.conn) is None
    status, health = call(app, "GET", "/health")
    assert health["precip_mm"] is None
    assert health["scenario_active"] is False


def test_evidence_counts_and_status_categories() -> None:
    app = create_app(":memory:", enable_polling=False)
    rows = list_evidence(app.state.conn)
    assert rows
    # Mark a few statuses for count buckets
    update_evidence(
        app.state.conn,
        rows[0]["id"],
        {**rows[0], "live_status": "ok", "live_verified": True},
    )
    update_evidence(
        app.state.conn,
        rows[1]["id"],
        {**rows[1], "live_status": "quote_miss", "live_verified": False},
    )
    update_evidence(
        app.state.conn,
        rows[2]["id"],
        {**rows[2], "live_status": "fetch_forbidden", "live_verified": False},
    )
    status, health = call(app, "GET", "/health")
    assert status == 200
    counts = health["evidence_counts"]
    assert counts["stored"] == len(list_evidence(app.state.conn))
    assert counts["verified"] >= 1
    assert counts["verification_failed"] >= 1
    assert counts["unavailable"] >= 1
    assert counts["not_reverified"] >= 1


def test_startup_with_no_live_rain_still_serves_fixture_board() -> None:
    app = create_app(":memory:", enable_polling=False)
    clear_rain(app.state.conn)
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health["precip_mm"] is None
    assert health["ok"] is True
    status, listing = call(app, "GET", "/points")
    assert status == 200
    assert len(listing["items"]) >= 32
    status, card = call(app, "GET", "/points/dp-purana-quila")
    assert status == 200
    assert card["evidence"]
