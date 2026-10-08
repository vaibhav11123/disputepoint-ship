# Traceability matrix (RTM)

Maps MUST (and key SHOULD) requirements → contracts → acceptance → tests. Industrial RTM practice: every requirement needs design and verification coverage; unmapped rows block Spec Readiness.

**Status legend:** DOCUMENTED = specs/AC exist · IMPLEMENTED = code exists · VERIFIED = tests run green.

Phase 7 code is not started in this pass — expect **DOCUMENTED** for implementation columns.

| FR | Priority | Contract / design | AC | Test / E2E | Status |
|----|----------|-------------------|----|------------|--------|
| FR-001 | MUST | DisputePointSeed (fixtures) → DisputePoint (API); GET /points | AC FR-001 | T-DATA-01 | DOCUMENTED |
| FR-002 | MUST | Evidence schema | AC FR-002 | fixture validate | DOCUMENTED |
| FR-003 | MUST | ownership_state enum | AC FR-003 | unit OwnershipEngine | DOCUMENTED |
| FR-004 | MUST | OpenAPI null agency; DATA_MODEL invariants | AC FR-004 | T-OWN-θ, T-OWN-CF-NULL | DOCUMENTED |
| FR-005 | MUST | PriorityScore schema; PointCard components | AC FR-005 | T-RANK-01 | DOCUMENTED |
| FR-006 | MUST | POST /rain/refresh; RainObservation | AC FR-006 | T-RAIN-01; E2E-02 | DOCUMENTED |
| FR-007 | MUST | POST /rain/scenario | AC FR-007 | T-RAIN-01; E2E-02 | DOCUMENTED |
| FR-008 | MUST | GET /points; UX QueueTable | AC FR-008 | T-UI-01; E2E-01 | DOCUMENTED |
| FR-009 | MUST | GET /points/{id}; UX PointCard | AC FR-009 | T-UI-01; E2E-01 | DOCUMENTED |
| FR-010 | MUST | ReadinessSignal; DESIGN_SYSTEM badge | AC FR-010 | T-UI-SYN; E2E-05 | DOCUMENTED |
| FR-011 | MUST | CONFLICT null hard stop | AC FR-011 | T-OWN-CF-NULL; E2E-03 | DOCUMENTED |
| FR-012 | MUST | ack/override/escalate OpenAPI; UX audit | AC FR-012 | T-HITL-UI; E2E-04 | DOCUMENTED |
| FR-013 | SHOULD | HIDE_SYNTHETIC flag | AC SHOULD | unit G=0 | DOCUMENTED |
| FR-014 | SHOULD | geometry optional | AC SHOULD | geo test | DOCUMENTED |
| FR-015 | MUST | LLD §22; tests/eval; optional EvalLink/Drawer | AC FR-015 | baseline_tournament; E2E-09 | DOCUMENTED |
| FR-016 | MUST | HLD + DEPLOYMENT | AC FR-016 | eligibility checklist | DOCUMENTED |
| FR-017 | MUST | LLD §2; E2E-06 | AC FR-017 | T-GOLD-PQ | DOCUMENTED |
| FR-018 | MUST | TEST_STRATEGY failure injection | AC FR-018 | subset suite | DOCUMENTED |
| FR-019 | MUST | provenance; LICENSE_AUDIT | AC FR-019 | T-PROV-01 | DOCUMENTED |
| FR-020 | MUST | UX queue-first; MapHUD secondary; DESIGN_SYSTEM | AC FR-020 | E2E-01; E2E-07 (skippable); UX review | DOCUMENTED |
| FR-021 | MUST | UX a11y | AC FR-021 | E2E-01; checklist | DOCUMENTED |
| FR-022 | COULD | rain source imd | — | config check | DOCUMENTED |
| FR-023 | MUST | counterfactuals OpenAPI | AC FR-023 | API + UI | DOCUMENTED |
| FR-024 | MUST | uncertainty bands LLD §16 | AC FR-024 | unit + UI | DOCUMENTED |
| FR-025 | SHOULD | Bedrock off; validation gate | AC SHOULD | §14A | DOCUMENTED |
| FR-026 | SHOULD | audit feedback row | AC SHOULD | schema | DOCUMENTED |
| FR-027 | MUST | PERFORMANCE; E2E-06 | AC FR-027 | T-KPI-TRIAGE | DOCUMENTED |

## Demo path (W1–W9 → FR / E2E)

Source moments: [DEMO_WOW.md](DEMO_WOW.md). Quality wiring: [TEST_STRATEGY.md](../quality/TEST_STRATEGY.md) Demo path.

| Wow | FR | E2E / notes |
|-----|----|-------------|
| W1 | FR-001, FR-008 | E2E-01 |
| W2 | FR-006, FR-007 | E2E-02 |
| W3 | FR-011, FR-017 | E2E-03, E2E-06 |
| W4 | FR-002, FR-009 | evidence + point-card |
| W5 | FR-023 | counterfactuals |
| W6 | FR-010 | E2E-05 |
| W7 | FR-012 | E2E-04 |
| W8 | FR-027 | T-KPI-TRIAGE |
| W9 | FR-016 | AWS beat / eligibility |

## NFR quick map

| NFR | Ops / design | Verify |
|-----|--------------|--------|
| NFR-001 / 002 | PERFORMANCE.md | timed tests |
| NFR-003 | DEPLOYMENT local offline | smoke without network |
| NFR-004 | SECURITY.md | gitignore + scan |
| NFR-005 | PERFORMANCE / DEPLOYMENT | cost check |
| NFR-006 | OBSERVABILITY.md | log sample |
| NFR-007 / 008 | UX §11–§12 + §23 Visual QA; DESIGN_SYSTEM extract | T-VIS-AUDIT (manual until UI) |
| NFR-009 | Makefile / README | clean-room clone |
| NFR-010 | LICENSE_AUDIT | contract |

## References

- [ACCEPTANCE_CRITERIA.md](../quality/ACCEPTANCE_CRITERIA.md)
- [openapi.yaml](../openapi.yaml)
- [LLD.md](../LLD.md) §10
