"""Decision API. Local store is SQLite. Ship It can front the same functions later."""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI

from backend.app.api.read import install_read_api
from backend.app.db.store import (
    connect,
    get_rain,
    list_evidence,
    list_points,
    save_rain,
    update_evidence,
    update_point,
)
from backend.app.services.evidence_live import verify_corpus
from backend.app.services.geocode import fill_missing
from backend.app.services.ingest import ingest_fixtures, repo_root, rescore
from backend.app.services.rain import RainUnavailable, refresh


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


def create_app(db_path: str | Path | None = None, *, live_fetch: bool | None = None) -> FastAPI:
    app = FastAPI(title="DisputePoint", version="0.1.0")
    path = Path(db_path) if db_path is not None else repo_root() / "runs" / "disputepoint.sqlite"
    conn = connect(path)
    if get_rain(conn) is None:
        ingest_fixtures(conn, repo_root())
    live_stats = empty_live_stats()
    use_live = live_fetch_enabled() if live_fetch is None else live_fetch
    live_stats["live_fetch"] = bool(use_live)
    if use_live:
        cache = get_rain(conn)
        try:
            obs = refresh(cache=cache)
            save_rain(conn, obs)
            rescore(conn, obs["precip_mm"])
        except RainUnavailable:
            pass
        before = {(point["id"], point.get("lat"), point.get("lon")) for point in list_points(conn)}
        filled = fill_missing(list_points(conn))
        for point in filled:
            update_point(conn, point)
        after = {(point["id"], point.get("lat"), point.get("lon")) for point in list_points(conn)}
        live_stats["geo_fill"] = "nominatim" if before != after else "fixture"
        live_stats.update(run_evidence_live(conn))
    app.state.conn = conn
    app.state.live_stats = live_stats
    install_read_api(app)
    try:
        from backend.app.api.hitl import install_hitl

        install_hitl(app)
    except ImportError:
        pass
    return app


app = create_app()
