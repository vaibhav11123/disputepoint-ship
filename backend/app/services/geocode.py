"""Nominatim lookup for points that still lack lat/lon. One request per second."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from typing import Any, Callable

USER_AGENT = "DisputePoint/0.1 (hackathon; https://github.com/vaibhavsingh/disputepoint)"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
LAT_MIN, LAT_MAX = 28.4, 28.9
LON_MIN, LON_MAX = 76.8, 77.5

QUERIES: dict[str, str] = {
    "dp-purana-quila": "Purana Quila Road Delhi",
    "dp-bharat-mandapam-tunnel": "Bharat Mandapam Delhi",
    "dp-mathura-rd-hc": "Delhi High Court",
    "dp-barapullah": "Barapullah Drain Delhi",
    "dp-minto-bridge": "Minto Bridge Delhi",
    "dp-aiims-aurobindo": "AIIMS Delhi",
    "dp-lodhi-moolchand": "Moolchand Flyover Delhi",
    "dp-maharani-bagh": "Maharani Bagh Delhi",
    "dp-who-ito-ring": "Ring Road WHO building Delhi",
    "dp-zakhira": "Zakhira Flyover Delhi",
    "dp-pul-prahladpur": "Pul Prahladpur underpass Delhi",
    "dp-azad-market": "Azad Market Delhi",
    "dp-pragati-bhairon": "Bhairon Marg Delhi",
    "dp-loni-rd": "Loni Road Delhi",
}

NAME_HINTS: dict[str, tuple[str, ...]] = {
    "dp-purana-quila": ("purana quila",),
    "dp-bharat-mandapam-tunnel": ("bharat mandapam",),
    "dp-mathura-rd-hc": ("high court",),
    "dp-barapullah": ("barapullah", "bara pullah", "barapulla"),
    "dp-minto-bridge": ("minto", "shivaji bridge"),
    "dp-aiims-aurobindo": ("aiims", "aurobindo"),
    "dp-lodhi-moolchand": ("moolchand",),
    "dp-maharani-bagh": ("maharani bagh",),
    "dp-who-ito-ring": ("who", "indraprastha", "ito", "ring road"),
    "dp-zakhira": ("zakhira",),
    "dp-pul-prahladpur": ("prahladpur", "pul prahlad"),
    "dp-azad-market": ("azad market",),
    "dp-pragati-bhairon": ("bhairon",),
    "dp-loni-rd": ("loni",),
}


def in_delhi(lat: float, lon: float) -> bool:
    return LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX


def name_matches(point_id: str, display_name: str) -> bool:
    lowered = display_name.lower()
    return any(hint in lowered for hint in NAME_HINTS.get(point_id, ()))


def lookup(point_id: str, opener: Callable = urllib.request.urlopen) -> dict[str, Any] | None:
    query = QUERIES.get(point_id)
    if not query:
        return None
    params = urllib.parse.urlencode({"q": query, "format": "json", "limit": "1"})
    request = urllib.request.Request(
        f"{NOMINATIM_URL}?{params}",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with opener(request, timeout=8) as response:
            payload = json.loads(response.read().decode())
    except Exception:
        return None
    if not payload:
        return None
    hit = payload[0]
    try:
        lat = float(hit["lat"])
        lon = float(hit["lon"])
    except (KeyError, TypeError, ValueError):
        return None
    display = str(hit.get("display_name") or "")
    if not in_delhi(lat, lon) or not name_matches(point_id, display):
        return None
    osm_type = hit.get("osm_type")
    osm_id = hit.get("osm_id")
    return {
        "lat": lat,
        "lon": lon,
        "geo_source": "nominatim",
        "geo_query": query,
        "geo_osm_id": f"{osm_type}/{osm_id}" if osm_type and osm_id else None,
        "geo_licence": "ODbL 1.0",
        "geo_display_name": display,
    }


def fill_missing(points: list[dict[str, Any]], opener: Callable = urllib.request.urlopen, sleep: Callable = time.sleep) -> list[dict[str, Any]]:
    updated: list[dict[str, Any]] = []
    first = True
    for point in points:
        if point.get("lat") is not None and point.get("lon") is not None:
            continue
        if not first:
            sleep(1.0)
        first = False
        hit = lookup(point["id"], opener=opener)
        if hit is None:
            continue
        point.update(hit)
        updated.append(point)
    return updated
