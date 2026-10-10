"""Historical replay — stored 29 Jul 2025 package; ownership never mutates."""

from __future__ import annotations

import asyncio
import json

from backend.app.main import create_app
from backend.app.services.replay import load_replay, milestone_times, state_at


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


def test_replay_package_loads_and_milestones() -> None:
    data = load_replay("delhi-2025-07-29")
    assert data["priority_uses"]["station"] == "Safdarjung"
    assert len(data["gaps"]["points_without_day_evidence"]) == 25
    ms = milestone_times(data)
    assert ms[0] == "start"
    assert "2025-07-29T11:30:00+05:30" in ms


def test_state_at_start_has_no_precip() -> None:
    data = load_replay()
    state = state_at(data, "start")
    assert state["precip_mm"] is None
    assert state["activated_point_ids"] == []


def test_state_at_morning_uses_safdarjung_only_for_priority() -> None:
    data = load_replay()
    state = state_at(data, "2025-07-29T11:30:00+05:30")
    assert state["precip_mm"] == 63.5
    stations = {s["station"]: s["precip_mm"] for s in state["stations"]}
    assert stations["Ridge"] == 129.4
    assert stations["Safdarjung"] == 63.5


def test_seek_activates_documented_points_not_purana() -> None:
    app = create_app(":memory:", enable_polling=False)
    status, state = call(app, "POST", "/replays/delhi-2025-07-29/seek", {"step_index": 2})
    assert status == 200
    assert state["ownership_unchanged"] is True
    assert "dp-zakhira" in state["activated_point_ids"]
    assert "dp-purana-quila" not in state["activated_point_ids"]
    status, health = call(app, "GET", "/health")
    assert health["rain_mode"] == "replay"
    assert health["replay_active"] is True
    assert health["precip_mm"] == 63.5
    status, card = call(app, "GET", "/points/dp-purana-quila")
    assert status == 200
    assert card["ownership_state"] == "CONFLICT"
    assert card["responsible_agency"] is None


def test_seek_does_not_assign_agency_on_activated_conflict() -> None:
    app = create_app(":memory:", enable_polling=False)
    # Advance far enough that lodhi/barapullah activate
    status, state = call(app, "POST", "/replays/delhi-2025-07-29/seek", {"t": "2025-07-29T17:30:00+05:30"})
    assert status == 200
    assert state["precip_mm"] == 68.1
    for pid in ("dp-barapullah", "dp-lodhi-moolchand", "dp-who-ito-ring"):
        if pid in state["activated_point_ids"]:
            st, card = call(app, "GET", f"/points/{pid}")
            assert st == 200
            if card["ownership_state"] == "CONFLICT":
                assert card["responsible_agency"] is None


def test_exit_clears_replay_mode() -> None:
    app = create_app(":memory:", enable_polling=False)
    call(app, "POST", "/replays/delhi-2025-07-29/seek", {"step_index": 1})
    status, out = call(app, "POST", "/replays/delhi-2025-07-29/exit", {})
    assert status == 200
    assert out["ok"] is True
    status, health = call(app, "GET", "/health")
    assert health.get("replay_active") is False
    # Cold path still lists points
    status, listing = call(app, "GET", "/points")
    assert status == 200
    assert len(listing["items"]) >= 32


def test_command_boot_not_auto_replay() -> None:
    app = create_app(":memory:", enable_polling=False)
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health.get("replay_active") is False
    assert health["rain_mode"] != "replay"


def test_r2_seek_start_preserves_last_live() -> None:
    from backend.app.db.store import save_rain

    app = create_app(":memory:", enable_polling=False)
    save_rain(
        app.state.conn,
        {
            "lat": 28.61,
            "lon": 77.2,
            "window_hours": 6,
            "precip_mm": 11.0,
            "source": "open-meteo",
            "retrieved_at": "2026-10-10T00:00:00Z",
            "observation_time": "2026-10-10T00:00:00Z",
            "is_synthetic": False,
        },
    )
    status, _ = call(app, "POST", "/replays/delhi-2025-07-29/seek", {"t": "start"})
    assert status == 200
    status, health = call(app, "GET", "/health")
    assert health["replay_active"] is True
    assert health["precip_mm"] is None
    assert health["has_last_live"] is True
    status, out = call(app, "POST", "/replays/delhi-2025-07-29/exit", {})
    assert status == 200
    assert float(out["rain"]["precip_mm"]) == 11.0
    status, health = call(app, "GET", "/health")
    assert health["replay_active"] is False
    assert health["precip_mm"] == 11.0
    assert health.get("rain_mode") != "replay"


