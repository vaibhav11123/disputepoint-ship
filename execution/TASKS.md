# Tasks (human view)

**Not the scheduler source of truth.** The orchestrator reads [`work-packages.yaml`](work-packages.yaml) and trusts [`plan-check.yaml`](plan-check.yaml) / derived [`waves.yaml`](waves.yaml).

Session entry: [`START.md`](START.md). Gates: [`GATES.md`](GATES.md). Residuals: [`RESIDUALS.md`](RESIDUALS.md).

Derived waves (do not hand-edit):

| Wave | Packages |
|------|----------|
| 0 | WP-00 |
| 1 | WP-01 |
| 2 | WP-02, WP-04 |
| 3 | WP-03 |
| 4 | WP-05, WP-06, WP-14 |
| 5 | WP-07 |
| 6 | WP-08, WP-09, WP-15 |
| 7 | WP-10, WP-11, WP-12 |
| 8 | WP-13 |
| 9 | WP-16 |

Locks on every package: `THETA=0.65`, `W_NORM=2.0`, Bedrock off, no ML runtime, U = coordination uncertainty, CONFLICT → `responsible_agency` null. No schema edits. Paths from LLD §3 / §8.

---

## WP-00 — Toolchain and Makefile

| Field | Value |
|-------|--------|
| Depends | — |
| Requirements | NFR-009 |
| Risk | LOW |
| Owned paths | `Makefile`, `pyproject.toml`, `package.json`, `backend/app/__init__.py`, `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/index.html` |
| Read | `docs/LLD.md` §3; `docs/operations/SUBMISSION_GIT.md`; AC NFR-009 |
| Done when | `make test` (may pass with zero tests) |

## WP-01 — Schema-shaped models

| Field | Value |
|-------|--------|
| Depends | WP-00 |
| Requirements | FR-001 (models slice) |
| Risk | MEDIUM |
| Owned paths | `backend/app/models/**`, `tests/test_models.py` |
| Read | DisputePointSeed + DisputePoint schemas; DATA_MODEL seed-to-runtime |
| Done when | `pytest tests/test_models.py -q` — seed validates; null lat fails runtime |

## WP-02 — OwnershipEngine

| Field | Value |
|-------|--------|
| Depends | WP-01 |
| Requirements | FR-003, FR-004, FR-011 |
| Risk | CRITICAL · human gate G-OWNERSHIP |
| Owned paths | `backend/app/services/ownership.py`, `tests/test_ownership.py` |
| Read | LLD §5; AC FR-003, FR-004 |
| Done when | `pytest tests/test_ownership.py -q` (`T-OWN-θ`, `T-OWN-CF-NULL`) |

## WP-03 — PriorityEngine

| Field | Value |
|-------|--------|
| Depends | WP-02 |
| Requirements | FR-005, FR-013, FR-023 |
| Risk | HIGH |
| Owned paths | `backend/app/services/priority.py`, `tests/test_priority.py` |
| Read | LLD §6, §19, §24; AC FR-005, FR-013, FR-023 |
| Done when | `pytest tests/test_priority.py -q` (`T-RANK-01`) |

## WP-04 — Evidence load

| Field | Value |
|-------|--------|
| Depends | WP-01 |
| Requirements | FR-002, FR-019 |
| Risk | HIGH |
| Owned paths | `backend/app/services/evidence.py`, `tests/test_evidence.py` |
| Read | Evidence schema; AC FR-002, FR-019; DATA_PLAYBOOK; `data/fixtures/evidence.json` |
| Done when | `pytest tests/test_evidence.py -q` (`T-PROV-01`) |

## WP-05 — Ingest

| Field | Value |
|-------|--------|
| Depends | WP-02, WP-03, WP-04 |
| Requirements | FR-001 |
| Risk | HIGH |
| Owned paths | `backend/app/services/ingest.py`, `backend/app/db/**`, `tests/test_ingest.py` |
| Read | LLD §9; DATA_MODEL; fixtures; AC FR-001; `execution/RESIDUALS.md` |
| Done when | `pytest tests/test_ingest.py -q` (`T-DATA-01`) — count ≥12; numeric-lat clause stays DOCUMENTED until human geocodes |

## WP-06 — Rain service

| Field | Value |
|-------|--------|
| Depends | WP-03 |
| Requirements | FR-006, FR-007 |
| Risk | MEDIUM |
| Owned paths | `backend/app/services/rain.py`, `tests/test_rain.py` |
| Read | RainObservation schema; OpenAPI rain; AC FR-006, FR-007 |
| Done when | `pytest tests/test_rain.py -q` (`T-RAIN-01`) with fake HTTP |

## WP-07 — Read API

| Field | Value |
|-------|--------|
| Depends | WP-05, WP-06 |
| Requirements | FR-001, FR-005, FR-006, FR-007, NFR-001, NFR-002, NFR-003, NFR-006 |
| Risk | HIGH |
| Owned paths | `backend/app/main.py`, `backend/app/api/__init__.py`, `backend/app/api/read.py`, `tests/test_api_read.py` |
| Read | LLD §7, §11; OpenAPI health/points/point/honesty/rain |
| Done when | `pytest tests/test_api_read.py -q` — six read/rain routes |

