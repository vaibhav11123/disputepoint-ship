#!/usr/bin/env python3
"""One-shot fixture enrichment → v0.3.1. Run from repo root."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POINTS = ROOT / "data/fixtures/points.json"
EVIDENCE = ROOT / "data/fixtures/evidence.json"

# URL → metadata (FACT from Research OS / Exa pass)
URL_META: dict[str, dict[str, str]] = {
    "https://www.livelaw.in/pdf_upload/mmh08042024cw75942018185925-533124.pdf": {
        "source_date": "2024-04-08",
        "title": "Delhi HC order — drainage / Yamuna (W.P.(C) 7594/2018)",
        "publisher": "Delhi High Court (via LiveLaw)",
    },
    "https://www.newslaundry.com/2024/06/29/whos-responsible-for-delhis-rain-mess-answers-from-5-of-the-worst-hit-spots": {
        "source_date": "2024-06-29",
        "title": "Who's responsible for Delhi's rain mess? Five worst-hit spots",
        "publisher": "Newslaundry",
    },
    "https://indianexpress.com/article/cities/delhi/breach-in-barapullah-drain-wall-led-to-south-new-delhi-flooding-9421799/": {
        "source_date": "2024-06-29",
        "title": "Breach in Barapullah drain wall led to South, New Delhi flooding",
        "publisher": "The Indian Express",
    },
    "https://timesofindia.indiatimes.com/city/delhi/delhi-underpasses-flooded-despite-preparedness-claims/articleshow/111497831.cms": {
        "source_date": "2024-07-05",
        "title": "Delhi underpasses flooded despite preparedness claims",
        "publisher": "The Times of India",
    },
    "https://www.hindustantimes.com/cities/delhi-news/infamous-flooded-underpasses-make-a-comeback-in-delhi-man-drowns-in-azadpur-101719598910444.html": {
        "source_date": "2024-06-29",
        "title": "Infamous flooded underpasses make a comeback in Delhi",
        "publisher": "Hindustan Times",
    },
    "https://www.newindianexpress.com/cities/delhi/2025/May/06/single-complaint-number-for-all-waterlogging-grievances-says-parvesh-verma": {
        "source_date": "2025-05-06",
        "title": "Single complaint number for all waterlogging grievances",
        "publisher": "The New Indian Express",
    },
    "https://timesofindia.indiatimes.com/city/delhi/flooding-and-crumbling-roads-at-minto-bridge-underpass-cause-commuter-woes-in-delhi/articleshow/112900606.cms": {
        "source_date": "2024-08-28",
        "title": "Flooding and crumbling roads at Minto Bridge underpass",
        "publisher": "The Times of India",
    },
    "https://economictimes.indiatimes.com/news/india/new-drains-sumps-automated-pump-house-delhi-pwds-plan-to-tackle-waterlogging-at-seven-hotspots/articleshow/121268671.cms": {
        "source_date": "2024-05-01",
        "title": "New drains, sumps, automated pump house — PWD seven hotspots plan",
        "publisher": "The Economic Times",
    },
    "https://home.iitd.ac.in/show.php?id=239&in_sections=Press": {
        "source_date": "2024-01-15",
        "title": "Aab Prahari — citizen science flood reporting (IIT Delhi)",
        "publisher": "IIT Delhi",
    },
    "https://www.livelaw.in/high-court/delhi-high-court/delhi-high-court-management-drainage-system-rejuvenation-yamuna-254753": {
        "source_date": "2024-04-10",
        "title": "Delhi HC issues directions on drainage system management",
        "publisher": "LiveLaw",
    },
    "https://timesofindia.indiatimes.com/city/delhi/assign-upkeep-of-all-drains-to-1-dept-hc/articleshow/109207116.cms": {
        "source_date": "2024-04-11",
        "title": "Assign upkeep of all drains to 1 dept: HC",
        "publisher": "The Times of India",
    },
    "https://indianexpress.com/article/cities/delhi/from-yamuna-tributary-to-monsoon-bane-the-story-of-barapullah-drain-9445811/": {
        "source_date": "2024-07-11",
        "title": "From Yamuna tributary to monsoon bane — Barapullah drain",
        "publisher": "The Indian Express",
    },
    "https://www.hindustantimes.com/cities/delhi-news/ngt-slams-agencies-over-choked-barapullah-drain-101722817653841.html": {
        "source_date": "2024-08-05",
        "title": "NGT slams agencies over choked Barapullah drain",
        "publisher": "Hindustan Times",
    },
    "https://theprint.in/india/waterlogging-in-lutyens-delhi-due-to-malfunctioning-pwd-pumps-ndmc-slams-aap-govt/2152351/": {
        "source_date": "2024-06-28",
        "title": "Waterlogging in Lutyens' Delhi — NDMC on PWD pumps",
        "publisher": "ThePrint (PTI)",
    },
    "https://www.thehindu.com/news/national/delhi-floods-two-boys-drown-in-waterlogged-siraspur-underpass/article68348651.ece": {
        "source_date": "2024-06-29",
        "title": "Siraspur underpass waterlogged after Delhi rains",
        "publisher": "The Hindu",
    },
    "https://timesofindia.indiatimes.com/city/delhi/delhi-traffic-update-okhla-underpass-waterlogged-movement-restricted/articleshow/111376332.cms": {
        "source_date": "2024-06-30",
        "title": "Okhla underpass waterlogged, movement restricted",
        "publisher": "The Times of India",
    },
    "https://timesofindia.indiatimes.com/city/delhi/ndmc-identifies-14-vulnerable-waterlogging-points-in-new-delhi/articleshow/111497773.cms": {
        "source_date": "2024-07-05",
        "title": "NDMC identifies 14 vulnerable waterlogging points",
        "publisher": "The Times of India",
    },
    "https://www.hindustantimes.com/india-news/delhis-minto-bridge-waterlogged-again-bjp-questions-aap-mayors-big-promises-101719546630515.html": {
        "source_date": "2024-06-28",
        "title": "Delhi's Minto Bridge waterlogged again",
        "publisher": "Hindustan Times",
    },
}

# Prefix / substring fallbacks for ET and similar URL variants
URL_PREFIX_META: list[tuple[str, dict[str, str]]] = [
    (
        "economictimes.indiatimes.com",
        {
            "source_date": "2024-05-01",
            "title": "Delhi waterlogging hotspot interventions",
            "publisher": "The Economic Times",
        },
    ),
    (
        "timesofindia.indiatimes.com",
        {
            "source_date": "2024-07-01",
            "title": "Delhi monsoon / waterlogging reporting",
            "publisher": "The Times of India",
        },
    ),
    (
        "hindustantimes.com",
        {
            "source_date": "2024-06-29",
            "title": "Delhi waterlogging reporting",
            "publisher": "Hindustan Times",
        },
    ),
    (
        "indianexpress.com",
        {
            "source_date": "2024-06-29",
            "title": "Delhi drainage / flooding reporting",
            "publisher": "The Indian Express",
        },
    ),
    (
        "newslaundry.com",
        {
            "source_date": "2024-06-29",
            "title": "Delhi rain responsibility reporting",
            "publisher": "Newslaundry",
        },
    ),
    (
        "livelaw.in",
        {
            "source_date": "2024-04-08",
            "title": "Delhi High Court drainage matter",
            "publisher": "LiveLaw",
        },
    ),
    (
        "thehindu.com",
        {
            "source_date": "2024-06-29",
            "title": "Delhi flood / underpass reporting",
            "publisher": "The Hindu",
        },
    ),
    (
        "indiatoday.in",
        {
            "source_date": "2024-06-29",
            "title": "Delhi waterlogging reporting",
            "publisher": "India Today",
        },
    ),
    (
        "theprint.in",
        {
            "source_date": "2024-06-28",
            "title": "Delhi waterlogging / agency statements",
            "publisher": "ThePrint",
        },
    ),
    (
        "iitd.ac.in",
        {
            "source_date": "2024-01-15",
            "title": "IIT Delhi flood / citizen reporting note",
            "publisher": "IIT Delhi",
        },
    ),
    (
        "newindianexpress.com",
        {
            "source_date": "2025-05-06",
            "title": "Delhi waterlogging grievance reporting",
            "publisher": "The New Indian Express",
        },
    ),
]

POINT_ENRICH: dict[str, dict] = {
    "dp-purana-quila": {
        "incident_summary": (
            "Storm-water corridor from India Gate toward the Yamuna along Purana Quila Road. "
            "Delhi High Court (8 Apr 2024) recorded that PWD informed the court the drain is "
            "sectioned across six jurisdictions of four authorities (NDMC, PWD, MCD, Irrigation "
            "& Flood Control). The 2023 monsoon flooded the carriageway and nearby High Court "
            "pool bungalows; exclusive operational ownership is not established."
        ),
        "claim_summaries": {
            "NDMC": "Court record lists NDMC jurisdiction on the India Gate–Priya Nursery–NSCI Club Gate segment.",
            "PWD": "Court record lists PWD on Purana Quila Road (Priya Nursery) to petrol pump and Gate No. 5 to open nallah segments.",
            "MCD": "Court record lists MCD on the petrol pump–ITPO Gate No. 5 stretch and open nallah–Ring Road control gate.",
            "IFC": "Court record lists Irrigation & Flood Control from the Ring Road control gate to the Yamuna outfall.",
        },
    },
    "dp-minto-bridge": {
        "incident_summary": (
            "Minto Road underpass near Connaught Place — a perennial monsoon waterlogging hotspot. "
            "Press reporting (Jun 2024) documents overlapping NDMC/MCD border claims, PWD road "
            "maintenance, and railways under-bridge neglect narratives. The underpass recurred "
            "after periods when agencies treated it as resolved; exclusive responsibility remains disputed."
        ),
        "claim_summaries": {
            "NDMC": "Press quotes NDMC stating outflow drains into MCD drains that were not cleaned.",
            "MCD": "Local representatives describe the bridge as on the NDMC–MCD border with mutual blame.",
            "PWD": "Road ownership and pump-house interventions are repeatedly attributed to PWD in press.",
            "RAILWAYS": "Some PWD officials told press the area under the bridge falls to railways and was neglected.",
        },
    },
    "dp-barapullah": {
        "incident_summary": (
            "Barapullah drain basin — major south/central Delhi storm outfall toward the Yamuna. "
            "Indian Express (29 Jun 2024) reported a wall breach and back-flow after extreme rain, "
            "plus a PWD→MCD→I&FC transfer with ongoing lack of clarity. Later NGT and L-G coverage "
            "continued to flag dredging and choke points across agencies."
        ),
        "claim_summaries": {
            "PWD": "PWD officials said the drain does not come under PWD after transfer, while citing back-flow impacts.",
            "MCD": "MCD officials told press they handed the drain to Irrigation & Flood Control.",
            "IFC": "I&FC officials said the department had not fully taken over; NGT later flagged unfinished stretches.",
        },
    },
    "dp-lodhi-moolchand": {
        "incident_summary": (
            "Lodhi Road / Moolchand Ring Road corridor — low-lying arterial and VIP-quarter approaches. "
            "Newslaundry (29 Jun 2024) documents split maintenance: CPWD for government quarters, "
            "PWD for the main road, MCD for bylanes. Drainage back-flow from Kushak/Barapullah basin "
            "is a recurring context; exclusive agency ownership is not established."
        ),
        "claim_summaries": {
            "PWD": "Main road maintenance under PWD; Moolchand underpass appears on PWD hotspot lists.",
            "CPWD": "Government quarters on Lodhi Road are maintained by CPWD per press attribution.",
            "MCD": "Bylanes maintained by MCD; political representatives also point to MCD drainage responsibility.",
        },
    },
    "dp-okhla-underpass": {
        "incident_summary": (
            "Okhla underpass — southeast Delhi depressed carriageway repeatedly closed in monsoon. "
            "TOI (5 Jul 2024) reports the underpass falls under DDA control and was listed as a "
            "traffic-police hotspot; PWD flood-control narratives cover many underpasses citywide. "
            "Exclusive operational responsibility between DDA and PWD remains disputed in the record."
        ),
        "claim_summaries": {
            "DDA": "TOI attributes Okhla underpass control to DDA; DDA has publicly contested some incident attributions.",
            "PWD": "Citywide underpass SOPs and flood-control orders are PWD-led; Okhla appears in multi-agency underpass lists.",
        },
    },
    "dp-samaypur-badli": {
        "incident_summary": (
            "Samaypur Badli / Siraspur underpass — northwest Delhi Metro-adjacent depressed section. "
            "TOI (5 Jul 2024) records conflicting attributions: the underpass appears in PWD flood-control "
            "lists while senior PWD officials insisted MCD manages Siraspur. Operational ownership stays disputed."
        ),
        "claim_summaries": {
            "PWD": "Underpass listed in PWD flood-control order / hotspot monitoring narratives.",
            "MCD": "PWD officials told TOI that Siraspur underpass jurisdiction is MCD.",
        },
    },
    "dp-bharat-mandapam-tunnel": {
        "incident_summary": (
            "Tunnel connecting to Bharat Mandapam on Purana Quila Road. Delhi HC (Apr 2024) noted "
            "the newly built tunnel, maintained by L&T under PWD supervision, flooded and closed "
            "during the 2023 monsoon. Treated as PWD-supervised asset in the court record."
        ),
    },
    "dp-mathura-rd-hc": {
        "incident_summary": (
            "Mathura Road / High Court pool bungalows. Delhi HC took judicial notice of 2023 monsoon "
            "flooding of the carriageway and bungalows alongside the Purana Quila storm-drain dispute."
        ),
    },
    "dp-aiims-aurobindo": {
        "incident_summary": (
            "AIIMS / Aurobindo Marg corridor — Newslaundry Jun 2024 documents multi-agency drain "
            "hand-offs (NDMC drains outflowing to MCD). Recurring monsoon congestion and waterlogging."
        ),
    },
    "dp-maharani-bagh": {
        "incident_summary": (
            "Maharani Bagh / Taimur Nagar drain and Ring Road wells — press-named chronic waterlogging "
            "stretch with PWD/MCD/DJB claim overlap in fixture evidence."
        ),
    },
    "dp-who-ito-ring": {
        "incident_summary": (
            "Ring Road opposite WHO (ITO) — listed among Delhi’s perennial waterlogging hotspots in "
            "traffic-police / PWD preparedness reporting."
        ),
    },
    "dp-zakhira": {
        "incident_summary": (
            "Zakhira flyover underpass — perennial hotspot; press notes railway-adjacent inflow and "
            "ongoing drain works under PWD coordination narratives."
        ),
    },
    "dp-pul-prahladpur": {
        "incident_summary": (
            "Pul Prahladpur underpass — repeatedly named in ET/TOI seven-hotspot and underpass flood lists; "
            "PWD-monitored depressed section."
        ),
    },
    "dp-azad-market": {
        "incident_summary": (
            "Azad Market underpass — central Delhi depressed section appearing in monsoon underpass "
            "coverage; agency attribution uses OTHER where exclusive owner is unclear in sources."
        ),
    },
    "dp-pragati-bhairon": {
        "incident_summary": (
            "Pragati Maidan / Bhairon corridor tunnel — HT and related press describe monsoon closures "
            "linking India Gate / Purana Quila approaches to Ring Road."
        ),
    },
    "dp-loni-rd": {
        "incident_summary": (
            "Loni Road roundabout — PWD long-term / short-term waterlogging action lists in HC compliance "
            "and monsoon hotspot reporting."
        ),
    },
    "dp-azadpur-underpass": {
        "incident_summary": (
            "Azadpur underpass — HT underpass comeback coverage; PWD/MCD claim edges in northwest corridor."
        ),
    },
    "dp-dhaula-kuan": {
        "incident_summary": (
            "Ring Road / Dhaula Kuan flyover underpass — arterial monsoon congestion and waterlogging "
            "point in traffic advisories."
        ),
    },
    "dp-sarita-vihar": {
        "incident_summary": (
            "Sarita Vihar underpass — named in citywide underpass inundation lists after Jun 2024 extreme rain."
        ),
    },
    "dp-karala-kanjhawala": {
        "incident_summary": (
            "Karala–Kanjhawala Road — PWD long-term remodelling hotspot cited in HC compliance and "
            "traffic-police critical lists."
        ),
    },
    "dp-jahangirpuri-metro": {
        "incident_summary": (
            "Jahangirpuri Metro Station Road — perennial waterlogging hotspot on traffic-police lists."
        ),
    },
    "dp-tilak-bridge": {
        "incident_summary": (
            "Tilak Bridge underpass (ITO) — central Delhi depressed section affecting Indraprastha / "
            "BSZ Marg approaches during heavy rain."
        ),
    },
    "dp-ashram-underpass": {
        "incident_summary": (
            "Ashram underpass — Mathura Road corridor congestion point during monsoon inundation."
        ),
    },
    "dp-shalimar-bagh-underpass": {
        "incident_summary": (
            "Shalimar Bagh underpass — northwest underpass appearing in Jun 2024 inundation reporting; "
            "not always on prior hotspot lists."
        ),
    },
    "dp-mehrauli-badarpur-saket": {
        "incident_summary": (
            "Mehrauli–Badarpur Road near Saket metro — south Delhi arterial stretch in monsoon press lists."
        ),
    },
    "dp-outer-ring-bhera-enclave": {
        "incident_summary": (
            "Outer Ring Road / Bhera Enclave underpass — west Delhi depressed section in underpass coverage."
        ),
    },
    "dp-outer-ring-mukarba-madhuban": {
        "incident_summary": (
            "Outer Ring Road / Mukarba–Madhuban (Metro pillar) — northwest Outer Ring depressed stretch."
        ),
    },
    "dp-gtk-depot": {
        "incident_summary": (
            "GTK Depot waterlogging stretch — north Delhi corridor named in monsoon operational lists."
        ),
    },
    "dp-kali-mandir": {
        "incident_summary": (
            "Kali Mandir stretch — central/NDMC-adjacent corridor with PWD/NDMC claim edges in fixtures."
        ),
    },
    "dp-qutub-minar-metro": {
        "incident_summary": (
            "Areas near Qutub Minar metro — south Delhi monsoon waterlogging corridor in press densify."
        ),
    },
    "dp-sarai-kale-khan": {
        "incident_summary": (
            "Sarai Kale Khan / Ring Road hub approaches — Barapullah basin outfall context; multi-agency edges."
        ),
    },
    "dp-patparganj-nh24": {
        "incident_summary": (
            "NH-24 Patparganj / Pandav Nagar underpasses — east Delhi depressed sections in monsoon lists."
        ),
    },
    "dp-mahipalpur-tpoint": {
        "incident_summary": (
            "Mahipalpur T-Point — airport-approach arterial waterlogging point in PWD hotspot narratives."
        ),
    },
    "dp-kartavya-path-boat-club": {
        "incident_summary": (
            "Kartavya Path near Boat Club — NDMC/PWD edge in Lutyens zone monsoon vulnerability lists."
        ),
    },
    "dp-dwarka-underpass": {
        "incident_summary": (
            "Dwarka underpass corridor — southwest Delhi depressed section named in citywide underpass inundation lists."
        ),
    },
}


def meta_for_url(url: str) -> dict[str, str]:
    if url in URL_META:
        return dict(URL_META[url])
    for needle, meta in URL_PREFIX_META:
        if needle in url:
            return dict(meta)
    return {}


def establishes_for(row: dict) -> tuple[str, str]:
    typ = row["type"]
    agency = row.get("agency")
    loc = row.get("location_span") or "this location"
    if typ == "COURT_ORDER":
        return (
            f"Court text tying drainage/flooding facts to {loc}"
            + (f" and naming {agency}" if agency else "")
            + ".",
            "Does not by itself assign exclusive field response to one agency for this incident.",
        )
    if row.get("is_synthetic") and row.get("channel") == "VOLUNTEER_REPORTED":
        return (
            "Illustrative volunteer observation useful for queue density and operator practice.",
            "Not a verified submission from a named real person; not an official agency statement.",
        )
    if agency:
        return (
            f"Public reporting associating {agency} with conditions or claims at {loc}.",
            "Does not prove exclusive operational ownership or settle competing claims alone.",
        )
    return (
        f"Public reporting describing waterlogging or drainage conditions at {loc}.",
        "Does not identify a single responsible agency by itself.",
    )


def new_volunteer(point_id: str, suffix: str, quote: str, when: str) -> dict:
    return {
        "id": f"ev-illust-{point_id}-{suffix}",
        "type": "PRESS_REPORT",
        "url": f"https://disputepoint.local/illustrative/volunteer/{point_id}/{suffix}",
        "quote": quote,
        "agency": None,
        "location_span": point_id,
        "source_date": when,
        "retrieved_at": "2026-10-09T12:00:00Z",
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": True,
        "channel": "VOLUNTEER_REPORTED",
        "title": "Illustrative volunteer report",
        "publisher": "DisputePoint sample (not a real submission)",
        "establishes": "Illustrative volunteer observation for demo density at this location.",
        "does_not_establish": "Not a verified submission from a named real person; not an official record.",
    }


# New sourced rows — quotes taken from Research OS / Exa highlights of public pages.
SOURCED_GAP: list[dict] = [
    {
        "id": "ev-enrich-purana-toi-hc",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/assign-upkeep-of-all-drains-to-1-dept-hc/articleshow/109207116.cms",
        "quote": "The court took note of the flooding of Purana Quila Road, Mathura Road, and the newly built tunnel near Bharat Mandapam during the monsoon of 2023",
        "agency": None,
        "location_span": "dp-purana-quila",
        "source_date": "2024-04-11",
        "retrieved_at": "2026-10-09T12:00:00Z",
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": False,
        "channel": "OFFICIAL",
        "title": "Assign upkeep of all drains to 1 dept: HC",
        "publisher": "The Times of India",
        "establishes": "Press summary of HC notice of 2023 Purana Quila / Mathura / tunnel flooding.",
        "does_not_establish": "Does not assign exclusive field response for the current incident.",
    },
    {
        "id": "ev-enrich-barapullah-ngt",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/cities/delhi-news/ngt-slams-agencies-over-choked-barapullah-drain-101722817653841.html",
        "quote": "None of the authorities is in the position to state as to who or which authority is responsible for desilting of the stretch from A-7 to B",
        "agency": None,
        "location_span": "dp-barapullah",
        "source_date": "2024-08-05",
        "retrieved_at": "2026-10-09T12:00:00Z",
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": False,
        "title": "NGT slams agencies over choked Barapullah drain",
        "publisher": "Hindustan Times",
        "establishes": "Public reporting that agencies could not state who desilts a critical Barapullah stretch.",
        "does_not_establish": "Does not invent an exclusive owner; supports CONFLICT framing.",
    },
    {
        "id": "ev-enrich-minto-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/india-news/delhis-minto-bridge-waterlogged-again-bjp-questions-aap-mayors-big-promises-101719546630515.html",
        "quote": "The waterlogging under Minto bridge occurred just a year after the Public Works Department (PWD) dropped the road from its list of waterlogging hot spots in the Capital",
        "agency": None,
        "location_span": "dp-minto-bridge",
        "source_date": "2024-06-28",
        "retrieved_at": "2026-10-09T12:00:00Z",
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": False,
        "title": "Delhi's Minto Bridge waterlogged again",
        "publisher": "Hindustan Times",
        "establishes": "PWD hotspot-list history and recurrence at Minto Bridge.",
        "does_not_establish": "Does not clear NDMC/MCD/Railways competing claims.",
    },
    {
        "id": "ev-enrich-okhla-toi-dda",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/delhi-underpasses-flooded-despite-preparedness-claims/articleshow/111497831.cms",
        "quote": "The Okhla underpass, which falls under the control of DDA and was also highlighted as a hotspot by traffic police",
        "agency": None,
        "location_span": "dp-okhla-underpass",
        "source_date": "2024-07-05",
        "retrieved_at": "2026-10-09T12:00:00Z",
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": False,
        "title": "Delhi underpasses flooded despite preparedness claims",
        "publisher": "The Times of India",
        "establishes": "Press attribution of Okhla underpass control to DDA.",
        "does_not_establish": "Does not settle PWD citywide underpass SOP claims.",
    },
    {
        "id": "ev-enrich-samaypur-mcd",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/delhi-underpasses-flooded-despite-preparedness-claims/articleshow/111497831.cms",
        "quote": "The unfortunate death of two people occurred at the Siraspur underpass in Samaypur Badli, which is under the jurisdiction of MCD",
        "agency": None,
        "location_span": "dp-samaypur-badli",
        "source_date": "2024-07-05",
        "retrieved_at": "2026-10-09T12:00:00Z",
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": False,
        "title": "Delhi underpasses flooded despite preparedness claims",
        "publisher": "The Times of India",
        "establishes": "PWD official attribution of Siraspur underpass jurisdiction to MCD.",
        "does_not_establish": "Does not clear PWD flood-control listing of the same underpass.",
    },
    {
        "id": "ev-enrich-lodhi-ndmc-pwd",
        "type": "PRESS_REPORT",
        "url": "https://theprint.in/india/waterlogging-in-lutyens-delhi-due-to-malfunctioning-pwd-pumps-ndmc-slams-aap-govt/2152351/",
        "quote": "in Lodhi Colony and Golf Links, the Kushak Nala pumps, also managed by the PWD, malfunctioned, leading to significant water accumulation",
        "agency": None,
        "location_span": "dp-lodhi-moolchand",
        "source_date": "2024-06-28",
        "retrieved_at": "2026-10-09T12:00:00Z",
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": False,
        "title": "Waterlogging in Lutyens' Delhi — NDMC on PWD pumps",
        "publisher": "ThePrint (PTI)",
        "establishes": "NDMC-attributed claim that PWD Kushak pumps affected Lodhi Colony flooding.",
        "does_not_establish": "Does not remove CPWD/MCD claim sides on Lodhi Road assets.",
    },
]

ILLUSTRATIVE: list[dict] = [
    new_volunteer(
        "dp-minto-bridge",
        "wl1",
        "Volunteer report: knee-deep standing water under Minto Bridge; buses slowing; road difficult to cross on foot.",
        "2024-06-28",
    ),
    new_volunteer(
        "dp-minto-bridge",
        "photo1",
        "Volunteer report: photograph submitted for review showing water at the Minto Road underpass carriageway edge.",
        "2024-06-28",
    ),
    new_volunteer(
        "dp-okhla-underpass",
        "wl1",
        "Volunteer report: Okhla underpass approach ponded after rain; traffic diverted; pedestrians avoiding the depressed section.",
        "2024-06-29",
    ),
    new_volunteer(
        "dp-okhla-underpass",
        "review1",
        "Volunteer report reviewed and linked to the Okhla underpass incident record for operator follow-up.",
        "2024-06-30",
    ),
    new_volunteer(
        "dp-samaypur-badli",
        "wl1",
        "Volunteer report: water pooled near Siraspur / Samaypur Badli underpass metro approach; crossing difficult.",
        "2024-06-29",
    ),
    new_volunteer(
        "dp-barapullah",
        "wl1",
        "Volunteer report: standing water and debris smell near Barapullah drain bank after overnight rain; path hard to use.",
        "2024-06-29",
    ),
    new_volunteer(
        "dp-lodhi-moolchand",
        "wl1",
        "Volunteer report: Lodhi Road service lane difficult to cross; shallow flooding near Moolchand Ring Road slip.",
        "2024-06-28",
    ),
    new_volunteer(
        "dp-purana-quila",
        "wl1",
        "Volunteer report: Purana Quila Road carriageway wet and slow-moving after rain; drain mouths submerged at kerb.",
        "2024-06-28",
    ),
    new_volunteer(
        "dp-pul-prahladpur",
        "wl1",
        "Volunteer report: Pul Prahladpur underpass holding water; two-wheelers turning back at the ramp.",
        "2024-06-28",
    ),
    new_volunteer(
        "dp-zakhira",
        "wl1",
        "Volunteer report: Zakhira underpass flooded at mid-span; photo marked for review against the open incident.",
        "2024-06-28",
    ),
    new_volunteer(
        "dp-dhaula-kuan",
        "wl1",
        "Volunteer report: Dhaula Kuan flyover underpass slow with standing water; multiple volunteers noted same stretch.",
        "2024-06-28",
    ),
    new_volunteer(
        "dp-who-ito-ring",
        "wl1",
        "Volunteer report: Ring Road opposite WHO holding water at kerb line; buses queuing through the ponded lane.",
        "2024-06-28",
    ),
]


def main() -> None:
    points_doc = json.loads(POINTS.read_text())
    evidence_doc = json.loads(EVIDENCE.read_text())

    points_doc["version"] = "0.3.1"
    points_doc["notes"] = (
        "v0.3.1 enrichment: incident_summary + claim_summaries; Research OS sourced metadata. "
        "Gate A + Expansion B. Not DM-71 bulk. Total points: 35."
    )
    evidence_doc["version"] = "0.3.1"
    evidence_doc["notes"] = (
        "v0.3.1 enrichment: source_date/title/publisher/establishes; illustrative volunteer rows "
        "use channel=VOLUNTEER_REPORTED and is_synthetic=true. COURT needs_review=true."
    )

    by_id = {row["id"]: row for row in evidence_doc["evidence"]}

    for row in evidence_doc["evidence"]:
        meta = meta_for_url(row["url"])
        if meta.get("source_date") and not row.get("source_date"):
            row["source_date"] = meta["source_date"]
        if meta.get("title"):
            row["title"] = meta["title"]
        if meta.get("publisher"):
            row["publisher"] = meta["publisher"]
        # Existing VOLUNTEER_REPORTED on real press URLs stay is_synthetic=false (sourced densify).
        # Only newly invented illustrative rows are synthetic.
        if row["type"] == "COURT_ORDER":
            row["needs_review"] = True
        est, does_not = establishes_for(row)
        row.setdefault("establishes", est)
        row.setdefault("does_not_establish", does_not)
        if not row.get("title"):
            row["title"] = f"{row['type'].replace('_', ' ').title()} — {row.get('location_span') or 'Delhi'}"
        if not row.get("publisher"):
            row["publisher"] = "Public source (see URL)"

    for row in SOURCED_GAP + ILLUSTRATIVE:
        if row["id"] not in by_id:
            evidence_doc["evidence"].append(row)
            by_id[row["id"]] = row

    for pt in points_doc["points"]:
        enrich = POINT_ENRICH.get(pt["id"], {})
        if "incident_summary" in enrich:
            pt["incident_summary"] = enrich["incident_summary"]
        if "claim_summaries" in enrich:
            pt["claim_summaries"] = enrich["claim_summaries"]
        for row in SOURCED_GAP + ILLUSTRATIVE:
            if row["location_span"] == pt["id"] and row["id"] not in pt.get("evidence_ids", []):
                pt.setdefault("evidence_ids", []).append(row["id"])

    POINTS.write_text(json.dumps(points_doc, indent=2, ensure_ascii=False) + "\n")
    EVIDENCE.write_text(json.dumps(evidence_doc, indent=2, ensure_ascii=False) + "\n")
    print(f"points={len(points_doc['points'])} evidence={len(evidence_doc['evidence'])}")
    dated = sum(1 for r in evidence_doc["evidence"] if r.get("source_date"))
    synth = sum(1 for r in evidence_doc["evidence"] if r.get("is_synthetic"))
    print(f"source_date_set={dated} synthetic={synth}")


if __name__ == "__main__":
    main()
