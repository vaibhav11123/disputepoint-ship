"""DisputePoint API package.

The read API lives in ``backend.app.main`` (WP-07). Until that module exists,
``make run`` loads :func:`create_app` so the toolchain can boot.
"""

from __future__ import annotations


def create_app():
    from fastapi import FastAPI

    app = FastAPI(title="DisputePoint", version="0.1.0")

    @app.get("/")
    def toolchain_root() -> dict[str, str]:
        return {"service": "disputepoint", "mode": "toolchain"}

    return app
