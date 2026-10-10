# Trace check — coverage of TRACEABILITY / routes / demo

Generated against authored `work-packages.yaml` + `status.json` + explicit skips. Not a second requirement list.

## MUST FRs

| Id | Placement | Result |
|----|-----------|--------|
| FR-001 | WP-05 (numeric lat residual G-GEO) | OK |
| FR-002 | WP-04 | OK |
| FR-003 | WP-02 | OK |
| FR-004 | WP-02 | OK |
| FR-005 | WP-03 | OK |
| FR-006 | WP-06 + WP-10 | OK |
| FR-007 | WP-06 + WP-10 | OK |
| FR-008 | WP-09 | OK |
| FR-009 | WP-09 | OK |
| FR-010 | WP-09 | OK |
| FR-011 | WP-02 + WP-09 | OK |
| FR-012 | WP-08 + WP-11 | OK |
| FR-015 | WP-14 (+ G-GOLD for metrics) | OK |
| FR-016 | WP-15 Ship It live 2026-10-10 (+ G-VIDEO for AWS on camera) | OK |
| FR-017 | WP-13 | OK |
| FR-018 | WP-15 | OK |
| FR-019 | WP-04 | OK |
| FR-020 | WP-09 | OK |
| FR-021 | WP-09 | OK |
| FR-023 | WP-03 + WP-12 | OK |
| FR-024 | WP-12 | OK |
| FR-027 | WP-16 + G-KPI | OK |

## SHOULD / COULD

| Id | Placement | Result |
|----|-----------|--------|
| FR-013 | WP-03 | OK |
| FR-014 | explicit skip | OK |
| FR-022 | explicit skip | OK |
| FR-025 | explicit skip | OK |
| FR-026 | WP-08 | OK |

## Nine DecisionAPI routes

| Route | Package | Result |
|-------|---------|--------|
| GET /health | WP-07 | OK |
| GET /points | WP-07 | OK |
| GET /points/{id} | WP-07 | OK |
| POST /rain/refresh | WP-07 | OK |
| POST /rain/scenario | WP-07 | OK |
| GET /meta/honesty | WP-07 | OK |
| POST …/ack | WP-08 | OK |
| POST …/override | WP-08 | OK |
| POST …/escalate | WP-08 | OK |

## E2E

| Id | Placement | Result |
|----|-----------|--------|
| E2E-01…06 | WP-13 | OK |
| E2E-07 | skip (G-GEO) | OK |
| E2E-08, E2E-09 | WP-12 | OK |

## Demo W1–W9

Defining artifact: [docs/build/DEMO_WOW.md](../docs/build/DEMO_WOW.md). Rehearsal / AWS dual path: [docs/build/DEMO_REHEARSAL.md](../docs/build/DEMO_REHEARSAL.md). Residuals: R-DEMO-WOW, R-DEMO-DETERMINISM, R-GIT-CLOCK in [RESIDUALS.md](RESIDUALS.md).

| Beat | Placement | Result |
|------|-----------|--------|
| W1, W3, W4, W6 | WP-09 / WP-13 · DEMO_WOW | OK |
| W2 | WP-10 · DEMO_WOW | OK |
| W5 | WP-12 · DEMO_WOW | OK |
| W7 | WP-11 · DEMO_WOW | OK |
| W8 | WP-16 + G-KPI · DEMO_WOW | OK |
| W9 | G-VIDEO · DEMO_REHEARSAL | OK |

## NFRs

| Id | Placement | Result |
|----|-----------|--------|
| NFR-001, 002, 003, 006 | WP-07 (rain offline with WP-06) | OK |
| NFR-004 | all commits | OK |
| NFR-005 | WP-15 | OK |
| NFR-007, 008 | G-VIS | OK |
| NFR-009 | WP-00 | OK |
| NFR-010 | G-FORM / LICENSE_AUDIT copy | OK |

## plan-check

`execution/plan-check.yaml` **PASS**. Derived waves PARALLEL_SAFE under five-part definition.

## Verdict

**PASS** — every MUST FR, NFR, E2E id, API route, and W1–W9 beat is on a package, a human gate, or an explicit skip. No invented `T-*` ids. No app code in this pass.
