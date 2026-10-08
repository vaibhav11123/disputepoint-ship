# Geocode candidates (Nominatim + Research OS)

**Purpose:** Offline candidates for `lat`/`lon` on Gate A points.  
**MapHUD gate:** Secondary MapLibre HUD (BUILD IF STABLE) ships markers only after human **VERIFIED** promote — see [../build/DEMO_WOW.md](../build/DEMO_WOW.md) M1 and GAP-DATA-04.  
**Policy:** [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/) — ≤1 req/s, identifying User-Agent, ODbL attribution.  
**User-Agent used:** `DisputePoint/0.1 (hackathon; https://github.com/vaibhavsingh/disputepoint)`  
**Licence on OSM hits:** Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright

## Runtime

`make run` sets `DP_LIVE_FETCH=1`. The app fills any still-null points through Nominatim (`backend/app/services/geocode.py`) at one request per second. Hits are stored on the sqlite row only. Unit tests and Playwright leave `DP_LIVE_FETCH` unset.

## Promoted into fixtures (2026-10-08)

| id | query | lat | lon | display_name | osm_id | cite | verify_status |
|----|-------|-----|-----|--------------|--------|------|---------------|
| dp-purana-quila | Purana Quila Road Delhi | 28.6149700 | 77.2362208 | Purana Quila Road, Central Vista… | way/1248027223 | https://www.openstreetmap.org/way/1248027223 | VERIFIED |
| dp-bharat-mandapam-tunnel | Bharat Mandapam Delhi | 28.6172378 | 77.2434616 | Bharat Mandapam, Bhairon Marg… | way/28103691 | https://www.openstreetmap.org/way/28103691 | VERIFIED |
| dp-mathura-rd-hc | Delhi High Court | 28.6087639 | 77.2364346 | Delhi High Court, Central Vista… | way/138946116 | https://www.openstreetmap.org/way/138946116 | VERIFIED |
| dp-minto-bridge | Minto Bridge Delhi | 28.6334521 | 77.2266682 | Shivaji Bridge (Minto alias) | node/1988513598 | https://www.openstreetmap.org/node/1988513598 | VERIFIED |
| dp-aiims-aurobindo | AIIMS Delhi | 28.5668602 | 77.2078058 | A.I.I.M.S., Aurobindo Marg… | node/7018301883 | https://www.openstreetmap.org/node/7018301883 | VERIFIED |
| dp-lodhi-moolchand | Moolchand Flyover Delhi | 28.5655290 | 77.2341536 | Moolchand Flyover… | way/44316330 | https://www.openstreetmap.org/way/44316330 | VERIFIED |
| dp-maharani-bagh | Maharani Bagh Delhi | 28.5720013 | 77.2633718 | Maharani Bagh… | node/2797954841 | https://www.openstreetmap.org/node/2797954841 | VERIFIED |
| dp-zakhira | Zakhira Flyover Delhi | 28.6704636 | 77.1606005 | Zakhira Flyover… | way/77769955 | https://www.openstreetmap.org/way/77769955 | VERIFIED |
| dp-azad-market | Azad Market Delhi | 28.6631328 | 77.2076461 | Azad Market… | node/5758572044 | https://www.openstreetmap.org/node/5758572044 | VERIFIED |
| dp-pragati-bhairon | Bhairon Marg Delhi | 28.6115295 | 77.2442955 | Bhairon Marg… | way/130987222 | https://www.openstreetmap.org/way/130987222 | VERIFIED |
| dp-loni-rd | Loni Road Delhi | 28.6917193 | 77.2918418 | Loni Road… | way/684354139 | https://www.openstreetmap.org/way/684354139 | VERIFIED |
| dp-barapullah | Barapullah Bridge Delhi | 28.5841993 | 77.2533482 | Barapullah Bridge, Lajpat Nagar… | way/1314555167 | https://www.openstreetmap.org/way/1314555167 | VERIFIED |
| dp-who-ito-ring | Indraprastha Estate Delhi | 28.6273744 | 77.2438287 | Indraprastha Estate (IP Estate / Ring Rd near WHO) | relation/3848453 | https://www.openstreetmap.org/relation/3848453 | VERIFIED |
| dp-pul-prahladpur | Pul Prahladpur Delhi | 28.5019105 | 77.2907092 | Police Station Pul Prahladpur, Mehrauli Badarpur Road… | node/6274319087 | https://www.openstreetmap.org/node/6274319087 | VERIFIED |

