"""Live-fetch evidence URLs and verify quote ⊆ source. Fail soft to fixtures."""

from __future__ import annotations

import html
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Callable

from backend.app.services.evidence import quote_subseteq_source

USER_AGENT = "DisputePoint/0.1 (hackathon; https://github.com/vaibhavsingh/disputepoint)"
TIMEOUT_S = 10
MAX_BYTES = 2_000_000
DELAY_S = 0.35

Opener = Callable[..., Any]


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_pdf(url: str, content_type: str) -> bool:
    lowered = (content_type or "").lower()
    if "pdf" in lowered:
        return True
    return url.lower().split("?")[0].endswith(".pdf")


def html_to_text(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_url(url: str, *, opener: Opener | None = None) -> tuple[bytes, str]:
    open_fn = opener or urllib.request.urlopen
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with open_fn(req, timeout=TIMEOUT_S) as response:
        content_type = ""
        if hasattr(response, "headers") and response.headers is not None:
            content_type = response.headers.get("Content-Type", "")
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raw = raw[:MAX_BYTES]
    return raw, content_type


def verify_row(
    row: dict[str, Any],
    *,
    opener: Opener | None = None,
) -> dict[str, Any]:
    """Return an updated evidence body with live_verified / live_status. Never drops the quote."""
    updated = dict(row)
    url = str(row.get("url") or "")
    quote = str(row.get("quote") or "")
    if not url or len(quote) < 10:
        updated["live_verified"] = False
        updated["live_status"] = "skipped_bad_row"
        return updated
    if url.lower().split("?")[0].endswith(".pdf"):
        updated["live_verified"] = False
        updated["live_status"] = "skipped_pdf"
        return updated
    try:
        raw, content_type = fetch_url(url, opener=opener)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        updated["live_verified"] = False
        updated["live_status"] = "fetch_failed"
        return updated
    if _is_pdf(url, content_type):
        updated["live_verified"] = False
        updated["live_status"] = "skipped_pdf"
        return updated
    text = html_to_text(raw)
    if quote_subseteq_source(quote, text):
        updated["live_verified"] = True
        updated["live_status"] = "ok"
        updated["retrieved_at"] = _utcnow()
        return updated
    updated["live_verified"] = False
    updated["live_status"] = "quote_miss"
    return updated


def verify_corpus(
    rows: list[dict[str, Any]],
    *,
    opener: Opener | None = None,
    sleeper: Callable[[float], None] | None = None,
    delay_s: float = DELAY_S,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    sleep = sleeper or time.sleep
    out: list[dict[str, Any]] = []
    stats = {"ok": 0, "fail": 0, "skipped": 0}
    for index, row in enumerate(rows):
        if index:
            sleep(delay_s)
        updated = verify_row(row, opener=opener)
        status = updated.get("live_status") or "fetch_failed"
        if status == "ok":
            stats["ok"] += 1
        elif status.startswith("skipped"):
            stats["skipped"] += 1
        else:
            stats["fail"] += 1
        out.append(updated)
    return out, stats
