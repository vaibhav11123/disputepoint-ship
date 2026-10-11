"""Demo HITL seeds — ACK + officer confirms for HUMAN VERIFIED board mix."""

from backend.app.main import create_app
from backend.app.services.demo_hitl_seed import seed_demo_officer_confirms
from backend.app.services.ingest import open_store, ingest_fixtures
from backend.app.db.store import list_points


EXPECTED_CONFIRMS = {
    "dp-minto-bridge": "NDMC",
    "dp-azadpur-underpass": "MCD",
    "dp-ashram-underpass": "PWD",
    "dp-mehrauli-badarpur-saket": "DMRC",
}


def test_seed_demo_officer_confirms_assigns_four_agencies(tmp_path, monkeypatch):
    monkeypatch.setenv("DP_SEED_DEMO_CONFIRM", "1")
    monkeypatch.delenv("DP_SEED_DEMO_ACK", raising=False)
    db = tmp_path / "seed.sqlite"
    conn = open_store(db)
    ingest_fixtures(conn)
    seeded = seed_demo_officer_confirms(conn)
    assert set(seeded) == set(EXPECTED_CONFIRMS)
    by_id = {p["id"]: p for p in list_points(conn)}
    for point_id, agency in EXPECTED_CONFIRMS.items():
        point = by_id[point_id]
        assert point["ownership_state"] == "ASSIGNED"
        assert point["responsible_agency"] == agency
        assert point["officer_confirmed"] is True
        assert not point.get("escalated")
        assert point.get("decision_record", {}).get("agency") == agency
        assert point["decision_record"].get("seed") == "demo_hitl_seed"
    # Idempotent
    assert seed_demo_officer_confirms(conn) == []


def test_create_app_seeds_officer_confirms():
    app = create_app()
    conn = app.state.conn
    by_id = {p["id"]: p for p in list_points(conn)}
    for point_id, agency in EXPECTED_CONFIRMS.items():
        point = by_id[point_id]
        assert point["ownership_state"] == "ASSIGNED"
        assert point["responsible_agency"] == agency
        assert point["officer_confirmed"] is True
