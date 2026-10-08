"""Decision API. Local store is SQLite. Ship It can front the same functions later."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from backend.app.api.read import install_read_api
from backend.app.db.store import connect, get_rain
from backend.app.services.ingest import ingest_fixtures, repo_root


def create_app(db_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(title="DisputePoint", version="0.1.0")
    path = Path(db_path) if db_path is not None else repo_root() / "runs" / "disputepoint.sqlite"
    conn = connect(path)
    if get_rain(conn) is None:
        ingest_fixtures(conn, repo_root())
    app.state.conn = conn
    install_read_api(app)
    try:
        from backend.app.api.hitl import install_hitl

        install_hitl(app)
    except ImportError:
        pass
    return app


app = create_app()