## WP-08 — HITL API

| Field | Value |
|-------|--------|
| Depends | WP-07 |
| Requirements | FR-012, FR-026 |
| Risk | CRITICAL · human gate G-HITL-API |
| Owned paths | `backend/app/api/hitl.py`, `tests/test_hitl.py` |
| Read | LLD §20; OpenAPI ack/override/escalate; AC FR-012, FR-026 |
| Done when | `pytest tests/test_hitl.py -q` |

## WP-09 — Queue UI

| Field | Value |
|-------|--------|
| Depends | WP-07 |
| Requirements | FR-008, FR-009, FR-010, FR-011, FR-020, FR-021 |
| Risk | HIGH |
| Owned paths | `frontend/src/App.tsx`, `main.tsx`, `styles/**`, QueueTable, PointCard, EvidenceList, AdvisoryBanner, TopBar, `api/client.ts`, ReadinessBlock, StateChip, AgencyBlock, ProvenanceFooter |
| Read | LLD §8; UX queue/card; DESIGN_SYSTEM; AC those FRs |
| Done when | `make test` + browser cold queue (not map-first) |

## WP-10 — Rain UI

| Field | Value |
|-------|--------|
| Depends | WP-09, WP-06 |
| Requirements | FR-006, FR-007 |
| Risk | MEDIUM |
| Owned paths | `frontend/src/components/RainControl.tsx`, `frontend/src/hooks/useRain.ts` |
| Read | UX rain control; AC FR-006, FR-007 |
| Done when | `make test` + browser scenario `precip_mm=40` |

## WP-11 — HITL UI

| Field | Value |
|-------|--------|
| Depends | WP-09, WP-08 |
| Requirements | FR-012 |
| Risk | CRITICAL · human gate G-HITL-UI |
| Owned paths | `ActionBlock.tsx`, `DecisionAuditPanel.tsx` |
| Read | UX HITL; AC FR-012 |
| Done when | `make test` + browser ACK/OVERRIDE/ESCALATE + audit panel (`T-HITL-UI`) |

## WP-12 — Explain and jump

| Field | Value |
|-------|--------|
| Depends | WP-09, WP-03 |
| Requirements | FR-023, FR-024 |
| Risk | MEDIUM |
| Owned paths | PriorityExplain, CommandPalette, EvalLink, EvalDrawer |
| Read | LLD §19; UX palette; DEMO_WOW; AC FR-023, FR-024; E2E-08, E2E-09 |
| Done when | `make test` + browser chips / Cmd+K / eval link |

## WP-13 — Browser gate

| Field | Value |
|-------|--------|
| Depends | WP-10, WP-11, WP-12 |
| Requirements | FR-017 (+ E2E proof for queue/HITL/synth) |
| Risk | HIGH |
| Owned paths | `tests/e2e/**`, `frontend/playwright.config.ts` |
| Read | E2E_SCENARIOS E2E-01…E2E-06; AC FR-017 |
| Done when | `npx playwright test` (`T-GOLD-PQ`, `T-UI-01`, `T-UI-SYN`, `T-HITL-UI`); E2E-07 skipped |

## WP-14 — Baseline tournament note

| Field | Value |
|-------|--------|
| Depends | WP-03 |
| Requirements | FR-015 |
| Risk | LOW |
| Owned paths | `tests/eval/baseline_tournament.md` |
| Read | LLD §22; baseline file; GAP-EVAL-02; AC FR-015 |
| Done when | File updated from pure functions; blank cells if no `gold_order.json` |

## WP-15 — Failures and AWS doc

| Field | Value |
|-------|--------|
| Depends | WP-07 |
| Requirements | FR-016, FR-018 |
| Risk | MEDIUM · human gate G-AWS (Ship It vs Build It) |
| Owned paths | `tests/test_failures.py`, `infra/template.yaml`, `infra/README.md` |
| Read | TEST_STRATEGY failure-injection; PHASE6 §16A only; AC FR-016, FR-018 |
| Done when | `pytest tests/test_failures.py -q` (four FR-018 cases); no deploy without human |

## WP-16 — Demo rehearsal

| Field | Value |
|-------|--------|
| Depends | WP-13 |
| Requirements | FR-027, FR-016 (video beat) |
| Risk | LOW · human gate G-VIDEO |
| Owned paths | `docs/build/DEMO_REHEARSAL.md` |
| Read | PHASE6 §39; DEMO_WOW W1–W9 |
| Done when | Rehearsal doc exists; human times path (`T-KPI-TRIAGE`); agent records reported time only |

---

## Explicit skips (not packages)

| Id | Reason |
|----|--------|
| FR-014 | Optional geometry |
| FR-022 | COULD IMD rain source |
| FR-025 | Bedrock off |
| E2E-07 / MapHUD | Until human VERIFIED geocode |
