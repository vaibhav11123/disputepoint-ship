# Spec Readiness Gate

DisputePoint stand-in for Spec Kit **checklist + analyze** before **tasks / implement** ([Agentic SDD](https://github.github.io/spec-kit/reference/agentic-sdd.html)).

**Rule:** Do not open `execution/` WORK_PACKAGES or Phase 7 **implementation** agents until **both** Spec package (A–E) and **§F Data Ready** are PASS. Spec package PASS alone is not enough to start coding. Phase 6 + root [AGENTS.md](../../AGENTS.md) win on any conflict with this file or `.mex/`.

## When to run

After MUST/SHOULD yellow-medium artifacts exist; before any parallel implementation plan.

## Rubric

Score each row PASS / FAIL / N/A. Gate **PASS** only if every MUST row is PASS.

### A. IEEE / ISO 29148 qualities (spot-check MUST FRs)

| Quality | Check | Status |
|---------|-------|--------|
| Correct | AC and OpenAPI match Phase 6 / PRD intent | PASS |
| Unambiguous | No vague “works well”; Gherkin observables | PASS |
| Complete | Every MUST FR has AC + TRACEABILITY row | PASS |
| Consistent | PRD ↔ LLD routes ↔ OpenAPI ↔ schemas ↔ UX ↔ AC | PASS |
| Ranked | MUST / SHOULD / COULD respected | PASS |
| Verifiable | Each MUST AC has test layer or checklist | PASS |
| Modifiable | FR ids stable; changes via Phase 6 amendment note | PASS |
| Traceable | [TRACEABILITY.md](../build/TRACEABILITY.md) filled | PASS |

### B. Spec Kit–style consistency (analyze)

| Check | Status |
|-------|--------|
| Nine DecisionAPI routes only in OpenAPI (LLD §7) | PASS |
| OpenAPI bodies/errors for HITL + rain + honesty | PASS |
| `CONFLICT → responsible_agency null` in AC + DATA_MODEL + OpenAPI notes | PASS |
| UX queue-first + required copy + tokens in DESIGN_SYSTEM | PASS |
| No FR-* renamed to foreign id schemes | PASS |
| EVENT_CONTRACTS / Pact deferred explicitly | PASS |

### C. Anthropic initializer readiness

| Artifact | Present |
|----------|---------|
| Frozen requirements (PHASE6 + PRD) | YES |
| HLD / LLD | YES |
| schemas/ | YES |
| openapi.yaml (bodies, not stub) | YES |
| ACCEPTANCE_CRITERIA + E2E + TEST_STRATEGY | YES |
| Agent constitution (AGENTS + AGENT_CONSTITUTION) | YES |

Progress/handoff files belong in later `execution/` — not required for this gate.

### D. Definition of Ready

| Check | Status |
|-------|--------|
| Happy + error + edge for HITL and rain | PASS |
| Non-goals explicit (no heatmap, no invent DM-71, Bedrock off) | PASS |
| Exit criteria in TEST_STRATEGY | PASS |
| GAPS P0 items LOCKED or READY (not UNKNOWN blockers without escalate) | PASS* |

\*Data quotes/coords remain READY for Phase 7 fill — tracked in GAPS/DATA_PLAYBOOK, not missing from the spec package.

### E. Hard stops

| Stop | Status |
|------|--------|
| No invent DM-71 / SCADA / GPS as real | PASS |
| U ≠ physical severity | PASS |
| No ML runtime KEEP in MVP | PASS |
| Secrets / `.env` / live `runs/` never committed | PASS |

### F. Data Ready (required before Phase 7 implement)

| Check | Status |
|-------|--------|
| Fixture **points** validate against [DisputePointSeed.schema.json](../schemas/DisputePointSeed.schema.json) (not runtime DisputePoint) | PASS (seed schema + null-geo policy) |
| AC FR-001 matches null-until-VERIFIED seed policy | PASS |
| Runtime [DisputePoint.schema.json](../schemas/DisputePoint.schema.json) + OpenAPI stay strict (numeric lat/lon, `evidence_ids` ≥1 on API responses) | PASS |
| ≥3 demo-spine Evidence rows with quote⊆source (Purana Quila / Minto / Barapullah class) | **PASS** — spine quotes in `data/fixtures/evidence.json`; verified ⊆ L0 sources under `data/audit/sources/` (gitignored); see [AUDIT_MATRIX.md](../../data/audit/AUDIT_MATRIX.md) |
| Geocodes VERIFIED or MapHUD skippable with null lat/lon documented | **PASS** — lat/lon remain null (`null_accept`); MapHUD/E2E-07 skippable; candidates stay in [geocode-candidates.md](../research/geocode-candidates.md) until human VERIFIED |

**Data Ready overall:** **PASS** — evidence floor met; geo policy = accept-null MapHUD skip. COURT extracts `needs_review=true` until human validates.

## Verdict

| Field | Value |
|-------|-------|
| Date | 2026-10-06 |
| Assessor | Data Ready runbook execute (collect → audit → promote) |
| Spec package (A–E) | **PASS** |
| Data Ready (§F) | **PASS** |
| Phase 7 implement | **UNBLOCKED** |
| Residual | AMBER thin quotes on some non-spine points; geocodes still CANDIDATE (map optional); COURT needs_review |

Re-score A–E if Phase 6 or runtime contracts change. Re-score §F if evidence/geocodes regress.

If Spec package FAIL: fix cited gaps; re-run.
## Benchmarks footer (Exa-backed)

- [ISO/IEC/IEEE 29148](https://www.iso.org/standard/72089.html) — SRS qualities
- [IEEE 830](https://standards.ieee.org/ieee/830/1222/) — historical SRS (superseded)
- [GitHub Spec Kit — Agentic SDD](https://github.github.io/spec-kit/reference/agentic-sdd.html) — constitution→…→analyze→implement
- [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [RFC 9457 / Problem Details practice](https://swagger.io/blog/problem-details-rfc9457-api-error-handling/)
- [Pact FAQ — OpenAPI alone is not enough for multi-service](https://docs.pact.io/faq/convinceme) (deferred for monolith MVP)
