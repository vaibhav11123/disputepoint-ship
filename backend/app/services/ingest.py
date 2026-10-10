"""Load seed fixtures into the local store. Never invent lat, lon, or severity."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from backend.app.db.store import connect, get_point, get_rain, list_points, replace_corpus, update_point
from backend.app.services.evidence import load_evidence
from backend.app.services.ownership import EvidenceScore, decide
from backend.app.services.priority import priority

FIXTURE_RETRIEVED_AT = "2026-10-06T00:00:00Z"
ROOT = Path(__file__).resolve().parents[3]


def repo_root() -> Path:
    return ROOT


def _dry_rain() -> dict[str, Any]:
    return {
        "lat": 28.6139,
        "lon": 77.2090,
        "window_hours": 6,
        "precip_mm": 0,
        "source": "fixture",
        "retrieved_at": FIXTURE_RETRIEVED_AT,
        "is_synthetic": True,
    }


def _score_point(raw: dict[str, Any], evidence: list[Any], readiness: dict[str, Any] | None, precip_mm: float) -> dict[str, Any]:
    decision = decide(
        [
            EvidenceScore(type=item.type.value, agency=item.agency, channel=item.channel)
            for item in evidence
        ]
    )
    readiness_body = None if readiness is None else {
        "state": readiness["state"],
        "is_synthetic": readiness["is_synthetic"],
    }
    probe = SimpleNamespace(
        severity=raw.get("severity"),
        is_arterial=bool(raw.get("is_arterial", False)),
        is_underpass=bool(raw.get("is_underpass", False)),
        recurrence_class=raw.get("recurrence_class"),
        ownership_confidence=decision.ownership_confidence,
        ownership_state=decision.ownership_state.value,
        readiness=readiness_body,
    )
    ranked = priority(probe, precip_mm=precip_mm)
    agency = None if decision.responsible_agency is None else decision.responsible_agency.value
    if decision.ownership_state.value == "CONFLICT":
        action = "Escalate to coordination cell"
    elif agency:
        action = f"Ask {agency}"
    else:
        action = "Escalate to coordination cell"
    body = {
        "id": raw["id"],
        "name": raw["name"],
        "lat": raw.get("lat"),
        "lon": raw.get("lon"),
        "agencies_claimed": raw["agencies_claimed"],
        "evidence_ids": raw.get("evidence_ids", []),
        "ownership_confidence": decision.ownership_confidence,
        "ownership_state": decision.ownership_state.value,
        "responsible_agency": agency,
        "recurrence_class": raw.get("recurrence_class"),
        "is_underpass": raw.get("is_underpass"),
        "is_arterial": raw.get("is_arterial"),
        "readiness": readiness_body,
        "priority_score": ranked.score,
        "priority_rank": 0,
        "components": ranked.components,
        "explanation": ranked.explanation,
        "counterfactuals": ranked.counterfactuals,
        "recommended_action": action,
        "status": raw.get("status", "OPEN"),
        "advisory": True,
        "provenance": {
            "source": "data/fixtures/points.json",
            "retrieved_at": FIXTURE_RETRIEVED_AT,
            "is_synthetic": False,
            "is_derived": True,
        },
        "uncertainty_band": "UNCERTAIN" if decision.ownership_confidence < 0.65 else (
            "HIGH" if decision.ownership_confidence >= 0.85 else "MEDIUM"
        ),
    }
    for key in (
        "geo_source",
        "geo_query",
        "geo_osm_id",
        "geo_licence",
        "geo_display_name",
        "verify_status",
        "geo_cite",
        "incident_summary",
        "claim_summaries",
    ):
        if key in raw:
            body[key] = raw[key]
    return body


def build_corpus(root: Path | None = None, precip_mm: float = 0.0) -> tuple[list[dict[str, Any]], list[tuple[str, str, dict[str, Any]]]]:
    root = root or repo_root()
    points_doc = json.loads((root / "data/fixtures/points.json").read_text())
    readiness_doc = json.loads((root / "data/fixtures/readiness.json").read_text())
    readiness_by_id = {row["point_id"]: row for row in readiness_doc["readiness"]}
    evidence = load_evidence(root / "data/fixtures/evidence.json")
    by_id = {item.id: item for item in evidence}
    scored = []
    evidence_rows: list[tuple[str, str, dict[str, Any]]] = []
    for raw in points_doc["points"]:
        attached = [by_id[evidence_id] for evidence_id in raw.get("evidence_ids", [])]
        point = _score_point(raw, attached, readiness_by_id.get(raw["id"]), precip_mm)
        scored.append(point)
        for item in attached:
            evidence_rows.append((raw["id"], item.id, item.model_dump(mode="json")))
    scored.sort(key=lambda point: (-point["priority_score"], point["id"]))
    for index, point in enumerate(scored, start=1):
        point["priority_rank"] = index
    return scored, evidence_rows


def ingest_fixtures(conn, root: Path | None = None, precip_mm: float = 0.0) -> list[dict[str, Any]]:
    points, evidence_rows = build_corpus(root, precip_mm)
    rain = _dry_rain()
    rain["precip_mm"] = precip_mm
    if precip_mm:
        rain["source"] = "scenario_slider"
        rain["is_synthetic"] = True
    replace_corpus(conn, points, evidence_rows, rain)
    return points


def rescore(conn, precip_mm: float) -> list[dict[str, Any]]:
    current = list_points(conn)
    rain = get_rain(conn)
    previous_rank = {point["id"]: point.get("priority_rank") for point in current}
    probes = []
    for point in current:
        probe = SimpleNamespace(
            severity=point.get("severity"),
            is_arterial=bool(point.get("is_arterial")),
            is_underpass=bool(point.get("is_underpass")),
            recurrence_class=point.get("recurrence_class"),
            ownership_confidence=point["ownership_confidence"],
            ownership_state=point["ownership_state"],
            readiness=point.get("readiness"),
        )
        ranked = priority(probe, precip_mm=precip_mm)
        point["priority_score"] = ranked.score
        point["components"] = ranked.components
        point["explanation"] = ranked.explanation
        point["counterfactuals"] = ranked.counterfactuals
        probes.append(point)
    probes.sort(key=lambda point: (-point["priority_score"], point["id"]))
    for index, point in enumerate(probes, start=1):
        prior = previous_rank.get(point["id"])
        point["priority_rank"] = index
        point["rain_delta"] = None if prior is None else prior - index
        update_point(conn, point)
    # Do not invent a dry fixture observation when rain cache is empty.
    # Historical replay keeps display mm (station/period context) while scoring uses precip_mm arg.
    if rain is not None and rain.get("source") != "historical_replay" and rain.get("priority_uses") is not False:
        rain["precip_mm"] = precip_mm
        from backend.app.db.store import save_rain

        save_rain(conn, rain)
    return probes


def open_store(path: str | Path):
    return connect(path)


def load_point(conn, point_id: str):
    return get_point(conn, point_id)
