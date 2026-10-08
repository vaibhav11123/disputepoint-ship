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

## Gate

- [ ] Every runtime dependency used in the submission has a row with a real license string  
- [ ] UI shows Open-Meteo attribution when live/cache rain is on  
- [ ] No L0 audit bodies in the public repo  

Owner: update during WP-00 (deps) and before G-FORM.
