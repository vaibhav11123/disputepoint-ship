# Data enrichment checklist

**SoT research log:** [../research/enrichment-source-pass.md](../research/enrichment-source-pass.md)  
**Fixtures:** `data/fixtures/points.json`, `evidence.json` → version **0.3.2**  
**Out of scope:** live IMD/CWC/Google; scoring formula changes; inventing COURT/GOV statements.

## Honesty

| Kind | Marker |
|------|--------|
| Sourced press/court | Real URL; `is_synthetic=false`; COURT → `needs_review=true` |
| Illustrative volunteer | `channel=VOLUNTEER_REPORTED` + `is_synthetic=true`; compact Volunteer chip |
| Computed fields | `ownership_*`, `priority_*`, `recommended_action` from ingest engines |

## Depth bar (all 35) — PASS v0.3.2

Every point has:

- Research-backed `incident_summary` (not a one-line label)
- `claim_summaries` for each entry in `agencies_claimed`
- ≥5 `evidence_ids` with `source_date` / `title` / `publisher` / establishes lines
- Six CONFLICT unchanged: Purana Quila, Minto, Barapullah, Lodhi/Moolchand, Okhla, Samaypur-Badli

## Batches

| Batch | Coverage |
|-------|----------|
| A | Six CONFLICT (spine) |
| B | Gate A assigned / multi-claim |
| C | Underpass Expansion B |
| D | Arterial / metro / outer |

## Generators

- `scripts/enrich_fixtures_v031.py` — initial metadata + six CONFLICT depth
- `scripts/enrich_fixtures_v032.py` — full-board deep pass

## Validation

- `make test`
- Ownership smoke: exactly six CONFLICT
- Spot-check Command + sample incidents across batches A–D
