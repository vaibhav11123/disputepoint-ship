# Geocode candidates (Nominatim one-shot)

**Purpose:** Offline candidates for `lat`/`lon` on Gate A points. **Not** fixture FACT until `verify_status=VERIFIED`.  
**MapHUD gate:** Secondary MapLibre HUD (BUILD IF STABLE) ships markers only after human **VERIFIED** promote — see [../build/DEMO_WOW.md](../build/DEMO_WOW.md) M1 and GAP-DATA-04.  
**Policy:** [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/) — ≤1 req/s, identifying User-Agent, ODbL attribution.  
**Do not** call Nominatim from the running demo app.  
**User-Agent used:** `DisputePoint/0.1 (hackathon; https://github.com/vaibhavsingh/disputepoint)`  
**Retrieved:** 2026-10-06  
**Licence on all hits:** Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright

Copy into `data/fixtures/points.json` only after human review. Wrong matches stay `CANDIDATE`.

| id | query | lat | lon | display_name | osm_id | licence | verify_status |
|----|-------|-----|-----|--------------|--------|---------|---------------|
| dp-purana-quila | `Purana Quila Road Delhi` | 28.6149700 | 77.2362208 | Purana Quila Road, Central Vista, New Delhi, Delhi, 110503, India | way/1248027223 | ODbL 1.0 | CANDIDATE |
| dp-bharat-mandapam-tunnel | `Bharat Mandapam Delhi` | 28.6172378 | 77.2434616 | Bharat Mandapam, Bhairon Marg, Central, Delhi, South East Delhi, Delhi, 110503, India | way/28103691 | ODbL 1.0 | CANDIDATE |
| dp-mathura-rd-hc | `Delhi High Court` | 28.6087639 | 77.2364346 | Delhi High Court, Central Vista, New Delhi, Delhi, 110503, India | way/138946116 | ODbL 1.0 | CANDIDATE |
| dp-barapullah | `Barapullah Nallah Delhi` | 28.5868478 | 77.2486545 | Baba Banda Singh Bahadur Setu, Kushak Nallah Bus Depot, Lajpat Nagar… (proxy near Barapullah corridor) | way/170767284 | ODbL 1.0 | CANDIDATE |
| dp-minto-bridge | `Minto Bridge Delhi` | 28.6334521 | 77.2266682 | Shivaji Bridge, Babar Road… (Nominatim alias for Minto/Shivaji Bridge area) | node/1988513598 | ODbL 1.0 | CANDIDATE |
| dp-aiims-aurobindo | `AIIMS Delhi` | 28.5668602 | 77.2078058 | A.I.I.M.S., Aurobindo Marg, Kidwai Nagar, New Delhi, Delhi, 110029, India | node/7018301883 | ODbL 1.0 | CANDIDATE |
| dp-lodhi-moolchand | `Moolchand Flyover Delhi` | 28.5655290 | 77.2341536 | Moolchand Flyover, Lajpat Nagar, Central, Delhi, South East Delhi, Delhi, 110049, India | way/44316330 | ODbL 1.0 | CANDIDATE |
| dp-maharani-bagh | `Maharani Bagh Delhi` | 28.5720013 | 77.2633718 | Maharani Bagh, Central, Delhi, South East Delhi, Delhi, 110014, India | node/2797954841 | ODbL 1.0 | CANDIDATE |
| dp-who-ito-ring | `Indraprastha Estate Ring Road Delhi` | 28.6303971 | 77.2458543 | service road, Sachivalaya Road Flyover… (ITO / IP Estate Ring Road proxy) | way/220369755 | ODbL 1.0 | CANDIDATE |
| dp-zakhira | `Zakhira Flyover Delhi` | 28.6704636 | 77.1606005 | Zakhira Flyover, Amar Park, Punjabi Bagh, Karol Bagh, Delhi, Central Delhi, Delhi, 110035, India | way/77769955 | ODbL 1.0 | CANDIDATE |
| dp-pul-prahladpur | `Pul Prahladpur Delhi` | 28.4991606 | 77.2914371 | elegantcasa… Pul Prahladpur, Surajkund Road… (area, not underpass node) | way/329244094 | ODbL 1.0 | CANDIDATE |
| dp-azad-market | `Azad Market Delhi` | 28.6631328 | 77.2076461 | Azad Market, Rani Jhansi Flyover, Beri Wala Bagh, Sadar Bazar… | node/5758572044 | ODbL 1.0 | CANDIDATE |
| dp-pragati-bhairon | `Bhairon Marg Delhi` | 28.6115295 | 77.2442955 | Bhairon Marg, Central, Delhi, South East Delhi, Delhi, 110503, India | way/130987222 | ODbL 1.0 | CANDIDATE |
| dp-loni-rd | `Loni Road Delhi` | 28.6917193 | 77.2918418 | Loni Road, Balbir Nagar Extension, Shahdara… | way/684354139 | ODbL 1.0 | CANDIDATE |

## Verify checklist (human)

- [ ] Match display_name to the waterlogging / underpass intent (not a random nearby POI).
- [ ] Prefer underpass / flyover / drain nodes when available.
- [ ] Set `verify_status=VERIFIED` only after map eyeball.
- [ ] On promote to fixtures: store `geo_source=nominatim`, `geo_query`, `geo_osm_id`, `geo_licence`.
- [ ] UI/README: OSM attribution when map or coords shown.

## Failed / weak queries (history)

| id | failed query | note |
|----|--------------|------|
| dp-mathura-rd-hc | `Mathura Road High Court Delhi` | empty |
| dp-mathura-rd-hc | `Mathura Road Delhi` | wrong hit (Okhla Estate Marg) — discarded |
| dp-who-ito-ring | `World Health Organization Ring Road Delhi` | empty |
| dp-who-ito-ring | `ITO Ring Road Delhi` | empty |
| dp-pul-prahladpur | `Pul Prahladpur underpass Delhi` | empty (earlier probe) |

Raw JSON responses (gitignored optional): `docs/research/_geocode_raw/` — local cache only; do not treat as SoT.
