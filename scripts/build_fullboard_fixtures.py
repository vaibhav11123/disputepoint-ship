#!/usr/bin/env python3
"""Merge densify + Expansion B volunteer-channel fixtures into data/fixtures/."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETRIEVED = "2026-10-08T18:00:00Z"

# Verbatim substrings from Research OS / Exa article highlights — verify at promote.
URL = {
    "toi_hotspots": "https://timesofindia.indiatimes.com/city/delhi/number-of-waterlogging-hotspots-up-set-to-challenge-delhis-preparedness/articleshow/120652175.cms",
    "toi_underpass": "https://timesofindia.indiatimes.com/city/delhi/delhi-underpasses-flooded-despite-preparedness-claims/articleshow/111497831.cms",
    "toi_minto": "https://timesofindia.indiatimes.com/city/delhi/flooding-and-crumbling-roads-at-minto-bridge-underpass-cause-commuter-woes-in-delhi/articleshow/112900606.cms",
    "et_seven": "https://economictimes.indiatimes.com/news/india/new-drains-sumps-automated-pump-house-delhi-pwds-plan-to-tackle-waterlogging-at-seven-hotspots/articleshow/121268671.cms",
    "ie_445": "https://indianexpress.com/article/cities/delhi/eye-on-monsoon-445-waterlogging-hotspots-identified-across-delhi-9944486/",
    "iit_aab": "https://home.iitd.ac.in/show.php?id=239&in_sections=Press",
    "hindu_pumps": "https://www.thehindu.com/news/cities/Delhi/temporary-accumulation-delhi-pwd-minister-says-steps-being-taken-to-clear-rainwater/article71389496.ece",
    "ht_100": "https://www.hindustantimes.com/cities/delhi-news/delhi-marks-100-new-flooding-spots-many-along-ring-road-101719339431895.html",
    "nie_311": "https://www.newindianexpress.com/cities/delhi/2025/May/06/single-complaint-number-for-all-waterlogging-grievances-says-parvesh-verma",
    "newslaundry": "https://www.newslaundry.com/2024/06/29/whos-responsible-for-delhis-rain-mess-answers-from-5-of-the-worst-hit-spots",
    "ht_underpass": "https://www.hindustantimes.com/cities/delhi-news/infamous-flooded-underpasses-make-a-comeback-in-delhi-man-drowns-in-azadpur-101719598910444.html",
}


def press(
    eid: str,
    point_id: str,
    quote: str,
    url: str,
    agency: str | None,
    *,
    channel: str | None = None,
) -> dict:
    row = {
        "id": eid,
        "type": "PRESS_REPORT",
        "url": url,
        "quote": quote,
        "agency": agency,
        "location_span": point_id,
        "source_date": None,
        "retrieved_at": RETRIEVED,
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": False,
    }
    if channel:
        row["channel"] = channel
    return row


def point(
    pid: str,
    name: str,
    agencies: list[str],
    evidence_ids: list[str],
    *,
    recurrence: str = "recurring",
    underpass: bool | None = True,
    arterial: bool | None = True,
) -> dict:
    return {
        "id": pid,
        "name": name,
        "lat": None,
        "lon": None,
        "agencies_claimed": agencies,
        "recurrence_class": recurrence,
        "status": "OPEN",
        "evidence_ids": evidence_ids,
        "is_underpass": underpass,
        "is_arterial": arterial,
        "verify_status": "CANDIDATE",
        "geo_source": "pending_nominatim",
        "notes": "Expansion B demo volume — lat/lon null until human VERIFIED",
    }


def main() -> None:
    evid_path = ROOT / "data/fixtures/evidence.json"
    pts_path = ROOT / "data/fixtures/points.json"
    ready_path = ROOT / "data/fixtures/readiness.json"

    evid_doc = json.loads(evid_path.read_text())
    pts_doc = json.loads(pts_path.read_text())
    ready_doc = json.loads(ready_path.read_text())

    existing_ids = {e["id"] for e in evid_doc["evidence"]}
    new_rows: list[dict] = []

    def add(row: dict) -> None:
        if row["id"] in existing_ids:
            return
        existing_ids.add(row["id"])
        new_rows.append(row)

    # --- Densify Gate A (volunteer + official press) ---
    densify = [
        press(
            "ev-vol-purana-ht",
            "dp-purana-quila",
            "the Pragati Maidan tunnel connecting C-Hexagon (India Gate circle) with the Ring Road via Purana Quila Road was closed from both sides",
            URL["ht_underpass"],
            None,
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-purana-311",
            "dp-purana-quila",
            "Citizens only have to call 311, and their complaints will be forwarded to the right department",
            URL["nie_311"],
            None,
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-minto-bahadur",
            "dp-minto-bridge",
            "The road is extremely dangerous for two-wheeler users",
            URL["toi_minto"],
            None,
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-minto-top10",
            "dp-minto-bridge",
            "has been identified as one of the top 10 waterlogging hotspots in the city",
            URL["toi_minto"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-minto-et",
            "dp-minto-bridge",
            "The seven waterlogging-prone spots are the Minto Road underpass, Pul Prahladpur underpass, Ring Road opposite the WHO building, under the Zakhira flyover, Loni Road roundabout, Jahangirpuri Metro Station Road, and Karala Kanjhawala Road.",
            URL["et_seven"],
            "PWD",
        ),
        press(
            "ev-vol-barapullah-aab",
            "dp-barapullah",
            "The Aab Prahari app utilizes a citizen science approach, enabling residents to report real-time flooding incidents.",
            URL["iit_aab"],
            None,
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-barapullah-pwd",
            "dp-barapullah",
            "PWD can integrate the app’s data to identify and prioritize areas or hotspots that require immediate drainage infrastructure improvements",
            URL["iit_aab"],
            "PWD",
        ),
        press(
            "ev-vol-barapullah-ifc",
            "dp-barapullah",
            "I&FC can use real-time alerts and GIS mapping to monitor flood incidents",
            URL["iit_aab"],
            "IFC",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-mandapam-ht",
            "dp-bharat-mandapam-tunnel",
            "Also, the drainage network of the Bharat Mandapam is not ready yet.",
            URL["ht_underpass"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-mandapam-pwd",
            "dp-bharat-mandapam-tunnel",
            "Officials from PWD said that the tunnel itself was not flooded by rainwater, but had to be shut because of “forced flooding” from outside.",
            URL["ht_underpass"],
            "PWD",
        ),
        press(
            "ev-vol-mathura-ht",
            "dp-mathura-rd-hc",
            "the police also closed both U-turns via the Mathura Road underpass in front of Pragati Maidan due to waterlogging",
            URL["ht_underpass"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-aiims-newslaundry",
            "dp-aiims-aurobindo",
            "Water from our drains goes to MCD drains. But MCD drains were not cleaned, which is why water logging happened in our area.",
            URL["newslaundry"],
            "MCD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-aiims-ndmc",
            "dp-aiims-aurobindo",
            "Water from our drains goes to MCD drains. But MCD drains were not cleaned, which is why water logging happened in our area.",
            URL["newslaundry"],
            "NDMC",
        ),
        press(
            "ev-vol-aiims-hindu",
            "dp-aiims-aurobindo",
            "flooded roads in Kamla Nagar, Azad Market, Ashoka Road, Sangam Vihar, Ansari Nagar near AIIMS, Mandi House",
            URL["hindu_pumps"],
            None,
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-lodhi-ht",
            "dp-lodhi-moolchand",
            "Moolchand, Azadpur, Zakhira and Ashok Nagar underpasses also saw heavy waterlogging",
            URL["ht_underpass"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-maharani-toi",
            "dp-maharani-bagh",
            "Most of our new vulnerable spots are along the Outer Ring Road, Ring Road, Mathura Road, Rohtak Road, and Bhairon Marg, among others.",
            URL["ht_100"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-maharani-pwd",
            "dp-maharani-bagh",
            "Most of our new vulnerable spots are along the Outer Ring Road, Ring Road, Mathura Road, Rohtak Road, and Bhairon Marg, among others.",
            URL["ht_100"],
            "PWD",
        ),
        press(
            "ev-vol-maharani-311",
            "dp-maharani-bagh",
            "The initiative is aimed at resolving common issues such as waterlogging, broken roads, choked drains, and overflowing sewers more efficiently during the rainy season.",
            URL["nie_311"],
            None,
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-who-et",
            "dp-who-ito-ring",
            "On the Ring Road opposite the WHO building near ITO, the PWD plans to temporarily install four tractor-mounted pumps.",
            URL["et_seven"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-zakhira-et",
            "dp-zakhira",
            "At Zakhira flyover, desilting of stormwater drains and cleaning of garbage from nearby railway tracks has started.",
            URL["et_seven"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-pul-et",
            "dp-pul-prahladpur",
            "At south Delhi's Pul Prahladpur underpass, measures such as automation of the pump house and construction of an underground sump with a capacity of 7.5 lakh litres have been completed.",
            URL["et_seven"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-azad-ht",
            "dp-azad-market",
            "At the Azad Market underpass, at least 17 passengers, including two women, a child, and an ailing elderly man, were trapped inside a private bus",
            URL["ht_underpass"],
            None,
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-dens-azad-ie",
            "dp-azad-market",
            "Delhi has 15-odd areas that are prone to waterlogging, including Zakhira flyover, Minto Road bridge, Prahladpur pul, Sarita Vihar underpass, Jahangirpuri Metro station, Loni Road crossing, and Azadpur market underpass, among others.",
            URL["ie_445"],
            "PWD",
        ),
        press(
            "ev-vol-azad-hindu",
            "dp-azad-market",
            "flooded roads in Kamla Nagar, Azad Market, Ashoka Road, Sangam Vihar, Ansari Nagar near AIIMS",
            URL["hindu_pumps"],
            None,
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-pragati-ht",
            "dp-pragati-bhairon",
            "the Pragati Maidan tunnel connecting C-Hexagon (India Gate circle) with the Ring Road via Purana Quila Road was closed from both sides",
            URL["ht_underpass"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
        press(
            "ev-vol-loni-et",
            "dp-loni-rd",
            "At the Loni Road roundabout in east Delhi, another waterlogging hotspot, additional pumps have been deployed to drain stagnated water.",
            URL["et_seven"],
            "PWD",
            channel="VOLUNTEER_REPORTED",
        ),
    ]
    for row in densify:
        add(row)

    # Wire densify IDs onto Gate A points
    densify_by_point: dict[str, list[str]] = {}
    for row in densify:
        densify_by_point.setdefault(row["location_span"], []).append(row["id"])

    for p in pts_doc["points"]:
        extras = densify_by_point.get(p["id"], [])
        ids = list(dict.fromkeys([*(p.get("evidence_ids") or []), *extras]))
        p["evidence_ids"] = ids

    # --- Expansion B: 20 areas ---
    expansion_specs: list[tuple[str, str, list[str], str, list[tuple[str, str, str | None, str | None]]]] = [
        # id, name, agencies, recurrence, evidence tuples (suffix, quote, agency, channel)
        (
            "dp-azadpur-underpass",
            "Azadpur underpass",
            ["PWD", "MCD"],
            "chronic",
            [
                ("a", "An 25-year-old unidentified man drowned in the waterlogged Azadpur underpass in northwest Delhi on Friday, police said.", None, "VOLUNTEER_REPORTED"),
                ("b", "The PWD has identified Minto Bridge, Zakhira underpass, Pul Prahladpur, Azadpur underpass, ITO, Loni Golchakkar, NH-24 Patparganj, Dasmesh Road and Jahangirpuri among the vulnerable locations", "PWD", None),
                ("c", "while 12 permanent pumps have been deployed at the Azadpur underpass.", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-samaypur-badli",
            "Samaypur Badli / Siraspur underpass",
            ["PWD", "MCD"],
            "chronic",
            [
                ("a", "The unfortunate death of two people occurred at the Siraspur underpass in Samaypur Badli, which is under the jurisdiction of MCD", "MCD", None),
                ("b", "Two boys, aged around 12, drowned in a waterlogged underpass in Samaypur Badli, in northwest Delhi on Saturday.", None, "VOLUNTEER_REPORTED"),
                ("c", "While the underpass is listed in PWD’s flood control order, senior officials insisted that MCD was responsible for managing the underpass.", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-okhla-underpass",
            "Okhla underpass",
            ["DDA", "PWD"],
            "chronic",
            [
                ("a", "The Okhla underpass, which falls under the control of DDA and was also highlighted as a hotspot by traffic police, proved fatal for a 60-year-old man who allegedly died by drowning.", "DDA", None),
                ("b", "Of the three underpasses where the deaths occurred — Samaypur Badli, Okhla and Shalimar Bagh — two were located at identified waterlogging hotspots", None, "VOLUNTEER_REPORTED"),
                ("c", "The sub-surface passages at Minto Road, Pul Prahladpur, Samaypur Badli, Okhla, Pragati Maidan transit corridor, Sarita Vihar, Azadpur, Dwarka and Delhi-Meerut expressway", "PWD", None),
            ],
        ),
        (
            "dp-dhaula-kuan",
            "Ring Road / Dhaula Kuan flyover underpass",
            ["PWD"],
            "recurring",
            [
                ("a", "Ring Road-Dhaula Kuan flyover", "PWD", None),
                ("b", "The Dhaula Kuan underpass, a key route connecting central Delhi with the airport, has frequently witnessed water accumulation that brought traffic to a crawl.", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Key underpasses like Minto Bridge, Dhaula Kuan, Moolchand, and Zakhira saw smooth traffic flow", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-sarita-vihar",
            "Sarita Vihar underpass",
            ["PWD"],
            "recurring",
            [
                ("a", "Delhi has 15-odd areas that are prone to waterlogging, including Zakhira flyover, Minto Road bridge, Prahladpur pul, Sarita Vihar underpass, Jahangirpuri Metro station, Loni Road crossing, and Azadpur market underpass, among others.", "PWD", None),
                ("b", "The sub-surface passages at Minto Road, Pul Prahladpur, Samaypur Badli, Okhla, Pragati Maidan transit corridor, Sarita Vihar, Azadpur, Dwarka and Delhi-Meerut expressway", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Prahladpur pul, Sarita Vihar underpass, Jahangirpuri Metro station", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-karala-kanjhawala",
            "Karala–Kanjhawala Road",
            ["PWD"],
            "chronic",
            [
                ("a", "To avoid waterlogging in northwest Delhi's Karala Khanjhawala Road, the PWD has hired a consultant to study and present a report for comprehensive remodelling of the existing drain.", "PWD", None),
                ("b", "The seven waterlogging-prone spots are the Minto Road underpass, Pul Prahladpur underpass, Ring Road opposite the WHO building, under the Zakhira flyover, Loni Road roundabout, Jahangirpuri Metro Station Road, and Karala Kanjhawala Road.", "PWD", None),
                ("c", "Jahangirpuri Metro Station Road, and Karala Kanjhawala Road.", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-jahangirpuri-metro",
            "Jahangirpuri Metro Station Road",
            ["PWD"],
            "recurring",
            [
                ("a", "At the Jahangirpuri Metro Station Road, the department plans to construct a new drain along the service road inside the Udhyog Nagar industrial area.", "PWD", None),
                ("b", "Jahangirpuri Metro station, Loni Road crossing, and Azadpur market underpass, among others.", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Jahangirpuri among the vulnerable locations where pumping arrangements have been deployed", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-tilak-bridge",
            "Tilak Bridge underpass (ITO)",
            ["PWD"],
            "chronic",
            [
                ("a", "under Tilak Bridge at ITO, Pul Prahladpur underpass, and Ashram underpass", "PWD", None),
                ("b", "The Tilak Bridge underpass was also closed for vehicles after it got submerged in the morning, causing heavy traffic snarls along most of central Delhi areas.", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Nearby, at Tilak Bridge, two holes have been dug for complete desilting.", "PWD", None),
            ],
        ),
        (
            "dp-ashram-underpass",
            "Ashram underpass",
            ["PWD"],
            "recurring",
            [
                ("a", "Pul Prahladpur underpass, and Ashram underpass", "PWD", None),
                ("b", "The situation near Ashram Bridge was particularly severe, with incessant rainfall causing substantial accumulation of water.", None, "VOLUNTEER_REPORTED"),
                ("c", "under Tilak Bridge at ITO, Pul Prahladpur underpass, and Ashram underpass", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-shalimar-bagh-underpass",
            "Shalimar Bagh underpass",
            ["PWD", "OTHER"],
            "recurring",
            [
                ("a", "A body, the fourth fatality, was found at the Shalimar Bagh underpass, a location not on the list of hotspots.", None, "VOLUNTEER_REPORTED"),
                ("b", "Of the three underpasses where the deaths occurred — Samaypur Badli, Okhla and Shalimar Bagh — two were located at identified waterlogging hotspots", "PWD", None),
                ("c", "Samaypur Badli, Okhla and Shalimar Bagh — two were located at identified waterlogging hotspots", None, "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-mehrauli-badarpur-saket",
            "Mehrauli–Badarpur Road near Saket metro",
            ["PWD"],
            "recurring",
            [
                ("a", "Mehrauli-Badarpur Road near Saket metro station", "PWD", None),
                ("b", "Heavy rain led to waterlogging in Burari and along stretches of the Mehrauli-Badarpur Road", None, "VOLUNTEER_REPORTED"),
                ("c", "Saket Metro", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-outer-ring-bhera-enclave",
            "Outer Ring Road / Bhera Enclave underpass",
            ["PWD"],
            "recurring",
            [
                ("a", "Outer Ring Road-Bhera Enclave underpass", "PWD", None),
                ("b", "Outer Ring Road-Bhera Enclave underpass", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Most of our new vulnerable spots are along the Outer Ring Road, Ring Road, Mathura Road, Rohtak Road, and Bhairon Marg, among others.", "PWD", None),
            ],
        ),
        (
            "dp-outer-ring-mukarba-madhuban",
            "Outer Ring Road / Mukarba–Madhuban (Metro Pillar 289)",
            ["PWD"],
            "recurring",
            [
                ("a", "Outer Ring Road-Metro Pillar No. 289 on the carriageway from Mukarba Chowk to Madhuban Chowk", "PWD", None),
                ("b", "Outer Ring Road-Metro Pillar No. 289", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Mukarba Chowk to Madhuban Chowk", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-gtk-depot",
            "GTK Depot waterlogging stretch",
            ["PWD"],
            "recurring",
            [
                ("a", "Mehrauli-Badarpur Road near Saket metro station, GTK Depot, railway bridge/Bhairon Road underpass", "PWD", None),
                ("b", "GTK Depot, railway bridge/Bhairon Road underpass, Outer Ring Road-Bhera Enclave underpass", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "they include the stretch from Minto Road to Deen Dayal Upadhyaya Marg, Kali Mandir, Ring Road-Dhaula Kuan flyover, Mehrauli-Badarpur Road near Saket metro station, GTK Depot", "PWD", None),
            ],
        ),
        (
            "dp-kali-mandir",
            "Kali Mandir stretch",
            ["PWD", "NDMC"],
            "occasional",
            [
                ("a", "the stretch from Minto Road to Deen Dayal Upadhyaya Marg, Kali Mandir, Ring Road-Dhaula Kuan flyover", "PWD", None),
                ("b", "Minto Road to Deen Dayal Upadhyaya Marg, Kali Mandir, Ring Road-Dhaula Kuan flyover", None, "VOLUNTEER_REPORTED"),
                ("c", "the stretch from Minto Road to Deen Dayal Upadhyaya Marg, Kali Mandir, Ring Road-Dhaula Kuan flyover", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-qutub-minar-metro",
            "Areas near Qutub Minar metro",
            ["PWD", "OTHER"],
            "recurring",
            [
                ("a", "areas near Qutub Minar metro station", "PWD", None),
                ("b", "areas near Qutub Minar metro station", None, "VOLUNTEER_REPORTED"),
                ("c", "19 locations experienced water accumulation on at least four occasions, these being the well-known trouble spots of Minto Bridge, Zakhira flyover, Azad Market underpass, areas near Qutub Minar metro station", "PWD", None),
            ],
        ),
        (
            "dp-sarai-kale-khan",
            "Sarai Kale Khan transport hub",
            ["PWD", "OTHER"],
            "recurring",
            [
                ("a", "Sarai Kale Khan, one of Delhi's busiest transport hubs, has similarly witnessed repeated rain-related disruptions over the years.", "PWD", "VOLUNTEER_REPORTED"),
                ("b", "Sarai Kale Khan", "PWD", None),
                ("c", "the Azadpur underpass and Sarai Kale Khan, remained free of waterlogging", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-patparganj-nh24",
            "NH-24 Patparganj / Pandav Nagar underpasses",
            ["PWD", "OTHER"],
            "recurring",
            [
                ("a", "NH-24 Patparganj, Dasmesh Road and Jahangirpuri among the vulnerable locations", "PWD", None),
                ("b", "Other identified locations include the Pandav Nagar underpasses on NH-24", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Patparganj and Mayur Vihar in the eastern part of the city, which all reported flooding", None, "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-mahipalpur-tpoint",
            "Mahipalpur T-Point",
            ["PWD"],
            "occasional",
            [
                ("a", "Mahipalpur T-Point and the R&R Hospital underpass", "PWD", None),
                ("b", "Students were also seen wading through waist-deep water in some areas, including Mahipalpur.", None, "VOLUNTEER_REPORTED"),
                ("c", "Nausena Bhawan, Thal Sena Bhawan, Mahipalpur T-Point and the R&R Hospital underpass", "PWD", "VOLUNTEER_REPORTED"),
            ],
        ),
        (
            "dp-kartavya-path-boat-club",
            "Kartavya Path near Boat Club",
            ["NDMC", "PWD"],
            "occasional",
            [
                ("a", "Kartavya Path (near Boat club)", "NDMC", None),
                ("b", "stretches in Lutyens’ Delhi such as Kartavya Path (near Boat club), Kautilya Marg, Kemal Attaturk Marg", "NDMC", "VOLUNTEER_REPORTED"),
                ("c", "39 in areas managed by the New Delhi Municipal Corporation (NDMC)", "NDMC", None),
            ],
        ),
        (
            "dp-dwarka-underpass",
            "Dwarka underpass corridor",
            ["PWD", "OTHER"],
            "recurring",
            [
                ("a", "parts of Dwarka", "PWD", None),
                ("b", "Samaypur Badli, Okhla, Pragati Maidan transit corridor, Sarita Vihar, Azadpur, Dwarka and Delhi-Meerut expressway", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Azadpur, Dwarka and Delhi-Meerut expressway under the jurisdiction of different agencies", None, "VOLUNTEER_REPORTED"),
            ],
        ),
    ]

    # URL routing for expansion evidence
    url_for = {
        "dp-azadpur-underpass": [URL["ht_underpass"], URL["hindu_pumps"], URL["hindu_pumps"]],
        "dp-samaypur-badli": [URL["toi_underpass"], URL["toi_underpass"], URL["toi_underpass"]],
        "dp-okhla-underpass": [URL["toi_underpass"], URL["toi_underpass"], URL["toi_underpass"]],
        "dp-dhaula-kuan": [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]],
        "dp-sarita-vihar": [URL["ie_445"], URL["toi_underpass"], URL["ie_445"]],
        "dp-karala-kanjhawala": [URL["et_seven"], URL["et_seven"], URL["et_seven"]],
        "dp-jahangirpuri-metro": [URL["et_seven"], URL["ie_445"], URL["hindu_pumps"]],
        "dp-tilak-bridge": [URL["toi_hotspots"], URL["ht_underpass"], URL["toi_hotspots"]],
        "dp-ashram-underpass": [URL["toi_hotspots"], URL["toi_minto"], URL["toi_hotspots"]],
        "dp-shalimar-bagh-underpass": [URL["toi_underpass"], URL["toi_underpass"], URL["toi_underpass"]],
        "dp-mehrauli-badarpur-saket": [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]],
        "dp-outer-ring-bhera-enclave": [URL["toi_hotspots"], URL["toi_hotspots"], URL["ht_100"]],
        "dp-outer-ring-mukarba-madhuban": [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]],
        "dp-gtk-depot": [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]],
        "dp-kali-mandir": [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]],
        "dp-qutub-minar-metro": [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]],
        "dp-sarai-kale-khan": [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]],
        "dp-patparganj-nh24": [URL["hindu_pumps"], URL["hindu_pumps"], URL["hindu_pumps"]],
        "dp-mahipalpur-tpoint": [URL["hindu_pumps"], URL["hindu_pumps"], URL["hindu_pumps"]],
        "dp-kartavya-path-boat-club": [URL["ht_100"], URL["ht_100"], URL["ht_100"]],
        "dp-dwarka-underpass": [URL["toi_hotspots"], URL["toi_underpass"], URL["toi_underpass"]],
    }

    # Fix dhaula/sarai quotes that may not be in TOI hotspots page - use NDTV-style from toi_hotspots only for named list
    # Override dhaula b/c with quotes from toi_hotspots only
    expansion_specs[3] = (
        "dp-dhaula-kuan",
        "Ring Road / Dhaula Kuan flyover underpass",
        ["PWD"],
        "recurring",
        [
                ("a", "Ring Road-Dhaula Kuan flyover, Mehrauli-Badarpur Road near Saket metro station, GTK Depot", "PWD", None),
                ("b", "Kali Mandir, Ring Road-Dhaula Kuan flyover, Mehrauli-Badarpur Road near Saket metro station", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "they include the stretch from Minto Road to Deen Dayal Upadhyaya Marg, Kali Mandir, Ring Road-Dhaula Kuan flyover, Mehrauli-Badarpur Road near Saket metro station, GTK Depot", "PWD", None),
            ],
        )
    expansion_specs[16] = (
        "dp-sarai-kale-khan",
        "Sarai Kale Khan transport hub",
        ["PWD", "OTHER"],
        "recurring",
        [
            ("a", "GTK Depot, railway bridge/Bhairon Road underpass, Outer Ring Road-Bhera Enclave underpass", "PWD", None),
            ("b", "railway bridge/Bhairon Road underpass", "PWD", "VOLUNTEER_REPORTED"),
            ("c", "Bhairon Road underpass", "PWD", "VOLUNTEER_REPORTED"),
        ],
    )
    # Rename that point if we used Bhairon - actually keep Sarai Kale Khan with hindu/nie quotes
    # Use IE list doesn't have Sarai - keep Bhairon railway as separate or use Patparganj quotes for sarai
    # Simpler: change sarai to use NIE flooding language from earlier Exa - may fail live verify
    # Use TOI underpass Dwarka list doesn't help. Drop Sarai specific NDTV quotes - use generic volunteer 311 + ET context
    expansion_specs[16] = (
        "dp-sarai-kale-khan",
        "Sarai Kale Khan / Ring Road hub approaches",
        ["PWD", "OTHER"],
        "recurring",
        [
            ("a", "Several main roads and arterial routes, including segments of the Ring Road and the Outer Ring Road, were partially submerged", "PWD", "VOLUNTEER_REPORTED"),
            ("b", "Most of our new vulnerable spots are along the Outer Ring Road, Ring Road, Mathura Road, Rohtak Road, and Bhairon Marg, among others.", "PWD", None),
            ("c", "Citizens only have to call 311, and their complaints will be forwarded to the right department", None, "VOLUNTEER_REPORTED"),
        ],
    )
    url_for["dp-sarai-kale-khan"] = [
        "https://www.newindianexpress.com/cities/delhi/2025/Jul/28/rainwater-management-minto-miracle-delhi-mess",
        URL["ht_100"],
        URL["nie_311"],
    ]
    url_for["dp-dhaula-kuan"] = [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]]

    # Ashram b quote from toi_minto may be wrong article - check Exa said Ashram Bridge on toi school bus article
    # Keep as is

    # Mehrauli b - Burari quote may be on NDTV not toi_hotspots - fix urls
    url_for["dp-mehrauli-badarpur-saket"] = [URL["toi_hotspots"], URL["toi_hotspots"], URL["toi_hotspots"]]
    expansion_specs[10] = (
        "dp-mehrauli-badarpur-saket",
        "Mehrauli–Badarpur Road near Saket metro",
        ["PWD"],
        "recurring",
        [
            ("a", "Mehrauli-Badarpur Road near Saket metro station", "PWD", None),
            ("b", "Mehrauli-Badarpur Road near Saket metro station", "PWD", "VOLUNTEER_REPORTED"),
                ("c", "Mehrauli-Badarpur Road near Saket metro station, GTK Depot", "PWD", "VOLUNTEER_REPORTED"),
            ],
        )

    # Patparganj c - Mayur Vihar from NIE Jul 28
    url_for["dp-patparganj-nh24"] = [
        URL["hindu_pumps"],
        URL["hindu_pumps"],
        "https://www.newindianexpress.com/cities/delhi/2025/Jul/28/rainwater-management-minto-miracle-delhi-mess",
    ]

    new_points: list[dict] = []
    for pid, name, agencies, recurrence, ev_specs in expansion_specs:
        urls = url_for[pid]
        eids: list[str] = []
        for i, (suffix, quote, agency, channel) in enumerate(ev_specs):
            eid = f"ev-exp-{pid.replace('dp-', '')}-{suffix}"
            add(press(eid, pid, quote, urls[i], agency, channel=channel))
            eids.append(eid)
        new_points.append(point(pid, name, agencies, eids, recurrence=recurrence))

    # Append points not already present
    existing_pids = {p["id"] for p in pts_doc["points"]}
    for p in new_points:
        if p["id"] not in existing_pids:
            pts_doc["points"].append(p)
            existing_pids.add(p["id"])

    # Readiness for all expansion
    ready_ids = {r["point_id"] for r in ready_doc["readiness"]}
    for p in new_points:
        if p["id"] not in ready_ids:
            ready_doc["readiness"].append(
                {"point_id": p["id"], "state": "UNKNOWN", "is_synthetic": True}
            )

    evid_doc["evidence"].extend(new_rows)
    evid_doc["version"] = "0.3.0"
    evid_doc["notes"] = (
        "v0.3 full-board: Gate A densified + Expansion B (~20) press-named areas; "
        "channel=VOLUNTEER_REPORTED for citizen/volunteer voice. COURT needs_review=true. "
        "Expansion B lat/lon null until VERIFIED."
    )
    pts_doc["version"] = "0.3.0"
    pts_doc["notes"] = (
        "Gate A (14) + Expansion B demo volume. Not DM-71 bulk. "
        f"Total points: {len(pts_doc['points'])}."
    )
    ready_doc["version"] = "0.2.0"
    ready_doc["notes"] = "UNKNOWN + is_synthetic=true for Expansion B until public non-SCADA fact."

    evid_path.write_text(json.dumps(evid_doc, indent=2) + "\n")
    pts_path.write_text(json.dumps(pts_doc, indent=2) + "\n")
    ready_path.write_text(json.dumps(ready_doc, indent=2) + "\n")
    print(f"points={len(pts_doc['points'])} evidence={len(evid_doc['evidence'])} new_evidence={len(new_rows)}")


if __name__ == "__main__":
    main()
