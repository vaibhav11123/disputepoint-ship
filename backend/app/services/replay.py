"""Stored historical replay — no live fetch; never invents incidents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.app.services.ingest import repo_root

REPLAY_ID = "delhi-2025-07-29"


def replay_path(replay_id: str = REPLAY_ID) -> Path:
    return repo_root() / "data" / "replays" / f"{replay_id}.json"


def load_replay(replay_id: str = REPLAY_ID) -> dict[str, Any]:
    path = replay_path(replay_id)
    if not path.is_file():
        raise FileNotFoundError(replay_id)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("replay_id") != replay_id:
        raise ValueError("replay_id mismatch")
    return data


def _step_time(step: dict[str, Any]) -> str:
    return str(step.get("t") or "")


def state_at(replay: dict[str, Any], seek_t: str | None) -> dict[str, Any]:
    """Project weather + activations at seek_t (inclusive). seek_t None = start of day (empty)."""
    steps = sorted(replay.get("steps") or [], key=_step_time)
    if seek_t is None or seek_t == "" or seek_t == "start":
        return {
            "clock": None,
            "precip_mm": None,
            "priority_station": (replay.get("priority_uses") or {}).get("station"),
            "priority_rule": (replay.get("priority_uses") or {}).get("rule"),
            "stations": [],
            "activated_point_ids": [],
            "weather_steps_applied": [],
            "incident_steps_applied": [],
            "gaps": replay.get("gaps") or {},
            "disclaimer": replay.get("disclaimer"),
            "label": replay.get("label"),
            "replay_id": replay.get("replay_id"),
            "mode": "historical_replay",
        }

    stations: dict[str, dict[str, Any]] = {}
    activated: list[str] = []
    weather_applied: list[dict[str, Any]] = []
    incident_applied: list[dict[str, Any]] = {}
    precip: float | None = None
    priority_station = (replay.get("priority_uses") or {}).get("station") or "Safdarjung"

    for step in steps:
        if _step_time(step) > seek_t:
            break
        kind = step.get("kind")
        if kind == "weather":
            weather_applied.append(step)
            stations[str(step.get("station"))] = {
                "station": step.get("station"),
                "precip_mm": step.get("precip_mm"),
                "period_start": step.get("period_start"),
                "period_end": step.get("period_end"),
                "affects_priority": bool(step.get("affects_priority")),
                "source_url": step.get("source_url"),
            }
            if step.get("affects_priority") and step.get("station") == priority_station:
                precip = float(step["precip_mm"])
        elif kind == "incident_activate":
            pid = step.get("point_id")
            if isinstance(pid, str) and pid not in activated:
                activated.append(pid)
                incident_applied[pid] = step

    return {
        "clock": seek_t,
        "precip_mm": precip,
        "priority_station": priority_station,
        "priority_rule": (replay.get("priority_uses") or {}).get("rule"),
        "stations": list(stations.values()),
        "activated_point_ids": activated,
        "weather_steps_applied": weather_applied,
        "incident_steps_applied": list(incident_applied.values()),
        "gaps": replay.get("gaps") or {},
        "disclaimer": replay.get("disclaimer"),
        "label": replay.get("label"),
        "replay_id": replay.get("replay_id"),
        "mode": "historical_replay",
    }


def milestone_times(replay: dict[str, Any]) -> list[str]:
    times = sorted({_step_time(s) for s in replay.get("steps") or [] if _step_time(s)})
    return ["start", *times]


def rain_observation_from_state(state: dict[str, Any]) -> dict[str, Any] | None:
    """Build rain_cache body for historical replay — display context, not 6h LIVE R."""
    precip = state.get("precip_mm")
    if precip is None:
        return None
    clock = state.get("clock") or "2025-07-29T00:00:00+05:30"
    station = state.get("priority_station") or "Safdarjung"
    period_start = None
    period_end = None
    for row in state.get("stations") or []:
        if row.get("station") == station:
            period_start = row.get("period_start")
            period_end = row.get("period_end")
            break
    return {
        "lat": 28.6139,
        "lon": 77.209,
        "window_hours": None,
        "precip_mm": float(precip),
        "source": "historical_replay",
        "retrieved_at": clock,
        "observation_time": clock,
        "is_synthetic": False,
        "priority_uses": False,
        "observation_type": "reported_station_total",
        "station": station,
        "period_start": period_start,
        "period_end": period_end,
        "replay_id": state.get("replay_id"),
        "priority_station": station,
        "stations": state.get("stations") or [],
    }