def test_r6_refresh_during_replay_keeps_historical_display(monkeypatch) -> None:
    from backend.app.db.store import save_rain
    from backend.app.services import rain as rain_mod

    app = create_app(":memory:", enable_polling=False)
    call(app, "POST", "/replays/delhi-2025-07-29/seek", {"t": "2025-07-29T11:30:00+05:30"})

    def fake_fetch():
        return {
            "lat": 28.61,
            "lon": 77.2,
            "window_hours": 6,
            "precip_mm": 3.5,
            "source": "open-meteo",
            "retrieved_at": "2026-10-10T01:00:00Z",
            "observation_time": "2026-10-10T01:00:00Z",
            "is_synthetic": False,
        }

    monkeypatch.setattr(rain_mod, "fetch_open_meteo", fake_fetch)
    status, body = call(app, "POST", "/rain/refresh", {})
    assert status == 200
    assert body["source"] == "historical_replay"
    assert body["precip_mm"] == 63.5
    assert body["display_unchanged"] is True
    assert body["last_live"]["precip_mm"] == 3.5
    status, health = call(app, "GET", "/health")
    assert health["replay_active"] is True
    assert health["precip_mm"] == 63.5
    assert health["has_last_live"] is True


def test_historical_rain_observation_has_period_and_priority_uses_false() -> None:
    from backend.app.services.replay import load_replay, rain_observation_from_state, state_at

    state = state_at(load_replay(), "2025-07-29T11:30:00+05:30")
    rain = rain_observation_from_state(state)
    assert rain is not None
    assert rain["priority_uses"] is False
    assert rain["period_start"] == "2025-07-29T08:30:00+05:30"
    assert rain["period_end"] == "2025-07-29T11:30:00+05:30"
    assert rain["station"] == "Safdarjung"


def test_r10_scenario_clears_replay_session() -> None:
    app = create_app(":memory:", enable_polling=False)
    call(app, "POST", "/replays/delhi-2025-07-29/seek", {"step_index": 2})
    status, rain = call(app, "POST", "/rain/scenario", {"precip_mm": 40})
    assert status == 200
    assert rain["source"] == "scenario_slider"
    status, health = call(app, "GET", "/health")
    assert health["replay_active"] is False
    assert health["scenario_active"] is True
    assert health["rain_mode"] == "slider"


def test_r3_r4_activations_grow_without_fabrication() -> None:
    app = create_app(":memory:", enable_polling=False)
    status, early = call(app, "POST", "/replays/delhi-2025-07-29/seek", {"t": "start"})
    assert status == 200
    assert early["activated_point_ids"] == []
    status, mid = call(app, "POST", "/replays/delhi-2025-07-29/seek", {"t": "2025-07-29T11:45:00+05:30"})
    assert status == 200
    mid_ids = set(mid["activated_point_ids"])
    assert mid_ids  # documented activations exist by late morning
    assert "dp-purana-quila" not in mid_ids
    status, late = call(app, "POST", "/replays/delhi-2025-07-29/seek", {"t": "2025-07-29T17:30:00+05:30"})
    assert status == 200
    late_ids = set(late["activated_point_ids"])
    assert mid_ids <= late_ids
    # Never invent gap points
    for pid in late.get("gaps", {}).get("points_without_day_evidence") or []:
        assert pid not in late_ids


def test_r7_failed_refresh_keeps_replay(monkeypatch) -> None:
    from backend.app.services import rain as rain_mod
    from backend.app.services.rain import RainUnavailable

    app = create_app(":memory:", enable_polling=False)
    call(app, "POST", "/replays/delhi-2025-07-29/seek", {"t": "2025-07-29T11:30:00+05:30"})

    def boom():
        raise RainUnavailable("timeout")

    monkeypatch.setattr(rain_mod, "fetch_open_meteo", boom)
    status, _ = call(app, "POST", "/rain/refresh", {})
    assert status == 503
    status, health = call(app, "GET", "/health")
    assert health["replay_active"] is True
    assert health["precip_mm"] == 63.5


def test_r9_exit_no_historical_leak() -> None:
    app = create_app(":memory:", enable_polling=False)
    call(app, "POST", "/replays/delhi-2025-07-29/seek", {"step_index": 2})
    call(app, "POST", "/replays/delhi-2025-07-29/exit", {})
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health["replay_active"] is False
    assert health["rain_mode"] != "replay"
    rain = health.get("rain_source_state")
    # Cleared path: unavailable / none — never historical_replay source on health mode
    assert health.get("precip_mm") in (None, 0.0) or health["rain_mode"] in {"live", "cache", "none", "slider"}


def test_p2_historical_period_not_six_hour_window() -> None:
    app = create_app(":memory:", enable_polling=False)
    call(app, "POST", "/replays/delhi-2025-07-29/seek", {"t": "2025-07-29T11:30:00+05:30"})
    status, health = call(app, "GET", "/health")
    assert status == 200
    assert health["rain_priority_uses"] is False
    assert health["rain_period_start"] == "2025-07-29T08:30:00+05:30"
    assert health["rain_period_end"] == "2025-07-29T11:30:00+05:30"
    assert health["rain_window_hours"] is None
