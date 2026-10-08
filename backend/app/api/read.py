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


@router.get("/health")
def health(request: Request) -> dict:
    rain = get_rain(request.app.state.conn)
    return {"ok": True, "rain_mode": rain_mode(None if rain is None else rain.get("source"))}


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
