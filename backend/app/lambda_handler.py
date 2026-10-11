"""AWS Lambda entry for Ship It (API Gateway HTTP API + EventBridge rain schedule).

Ship It is live-first: Open-Meteo is fetched on cold start and whenever rain is
not LIVE, so the UI never sits on fixture/cache UNAVAILABLE.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Live defaults before create_app reads the env.
os.environ.setdefault("DP_LAMBDA", "1")
os.environ["DP_LIVE_FETCH"] = os.environ.get("DP_LIVE_FETCH") or "1"
if os.environ.get("DP_SOURCE_POLLING", "").strip() == "":
    os.environ["DP_SOURCE_POLLING"] = "1"

from mangum import Mangum

from backend.app.db.store import get_rain, save_rain
from backend.app.main import create_app
from backend.app.services.rain import RainUnavailable, fetch_open_meteo
from backend.app.services.source_health import apply_failure, apply_success, sync_rain_record
from backend.app.services.source_registry import SourceState

log = logging.getLogger("disputepoint.lambda")

_DB = os.environ.get("DP_DB_PATH", "/tmp/disputepoint.sqlite")
_DB_S3_KEY = os.environ.get("DP_DB_S3_KEY", "runtime/disputepoint.sqlite")


def _s3_client():
    import boto3

    return boto3.client("s3")


def _evidence_verified_count(conn) -> int:
    """Count rows with live_status=ok (quote re-check passed)."""
    try:
        from backend.app.db.store import list_evidence

        return sum(1 for row in list_evidence(conn) if row.get("live_status") == "ok")
    except Exception:
        return 0


def _sqlite_verified_count(path: Path) -> int:
    if not path.is_file():
        return 0
    try:
        import sqlite3

        from backend.app.db.store import list_evidence

        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            return _evidence_verified_count(conn)
        finally:
            conn.close()
    except Exception:
        return 0


def restore_db_from_s3() -> bool:
    """Pull last live SQLite snapshot so cold starts keep Open-Meteo / evidence state."""
    bucket = os.environ.get("EVIDENCE_BUCKET", "").strip()
    if not bucket:
        return False
    path = Path(_DB)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        _s3_client().download_file(bucket, _DB_S3_KEY, str(path))
        log.info("shipit restored db s3://%s/%s", bucket, _DB_S3_KEY)
        return True
    except Exception as exc:
        log.info("shipit no db snapshot yet (%s)", type(exc).__name__)
        return False


def persist_db_to_s3() -> None:
    bucket = os.environ.get("EVIDENCE_BUCKET", "").strip()
    if not bucket or not Path(_DB).is_file():
        return
    try:
        # Checkpoint so the file on disk is consistent before upload.
        conn = getattr(getattr(_app, "state", None), "conn", None)
        if conn is not None:
            conn.execute("PRAGMA wal_checkpoint(FULL)")
            conn.commit()
        # Concurrent Lambdas: a rain-only warm instance must not overwrite a snapshot
        # that already has more live evidence verification stamps.
        local_ok = _evidence_verified_count(conn) if conn is not None else _sqlite_verified_count(Path(_DB))
        tmp = Path(_DB + ".remote-check")
        try:
            _s3_client().download_file(bucket, _DB_S3_KEY, str(tmp))
            remote_ok = _sqlite_verified_count(tmp)
            if remote_ok > local_ok:
                log.warning(
                    "shipit skip db persist: local verified=%s remote verified=%s",
                    local_ok,
                    remote_ok,
                )
                return
        except Exception:
            pass
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass
        _s3_client().upload_file(str(_DB), bucket, _DB_S3_KEY)
        _stamp_dynamo("db_persist")
    except Exception as exc:
        log.warning("shipit db persist failed: %s", exc)


restore_db_from_s3()
_app = create_app(db_path=_DB, live_fetch=True, enable_polling=True)
_asgi = Mangum(_app, lifespan="auto")
_bootstrapped = False
_evidence_lock = threading.Lock()
_evidence_running = False


def _stamp_dynamo(kind: str) -> None:
    table = os.environ.get("POINTS_TABLE", "").strip()
    if not table:
        return
    try:
        import boto3

        boto3.resource("dynamodb").Table(table).put_item(
            Item={
                "id": f"_shipit_{kind}",
                "kind": kind,
                "ts": datetime.now(timezone.utc).isoformat(),
            }
        )
    except Exception:
        pass


def _rain_record():
    registry = getattr(_app.state, "source_registry", None) or {}
    return registry.get("open-meteo-rain")


def _apply_live_rain(obs: dict[str, Any]) -> dict[str, Any]:
    conn = _app.state.conn
    live_body = {k: v for k, v in obs.items() if k != "last_live"}
    obs = dict(obs)
    obs["last_live"] = live_body
    save_rain(conn, obs)
    record = _rain_record()
    if record is not None:
        apply_success(
            record,
            value=obs.get("precip_mm"),
            observation_time=obs.get("observation_time") or obs.get("retrieved_at"),
            retrieved_at=obs.get("retrieved_at"),
            is_synthetic=False,
            units="mm",
        )
        sync_rain_record(record, obs)
    live = getattr(_app.state, "live_stats", None)
    if isinstance(live, dict):
        live["live_fetch"] = True
    return obs


def refresh_live_rain(*, force: bool = False) -> dict[str, Any]:
    """Pull Open-Meteo into the in-process store + registry."""
    conn = _app.state.conn
    rain = get_rain(conn)
    record = _rain_record()
    state = None if record is None else record.source_state
    needs = force or rain is None or bool(rain.get("is_synthetic")) or rain.get("source") in {
        "fixture",
        "scenario_slider",
    }
    if not needs and state is not None and state != SourceState.LIVE:
        needs = True
    if not needs and rain is not None and rain.get("source") == "open-meteo" and state == SourceState.LIVE:
        return {"ok": True, "skipped": True, "precip_mm": rain.get("precip_mm"), "source": rain.get("source")}

    try:
        obs = fetch_open_meteo()
    except RainUnavailable as exc:
        if record is not None:
            apply_failure(record, error_category="network")
        _stamp_dynamo("rain_live_fail")
        return {"ok": False, "error": str(exc)}
    applied = _apply_live_rain(obs)
    _stamp_dynamo("rain_live")
    persist_db_to_s3()
    return {
        "ok": True,
        "precip_mm": applied.get("precip_mm"),
        "source": applied.get("source"),
        "observation_time": applied.get("observation_time"),
        "source_state": None if _rain_record() is None else _rain_record().source_state.value,
    }


def refresh_live_evidence() -> dict[str, Any]:
    """Verify evidence URLs against live sources (EventBridge / direct invoke — not API GW)."""
    try:
        from backend.app.db.store import list_evidence, update_evidence
        from backend.app.services.evidence_live import verify_corpus

        rows = list_evidence(_app.state.conn)
        # Prefer OFFICIAL / non-volunteer first; cap so a 5‑min Lambda can finish.
        def _rank(row: dict[str, Any]) -> tuple[int, str]:
            channel = str(row.get("channel") or "").upper()
            official = 0 if channel == "OFFICIAL" or channel == "" else 1
            volunteer = 2 if "VOLUNTEER" in channel else 0
            return (official + volunteer, str(row.get("id") or ""))

        # Prefer rows not yet re-checked so later jobs fill the corpus.
        def _needs_check(row: dict[str, Any]) -> int:
            return 0 if not row.get("live_status") else 1

        ordered = sorted(rows, key=lambda row: (_needs_check(row), *_rank(row)))
        limit = int(os.environ.get("DP_EVIDENCE_MAX", "80"))
        batch = ordered[: max(1, limit)]
        updated, stats = verify_corpus(batch, delay_s=float(os.environ.get("DP_EVIDENCE_DELAY_S", "0.05")))
        for row in updated:
            update_evidence(_app.state.conn, row["id"], row)
        live = getattr(_app.state, "live_stats", None)
        if isinstance(live, dict):
            live["evidence_live_ok"] = stats["ok"]
            live["evidence_live_fail"] = stats["fail"]
            live["evidence_live_skipped"] = stats["skipped"]
            live["live_fetch"] = True
        record = (getattr(_app.state, "source_registry", None) or {}).get("evidence-live")
        if record is not None:
            record.source_state = SourceState.LIVE
            record.access_status = "active"
            record.last_success_at = datetime.now(timezone.utc).isoformat()
            record.retrieval_ok = True
            record.value = {"verified": stats["ok"], "fail": stats["fail"], "skipped": stats["skipped"]}
        _stamp_dynamo("evidence_live")
        persist_db_to_s3()
        return {"ok": True, "batch": len(batch), "corpus": len(rows), **stats}
    except Exception as exc:
        _stamp_dynamo("evidence_live_fail")
        return {"ok": False, "error": str(exc)}


def kick_evidence_async() -> None:
    """Start evidence verify off the request path (API GW 29s limit)."""
    global _evidence_running
    with _evidence_lock:
        if _evidence_running:
            return
        _evidence_running = True

    def _run() -> None:
        global _evidence_running
        try:
            result = refresh_live_evidence()
            log.info("shipit evidence async %s", result)
        finally:
            with _evidence_lock:
                _evidence_running = False

    threading.Thread(target=_run, name="dp-evidence-live", daemon=True).start()


def bootstrap_live() -> None:
    """Cold-start: force live Open-Meteo so Ship It is never fixture-dark."""
    global _bootstrapped
    if _bootstrapped:
        return
    rain_result = refresh_live_rain(force=True)
    log.info("shipit bootstrap rain %s", rain_result)
    evidence = (getattr(_app.state, "source_registry", None) or {}).get("evidence-live")
    if evidence is not None and evidence.source_state == SourceState.SCENARIO:
        evidence.source_state = SourceState.UNKNOWN
        evidence.access_status = "active"
    kick_evidence_async()
    _bootstrapped = True


try:
    bootstrap_live()
except Exception as exc:
    log.warning("shipit bootstrap failed: %s", exc)


def _is_schedule_event(event: dict[str, Any]) -> bool:
    if event.get("source") == "aws.events":
        return True
    if event.get("job") in {"evidence", "rain"}:
        return True
    detail = event.get("detail")
    return isinstance(detail, dict) and detail.get("job") in {"evidence", "rain"}


def _wants_evidence(event: dict[str, Any]) -> bool:
    if event.get("job") == "evidence":
        return True
    detail = event.get("detail")
    if isinstance(detail, dict) and detail.get("job") == "evidence":
        return True
    return "evidence" in str(event.get("detail-type") or "").lower()


def _http_method(event: dict[str, Any]) -> str:
    ctx = event.get("requestContext") or {}
    http = ctx.get("http") if isinstance(ctx, dict) else None
    if isinstance(http, dict) and http.get("method"):
        return str(http["method"]).upper()
    if event.get("httpMethod"):
        return str(event["httpMethod"]).upper()
    return ""


def handler(event: dict[str, Any], context: Any) -> Any:
    if isinstance(event, dict) and _is_schedule_event(event):
        if _wants_evidence(event):
            result = refresh_live_evidence()
        else:
            result = refresh_live_rain(force=True)
        return {"statusCode": 200 if result.get("ok") else 503, "body": json.dumps(result)}
    bootstrap_live()
    refresh_live_rain(force=False)
    _stamp_dynamo("api_invoke")
    response = _asgi(event, context)
    # Persist HITL / rain-scenario writes so cold starts do not restore a pre-confirm board.
    if isinstance(event, dict) and _http_method(event) in {"POST", "PUT", "PATCH", "DELETE"}:
        persist_db_to_s3()
    return response
