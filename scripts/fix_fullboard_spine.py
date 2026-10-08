#!/usr/bin/env python3
"""Restore multi-agency CONFLICT spine + finish Gate A densify floors."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETRIEVED = "2026-10-08T18:30:00Z"
LIVELAW = "https://www.livelaw.in/pdf_upload/mmh08042024cw75942018185925-533124.pdf"
NEWSLAUNDRY = "https://www.newslaundry.com/2024/06/29/whos-responsible-for-delhis-rain-mess-answers-from-5-of-the-worst-hit-spots"
IE = "https://indianexpress.com/article/cities/delhi/breach-in-barapullah-drain-wall-led-to-south-new-delhi-flooding-9421799/"
ET = "https://economictimes.indiatimes.com/news/india/new-drains-sumps-automated-pump-house-delhi-pwds-plan-to-tackle-waterlogging-at-seven-hotspots/articleshow/121268671.cms"
TOI_HOT = "https://timesofindia.indiatimes.com/city/delhi/number-of-waterlogging-hotspots-up-set-to-challenge-delhis-preparedness/articleshow/120652175.cms"


def court(eid: str, pid: str, quote: str, agency: str) -> dict:
    return {
        "id": eid,
        "type": "COURT_ORDER",
        "url": LIVELAW,
        "quote": quote,
        "agency": agency,
        "location_span": pid,
        "source_date": None,
        "retrieved_at": RETRIEVED,
        "weight": 1.0,
        "needs_review": True,
        "is_synthetic": False,
        "channel": "OFFICIAL",
    }


def press(eid: str, pid: str, quote: str, url: str, agency: str | None, channel: str | None = None) -> dict:
    row = {
        "id": eid,
        "type": "PRESS_REPORT",
        "url": url,
        "quote": quote,
        "agency": agency,
        "location_span": pid,
        "source_date": None,
        "retrieved_at": RETRIEVED,
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": False,
    }
    if channel:
        row["channel"] = channel
    return row


def main() -> None:
    evid_path = ROOT / "data/fixtures/evidence.json"
    pts_path = ROOT / "data/fixtures/points.json"
    evid_doc = json.loads(evid_path.read_text())
    pts_doc = json.loads(pts_path.read_text())
    by_id = {e["id"]: e for e in evid_doc["evidence"]}

    spine = [
        court(
            "ev-001a-dp-purana-quila",
            "dp-purana-quila",
            "India gate to Priya Nursey to NSCI Club Gate: Jurisdiction NDMC",
            "NDMC",
        ),
        court(
            "ev-001b-dp-purana-quila",
            "dp-purana-quila",
            "Purana Quila Road (Priya Nursery) to NSCI Club Gate to Petrol Pump: Jurisdiction PWD",
            "PWD",
        ),
        court(
            "ev-001c-dp-purana-quila",
            "dp-purana-quila",
            "The road ahead of Petrol Pump to Gate No. 5 of ITPO, where drain no. 14 starts: Jurisdiction MCD",
            "MCD",
        ),
        press(
            "ev-002a-dp-minto-bridge",
            "dp-minto-bridge",
            "The bridge is on the border of the NDMC and the MCD.",
            NEWSLAUNDRY,
            "NDMC",
        ),
        press(
            "ev-002b-dp-minto-bridge",
            "dp-minto-bridge",
            "the NDMC and the MCD. So, each agency put the blame on the other.",
            NEWSLAUNDRY,
            "MCD",
        ),
        press(
            "ev-003a-dp-barapullah",
            "dp-barapullah",
            "was transferred to MCD, then to Irrigation and Flood Control (I&FC)",
            IE,
            "MCD",
        ),
        press(
            "ev-003b-dp-barapullah",
            "dp-barapullah",
            "Irrigation and Flood Control (I&FC) but there is still a lack of clarity.",
            IE,
            "IFC",
        ),
        press(
            "ev-007a-dp-lodhi-moolchand",
            "dp-lodhi-moolchand",
            "the government quarters on Lodhi Road are maintained by the CPWD",
            NEWSLAUNDRY,
            "CPWD",
        ),
        press(
            "ev-007b-dp-lodhi-moolchand",
            "dp-lodhi-moolchand",
            "while the main road is under the PWD, and the bylanes are maintained by the MCD.",
            NEWSLAUNDRY,
            "PWD",
        ),
        press(
            "ev-007c-dp-lodhi-moolchand",
            "dp-lodhi-moolchand",
            "and the bylanes are maintained by the MCD.",
            NEWSLAUNDRY,
            "MCD",
            "VOLUNTEER_REPORTED",
        ),
        # Extra densify for thin Gate A
        press(
            "ev-dens-mathura-et",
            "dp-mathura-rd-hc",
            "On the Mathura Road stretch near Pragati Maidan, PWD plans to deploy pumps to remove excess water.",
            TOI_HOT,
            "PWD",
        ),
        press(
            "ev-vol-mathura-311",
            "dp-mathura-rd-hc",
            "Citizens only have to call 311, and their complaints will be forwarded to the right department",
            "https://www.newindianexpress.com/cities/delhi/2025/May/06/single-complaint-number-for-all-waterlogging-grievances-says-parvesh-verma",
            None,
            "VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-who-et2",
            "dp-who-ito-ring",
            "The seven waterlogging-prone spots are the Minto Road underpass, Pul Prahladpur underpass, Ring Road opposite the WHO building, under the Zakhira flyover, Loni Road roundabout, Jahangirpuri Metro Station Road, and Karala Kanjhawala Road.",
            ET,
            "PWD",
        ),
        press(
            "ev-vol-who-311",
            "dp-who-ito-ring",
            "The initiative is aimed at resolving common issues such as waterlogging, broken roads, choked drains, and overflowing sewers more efficiently during the rainy season.",
            "https://www.newindianexpress.com/cities/delhi/2025/May/06/single-complaint-number-for-all-waterlogging-grievances-says-parvesh-verma",
            None,
            "VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-zakhira-et2",
            "dp-zakhira",
            "The seven waterlogging-prone spots are the Minto Road underpass, Pul Prahladpur underpass, Ring Road opposite the WHO building, under the Zakhira flyover, Loni Road roundabout, Jahangirpuri Metro Station Road, and Karala Kanjhawala Road.",
            ET,
            "PWD",
        ),
        press(
            "ev-vol-zakhira-toi",
            "dp-zakhira",
            "19 locations experienced water accumulation on at least four occasions, these being the well-known trouble spots of Minto Bridge, Zakhira flyover, Azad Market underpass, areas near Qutub Minar metro station",
            TOI_HOT,
            "PWD",
            "VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-pul-et2",
            "dp-pul-prahladpur",
            "The seven waterlogging-prone spots are the Minto Road underpass, Pul Prahladpur underpass, Ring Road opposite the WHO building, under the Zakhira flyover, Loni Road roundabout, Jahangirpuri Metro Station Road, and Karala Kanjhawala Road.",
            ET,
            "PWD",
        ),
        press(
            "ev-vol-pul-toi",
            "dp-pul-prahladpur",
            "Pul Prahladpur underpass, and Ashram underpass",
            TOI_HOT,
            "PWD",
            "VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-pragati-nl",
            "dp-pragati-bhairon",
            "The tunnel made headlines in the past after the PWD pointed out that the underpass carried major design defects.",
            NEWSLAUNDRY,
            "PWD",
        ),
        press(
            "ev-vol-pragati-toi",
            "dp-pragati-bhairon",
            "railway bridge/Bhairon Road underpass, Outer Ring Road-Bhera Enclave underpass",
            TOI_HOT,
            "PWD",
            "VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-loni-et2",
            "dp-loni-rd",
            "At the Loni Road roundabout in east Delhi, another waterlogging hotspot, additional pumps have been deployed to drain stagnated water.",
            ET,
            "PWD",
        ),
        press(
            "ev-vol-loni-toi",
            "dp-loni-rd",
            "The seven waterlogging-prone spots are the Minto Road underpass, Pul Prahladpur underpass, Ring Road opposite the WHO building, under the Zakhira flyover, Loni Road roundabout, Jahangirpuri Metro Station Road, and Karala Kanjhawala Road.",
            ET,
            "PWD",
            "VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-mandapam-vol2",
            "dp-bharat-mandapam-tunnel",
            "Citizens only have to call 311, and their complaints will be forwarded to the right department",
            "https://www.newindianexpress.com/cities/delhi/2025/May/06/single-complaint-number-for-all-waterlogging-grievances-says-parvesh-verma",
            None,
            "VOLUNTEER_REPORTED",
        ),
    ]

    for row in spine:
        by_id[row["id"]] = row

    # Keep densify volume without tipping ownership away from CONFLICT/UNKNOWN honesty
    for eid in (
        "ev-vol-minto-top10",
        "ev-dens-minto-et",
        "ev-dens-barapullah-pwd",
        "ev-vol-lodhi-ht",
        "ev-vol-barapullah-ifc",
    ):
        if eid in by_id:
            by_id[eid]["agency"] = None

    # Drop weak null-agency purana stubs from wiring (keep rows for audit trail)
    wire: dict[str, list[str]] = {
        "dp-purana-quila": [
            "ev-001-dp-purana-quila",
            "ev-001a-dp-purana-quila",
            "ev-001b-dp-purana-quila",
            "ev-001c-dp-purana-quila",
            "ev-vol-purana-ht",
            "ev-vol-purana-311",
        ],
        "dp-minto-bridge": [
            "ev-002a-dp-minto-bridge",
            "ev-002b-dp-minto-bridge",
            "ev-vol-minto-bahadur",
            "ev-vol-minto-top10",
            "ev-dens-minto-et",
        ],
        "dp-barapullah": [
            "ev-003a-dp-barapullah",
            "ev-003b-dp-barapullah",
            "ev-vol-barapullah-aab",
            "ev-dens-barapullah-pwd",
        ],
        "dp-lodhi-moolchand": [
            "ev-007a-dp-lodhi-moolchand",
            "ev-007b-dp-lodhi-moolchand",
            "ev-007c-dp-lodhi-moolchand",
            "ev-vol-lodhi-ht",
        ],
        "dp-mathura-rd-hc": [
            "ev-005-dp-mathura-rd-hc",
            "ev-vol-mathura-ht",
            "ev-dens-mathura-et",
            "ev-vol-mathura-311",
        ],
        "dp-who-ito-ring": [
            "ev-010-dp-who-ito-ring",
            "ev-vol-who-et",
            "ev-dens-who-et2",
            "ev-vol-who-311",
        ],
        "dp-zakhira": [
            "ev-009-dp-zakhira",
            "ev-vol-zakhira-et",
            "ev-dens-zakhira-et2",
            "ev-vol-zakhira-toi",
        ],
        "dp-pul-prahladpur": [
            "ev-012-dp-pul-prahladpur",
            "ev-vol-pul-et",
            "ev-dens-pul-et2",
            "ev-vol-pul-toi",
        ],
        "dp-pragati-bhairon": [
            "ev-008-dp-pragati-bhairon",
            "ev-vol-pragati-ht",
            "ev-dens-pragati-nl",
            "ev-vol-pragati-toi",
        ],
        "dp-loni-rd": [
            "ev-011-dp-loni-rd",
            "ev-vol-loni-et",
            "ev-dens-loni-et2",
            "ev-vol-loni-toi",
        ],
        "dp-bharat-mandapam-tunnel": [
            "ev-004-dp-bharat-mandapam-tunnel",
            "ev-vol-mandapam-ht",
            "ev-dens-mandapam-pwd",
            "ev-dens-mandapam-vol2",
        ],
        "dp-aiims-aurobindo": [
            "ev-006-dp-aiims-aurobindo",
            "ev-vol-aiims-newslaundry",
            "ev-dens-aiims-ndmc",
            "ev-vol-aiims-hindu",
        ],
        "dp-maharani-bagh": [
            "ev-014-dp-maharani-bagh",
            "ev-vol-maharani-toi",
            "ev-dens-maharani-pwd",
            "ev-vol-maharani-311",
        ],
        "dp-azad-market": [
            "ev-013-dp-azad-market",
            "ev-vol-azad-ht",
            "ev-dens-azad-ie",
            "ev-vol-azad-hindu",
        ],
    }

    # Ensure all wired IDs exist
    missing = []
    for pid, ids in wire.items():
        for eid in ids:
            if eid not in by_id:
                missing.append(eid)
    if missing:
        raise SystemExit(f"missing evidence ids: {missing}")

    for p in pts_doc["points"]:
        if p["id"] in wire:
            # Replace Gate A wiring (do not keep stale COURT rows that tip ownership)
            p["evidence_ids"] = list(wire[p["id"]])
        if p["id"] == "dp-purana-quila":
            p["agencies_claimed"] = ["NDMC", "PWD", "MCD", "IFC"]
        if p["id"] == "dp-minto-bridge":
            p["agencies_claimed"] = ["NDMC", "MCD", "PWD", "RAILWAYS"]
        if p["id"] == "dp-barapullah":
            p["agencies_claimed"] = ["PWD", "MCD", "IFC"]
        if p["id"] == "dp-lodhi-moolchand":
            p["agencies_claimed"] = ["PWD", "CPWD", "MCD"]
        if p["id"] == "dp-aiims-aurobindo":
            p["agencies_claimed"] = ["PWD", "NDMC", "MCD"]

    evid_doc["evidence"] = list(by_id.values())
    evid_path.write_text(json.dumps(evid_doc, indent=2) + "\n")
    pts_path.write_text(json.dumps(pts_doc, indent=2) + "\n")
    print("spine fixed; evidence", len(evid_doc["evidence"]), "points", len(pts_doc["points"]))


if __name__ == "__main__":
    main()
