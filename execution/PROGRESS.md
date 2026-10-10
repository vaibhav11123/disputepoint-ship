# Progress log

Append-only. Sessions add dated entries. Do not rewrite history.

## Header

- Control plane created from Phase 7 execution plan.
- `plan-check.yaml` status: PASS (derived waves in `waves.yaml`).
- Product app: **shipped** in this repo (Ship It live 2026-10-10). G-VIDEO still open.

## Log

### 2026-10-06 — control plane authored

- Authored: work-packages, ownership, contract-ownership, scheduler, START, TASKS, GATES, RESIDUALS, status, work-status.
- Derived: dependency-graph, plan-check, PLAN_CHECK, waves.
- AGENTS.md read order points at `execution/START.md`.
- Next human: accept PLAN_CHECK (G-PLAN); at Oct 8 declare clock (G-CLOCK) then WP-00 alone.

### 2026-10-08 — WP-00 toolchain

- G-PLAN accepted on main before this package (`plan-check.yaml` PASS).
- Branch `wp/WP-00`: Makefile install/test/run, root `pyproject.toml` and npm workspace, Vite shell, toolchain `create_app` until `backend/app/main.py` exists.
- `make install`, `make test` (no `tests/` yet), and `make run` (API `127.0.0.1:8000`, UI `127.0.0.1:5173`) passed.
- NFR-009 set to VERIFIED. WP-01 is READY. *(Historical: deploy was gated on G-AWS; cleared 2026-10-10 — see Ship It section below.)*

### 2026-10-08 — WP-01 models

- `DisputePointSeed` accepts fixture null lat/lon. `DisputePoint` rejects null lat/lon and empty `evidence_ids`.
- CONFLICT or UNKNOWN with a non-null `responsible_agency` fails validation.
- `pytest tests/test_models.py -q`: 9 passed. Fixture file was not given coordinates.
- FR-001 stays DOCUMENTED (numeric lat still waits on G-GEO).
- Same-session MEDIUM review: schema required fields and bbox match the JSON Schema; no schema file edited.
- WP-02 and WP-04 are READY.

### 2026-10-08 — WP-02 and WP-04, then G-OWNERSHIP

- OwnershipEngine: confidence is `min(1, top_weight_sum / 2.0)`. Below 0.65 the agency is null. A close pair (sums within 0.1 and both above 0.4) is CONFLICT with a null agency even when confidence is at least 0.65.
- Evidence loader validates fixture rows. Quote ⊆ source is checked against caller-supplied text. Gitignored L0 bodies were not opened.
- Package tests passed, then `make test` (18 passed). Schemas and OpenAPI were not edited.
- FR-002, FR-003, and FR-004 are VERIFIED. FR-001 stays DOCUMENTED pending G-GEO. FR-011 stays DOCUMENTED pending E2E-03. FR-019 stays DOCUMENTED until an audit-list check is named against committed sources.
- **G-OWNERSHIP is open.** WP-03 stays BLOCKED until a human reviews CONFLICT → `responsible_agency` null.

### 2026-10-08 — G-OWNERSHIP cleared

- Read-only review of `decide`: the CONFLICT branch returns `responsible_agency=None` and does not pass the top agency through.
- `DisputePoint` rejects CONFLICT or UNKNOWN when an agency is set.
- `pytest` on the conflict and null-agency cases: 6 passed.
- Gate closed. WP-03 is READY.

### 2026-10-08 — WP-03 through WP-16