## Weak-three research notes (promoted 2026-10-08)

| id | note |
|----|------|
| dp-barapullah | Nominatim `Barapullah Bridge` — name token matches; bridge sits on the drain corridor (not the earlier Kushak Nallah proxy). |
| dp-who-ito-ring | Press places the hotspot on Ring Road near WHO / IP Estate; OSM has no WHO building node, so Indraprastha Estate relation is the cited corridor pin. |
| dp-pul-prahladpur | Police Station Pul Prahladpur on Mehrauli–Badarpur Road (underpass corridor named in PWD / ThePrint coverage). |

All 14 Gate A points now carry cited coordinates (FR-001 map markers).

## Expansion B candidates (2026-10-08) — not promoted

Demo volume points. **`lat`/`lon` stay null** until a human marks VERIFIED. Suggested Nominatim queries only:

| id | suggested query | status |
|----|-----------------|--------|
| dp-azadpur-underpass | Azadpur underpass Delhi | CANDIDATE |
| dp-samaypur-badli | Samaypur Badli Delhi | CANDIDATE |
| dp-okhla-underpass | Okhla underpass Delhi | CANDIDATE |
| dp-dhaula-kuan | Dhaula Kuan flyover Delhi | CANDIDATE |
| dp-sarita-vihar | Sarita Vihar underpass Delhi | CANDIDATE |
| dp-karala-kanjhawala | Karala Kanjhawala Road Delhi | CANDIDATE |
| dp-jahangirpuri-metro | Jahangirpuri Metro Station Delhi | CANDIDATE |
| dp-tilak-bridge | Tilak Bridge ITO Delhi | CANDIDATE |
| dp-ashram-underpass | Ashram underpass Delhi | CANDIDATE |
| dp-shalimar-bagh-underpass | Shalimar Bagh underpass Delhi | CANDIDATE |
| dp-mehrauli-badarpur-saket | Saket Metro Station Delhi | CANDIDATE |
| dp-outer-ring-bhera-enclave | Bhera Enclave Outer Ring Road Delhi | CANDIDATE |
| dp-outer-ring-mukarba-madhuban | Mukarba Chowk Delhi | CANDIDATE |
| dp-gtk-depot | GTK Depot Delhi | CANDIDATE |
| dp-kali-mandir | Kali Mandir Delhi | CANDIDATE |
| dp-qutub-minar-metro | Qutub Minar Metro Station Delhi | CANDIDATE |
| dp-sarai-kale-khan | Sarai Kale Khan Delhi | CANDIDATE |
| dp-patparganj-nh24 | Pandav Nagar NH-24 Delhi | CANDIDATE |
| dp-mahipalpur-tpoint | Mahipalpur Delhi | CANDIDATE |
| dp-kartavya-path-boat-club | Kartavya Path Delhi | CANDIDATE |
| dp-dwarka-underpass | Dwarka underpass Delhi | CANDIDATE |

Do not invent decimals. Offline Nominatim ≤1 req/s when human promotes.

## Failed / weak queries (history)

| id | failed query | note |
|----|--------------|------|
| dp-mathura-rd-hc | Mathura Road High Court Delhi | empty |
| dp-mathura-rd-hc | Mathura Road Delhi | wrong hit (Okhla Estate Marg) — discarded |
| dp-who-ito-ring | World Health Organization Ring Road Delhi | empty |
| dp-who-ito-ring | ITO Ring Road Delhi | empty |
| dp-pul-prahladpur | Pul Prahladpur underpass Delhi | empty (earlier probe) |
| dp-barapullah | Barapullah Nallah Delhi | proxy bridge — discarded |

Raw JSON responses (gitignored optional): `docs/research/_geocode_raw/` — local cache only; do not treat as SoT.
