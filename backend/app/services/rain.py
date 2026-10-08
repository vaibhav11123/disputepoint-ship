"""Metro rain. Locked Delhi centroid. Live failure falls back to cache, then the caller uses the slider."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen

DELHI_LAT = 28.6139
DELHI_LON = 77.2090
WINDOW_HOURS = 6
OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=28.6139&longitude=77.2090&hourly=precipitation"
    "&past_hours=6&forecast_hours=0&timezone=Asia%2FKolkata"
)


class RainUnavailable(RuntimeError):
    code = "DP-503-RAIN"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def observation(
    precip_mm: float,
    *,
    source: str,
    is_synthetic: bool,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    if precip_mm < 0:
        raise ValueError("precip_mm")
    return {
        "lat": DELHI_LAT,
        "lon": DELHI_LON,
        "window_hours": WINDOW_HOURS,
        "precip_mm": precip_mm,
        "source": source,
        "retrieved_at": retrieved_at or _now(),
        "is_synthetic": is_synthetic,
    }


def precip_from_payload(payload: dict[str, Any]) -> float:
    hourly = payload.get("hourly", {}).get("precipitation") or []
    return float(sum(value or 0 for value in hourly))


def fetch_open_meteo(opener=urlopen, timeout: float = 5.0) -> dict[str, Any]:
    try:
        with opener(OPEN_METEO_URL, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if status != 200:
                raise RainUnavailable(f"open-meteo status {status}")
            payload = json.loads(response.read().decode())
    except (URLError, TimeoutError, RainUnavailable) as exc:
        raise RainUnavailable(str(exc)) from exc
    return observation(precip_from_payload(payload), source="open-meteo", is_synthetic=False)


def scenario(precip_mm: float) -> dict[str, Any]:
    return observation(precip_mm, source="scenario_slider", is_synthetic=True)


def refresh(opener=urlopen, cache: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        return fetch_open_meteo(opener)
    except RainUnavailable:
        if cache is not None:
            cached = dict(cache)
            cached["source"] = "fixture" if cached.get("source") == "open-meteo" else cached.get("source", "fixture")
            return cached
        raise
