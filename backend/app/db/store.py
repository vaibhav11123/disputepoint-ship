"""Local SQLite store. DynamoDB is the AWS shape; this is the local substitute."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS points (
  id TEXT PRIMARY KEY,
  body TEXT NOT NULL,
  priority_score REAL NOT NULL,
  status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS evidence (
  id TEXT PRIMARY KEY,
  point_id TEXT NOT NULL,
  body TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS rain_cache (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  precip_mm REAL NOT NULL,
  retrieved_at TEXT NOT NULL,
  mode TEXT NOT NULL,
  body TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  point_id TEXT NOT NULL,
  action TEXT NOT NULL,
  ts TEXT NOT NULL,
  body TEXT NOT NULL
);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def replace_corpus(
    conn: sqlite3.Connection,
    points: list[dict[str, Any]],
    evidence_rows: list[tuple[str, str, dict[str, Any]]],
    rain: dict[str, Any],
) -> None:
    conn.execute("DELETE FROM points")
    conn.execute("DELETE FROM evidence")
    for point in points:
        conn.execute(
            "INSERT INTO points (id, body, priority_score, status) VALUES (?, ?, ?, ?)",
            (point["id"], json.dumps(point), point["priority_score"], point["status"]),
        )
    for point_id, evidence_id, body in evidence_rows:
        conn.execute(
            "INSERT INTO evidence (id, point_id, body) VALUES (?, ?, ?)",
            (evidence_id, point_id, json.dumps(body)),
        )
    save_rain(conn, rain)
    conn.commit()


def list_points(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT body FROM points ORDER BY priority_score DESC, id ASC").fetchall()
    return [json.loads(row["body"]) for row in rows]


def get_point(conn: sqlite3.Connection, point_id: str) -> dict[str, Any] | None:
    row = conn.execute("SELECT body FROM points WHERE id = ?", (point_id,)).fetchone()
    if row is None:
        return None
    point = json.loads(row["body"])
    evidence = conn.execute("SELECT body FROM evidence WHERE point_id = ? ORDER BY id", (point_id,)).fetchall()
    point["evidence"] = [json.loads(item["body"]) for item in evidence]
    point["audit"] = list_audit(conn, point_id)
    return point


def update_point(conn: sqlite3.Connection, point: dict[str, Any]) -> None:
    conn.execute(
        "UPDATE points SET body = ?, priority_score = ?, status = ? WHERE id = ?",
        (json.dumps(point), point["priority_score"], point["status"], point["id"]),
    )
    conn.commit()


def save_rain(conn: sqlite3.Connection, rain: dict[str, Any]) -> None:
    conn.execute("DELETE FROM rain_cache")
    conn.execute(
        "INSERT INTO rain_cache (id, precip_mm, retrieved_at, mode, body) VALUES (1, ?, ?, ?, ?)",
        (rain["precip_mm"], rain["retrieved_at"], rain["source"], json.dumps(rain)),
    )
    conn.commit()


def get_rain(conn: sqlite3.Connection) -> dict[str, Any] | None:
    row = conn.execute("SELECT body FROM rain_cache WHERE id = 1").fetchone()
    return None if row is None else json.loads(row["body"])


def add_audit(conn: sqlite3.Connection, row: dict[str, Any]) -> dict[str, Any]:
    conn.execute(
        "INSERT INTO audit (point_id, action, ts, body) VALUES (?, ?, ?, ?)",
        (row["point_id"], row["action"], row["timestamp"], json.dumps(row)),
    )
    conn.commit()
    return row


def list_audit(conn: sqlite3.Connection, point_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT body FROM audit WHERE point_id = ? ORDER BY id",
        (point_id,),
    ).fetchall()
    return [json.loads(row["body"]) for row in rows]
