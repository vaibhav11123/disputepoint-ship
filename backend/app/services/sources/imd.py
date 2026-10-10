"""IMD API adapters — key-gated; never block demo when key missing."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from backend.app.services.source_registry import utcnow

BASE = "https://api.imd.gov.in/api/v1"


def _key() -> str | None:
    key = os.environ.get("IMD_API_KEY", "").strip()
    return key or None


def _get(path: str) -> dict[str, Any]:
    key = _key()
    if not key:
        return {"ok": False, "error_category": "auth", "message": "IMD_API_KEY missing"}
    url = f"{BASE}{path}"
    req = Request(url, headers={"Accept": "application/json", "X-API-Key": key, "Authorization": f"Bearer {key}"})
    try:
        with urlopen(req, timeout=10) as response:  # noqa: S310 — gov API
            status = getattr(response, "status", 200)
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        if exc.code in {401, 403}:
            return {"ok": False, "error_category": "auth", "message": f"IMD HTTP {exc.code}"}
        return {"ok": False, "error_category": "network", "message": f"IMD HTTP {exc.code}"}
    except (URLError, TimeoutError, OSError) as exc:
        return {"ok": False, "error_category": "network", "message": type(exc).__name__}
    if status != 200:
        return {"ok": False, "error_category": "network", "message": f"IMD status {status}"}
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return {"ok": False, "error_category": "parse", "message": "IMD JSON parse failed"}
    return {"ok": True, "payload": payload, "observation_time": utcnow(), "retrieved_at": utcnow()}


def fetch_district_rainfall() -> dict[str, Any]:
    result = _get("/districtrainfall")
    if not result.get("ok"):
        return result
    return {
        "ok": True,
        "value": result.get("payload"),
        "observation_time": result.get("observation_time"),
        "units": "mm",
        "station_id": "delhi-districts",
    }


def fetch_district_warning() -> dict[str, Any]:
    result = _get("/districtwarning")
    if not result.get("ok"):
        return result
    return {
        "ok": True,
        "value": result.get("payload"),
        "observation_time": result.get("observation_time"),
        "station_id": "delhi-districts",
    }


def fetch_aws() -> dict[str, Any]:
    # State id 7 = DELHI per IMD catalogue
    result = _get("/aws_data?sid=7")
    if not result.get("ok"):
        return result
    return {
        "ok": True,
        "value": result.get("payload"),
        "observation_time": result.get("observation_time"),
        "units": "varies",
        "station_id": "DELHI-AWS",
    }
