# Data audit staging (Data Ready)

Tiered corpus for Gate A evidence curation. Product SoT remains Phase 6 + playbook.

| Tier | Path | Git |
|------|------|-----|
| L0 raw | `sources/`, `rain/`, `geo/`, `_work/` | **Ignored** — full fetch bodies |
| L1 decisions | `FETCH_MANIFEST.json`, `AUDIT_MATRIX.md`, `GAP_ASK.md`, this README | Committed |
| L2 product | `../fixtures/*` | Committed — short quote⊆source only |

## Rules

- Mine Research OS (`/Users/vaibhavsingh/market-research`) before re-downloading.
- No paywall/CAPTCHA bypass. Mark `gated` / `failed` in `meta.json`.
- Promote only verbatim quotes (≥10 chars) that appear in stored L0 bodies.
- Do not invent DM-71 spots, SCADA, or GPS. Do not weaken runtime DisputePoint/OpenAPI.
- Nominatim: use existing `docs/research/geocode-candidates.md`; no re-hit by default.
