"""Google Flood Forecasting — waitlist-gated; context only."""

from __future__ import annotations

import os
from typing import Any


def fetch_forecast() -> dict[str, Any]:
    if not os.environ.get("GOOGLE_FLOOD_API_KEY", "").strip():
        return {
            "ok": False,
            "error_category": "waitlist",
            "message": "Google Flood Forecasting access not granted / key missing",
        }
    # Adapter body deferred until pilot access + Yamuna coverage validated.
    return {
        "ok": False,
        "error_category": "coverage",
        "message": "Google Flood adapter awaiting validated Yamuna gauge coverage",
    }
