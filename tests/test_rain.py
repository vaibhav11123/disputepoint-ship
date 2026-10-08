"""T-RAIN-01. Fake HTTP. Slider is synthetic. Timeout keeps a cache."""

import json
from io import BytesIO

import pytest

from backend.app.services.rain import OPEN_METEO_URL, RainUnavailable, fetch_open_meteo, refresh, scenario


class _Response:
    status = 200

    def __init__(self, body: bytes):
        self._body = BytesIO(body)

    def read(self) -> bytes:
        return self._body.read()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_t_rain_01_fake_open_meteo_sums_hourly() -> None:
    def opener(url, timeout=5.0):
        assert url == OPEN_METEO_URL
        payload = {"hourly": {"precipitation": [10, 10, 20, None]}}
        return _Response(json.dumps(payload).encode())

    rain = fetch_open_meteo(opener)
    assert rain["source"] == "open-meteo"
    assert rain["is_synthetic"] is False
    assert rain["precip_mm"] == 40
    assert rain["lat"] == 28.6139
    assert rain["window_hours"] == 6


def test_t_rain_01_timeout_uses_cache() -> None:
    def opener(url, timeout=5.0):
        raise TimeoutError("upstream")

    cache = scenario(0)
    cache["source"] = "open-meteo"
    cache["is_synthetic"] = False
    rain = refresh(opener, cache=cache)
    assert rain["precip_mm"] == 0
    assert rain["source"] == "fixture"


def test_t_rain_01_scenario_slider_is_synthetic() -> None:
    rain = scenario(40)
    assert rain["source"] == "scenario_slider"
    assert rain["is_synthetic"] is True
    assert rain["precip_mm"] == 40


def test_refresh_without_cache_raises() -> None:
    def opener(url, timeout=5.0):
        raise TimeoutError("upstream")

    with pytest.raises(RainUnavailable):
        refresh(opener, cache=None)
