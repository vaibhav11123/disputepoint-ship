#!/usr/bin/env python3
"""Full-board deep enrichment → v0.3.2. Run from repo root. Idempotent on evidence ids."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POINTS = ROOT / "data/fixtures/points.json"
EVIDENCE = ROOT / "data/fixtures/evidence.json"

# Deep research-backed summaries + claims for all 35 (FACT paraphrase from Exa / L1).
POINT_DEEP: dict[str, dict] = {
    "dp-purana-quila": {
        "incident_summary": (
            "India Gate→Yamuna storm-water corridor along Purana Quila Road. Delhi HC (8 Apr 2024) "
            "recorded PWD’s six-segment jurisdiction map across NDMC, PWD, MCD and Irrigation & Flood "
            "Control after 2023 monsoon flooding of the carriageway and High Court pool bungalows. "
            "Exclusive operational ownership remains unresolved."
        ),
        "claim_summaries": {
            "NDMC": "HC record: India Gate–Priya Nursery–NSCI Club Gate segment under NDMC.",
            "PWD": "HC record: Purana Quila Road (Priya Nursery) to petrol pump and Gate No. 5–open nallah under PWD.",
            "MCD": "HC record: petrol pump–ITPO Gate No. 5 and open nallah–Ring Road control gate under MCD.",
            "IFC": "HC record: Ring Road control gate to Yamuna outfall under Irrigation & Flood Control.",
        },
    },
    "dp-minto-bridge": {
        "incident_summary": (
            "Minto Road underpass near Connaught Place — perennial monsoon hotspot. Jun 2024 press "
            "documents NDMC/MCD border blame, PWD road/pump interventions, and railways under-bridge "
            "neglect narratives after the underpass flooded again following hotspot delisting periods."
        ),
        "claim_summaries": {
            "NDMC": "Press: NDMC says outflow drains into MCD drains that were not cleaned.",
            "MCD": "MLA/press: bridge sits on NDMC–MCD border; agencies blame each other.",
            "PWD": "Press: road ownership and pump-house capacity upgrades attributed to PWD.",
            "RAILWAYS": "Press: some PWD officials said the area under the bridge falls to railways.",
        },
    },
    "dp-barapullah": {
        "incident_summary": (
            "Barapullah basin — major south/central outfall to the Yamuna. IE (29 Jun 2024) reported "
            "wall breach and back-flow after extreme rain plus a PWD→MCD→I&FC transfer with lack of "
            "clarity. Later NGT/L-G coverage continued to flag unfinished dredging stretches."
        ),
        "claim_summaries": {
            "PWD": "PWD officials: drain not under PWD after transfer; cite back-flow impacts citywide.",
            "MCD": "MCD officials: handed the drain to Irrigation & Flood Control.",
            "IFC": "I&FC: takeover incomplete; NGT later flagged stretches with no stated desilt owner.",
        },
    },
    "dp-lodhi-moolchand": {
        "incident_summary": (
            "Lodhi Road / Moolchand Ring Road — low-lying arterial and VIP-quarter approaches. "
            "Newslaundry (29 Jun 2024): CPWD quarters, PWD main road, MCD bylanes. Kushak/Barapullah "
            "back-flow context recurs in NDMC/PWD pump disputes."
        ),
        "claim_summaries": {
            "PWD": "Main road and Moolchand underpass hotspot monitoring attributed to PWD.",
            "CPWD": "Government quarters on Lodhi Road maintained by CPWD per press.",
            "MCD": "Bylanes under MCD; representatives also point to city drainage responsibility.",
        },
    },
    "dp-okhla-underpass": {
        "incident_summary": (
            "Okhla underpass — southeast depressed carriageway repeatedly closed in monsoon. TOI "
            "(5 Jul 2024) attributes control to DDA and notes traffic-police hotspot listing; PWD "
            "citywide underpass SOPs cover many facilities. Exclusive ownership remains disputed."
        ),
        "claim_summaries": {
            "DDA": "TOI: Okhla underpass falls under DDA control; DDA has contested some attributions.",
            "PWD": "PWD flood-control / underpass SOP narratives cover citywide depressed sections.",
        },
    },
    "dp-samaypur-badli": {
        "incident_summary": (
            "Samaypur Badli / Siraspur underpass — northwest Metro-adjacent depressed section. TOI "
            "(5 Jul 2024): listed in PWD flood-control order while senior PWD officials insisted MCD "
            "manages Siraspur. Operational ownership stays disputed."
        ),
        "claim_summaries": {
            "PWD": "Underpass appears on PWD flood-control / hotspot monitoring lists.",
            "MCD": "PWD officials told TOI Siraspur underpass jurisdiction is MCD.",
        },
    },
    "dp-bharat-mandapam-tunnel": {
        "incident_summary": (
            "Bharat Mandapam / Purana Quila tunnel — HC (Apr 2024) noted 2023 monsoon closure of the "
            "newly built tunnel maintained by L&T under PWD supervision. TOI (Jul 2024) links repeated "
            "flooding to ITPO underground parking seepage and incomplete Bharat Mandapam drainage."
        ),
        "claim_summaries": {
            "PWD": "Court and press attribute tunnel maintenance supervision and corridor drainage works to PWD.",
        },
    },
    "dp-mathura-rd-hc": {
        "incident_summary": (
            "Mathura Road / High Court pool bungalows — HC took judicial notice of 2023 carriageway "
            "and bungalow flooding alongside the Purana Quila drain dispute. TOI notes VIP Mathura Road "
            "as low-lying with ongoing stormwater redesign tied to the Pragati corridor."
        ),
        "claim_summaries": {
            "PWD": "PWD informed the court and leads Mathura Road desilt/redesign narratives in press.",
        },
    },
    "dp-aiims-aurobindo": {
        "incident_summary": (
            "AIIMS / Aurobindo Marg — Newslaundry (29 Jun 2024): nearly five-feet inundation; PWD "
            "maintains Aurobindo Marg to Gautam Nagar turn while drains near AAI/Rajiv Bhavan fall "
            "under NDMC, which blamed blocked MCD downstream drains. NDMC later listed AIIMS underbridges "
            "among vulnerable CCTV-monitored points."
        ),
        "claim_summaries": {
            "PWD": "Road maintenance on Aurobindo Marg to Gautam Nagar turn attributed to PWD.",
            "NDMC": "Drains near AAI office under NDMC; NDMC lists AIIMS underbridges as vulnerable.",
            "MCD": "NDMC stated waterlogging followed from uncleared MCD drains receiving NDMC outflow.",
        },
    },
    "dp-maharani-bagh": {
        "incident_summary": (
            "Maharani Bagh / Taimur Nagar drain / Ring Road wells — HT (28 Jun 2024) documented "
            "sewage-mixed flooding of homes after Taimoor Nagar drain outfall clogging; RWA had warned "
            "for months. Fixture evidence also ties PWD/MCD/DJB claim edges on wells and drains."
        ),
        "claim_summaries": {
            "PWD": "Arterial / Ring Road well and drain interventions appear in PWD complaint clusters.",
            "MCD": "MCD desilting claims and colony drain maintenance disputed by residents/RWA.",
            "DJB": "Sewer overflow mixing with stormwater raises DJB network questions in press coverage.",
        },
    },
    "dp-who-ito-ring": {
        "incident_summary": (
            "Ring Road opposite WHO (ITO) — perennial hotspot. IE (29 Jun 2024): a drain connecting "
            "Central Delhi, ITO and the WHO building overflowed for hours, delaying clearance at ITO "
            "and Minto. TOI (Aug 2024) again named ITO among usual suspects with insufficient pumps."
        ),
        "claim_summaries": {
            "PWD": "PWD control-room and hotspot lists treat the WHO/ITO Ring Road stretch as a critical PWD location.",
        },
    },
    "dp-zakhira": {
        "incident_summary": (
            "Zakhira flyover underpass — chronic monsoon hotspot. TOI (Aug 2024): railway-adjacent "
            "waste/inflow clogs pumps; PWD minister wrote to Railways that a shared-cost culvert on "
            "railway land remains unbuilt after PWD deposited its share (Jul 2023)."
        ),
        "claim_summaries": {
            "PWD": "Road-owning agency for the underpass; installed screens and pursues railway culvert works.",
        },
    },
    "dp-pul-prahladpur": {
        "incident_summary": (
            "Pul Prahladpur underpass — critical PWD hotspot. TOI (Aug 2024): despite a 2022 underground "
            "sump (7.5 lakh litres) and 600 HP permanent pump house, the underpass still flooded when "
            "pumps were overwhelmed; named again in citywide underpass inundation lists."
        ),
        "claim_summaries": {
            "PWD": "PWD constructed sump/pump house and lists the underpass among critical monsoon points.",
        },
    },
    "dp-azad-market": {
        "incident_summary": (
            "Azad Market underpass — central Delhi depressed section. HT (Jun 2024): severe inundation "
            "with passengers trapped in a submerged bus; traffic alerts closed or diverted the stretch. "
            "Exclusive agency owner is unclear in sources (fixture uses OTHER)."
        ),
        "claim_summaries": {
            "OTHER": "Press documents severe underpass inundation without a clean exclusive agency assignment.",
        },
    },
    "dp-pragati-bhairon": {
        "incident_summary": (
            "Pragati Maidan / Bhairon corridor tunnel — repeatedly closed in monsoon. TOI (Jul 2024): "
            "PWD building a supplementary drain on Purana Quila Road; cites rainwater from Bhairon Marg "
            "VIP low-lying stretch and incomplete Bharat Mandapam/ITPO parking drainage entering the tunnel."
        ),
        "claim_summaries": {
            "PWD": "PWD manages the transit corridor and is constructing supplementary drainage works.",
        },
    },
    "dp-loni-rd": {
        "incident_summary": (
            "Loni Road roundabout — converging point from Loni Road and Wazirabad/Signature Bridge "
            "approaches. TOI (Aug 2024): PWD plans drain remodel, pump house and sump well as a "
            "long-term waterlogging intervention at this hotspot."
        ),
        "claim_summaries": {
            "PWD": "PWD road-owning agency with published remodel / pump-house plans for the roundabout.",
        },
    },
    "dp-azadpur-underpass": {
        "incident_summary": (
            "Azadpur underpass — northwest depressed section among worst-hit in Jun 2024. HT: PWD "
            "deployed multiple pumps while sewer backflow raised water levels; underpass closed after "
            "vehicles broke down. Multi-agency edges (PWD/MCD) appear in fixture claims."
        ),
        "claim_summaries": {
            "PWD": "PWD pump houses and clearance operations cited in press for Azadpur underpass.",
            "MCD": "Local drain/colony interfaces and MCD complaint channels appear in wider monsoon coverage.",
        },
    },
    "dp-dhaula-kuan": {
        "incident_summary": (
            "Ring Road / Dhaula Kuan flyover underpass — critical airport-approach arterial. NDTV "
            "(Aug 2024): PWD minister directed drainage upgrade for 100 mm/hr and more mobile pumps "
            "after bowl-shaped ponding; IE listed Dhaula Kuan among concentrated PWD complaint clusters."
        ),
        "claim_summaries": {
            "PWD": "PWD engineers cite bowl geometry; minister ordered drainage and pumping upgrades.",
        },
    },
    "dp-sarita-vihar": {
        "incident_summary": (
            "Sarita Vihar underpass — southeast depressed section named in TOI’s Jun/Jul 2024 citywide "
            "underpass inundation list; HT (Aug 2024) again reported Sarita Vihar waterlogging with "
            "traffic advisories affecting Nehru Place–Jasola approaches."
        ),
        "claim_summaries": {
            "PWD": "Appears on PWD-linked underpass inundation and traffic-advisory lists.",
        },
    },
    "dp-karala-kanjhawala": {
        "incident_summary": (
            "Karala–Kanjhawala Road — west Delhi industrial-approach stretch. TOI (Aug 2024): PWD "
            "found existing drainage inadequate; consultancy engaged 2023 with remodel works targeted "
            "after report submission — a documented long-term hotspot intervention."
        ),
        "claim_summaries": {
            "PWD": "PWD is the road-owning agency leading the drainage remodel consultancy and works.",
        },
    },
    "dp-jahangirpuri-metro": {
        "incident_summary": (
            "Jahangirpuri Metro Station Road — listed among Delhi’s perennial waterlogging hotspots "
            "in traffic-police / PWD preparedness reporting alongside other chronic underpass and "
            "metro-approach points."
        ),
        "claim_summaries": {
            "PWD": "Treated as a PWD-monitored perennial hotspot in city hotspot compilations.",
        },
    },
    "dp-tilak-bridge": {
        "incident_summary": (
            "Tilak Bridge underpass (ITO) — HT (Jun 2024): closed after a drain wall collapsed and "
            "water filled the underpass, snarling Indraprastha Marg / BSZ Marg / Vikas Marg. TOI "
            "(Aug 2024) again paired Tilak Bridge with ITO among usual suspects."
        ),
        "claim_summaries": {
            "PWD": "PWD officials described drain-wall collapse and multi-pump clearance at the underpass.",
        },
    },
    "dp-ashram-underpass": {
        "incident_summary": (
            "Ashram underpass / Ashram Bridge approaches — The Hindu (20 Aug 2024) reported severe "
            "waterlogging near Ashram Bridge after heavy showers, with Mathura Road corridor congestion "
            "typical of monsoon inundation at this southeast arterial node."
        ),
        "claim_summaries": {
            "PWD": "Arterial underpass/bridge approaches fall under PWD monsoon response narratives.",
        },
    },
    "dp-shalimar-bagh-underpass": {
        "incident_summary": (
            "Shalimar Bagh underpass — northwest depressed section inundated in Jun 2024 extreme rain. "
            "TOI notes it was not on the prior hotspot list yet still flooded; fixture retains PWD/OTHER "
            "edges where exclusive ownership is unclear."
        ),
        "claim_summaries": {
            "PWD": "Citywide underpass SOPs and inundation lists include Shalimar Bagh in PWD reporting.",
            "OTHER": "Not previously listed as a hotspot; exclusive owner unclear in some press accounts.",
        },
    },
    "dp-mehrauli-badarpur-saket": {
        "incident_summary": (
            "Mehrauli–Badarpur Road near Saket metro — TOI (26 Jul 2024) drone visuals of severe "
            "waterlogging at Saket Metro; HT (29 Aug 2024) traffic advisories on MB Road from Khanpur "
            "toward shooting-range T-point after overnight rain."
        ),
        "claim_summaries": {
            "PWD": "MB Road / Saket arterial waterlogging appears in PWD and traffic-police advisories.",
        },
    },
    "dp-outer-ring-bhera-enclave": {
        "incident_summary": (
            "Outer Ring Road / Bhera Enclave underpass — HT (29 Aug 2024) traffic advisory to avoid "
            "Outer Ring Road from Bhera roundabout toward Peeragarhi after waterlogging; west Delhi "
            "depressed Outer Ring section in monsoon coverage."
        ),
        "claim_summaries": {
            "PWD": "Outer Ring depressed sections are PWD road assets in monsoon advisory coverage.",
        },
    },
    "dp-outer-ring-mukarba-madhuban": {
        "incident_summary": (
            "Outer Ring / Mukarba–Madhuban (Metro pillar) — HT (29 Aug 2024): waterlogging reported "
            "at Mukarba Chowk and GT Karnal Road (Mukarba toward Azadpur) with diversion advisories; "
            "northwest Outer Ring metro-pillar approaches recur in monsoon snarls."
        ),
        "claim_summaries": {
            "PWD": "GT Karnal / Outer Ring approaches treated as PWD arterial assets in advisories.",
        },
    },
    "dp-gtk-depot": {
        "incident_summary": (
            "GTK Depot waterlogging stretch — north Delhi GT Karnal corridor context. HT (29 Aug 2024) "
            "advisories covered GT Karnal from Mukarba toward Azadpur Chowk; depot approaches sit in "
            "the same monsoon congestion band."
        ),
        "claim_summaries": {
            "PWD": "GT Karnal corridor waterlogging responses attributed to PWD / traffic coordination.",
        },
    },
    "dp-kali-mandir": {
        "incident_summary": (
            "Kali Mandir stretch — central Delhi corridor with PWD/NDMC claim edges. NDMC’s 2024 "
            "vulnerable-point CCTV expansion covers multiple Lutyens/central underbridges and "
            "intersections in the same operational zone."
        ),
        "claim_summaries": {
            "PWD": "Arterial segments in the corridor appear under PWD maintenance narratives.",
            "NDMC": "NDMC vulnerable-point monitoring covers adjacent central New Delhi locations.",
        },
    },
    "dp-qutub-minar-metro": {
        "incident_summary": (
            "Areas near Qutub Minar metro — HT (29 Aug 2024) listed Qutub Minar Metro Station among "
            "locations with waterlogging and traffic snarls after heavy rain, alongside Saket and "
            "Mehrauli–Badarpur approaches."
        ),
        "claim_summaries": {
            "PWD": "Metro-approach arterial flooding appears in PWD/traffic monsoon advisories.",
            "OTHER": "Metro station interface may involve additional asset owners beyond PWD roads.",
        },
    },
    "dp-sarai-kale-khan": {
        "incident_summary": (
            "Sarai Kale Khan / Ring Road hub — Newslaundry (29 Jun 2024) named Sarai Kale Khan among "
            "excessively waterlogged sites; Barapullah basin outfall and ISBT/hub approaches amplify "
            "recurrence. Multi-agency edges retained as PWD/OTHER in fixtures."
        ),
        "claim_summaries": {
            "PWD": "Ring Road / hub approaches appear in PWD complaint and flooding narratives.",
            "OTHER": "Transport hub interfaces involve multiple asset owners beyond a single drain agency.",
        },
    },
    "dp-patparganj-nh24": {
        "incident_summary": (
            "NH-24 Patparganj / Pandav Nagar underpasses — east Delhi depressed sections. NIE "
            "(28 Jun 2024) recorded MCD activity including Patparganj fallen-tree calls during the "
            "same extreme-rain window; underpass inundation fits citywide east-corridor monsoon pattern."
        ),
        "claim_summaries": {
            "PWD": "NH/arterial underpass assets typically sit with PWD in city flood-control framing.",
            "OTHER": "Local MCD interfaces and NH agency edges keep exclusive ownership unclear.",
        },
    },
    "dp-mahipalpur-tpoint": {
        "incident_summary": (
            "Mahipalpur T-Point — airport-approach arterial. NIE (28 Jun 2024) noted heavy traffic on "
            "the Mahipalpur–Gurgaon route; HT (29 Aug 2024) listed Mahipalpur among waterlogged "
            "locations after overnight rain."
        ),
        "claim_summaries": {
            "PWD": "Airport-route arterial waterlogging responses attributed to PWD in monsoon coverage.",
        },
    },
    "dp-kartavya-path-boat-club": {
        "incident_summary": (
            "Kartavya Path near Boat Club — Lutyens / ceremonial axis with NDMC–PWD edges. NDMC "
            "(TOI 5 Jul 2024) expanded vulnerable-point CCTV monitoring across central New Delhi "
            "including Raisina/Mandir Marg class locations in the same operational band."
        ),
        "claim_summaries": {
            "NDMC": "NDMC manages large parts of Lutyens stormwater and lists central vulnerable points.",
            "PWD": "Some arterial / pump interfaces in the wider central zone remain PWD-managed.",
        },
    },
    "dp-dwarka-underpass": {
        "incident_summary": (
            "Dwarka underpass corridor — southwest depressed sections. TOI (5 Jul 2024) named Dwarka "
            "among underpasses inundated despite preparedness claims; Patriot and traffic coverage "
            "also flagged Dwarka-area waterlogging in the Jun 2024 extreme-rain window."
        ),
        "claim_summaries": {
            "PWD": "Underpass inundation lists place Dwarka among PWD flood-control action-plan facilities.",
            "OTHER": "DDA/local interfaces in Dwarka sectors can blur exclusive underpass ownership.",
        },
    },
}

# Sourced gap-fill (agency null to protect ownership). Quotes from Exa highlights.
SOURCED: list[dict] = [
    {
        "id": "ev-v032-zakhira-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/delhi-waterlogging-woes-from-zakhira-to-pul-prahladpur/articleshow/112207005.cms",
        "quote": "During monsoon, waste from temporary drains built by railways blocks this underpass, due to which the water pumps get clogged",
        "agency": None,
        "location_span": "dp-zakhira",
        "source_date": "2024-08-02",
        "title": "Delhi waterlogging woes: From Zakhira to Pul Prahladpur",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-pul-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/delhi-waterlogging-woes-from-zakhira-to-pul-prahladpur/articleshow/112207005.cms",
        "quote": "In 2022, PWD, to avoid a repeat of waterlogging, constructed an underground sump of 7.5 lakh litres capacity and a permanent pump house of 600 horsepower",
        "agency": None,
        "location_span": "dp-pul-prahladpur",
        "source_date": "2024-08-02",
        "title": "Delhi waterlogging woes: From Zakhira to Pul Prahladpur",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-pragati-toi-drain",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/new-drain-construction-to-prevent-flooding-in-pragati-tunnel/articleshow/111617356.cms",
        "quote": "Public Works Department(PWD) has started constructing a supplementary drain along Purana Quila Road, adjacent to the Pragati Maidan tunnel",
        "agency": None,
        "location_span": "dp-pragati-bhairon",
        "source_date": "2024-07-10",
        "title": "New drain construction to prevent flooding in Pragati tunnel",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-aiims-nl",
        "type": "PRESS_REPORT",
        "url": "https://www.newslaundry.com/2024/06/29/whos-responsible-for-delhis-rain-mess-answers-from-5-of-the-worst-hit-spots",
        "quote": "Aurobindo Marg is maintained by the PWD till Gautam Nagar turn, but the drains near the AAI office fall under the NDMC",
        "agency": None,
        "location_span": "dp-aiims-aurobindo",
        "source_date": "2024-06-29",
        "title": "Who's responsible for Delhi's rain mess? Five worst-hit spots",
        "publisher": "Newslaundry",
    },
    {
        "id": "ev-v032-maharani-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/cities/delhi-news/carpets-furniture-damaged-as-delhi-neighbourhoods-flooded-101719599032443.html",
        "quote": "We have been raising warnings about the outfall of the Taimoor Nagar drain being clogged for months, but no one listened",
        "agency": None,
        "location_span": "dp-maharani-bagh",
        "source_date": "2024-06-28",
        "title": "Carpets, furniture damaged as Delhi neighbourhoods flooded",
        "publisher": "Hindustan Times",
    },
    {
        "id": "ev-v032-who-ie",
        "type": "PRESS_REPORT",
        "url": "https://indianexpress.com/article/cities/delhi/breach-in-barapullah-drain-wall-led-to-south-new-delhi-flooding-9421799/",
        "quote": "A drain that connects Central Delhi, ITO and the WHO building and flows into the Yamuna also overflowed for several hours",
        "agency": None,
        "location_span": "dp-who-ito-ring",
        "source_date": "2024-06-29",
        "title": "Breach in Barapullah drain wall led to South, New Delhi flooding",
        "publisher": "The Indian Express",
    },
    {
        "id": "ev-v032-tilak-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/cities/delhi-news/infamous-flooded-underpasses-make-a-comeback-in-delhi-man-drowns-in-azadpur-101719598910444.html",
        "quote": "The Tilak Bridge underpass was also closed for vehicles after it got submerged in the morning, causing heavy traffic snarls along most of central Delhi areas",
        "agency": None,
        "location_span": "dp-tilak-bridge",
        "source_date": "2024-06-29",
        "title": "Infamous flooded underpasses make a comeback in Delhi",
        "publisher": "Hindustan Times",
    },
    {
        "id": "ev-v032-dhaula-ndtv",
        "type": "PRESS_REPORT",
        "url": "https://www.ndtv.com/india-news/take-measures-to-prevent-waterlogging-at-dhaula-kuan-aaps-atishi-to-officials-6429237",
        "quote": "The PWD engineers shared with the minister that the reason for waterlogging on this stretch of Dhaula Kuan is its bowl shape",
        "agency": None,
        "location_span": "dp-dhaula-kuan",
        "source_date": "2024-08-27",
        "title": "Take measures to prevent waterlogging at Dhaula Kuan",
        "publisher": "NDTV",
    },
    {
        "id": "ev-v032-saket-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/delhi-rain-drone-visuals-show-heavy-waterlogging-near-saket-metro-station/articleshow/112036486.cms",
        "quote": "The Saket Metro Station in the upscale south Delhi also witnessed severe waterlogging due to the heavy downpour",
        "agency": None,
        "location_span": "dp-mehrauli-badarpur-saket",
        "source_date": "2024-07-26",
        "title": "Drone visuals show heavy waterlogging near Saket Metro station",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-qutub-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/india-news/heavy-rainfall-inundates-parts-of-delhi-triggers-traffic-snarls-101724906705594.html",
        "quote": "Waterlogging was reported from areas such as Sarita Vihar, Qutub Minar Metro Station, Saket, Mukarba Chowk, Azadpur, Mahipalpur, and Mehrauli-Badarpur Road",
        "agency": None,
        "location_span": "dp-qutub-minar-metro",
        "source_date": "2024-08-29",
        "title": "Heavy rainfall inundates parts of Delhi, triggers traffic snarls",
        "publisher": "Hindustan Times",
    },
    {
        "id": "ev-v032-sarita-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/india-news/heavy-rainfall-inundates-parts-of-delhi-triggers-traffic-snarls-101724906705594.html",
        "quote": "Waterlogging was reported from areas such as Sarita Vihar, Qutub Minar Metro Station, Saket, Mukarba Chowk, Azadpur, Mahipalpur, and Mehrauli-Badarpur Road",
        "agency": None,
        "location_span": "dp-sarita-vihar",
        "source_date": "2024-08-29",
        "title": "Heavy rainfall inundates parts of Delhi, triggers traffic snarls",
        "publisher": "Hindustan Times",
    },
    {
        "id": "ev-v032-bhera-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/india-news/heavy-rainfall-inundates-parts-of-delhi-triggers-traffic-snarls-101724906705594.html",
        "quote": "Outer ring Road (from Bhera roundabout towards Peeragarhi) and underneath the railway bridge at Pul Prahladpur",
        "agency": None,
        "location_span": "dp-outer-ring-bhera-enclave",
        "source_date": "2024-08-29",
        "title": "Heavy rainfall inundates parts of Delhi, triggers traffic snarls",
        "publisher": "Hindustan Times",
    },
    {
        "id": "ev-v032-mukarba-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/india-news/heavy-rainfall-inundates-parts-of-delhi-triggers-traffic-snarls-101724906705594.html",
        "quote": "Waterlogging was reported from areas such as Sarita Vihar, Qutub Minar Metro Station, Saket, Mukarba Chowk, Azadpur, Mahipalpur, and Mehrauli-Badarpur Road",
        "agency": None,
        "location_span": "dp-outer-ring-mukarba-madhuban",
        "source_date": "2024-08-29",
        "title": "Heavy rainfall inundates parts of Delhi, triggers traffic snarls",
        "publisher": "Hindustan Times",
    },
    {
        "id": "ev-v032-mahipalpur-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/india-news/heavy-rainfall-inundates-parts-of-delhi-triggers-traffic-snarls-101724906705594.html",
        "quote": "Waterlogging was reported from areas such as Sarita Vihar, Qutub Minar Metro Station, Saket, Mukarba Chowk, Azadpur, Mahipalpur, and Mehrauli-Badarpur Road",
        "agency": None,
        "location_span": "dp-mahipalpur-tpoint",
        "source_date": "2024-08-29",
        "title": "Heavy rainfall inundates parts of Delhi, triggers traffic snarls",
        "publisher": "Hindustan Times",
    },
    {
        "id": "ev-v032-ashram-hindu",
        "type": "PRESS_REPORT",
        "url": "https://www.thehindu.com/news/cities/Delhi/parts-of-delhi-witness-severe-waterlogging-following-heavy-rains/article68545452.ece",
        "quote": "Severe waterlogging was witnessed near Ashram Bridge after incessant rainfall",
        "agency": None,
        "location_span": "dp-ashram-underpass",
        "source_date": "2024-08-20",
        "title": "Parts of Delhi witness severe waterlogging following heavy rains",
        "publisher": "The Hindu",
    },
    {
        "id": "ev-v032-loni-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/zakhira-underpass-waterlogging-issue-in-delhi/articleshow/112664691.cms",
        "quote": "At the Loni roundabout, PWD plans to remodel the drain, construct a pump house and build a sump well, along with desilting a new well nearby",
        "agency": None,
        "location_span": "dp-loni-rd",
        "source_date": "2024-08-21",
        "title": "Zakhira underpass waterlogging issue in Delhi",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-karala-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/zakhira-underpass-waterlogging-issue-in-delhi/articleshow/112664691.cms",
        "quote": "In west Delhi, Karala Road, near Kanjhawala industrial area, is another waterlogging-prone stretch",
        "agency": None,
        "location_span": "dp-karala-kanjhawala",
        "source_date": "2024-08-21",
        "title": "Zakhira underpass waterlogging issue in Delhi",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-sarai-nl",
        "type": "PRESS_REPORT",
        "url": "https://www.newslaundry.com/2024/06/29/whos-responsible-for-delhis-rain-mess-answers-from-5-of-the-worst-hit-spots",
        "quote": "Excessive waterlogging was also witnessed at Pragati Maidan Tunnel, Azad Market, and Sarai Kale Khan, among others",
        "agency": None,
        "location_span": "dp-sarai-kale-khan",
        "source_date": "2024-06-29",
        "title": "Who's responsible for Delhi's rain mess? Five worst-hit spots",
        "publisher": "Newslaundry",
    },
    {
        "id": "ev-v032-azad-mkt-nl",
        "type": "PRESS_REPORT",
        "url": "https://www.newslaundry.com/2024/06/29/whos-responsible-for-delhis-rain-mess-answers-from-5-of-the-worst-hit-spots",
        "quote": "Videos of vehicles being stuck in Azad Market underpass are also being widely-shared on social media",
        "agency": None,
        "location_span": "dp-azad-market",
        "source_date": "2024-06-29",
        "title": "Who's responsible for Delhi's rain mess? Five worst-hit spots",
        "publisher": "Newslaundry",
    },
    {
        "id": "ev-v032-mandapam-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/new-drain-construction-to-prevent-flooding-in-pragati-tunnel/articleshow/111617356.cms",
        "quote": "Still the tunnel gets heavily flooded every monsoon or during any heavy downpour due to water entering through an underground parking facility, which is managed by India Trade Promotion Organisation",
        "agency": None,
        "location_span": "dp-bharat-mandapam-tunnel",
        "source_date": "2024-07-10",
        "title": "New drain construction to prevent flooding in Pragati tunnel",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-mathura-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/new-drain-construction-to-prevent-flooding-in-pragati-tunnel/articleshow/111617356.cms",
        "quote": "The VIP area along Mathura Road has been prone to flooding even during light rainfall due to the absence of an adequate drainage system and as it is a low-lying spot",
        "agency": None,
        "location_span": "dp-mathura-rd-hc",
        "source_date": "2024-07-10",
        "title": "New drain construction to prevent flooding in Pragati tunnel",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-dwarka-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/delhi-underpasses-flooded-despite-preparedness-claims/articleshow/111497831.cms",
        "quote": "The sub-surface passages at Minto Road, Pul Prahladpur, Samaypur Badli, Okhla, Pragati Maidan transit corridor, Sarita Vihar, Azadpur, Dwarka and Delhi-Meerut expressway under the jurisdiction of different agencies were all inundated",
        "agency": None,
        "location_span": "dp-dwarka-underpass",
        "source_date": "2024-07-05",
        "title": "Delhi underpasses flooded despite preparedness claims",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-shalimar-toi",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/delhi-underpasses-flooded-despite-preparedness-claims/articleshow/111497831.cms",
        "quote": "A body, the fourth fatality, was found at the Shalimar Bagh underpass, a location not on the list of hotspots",
        "agency": None,
        "location_span": "dp-shalimar-bagh-underpass",
        "source_date": "2024-07-05",
        "title": "Delhi underpasses flooded despite preparedness claims",
        "publisher": "The Times of India",
    },
    {
        "id": "ev-v032-azadpur-ht",
        "type": "PRESS_REPORT",
        "url": "https://www.hindustantimes.com/cities/delhi-news/infamous-flooded-underpasses-make-a-comeback-in-delhi-man-drowns-in-azadpur-101719598910444.html",
        "quote": "Two of our pump houses were completely submerged and water level was rising due to backflow from the adjacent sewer line",
        "agency": None,
        "location_span": "dp-azadpur-underpass",
        "source_date": "2024-06-29",
        "title": "Infamous flooded underpasses make a comeback in Delhi",
        "publisher": "Hindustan Times",
    },
    {
        "id": "ev-v032-ndmc-kartavya",
        "type": "PRESS_REPORT",
        "url": "https://timesofindia.indiatimes.com/city/delhi/ndmc-identifies-14-vulnerable-waterlogging-points-in-new-delhi/articleshow/111497773.cms",
        "quote": "Previously, NDMC had six vulnerable points at “Satya Sadan, Lodhi Estate, Africa Avenue underpass, Panchkuian Road, Purana Qila and DLF parking”",
        "agency": None,
        "location_span": "dp-kartavya-path-boat-club",
        "source_date": "2024-07-05",
        "title": "NDMC identifies 14 vulnerable waterlogging points",
        "publisher": "The Times of India",
    },
]


def volunteer(point_id: str, suffix: str, quote: str, when: str = "2024-06-28") -> dict:
    return {
        "id": f"ev-illust-v032-{point_id}-{suffix}",
        "type": "PRESS_REPORT",
        "url": f"https://disputepoint.local/illustrative/volunteer/{point_id}/{suffix}",
        "quote": quote,
        "agency": None,
        "location_span": point_id,
        "source_date": when,
        "retrieved_at": "2026-10-09T13:30:00Z",
        "weight": 0.55,
        "needs_review": False,
        "is_synthetic": True,
        "channel": "VOLUNTEER_REPORTED",
        "title": "Illustrative volunteer report",
        "publisher": "DisputePoint sample (not a real submission)",
        "establishes": "Illustrative volunteer observation for demo density at this location.",
        "does_not_establish": "Not a verified submission from a named real person; not an official record.",
    }


# Extra volunteers for points that still need density after sourced adds.
VOL_TEMPLATES: dict[str, list[tuple[str, str]]] = {
    "dp-jahangirpuri-metro": [
        ("wl1", "Volunteer report: standing water on Jahangirpuri Metro Station Road approach; pedestrians detouring."),
        ("photo1", "Volunteer report: photograph marked for review of ponded lane near Jahangirpuri metro exit."),
    ],
    "dp-gtk-depot": [
        ("wl1", "Volunteer report: GTK Depot stretch holding water at kerb; buses slow through the ponded section."),
        ("cross1", "Volunteer report: road difficult to cross near GTK Depot after overnight rain."),
    ],
    "dp-kali-mandir": [
        ("wl1", "Volunteer report: Kali Mandir stretch wet and slow; drain mouths submerged at the kerb."),
        ("photo1", "Volunteer report: photo submitted for review linking ponding to the open Kali Mandir incident."),
    ],
    "dp-patparganj-nh24": [
        ("wl1", "Volunteer report: NH-24 Patparganj underpass approach ponded; traffic diverting."),
        ("cross1", "Volunteer report: pedestrians avoiding depressed section near Pandav Nagar underpass."),
    ],
    "dp-ashram-underpass": [
        ("wl1", "Volunteer report: Ashram underpass approach difficult to cross; shallow flooding at the ramp."),
    ],
    "dp-sarita-vihar": [
        ("wl1", "Volunteer report: Sarita Vihar underpass holding water; two-wheelers turning back."),
    ],
    "dp-karala-kanjhawala": [
        ("wl1", "Volunteer report: Karala–Kanjhawala Road ponded after rain; trucks slowing on the industrial approach."),
    ],
    "dp-outer-ring-bhera-enclave": [
        ("wl1", "Volunteer report: Outer Ring near Bhera Enclave underpass wet; multiple volunteers noted same stretch."),
    ],
    "dp-outer-ring-mukarba-madhuban": [
        ("wl1", "Volunteer report: Mukarba–Madhuban Outer Ring approach ponded at metro pillar."),
    ],
    "dp-mahipalpur-tpoint": [
        ("wl1", "Volunteer report: Mahipalpur T-Point holding water; airport-bound traffic crawling."),
    ],
    "dp-qutub-minar-metro": [
        ("wl1", "Volunteer report: Qutub Minar metro approach lanes ponded; photo marked for review."),
    ],
    "dp-dwarka-underpass": [
        ("wl1", "Volunteer report: Dwarka underpass corridor holding water; diversions advised by volunteers."),
    ],
    "dp-shalimar-bagh-underpass": [
        ("wl1", "Volunteer report: Shalimar Bagh underpass approach wet; crossing difficult on foot."),
    ],
    "dp-azadpur-underpass": [
        ("wl1", "Volunteer report: Azadpur underpass still ponded hours after rain; photo for review."),
    ],
    "dp-dhaula-kuan": [
        ("wl1", "Volunteer report: Dhaula Kuan flyover underpass slow with standing water on Ring Road."),
    ],
    "dp-tilak-bridge": [
        ("wl1", "Volunteer report: Tilak Bridge underpass closed feel — water at mid-span; pedestrians detour."),
    ],
    "dp-loni-rd": [
        ("wl1", "Volunteer report: Loni Road roundabout kerbs submerged; autos taking longer routes."),
    ],
    "dp-azad-market": [
        ("wl1", "Volunteer report: Azad Market underpass approach ponded; bus passengers delaying entry."),
    ],
    "dp-pragati-bhairon": [
        ("wl1", "Volunteer report: Pragati / Bhairon corridor approaches wet; tunnel entry looks closed."),
    ],
    "dp-bharat-mandapam-tunnel": [
        ("wl1", "Volunteer report: Bharat Mandapam tunnel approach ponded; traffic using Ring Road alternate."),
    ],
    "dp-mathura-rd-hc": [
        ("wl1", "Volunteer report: Mathura Road near HC pool approaches slow with standing water."),
    ],
    "dp-aiims-aurobindo": [
        ("wl1", "Volunteer report: AIIMS / Aurobindo Marg roundabout holding water; pedestrians wading kerbs."),
    ],
    "dp-maharani-bagh": [
        ("wl1", "Volunteer report: Maharani Bagh lane difficult to cross; drain smell after overnight rain."),
    ],
    "dp-sarai-kale-khan": [
        ("wl1", "Volunteer report: Sarai Kale Khan hub approaches ponded; walkways hard to use."),
    ],
    "dp-kartavya-path-boat-club": [
        ("wl1", "Volunteer report: Kartavya Path near Boat Club wet at kerb; ceremonial stretch slow."),
    ],
    "dp-mehrauli-badarpur-saket": [
        ("wl1", "Volunteer report: Saket metro road holding water; MB Road approach crawling."),
    ],
}


def finish_row(row: dict) -> dict:
    row.setdefault("retrieved_at", "2026-10-09T13:30:00Z")
    row.setdefault("weight", 0.55)
    row.setdefault("needs_review", False)
    row.setdefault("is_synthetic", False)
    row.setdefault(
        "establishes",
        f"Public reporting describing conditions at {row.get('location_span') or 'this location'}.",
    )
    row.setdefault(
        "does_not_establish",
        "Does not by itself assign exclusive operational ownership for this incident.",
    )
    return row


def main() -> None:
    points_doc = json.loads(POINTS.read_text())
    evidence_doc = json.loads(EVIDENCE.read_text())
    points_doc["version"] = "0.3.2"
    points_doc["notes"] = (
        "v0.3.2 full-board deep enrichment: Research OS / Exa for all 35; incident_summary + "
        "claim_summaries on every point; ≥5 evidence each. Not DM-71 bulk."
    )
    evidence_doc["version"] = "0.3.2"
    evidence_doc["notes"] = (
        "v0.3.2: sourced gap-fill from Exa FACT pass + illustrative volunteer rows "
        "(VOLUNTEER_REPORTED + is_synthetic=true). COURT needs_review=true."
    )

    by_id = {r["id"]: r for r in evidence_doc["evidence"]}

    for row in SOURCED:
        finished = finish_row(dict(row))
        if finished["id"] not in by_id:
            evidence_doc["evidence"].append(finished)
            by_id[finished["id"]] = finished

    for point_id, pairs in VOL_TEMPLATES.items():
        for suffix, quote in pairs:
            vol = volunteer(point_id, suffix, quote)
            if vol["id"] not in by_id:
                evidence_doc["evidence"].append(vol)
                by_id[vol["id"]] = vol

    for pt in points_doc["points"]:
        deep = POINT_DEEP.get(pt["id"])
        if not deep:
            raise SystemExit(f"missing POINT_DEEP for {pt['id']}")
        pt["incident_summary"] = deep["incident_summary"]
        pt["claim_summaries"] = deep["claim_summaries"]

        ids = list(pt.get("evidence_ids", []))
        for row in evidence_doc["evidence"]:
            if row.get("location_span") == pt["id"] and row["id"] not in ids:
                # Only auto-attach v032 / illustrative rows we just added
                if row["id"].startswith("ev-v032-") or row["id"].startswith("ev-illust-v032-"):
                    ids.append(row["id"])

        # Ensure ≥5 with additional volunteers if still short
        n = 0
        while len(ids) < 5:
            n += 1
            vol = volunteer(
                pt["id"],
                f"pad{n}",
                f"Volunteer report: waterlogging conditions noted near {pt['name']}; linked to open incident for review.",
            )
            if vol["id"] not in by_id:
                evidence_doc["evidence"].append(vol)
                by_id[vol["id"]] = vol
            if vol["id"] not in ids:
                ids.append(vol["id"])
            if n > 5:
                break
        pt["evidence_ids"] = ids

    for row in evidence_doc["evidence"]:
        if row.get("type") == "COURT_ORDER":
            row["needs_review"] = True
        row.setdefault("title", f"{row['type']} — {row.get('location_span') or 'Delhi'}")
        row.setdefault("publisher", "Public source (see URL)")
        if not row.get("establishes"):
            finish_row(row)

    POINTS.write_text(json.dumps(points_doc, indent=2, ensure_ascii=False) + "\n")
    EVIDENCE.write_text(json.dumps(evidence_doc, indent=2, ensure_ascii=False) + "\n")

    thin = [p["id"] for p in points_doc["points"] if len(p.get("evidence_ids", [])) < 5]
    no_claim = [p["id"] for p in points_doc["points"] if not p.get("claim_summaries")]
    print(f"points={len(points_doc['points'])} evidence={len(evidence_doc['evidence'])}")
    print(f"thin(<5)={thin} no_claims={no_claim}")


if __name__ == "__main__":
    main()
