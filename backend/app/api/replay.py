"""Historical replay read/seek — stored package only; never assigns agencies."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from backend.app.db.store import clear_rain, get_rain, save_rain
from backend.app.services.ingest import rescore
from backend.app.services.replay import (
    REPLAY_ID,
    load_replay,
    milestone_times,
    rain_observation_from_state,
    state_at,
)
from backend.app.services.source_health import sync_rain_record

router = APIRouter(prefix="/replays", tags=["replay"])


class SeekBody(BaseModel):
    t: str | None = Field(default=None, description="ISO clock or 'start'")
    step_index: int | None = Field(default=None, ge=0)


def _registry(request: Request):
    return getattr(request.app.state, "source_registry", None)


def _strip_last_live(rain: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in rain.items() if key != "last_live"}


def _carry_last_live(cache: dict[str, Any] | None) -> dict[str, Any] | None:
    """Preserve usable live observation across historical seek/park."""
    if not cache:
        return None
    if cache.get("source") == "open-meteo" and not cache.get("is_synthetic"):
        return _strip_last_live(cache)
    prior = cache.get("last_live")
    return dict(prior) if isinstance(prior, dict) else None


def _park_historical_null_rain(conn, cache: dict[str, Any] | None) -> dict[str, Any]:
    """Clear active mm for start-of-day without destroying last_live."""
    body: dict[str, Any] = {
        "lat": 28.6139,
        "lon": 77.209,
        "window_hours": None,
        "precip_mm": None,
        "source": "historical_replay",
        "retrieved_at": "2025-07-29T00:00:00+05:30",
        "observation_time": None,
        "is_synthetic": False,
        "priority_uses": False,
        "observation_type": "parked_historical",
        "parked": True,
    }
    last = _carry_last_live(cache)
    if last is not None:
        body["last_live"] = last
    save_rain(conn, body)
    return body


@router.get("/{replay_id}")
def get_replay(replay_id: str) -> dict:
    try:
        data = load_replay(replay_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail={"code": "DP-404-REPLAY", "message": str(exc)}) from exc
    return {
        **data,
        "milestones": milestone_times(data),
        "mode": "historical_replay",
    }


@router.get("/{replay_id}/state")
def get_replay_state(replay_id: str, t: str | None = None) -> dict:
    try:
        data = load_replay(replay_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail={"code": "DP-404-REPLAY", "message": str(exc)}) from exc
    return state_at(data, t)


@router.post("/{replay_id}/seek")
def seek_replay(replay_id: str, body: SeekBody, request: Request) -> dict:
    """Advance replay clock. Display rain only; rescore with 0 (no false 6h R). Ownership untouched."""
    try:
        data = load_replay(replay_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail={"code": "DP-404-REPLAY", "message": str(exc)}) from exc

    seek_t = body.t
    milestones = milestone_times(data)
    if body.step_index is not None:
        if body.step_index >= len(milestones):
            raise HTTPException(
                status_code=400,
                detail={"code": "DP-400-REPLAY", "message": "step_index out of range"},
            )
        seek_t = milestones[body.step_index]

    state = state_at(data, seek_t)
    conn = request.app.state.conn
    cache = get_rain(conn)
    rain = rain_observation_from_state(state)
    if rain is None:
        _park_historical_null_rain(conn, cache)
    else:
        last = _carry_last_live(cache)
        if last is not None:
            rain["last_live"] = last
        save_rain(conn, rain)
    # Historical mm is context only — do not drive 6h priority R.
    rescore(conn, 0.0)

    registry = _registry(request)
    if registry is not None:
        sync_rain_record(registry["open-meteo-rain"], get_rain(conn))

    request.app.state.replay_state = {
        "replay_id": replay_id,
        "active": True,
        "clock": state.get("clock"),
        "activated_point_ids": state.get("activated_point_ids") or [],
    }
    return {
        **state,
        "milestones": milestones,
        "ownership_unchanged": True,
    }


@router.post("/{replay_id}/exit")
def exit_replay(replay_id: str, request: Request) -> dict:
    """Leave historical replay; restore last_live if present, else clear — never invent live 0."""
    conn = request.app.state.conn
    cache = get_rain(conn)
    last = cache.get("last_live") if cache and isinstance(cache.get("last_live"), dict) else None
    registry = _registry(request)
    record = None if registry is None else registry.get("open-meteo-rain")
    if last is not None:
        restored = dict(last)
        restored["last_live"] = {k: v for k, v in restored.items() if k != "last_live"}
        save_rain(conn, restored)
        if record is not None:
            sync_rain_record(record, restored)
        rescore(conn, float(restored.get("precip_mm") or 0))
        out = restored
    else:
        clear_rain(conn)
        if record is not None:
            sync_rain_record(record, None)
        rescore(conn, 0.0)
        out = {"cleared": True, "precip_mm": None, "source": None}

    request.app.state.replay_state = {
        "replay_id": replay_id,
        "active": False,
        "clock": None,
        "activated_point_ids": [],
    }
    return {"ok": True, "rain": out, "mode": "exited_historical_replay"}


def install_replay_api(app: FastAPI) -> None:
    app.include_router(router)
    app.state.replay_state = {
        "replay_id": REPLAY_ID,
        "active": False,
        "clock": None,
        "activated_point_ids": [],
    }
