"""Decision API. Local store is SQLite. Ship It can front the same functions later."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI

from backend.app.api.read import install_read_api
from backend.app.db.store import (
    connect,
    get_rain,
    list_evidence,
    update_evidence,
)
from backend.app.services.evidence_live import verify_corpus
from backend.app.services.ingest import ingest_fixtures, repo_root
from backend.app.services.source_health import sync_rain_record
from backend.app.services.source_registry import SourceState, new_registry
from backend.app.services.source_scheduler import SourceScheduler
from backend.app.services.sources import google_flood, nwdp_cwc


def live_fetch_enabled() -> bool:
    return os.environ.get("DP_LIVE_FETCH", "").lower() in {"1", "true", "yes"}


def empty_live_stats() -> dict:
    return {
        "live_fetch": False,
        "evidence_live_ok": 0,
        "evidence_live_fail": 0,
        "evidence_live_skipped": 0,
        "geo_fill": "none",
    }


def run_evidence_live(conn) -> dict:
    rows = list_evidence(conn)
    updated, stats = verify_corpus(rows)
    for row in updated:
        evidence_id = row["id"]
        update_evidence(conn, evidence_id, row)
    return {
        "evidence_live_ok": stats["ok"],
        "evidence_live_fail": stats["fail"],
        "evidence_live_skipped": stats["skipped"],
    }


def _seed_gated_sources(registry) -> None:
    """Reflect access gates without claiming LIVE."""
    if not os.environ.get("IMD_API_KEY", "").strip():
        for sid in ("imd-district-rainfall", "imd-district-warning", "imd-aws"):
            registry[sid].access_status = "key_required"
            registry[sid].last_error_category = "auth"
    nw = nwdp_cwc.fetch_observation()
    if not nw.get("ok"):
        registry["nwdp-cwc-yamuna-wl"].access_status = "investigating"
        registry["nwdp-cwc-yamuna-wl"].last_error_category = str(nw.get("error_category") or "unknown")
    gf = google_flood.fetch_forecast()
    if not gf.get("ok"):
        registry["google-flood-yamuna"].access_status = "waitlist"
        registry["google-flood-yamuna"].last_error_category = str(gf.get("error_category") or "waitlist")


def create_app(
    db_path: str | Path | None = None,
    *,
    live_fetch: bool | None = None,
    enable_polling: bool | None = None,
) -> FastAPI:
    """Create app. Live network work is never synchronous on the startup path."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        scheduler = SourceScheduler(app)
        app.state.source_scheduler = scheduler
        scheduler.start()
        try:
            yield
        finally:
            await scheduler.stop()

    app = FastAPI(title="DisputePoint", version="0.1.0", lifespan=lifespan)
    path = Path(db_path) if db_path is not None else repo_root() / "runs" / "disputepoint.sqlite"
    conn = connect(path)
    if get_rain(conn) is None:
        ingest_fixtures(conn, repo_root())

    live_stats = empty_live_stats()
    use_live = live_fetch_enabled() if live_fetch is None else live_fetch
    live_stats["live_fetch"] = bool(use_live)

    registry = new_registry()
    sync_rain_record(registry["open-meteo-rain"], get_rain(conn))
    if not use_live:
        registry["evidence-live"].source_state = SourceState.SCENARIO
        registry["evidence-live"].access_status = "active"
    _seed_gated_sources(registry)

    app.state.conn = conn
    app.state.live_stats = live_stats
    app.state.source_registry = registry
    app.state.enable_polling = True if enable_polling is None else bool(enable_polling)
    install_read_api(app)
    try:
        from backend.app.api.replay import install_replay_api

        install_replay_api(app)
    except ImportError:
        pass
    try:
        from backend.app.api.hitl import install_hitl

        install_hitl(app)
    except ImportError:
        pass
    return app


app = create_app()
