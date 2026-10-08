"""Read routes: health, points, point, honesty, rain refresh, rain scenario."""

from __future__ import annotations

import json
import logging
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend.app.db.store import get_rain, save_rain
from backend.app.services.ingest import list_points as stored_points
from backend.app.services.ingest import load_point, rescore
from backend.app.services.ownership import THETA, W_NORM
from backend.app.services.priority import U_SEMANTICS, WEIGHTS
from backend.app.services.rain import RainUnavailable, refresh, scenario

router = APIRouter()
log = logging.getLogger("disputepoint.api")


class ScenarioBody(BaseModel):
    precip_mm: float = Field(ge=0)


def rain_mode(source: str | None) -> str:
    if source == "open-meteo":
        return "live"
    if source == "scenario_slider":
        return "slider"
    return "cache"


def _live_stats(request: Request) -> dict:
    return getattr(request.app.state, "live_stats", None) or {
        "live_fetch": False,
        "evidence_live_ok": 0,
        "evidence_live_fail": 0,
        "evidence_live_skipped": 0,
        "geo_fill": "none",
    }


@router.get("/health")
def health(request: Request) -> dict:
    rain = get_rain(request.app.state.conn)
    source = None if rain is None else rain.get("source")
    stats = _live_stats(request)
    return {
        "ok": True,
        "rain_mode": rain_mode(source),
        "precip_mm": 0.0 if rain is None else float(rain.get("precip_mm") or 0),
        "rain_retrieved_at": None if rain is None else rain.get("retrieved_at"),
        "live_fetch": bool(stats.get("live_fetch")),
        "geo_fill": stats.get("geo_fill") or "none",
        "evidence_live_ok": int(stats.get("evidence_live_ok") or 0),
        "evidence_live_fail": int(stats.get("evidence_live_fail") or 0),
        "evidence_live_skipped": int(stats.get("evidence_live_skipped") or 0),
    }


@router.get("/points")
def list_points(request: Request) -> dict:
    items = stored_points(request.app.state.conn)
    items.sort(key=lambda point: point["priority_rank"])
    return {"items": items}


@router.get("/points/{point_id}")
def get_point(point_id: str, request: Request) -> dict:
    point = load_point(request.app.state.conn, point_id)
    if point is None:
        raise HTTPException(status_code=404, detail={"code": "DP-404-POINT", "message": "Unknown point"})
    point["advisory"] = True
    return point


@router.post("/rain/refresh")
def rain_refresh(request: Request) -> dict:
    conn = request.app.state.conn
    cache = get_rain(conn)
    try:
        obs = refresh(cache=cache)
    except RainUnavailable as exc:
        raise HTTPException(status_code=503, detail={"code": "DP-503-RAIN", "message": str(exc)}) from exc
    save_rain(conn, obs)
    rescore(conn, obs["precip_mm"])
    return obs


@router.post("/rain/scenario")
def rain_scenario(body: ScenarioBody, request: Request) -> dict:
    conn = request.app.state.conn
    obs = scenario(body.precip_mm)
    save_rain(conn, obs)
    rescore(conn, obs["precip_mm"])
    return get_rain(conn)


@router.post("/evidence/refresh")
def evidence_refresh(request: Request) -> dict:
    from backend.app.db.store import list_evidence, update_evidence
    from backend.app.main import live_fetch_enabled
    from backend.app.services.evidence_live import verify_corpus

    stats_state = _live_stats(request)
    if not live_fetch_enabled() and not stats_state.get("live_fetch") and not getattr(request.app.state, "allow_evidence_refresh", False):
        raise HTTPException(
            status_code=503,
            detail={"code": "DP-503-LIVE", "message": "Live evidence refresh requires DP_LIVE_FETCH=1"},
        )
    rows = list_evidence(request.app.state.conn)
    updated, counts = verify_corpus(rows)
    for row in updated:
        update_evidence(request.app.state.conn, row["id"], row)
    stats = {
        "evidence_live_ok": counts["ok"],
        "evidence_live_fail": counts["fail"],
        "evidence_live_skipped": counts["skipped"],
    }
    live = dict(stats_state)
    live.update(stats)
    live["live_fetch"] = True
    request.app.state.live_stats = live
    return {"ok": True, **stats}


@router.get("/meta/honesty")
def honesty() -> dict:
    return {
        "advisory": True,
        "theta_assign": THETA,
        "w_norm": W_NORM,
        "weights": WEIGHTS,
        "u_semantics": U_SEMANTICS,
        "bedrock_enabled": False,
        "policy_strings": [
            "CONFLICT sets responsible_agency null",
            "U is coordination_uncertainty, not physical severity",
            "No ML runtime in the MVP",
        ],
    }


def install_read_api(app: FastAPI) -> None:
    app.include_router(router)

    @app.middleware("http")
    async def request_log(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid4())
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        log.info(json.dumps({"request_id": request_id, "stage": "api", "path": request.url.path, "status": response.status_code}))
        return response

    @app.exception_handler(RequestValidationError)
    async def bad_schema(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=400, content={"code": "DP-400-SCHEMA", "message": "Request body failed validation"})
