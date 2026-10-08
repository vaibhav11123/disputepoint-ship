"""T-DATA-01. Queue length comes from the seed. Coordinates match the seed only."""

import json
from pathlib import Path

from backend.app.db.store import connect
from backend.app.services.ingest import ingest_fixtures, load_point

ROOT = Path(__file__).resolve().parents[1]


def test_t_data_01_loads_seed_without_inventing_coordinates() -> None:
    conn = connect(":memory:")
    points = ingest_fixtures(conn, ROOT)
    raw = json.loads((ROOT / "data/fixtures/points.json").read_text())["points"]
    by_id = {row["id"]: row for row in raw}
    assert len(points) >= 12
    assert len(points) == len(raw)
    assert [point["priority_rank"] for point in points] == list(range(1, len(points) + 1))
    for point in points:
        seed = by_id[point["id"]]
        assert point["id"].startswith("dp-")
        assert point["lat"] == seed.get("lat")
        assert point["lon"] == seed.get("lon")
        assert set(point["components"]) == {"R", "S", "C", "Q", "U", "G"}
        if point["ownership_state"] == "CONFLICT":
            assert point["responsible_agency"] is None
    card = load_point(conn, "dp-purana-quila")
    assert card is not None
    assert card["evidence"]
    assert card["responsible_agency"] is None
    assert card["lat"] == 28.61497
    assert load_point(conn, "dp-barapullah")["lat"] == 28.5841993
    assert load_point(conn, "dp-purana-quila")["ownership_state"] == "CONFLICT"
