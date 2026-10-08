"""Nominatim fill for null points. Stubbed network."""

from __future__ import annotations

import io
import json

from backend.app.services.geocode import fill_missing, lookup, name_matches


class FakeResponse:
    def __init__(self, payload: list[dict]):
        self._raw = json.dumps(payload).encode()

    def read(self):
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_lookup_keeps_delhi_match_and_rejects_proxy() -> None:
    def opener(request, timeout=8):
        return FakeResponse(
            [
                {
                    "lat": "28.6334521",
                    "lon": "77.2266682",
                    "display_name": "Shivaji Bridge, Babar Road, New Delhi",
                    "osm_type": "node",
                    "osm_id": 1988513598,
                }
            ]
        )

    hit = lookup("dp-minto-bridge", opener=opener)
    assert hit is not None
    assert hit["lat"] == 28.6334521
    assert hit["geo_source"] == "nominatim"

    def bad(request, timeout=8):
        return FakeResponse(
            [
                {
                    "lat": "28.5868478",
                    "lon": "77.2486545",
                    "display_name": "Baba Banda Singh Bahadur Setu, Lajpat Nagar",
                    "osm_type": "way",
                    "osm_id": 1,
                }
            ]
        )

    assert lookup("dp-barapullah", opener=bad) is None
    assert name_matches("dp-barapullah", "Barapullah Drain, Delhi")


def test_fill_missing_sleeps_between_calls() -> None:
    sleeps: list[float] = []
    calls = {"n": 0}

    def opener(request, timeout=8):
        calls["n"] += 1
        return FakeResponse(
            [
                {
                    "lat": "28.6704636",
                    "lon": "77.1606005",
                    "display_name": "Zakhira Flyover, Delhi",
                    "osm_type": "way",
                    "osm_id": 2,
                }
            ]
        )

    points = [
        {"id": "dp-zakhira", "lat": None, "lon": None},
        {"id": "dp-azad-market", "lat": None, "lon": None},
    ]

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    # Second point needs a matching name; return Azad on second call.
    payloads = [
        [
            {
                "lat": "28.6704636",
                "lon": "77.1606005",
                "display_name": "Zakhira Flyover, Delhi",
                "osm_type": "way",
                "osm_id": 2,
            }
        ],
        [
            {
                "lat": "28.6631328",
                "lon": "77.2076461",
                "display_name": "Azad Market, Delhi",
                "osm_type": "node",
                "osm_id": 3,
            }
        ],
    ]
    idx = {"i": 0}

    def sequenced(request, timeout=8):
        payload = payloads[idx["i"]]
        idx["i"] += 1
        return FakeResponse(payload)

    updated = fill_missing(points, opener=sequenced, sleep=sleep)
    assert len(updated) == 2
    assert sleeps == [1.0]
    assert points[0]["lat"] == 28.6704636
    assert points[1]["lat"] == 28.6631328
