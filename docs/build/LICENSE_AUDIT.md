# LICENSE_AUDIT — third-party assets

**Purpose:** One row per external asset before submission. Block ship if `allowed_for_demo=false` or required attribution is missing. Fields follow [aws-strategy](../research/aws-strategy-and-submission-notes.md) §3.

**Rule:** Update this table when you add a dependency or dataset. Do not invent licenses.

| Asset | Source / URL | Retrieved / pin | License / terms | Attribution required | allowed_for_demo | allowed_for_redistribution | Notes |
|-------|--------------|-----------------|-----------------|----------------------|------------------|----------------------------|-------|
| Open-Meteo Forecast API | https://open-meteo.com | runtime; metro Delhi locks in LLD | CC-BY 4.0 (non-commercial free tier) | Yes — UI credit | true | false (cache OK; do not republish bulk) | Rain ingest only |
| Delhi HC / drain ownership quotes | LiveLaw PDF + TOI (see DEMO_SCRIPT) | fixtures `evidence.json` | Fair-use short quotes + link-out | Link to source | true | false — no wholesale PDF redistrib | `needs_review` until human OK |
| DisputePoint fixtures (points/evidence/readiness) | `data/fixtures/` | v0.2 | Project MIT for our JSON; quotes remain third-party | Per-row sources | true | true for our fields | Mark `is_synthetic` when synthetic |
| IBM Plex Sans / Mono | @fontsource / IBM | Phase 7 package lock | SIL Open Font License 1.1 | Yes if required by OFL | true | true | UX lock |
| FastAPI / Starlette / Uvicorn | PyPI | TBD at WP-00 | MIT / BSD (verify pin) | LICENSE in venv/vendor | true | true | Fill version after install |
| React / Vite | npm | TBD at WP-00 | MIT | LICENSE in node_modules | true | true | Fill version after install |
| AWS SDK / SAM / boto3 | AWS | TBD at WP-15 | AWS Customer Agreement / Apache-2.0 as packaged | As per package | true | true | Ship It path |
| Carbon / Lucide icons (if used) | npm | TBD | Apache-2.0 / ISC (verify) | Package license | true | true | Only if imported |
| OSM / Overpass (if MapHUD) | openstreetmap.org | TBD | ODbL | Yes | true | follow ODbL | Only after G-GEO |
| MapLibre GL JS / react-map-gl | npm maplibre-gl, react-map-gl | frontend package.json | BSD-3-Clause | Yes (in LICENSE notices) | true | true | Product map (Mode A) |
| RainViewer API (radar frames) | https://www.rainviewer.com/api.html | runtime optional | RainViewer API terms; attribution | Yes when radar shown | true | false (tiles) | Rain Strike / Follow Storm only — not permanent radar |
| Civic-Resolve (queue/lifecycle IA) | https://github.com/saurabhkun/Civic-Resolve | 2026-10-08 | **No LICENSE in repo** | N/A | true (reference) | false | **Reference only** — density/stepper IA; no source paste |
| WorldIntel (shell IA) | https://github.com/Sheehan007/WorldIntel | 2026-10-08 | **No LICENSE** | N/A | true (reference) | false | **Reference only** — TopBar/Detail/OpsLog concepts |
| Crisis Logistics (master-detail) | https://github.com/alpatamerr/crisis-logistics-command-system | 2026-10-08 | **No LICENSE** | N/A | true (reference) | false | **Reference only** — flyTo/escalate workflow |
| Blackleets/aegis (layer patterns) | https://github.com/Blackleets/aegis | 2026-10-08 | MIT | NOTICE if code copied | true | true | Prefer pattern reimplementation under `--dp-*` |
| osm-in/flood-map | https://github.com/osm-in/flood-map | 2026-10-08 | MIT | Yes if code used | true | true | GIS patterns only — not product UI |
| react-flip-move (if used) | https://github.com/joshwcomeau/react-flip-move | npm optional | MIT | Package license | true | true | Queue reorder; CSS FLIP OK as substitute |
| IBM Carbon (if used) | @carbon/react | not pinned yet | Apache-2.0 | Package license | true | true | Selective primitives only |
| Google Earth Studio | https://www.google.com/earth/studio/ | video export | Google Earth / Studio terms | Per Google terms | true (video tool) | false into frontend | **Mode C only** — not app dependency |

## Donor Copy/Reference lock (2026-10-08)

| Donor | Gate | Extract |
|-------|------|---------|
| Civic-Resolve | Reference until LICENSE | Queue density, StatusStepper → Event Rail |
| WorldIntel | Reference only | Shell IA |
| Crisis Logistics | Reference only | Master-detail → escalate |
| AEGIS / flood-map / FLIP / MapLibre / RainViewer | Copy/use where SPDX/API allows | Layers, radar loop, reorder |
| Earth Studio | Video tool only | Opening shot |

## Gate

- [x] Donor Copy/Reference rows locked (2026-10-08)  
- [ ] Every runtime dependency used in the submission has a row with a real license string  
- [ ] UI shows Open-Meteo attribution when live/cache rain is on  
- [ ] No L0 audit bodies in the public repo  

Owner: update during WP-00 (deps) and before G-FORM.
