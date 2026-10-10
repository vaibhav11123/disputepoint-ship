"""Evidence refresh categories — 403 is retrieval failure, not false claim."""

from __future__ import annotations

import http.client
import urllib.error

from backend.app.services.evidence_live import verify_row


def _http_error(url: str, code: int, msg: str) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url, code, msg, http.client.HTTPMessage(), None)


def test_http_403_is_fetch_forbidden_preserves_prior() -> None:
    quote = "The bridge is on the border of the NDMC and the MCD."
    prior = {
        "id": "ev-test",
        "url": "https://example.com/story",
        "quote": quote,
        "live_verified": True,
        "live_status": "ok",
        "retrieved_at": "2026-01-01T00:00:00Z",
    }

    def opener(request, timeout=10):
        raise _http_error("https://example.com/story", 403, "Forbidden")

    out = verify_row(prior, opener=opener)
    assert out["live_status"] == "fetch_forbidden"
    assert out["retrieved_at"] == "2026-01-01T00:00:00Z"
    assert out["quote"] == quote


def test_http_429_is_rate_limited() -> None:
    quote = "PWD is constructing a concrete drain under the main carriageway."

    def opener(request, timeout=10):
        raise _http_error("https://example.com/x", 429, "Too Many")

    out = verify_row({"id": "a", "url": "https://example.com/x", "quote": quote}, opener=opener)
    assert out["live_status"] == "fetch_rate_limited"
    assert out["live_verified"] is False


def test_quote_miss_is_verification_failed_preserves_quote() -> None:
    quote = "Exclusive jurisdiction sentence that will not appear."

    class _Ok:
        status = 200
        headers = {"Content-Type": "text/html"}

        def read(self, _n=-1):
            return b"<html><body>Unrelated page body without the quote.</body></html>"

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def opener(request, timeout=10):
        return _Ok()

    out = verify_row(
        {"id": "a", "url": "https://example.com/page", "quote": quote, "live_verified": False},
        opener=opener,
    )
    assert out["live_status"] == "quote_miss"
    assert out["live_verified"] is False
    assert out["quote"] == quote


def test_http_403_retains_quote_for_source_unavailable() -> None:
    quote = "Must remain visible when source returns 403."

    def opener(request, timeout=10):
        raise _http_error("https://example.com/story", 403, "Forbidden")

    out = verify_row({"id": "b", "url": "https://example.com/story", "quote": quote}, opener=opener)
    assert out["live_status"] == "fetch_forbidden"
    assert out["quote"] == quote
