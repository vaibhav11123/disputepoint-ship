"""NWDP/CWC Yamuna water-level adapter.

Gate: remains investigating until a validated Delhi/Yamuna station observation
is retrieved. Does not invent levels or claim LIVE without access proof.
"""

from __future__ import annotations

import os
from typing import Any


def fetch_observation() -> dict[str, Any]:
    """Attempt NWDP/CWC retrieval. Default: not yet validated."""
    resource = os.environ.get("DP_NWDP_CWC_RESOURCE", "").strip()
    if not resource:
        return {
            "ok": False,
            "error_category": "unknown",
            "message": "NWDP/CWC resource not configured — investigate portal coverage first",
        }
    # Optional future: HTTP GET resource and parse. Until a real URL+schema is validated,
    # refuse to fabricate observations.
    return {
        "ok": False,
        "error_category": "coverage",
        "message": "NWDP/CWC adapter awaiting validated station resource",
    }
