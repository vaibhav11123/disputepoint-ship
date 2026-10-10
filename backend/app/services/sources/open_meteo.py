"""Thin Open-Meteo wrapper — delegates to rain.py (single implementation)."""

from __future__ import annotations

from typing import Any

from backend.app.services.rain import RainUnavailable, fetch_open_meteo, refresh


def fetch_rain(*, cache: dict[str, Any] | None = None) -> dict[str, Any]:
    return refresh(cache=cache)


__all__ = ["RainUnavailable", "fetch_open_meteo", "fetch_rain"]
