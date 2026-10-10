"""Rainfall failure modes — last-good preserved; no invented observation."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timedelta, timezone

from backend.app.db.store import get_rain, save_rain
from backend.app.main import create_app
from backend.app.services.rain import RainUnavailable, observation
from backend.app.services.source_health import apply_failure, apply_success
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


def test_scenario_marks_source_scenario() -> None:
    app = create_app(":memory:", enable_polling=False)
    status, obs = call(app, "POST", "/rain/scenario", {"precip_mm": 42})
    assert status == 200
    assert obs["is_synthetic"] is True
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health["rain_mode"] == "slider"
    assert health["rain_source_state"] == "SCENARIO"
    assert health["scenario_active"] is True
    rain = next(s for s in health["sources"] if s["source_id"] == "open-meteo-rain")
    assert rain["source_state"] == "SCENARIO"
    assert rain["value"] == 42


def test_old_observation_is_stale_not_live() -> None:
    app = create_app(":memory:", enable_polling=False)
    record = app.state.source_registry["open-meteo-rain"]
    old = (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat().replace("+00:00", "Z")
    apply_success(record, value=3.0, observation_time=old, units="mm")
    assert record.source_state == SourceState.STALE


def test_failed_poll_does_not_wipe_cache() -> None:
    app = create_app(":memory:", enable_polling=False)
    conn = app.state.conn
    obs = observation(7.5, source="open-meteo", is_synthetic=False)
    save_rain(conn, obs)
    apply_success(
        app.state.source_registry["open-meteo-rain"],
        value=7.5,
        observation_time=obs["observation_time"],
        retrieved_at=obs["retrieved_at"],
    )
    apply_failure(app.state.source_registry["open-meteo-rain"], error_category="network")
    cached = get_rain(conn)
    assert cached is not None
    assert float(cached["precip_mm"]) == 7.5
    assert app.state.source_registry["open-meteo-rain"].value == 7.5


def test_rain_unavailable_raises() -> None:
    def boom(*_a, **_k):
        raise RainUnavailable("timeout")

    try:
        from backend.app.services import rain as rain_mod

        rain_mod.fetch_open_meteo(opener=boom)
        raise AssertionError("expected RainUnavailable")
    except RainUnavailable:
        pass