- Rank, ingest, rain, read API, and HITL API are on main. `make test`: 33 passed. Schemas and OpenAPI were not edited.
- Queue is home. Playwright E2E-01 through E2E-06, E2E-08, and E2E-09 passed. E2E-07 stays skipped.
- Fixture rows are UNKNOWN with a null agency. CONFLICT → null remains the unit case. No coordinates were added.
- G-HITL-API closed: ACK is 409 unless ASSIGNED and OPEN. OVERRIDE and ESCALATE stay off RESOLVED. Audit row is written.
- G-HITL-UI closed: ACK stays disabled on the fixture card. OVERRIDE and ESCALATE fill the audit panel.
- *(Historical)* G-AWS was open / no live URL. **Superseded 2026-10-10** — Ship It live; see section below.
- G-VIDEO and G-KPI stay open. Rehearsal file is tracked. No measured triage time. FR-027, W8, and W9 stay DOCUMENTED.
- FR-001 stays DOCUMENTED pending G-GEO. FR-015 gold cells stay blank. FR-016 stays DOCUMENTED until AWS is on screen.

### 2026-10-08 — live evidence hydrate

- `DP_LIVE_FETCH=1` now also HTTP-GETs each evidence URL, runs quote⊆source, stamps `retrieved_at` / `live_verified` (PDF skipped, fail soft).
- `/health` exposes live_fetch + evidence_live_* counts; UI Live sources strip + Refresh evidence.
- All 14 points carry cited coords; MapHUD + E2E-07 green. Status sync: FR-001 / E2E-07 marked VERIFIED (G-GEO formal stamp still human).
- G-AWS / G-VIDEO / G-KPI still open.

### 2026-10-08 — demo UX Tier S (Mode A/B/C packaging)

- Donor matrix locked in `docs/build/LICENSE_AUDIT.md` + `DONOR_MATRIX.md` (Reference vs Copy).
- Mode A: Rain Strike, Ownership Conflict (NO AUTO-ASSIGN), Evidence Ledger + Trace, Event Rail, escalate preset, Coordination Brief, Accountability Clock; map collapsed default; cold-open Purana Quila; `?judges=1` for theta/eval/Cmd+K.
- Mode B: Incident Replay scrubber. Tier A: Follow Storm (10s demo).
- Mode C docs: `EARTH_STUDIO_SHOT.md`. AWS beat: `AWS_DEMO_BEAT.md`. Submission: `SUBMISSION_CHECKLIST.md`. Visual QA: `VISUAL_QA_BASELINE.md`.
- `npx playwright test -c frontend/playwright.config.ts`: 9 passed. Frontend `npm run build` OK.
- G-AWS Ship It is live (2026-10-10). G-VIDEO still needs AWS on camera + Earth Studio export.

## 2026-10-10 — Ship It (G-AWS)

- Path: **Ship It** (not Build It). Stack `disputepoint` / `ap-south-1`.
- `make deploy` stages SAM, deploys API GW + Lambda + DynamoDB + S3 UI/evidence + EventBridge, builds UI with `VITE_API_URL`, smokes `/health` + `/points`.
- Live: Open-Meteo `rain_source_state=LIVE`, evidence batch LIVE, CORS allowlist, `/docs` 404.
- Pins: `docs/operations/AWS_OPERATOR.md`, `docs/build/AWS_DEMO_BEAT.md`. Mex ROUTER/context refreshed.
- Still open: G-VIDEO, G-VIS human slots, form/write-up, optional IAM-not-root, post-video cleanup.

## 2026-10-10 — Demo board mix + win-docs pass

- Fixtures evidence **0.3.4** / points **0.3.3**: engine board mix ASSIGNED/CONFLICT/UNKNOWN; spine CONFLICT→null; `DP_SEED_DEMO_ACK` on Mathura Rd + Bharat Mandapam; no frontend rank rewrite.
- Docs: ground-language [DEMO_SCRIPT.md](../docs/build/DEMO_SCRIPT.md); cite log [video-win-pass-2026-10-10.md](../docs/research/video-win-pass-2026-10-10.md); README judged-entry + live URLs.
- HITL on camera: ESCALATE/OVERRIDE on CONFLICT; ACK only on seeded ASSIGNED.
- Still open: G-VIDEO (human record ≤3 min with AWS on screen).
