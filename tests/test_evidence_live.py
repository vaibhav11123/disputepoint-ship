"""Live evidence URL verify. Stubbed network — no DP_LIVE_FETCH."""

from __future__ import annotations

from backend.app.services.evidence_live import html_to_text, verify_corpus, verify_row


class FakeResponse:
    def __init__(self, body: bytes, content_type: str = "text/html"):
        self._raw = body
        self.headers = {"Content-Type": content_type}

    def read(self, n=-1):
        if n < 0:
            return self._raw
        return self._raw[:n]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_html_to_text_strips_tags() -> None:
    raw = b"<html><script>x</script><p>Hello NDMC world</p></html>"
    assert "Hello NDMC world" in html_to_text(raw)
    assert "<p>" not in html_to_text(raw)


def test_verify_row_ok_and_soft_fail() -> None:
    quote = "The bridge is on the border of the NDMC and the MCD."

    def opener(request, timeout=10):
        page = f"<html><body><p>{quote} Extra.</p></body></html>".encode()
        return FakeResponse(page)

    row = {
        "id": "ev-test",
        "url": "https://example.com/story",
        "quote": quote,
        "type": "PRESS_REPORT",
        "agency": "NDMC",
    }
    ok = verify_row(row, opener=opener)
    assert ok["live_verified"] is True
    assert ok["live_status"] == "ok"
    assert ok["retrieved_at"]

    def miss(request, timeout=10):
        return FakeResponse(b"<html><body>No matching quote here.</body></html>")

    bad = verify_row(row, opener=miss)
    assert bad["live_verified"] is False
    assert bad["live_status"] == "quote_miss"
    assert bad["quote"] == quote


def test_verify_row_skips_pdf() -> None:
    row = {
        "id": "ev-pdf",
        "url": "https://example.com/order.pdf",
        "quote": "Jurisdiction NDMC appears in this long enough quote.",
        "type": "COURT_ORDER",
        "agency": "NDMC",
    }
    out = verify_row(row, opener=lambda *a, **k: FakeResponse(b"%PDF-1.4", "application/pdf"))
    assert out["live_status"] == "skipped_pdf"
    assert out["live_verified"] is False


def test_verify_corpus_stats_and_delay() -> None:
    sleeps: list[float] = []
    quote = "PWD is constructing a concrete drain under the main carriageway."

    def opener(request, timeout=10):
        return FakeResponse(f"<p>{quote}</p>".encode())

    rows = [
        {"id": "a", "url": "https://example.com/a", "quote": quote},
        {"id": "b", "url": "https://example.com/b.pdf", "quote": quote},
    ]
    updated, stats = verify_corpus(rows, opener=opener, sleeper=sleeps.append, delay_s=0.2)
    assert stats["ok"] == 1
    assert stats["skipped"] == 1
    assert sleeps == [0.2]
    assert updated[0]["live_verified"] is True
    assert updated[1]["live_status"] == "skipped_pdf"
