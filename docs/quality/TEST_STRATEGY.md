# Test strategy

How DisputePoint proves FRs without inventing a second product. Exit criteria tie to [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) and LLD §10 mapped ids.

## Pyramid (MVP)

```text
        /\
       /E2E\      Playwright (or project e2e) — demo spine, HITL UI
      /------\
     / integ  \   API + rain refresh/scenario + OpenAPI shape checks
    /----------\
   /   unit     \ OwnershipEngine, PriorityEngine, schema validate
  /--------------\
```

| Layer | Tools (when Phase 7 lands) | Owns |
|-------|----------------------------|------|
| Unit | `pytest` | θ, CONFLICT→null, normalize_rain, recurrence, priority math |
| Integration | `pytest` + httpx/TestClient | Nine DecisionAPI routes, DP-* errors |
| Contract | schema validators + OpenAPI examples | Evidence/DisputePoint/Rain/PriorityScore |
| E2E | Frontend e2e runner | Queue, card, rain slider, ACK/OVERRIDE/ESCALATE, SYNTHETIC |
| Eval | `tests/eval/` | Baseline tournament markdown MUST (FR-015); optional UI link/drawer must not invent metrics; no ML KEEP |
| Checklist | Manual (`T-VIS-AUDIT`) | UX §12 anti-slop + §23 Visual QA; NFR-007/008 |

**Pact / CDCT:** deferred — single FastAPI + Vite monolith ([DATA_MODEL.md](../contracts/DATA_MODEL.md)).

## Mapped Phase 6 tests (do not rename)

| Test ID | FR | Layer |
|---------|----|-------|
| T-DATA-01 | FR-001 | unit / fixture |
| T-OWN-θ | FR-004 | unit |
| T-OWN-CF-NULL | FR-004 / FR-011 | unit + e2e |
| T-RANK-01 | FR-005 | unit |
| T-RAIN-01 | FR-006 / FR-007 | integration |
| T-UI-01 | FR-008 / FR-009 | e2e |
| T-UI-SYN | FR-010 | e2e |
| T-HITL-UI | FR-012 | e2e |
| T-GOLD-PQ | FR-017 | e2e |
| T-PROV-01 | FR-019 | contract |
| T-KPI-TRIAGE | FR-027 | demo timing |
| T-VIS-AUDIT | NFR-007 / NFR-008 | UX §12 + §23 (manual) |

Unmapped FRs: acceptance = PRD/AC text; do not invent new test ids (LLD §10).

## T-VIS-AUDIT (visual / anti-slop)

**Procedure SoT:** [UX.md](../UX.md) §12 (checklist) + §23 (8-frame Visual QA board).  
**When:** Manual before demo video / Design review. **Blocked until frontend exists** — document as pending, do not claim pass.  
**Fail if:** banned chrome (§10), missing skip link / labels, color-only state chips, motion ignoring `prefers-reduced-motion`, HITL controls &lt;44px, map-as-home.  
**Not visual SoT:** E2E-01…09 assert behavior (queue≠map, CONFLICT null, etc.), not pixels.  
**Phase 7 SHOULD:** five Playwright golden frames (cold queue, PQ CONFLICT, rain slider, HITL audit, wet re-rank) — not Percy/Chromatic for MVP.

## Exit criteria (Spec Readiness → implement)

1. Every MUST FR has ≥1 AC scenario and a TRACEABILITY row.
2. Unit: CONFLICT→null and θ gates green.
3. Integration: OpenAPI paths respond with documented status codes (happy + DP-409 / DP-404 / DP-503).
4. E2E: scenarios E2E-01…E2E-05 in [E2E_SCENARIOS.md](E2E_SCENARIOS.md) pass on fixture spine. E2E-07 (MapHUD) skippable without VERIFIED coords; E2E-08/09 when UI aids land.
5. Eval: baseline tournament markdown filled (ML skipped). Judges UI optional — link-out OK while TBD.
6. No silent conversion of errors to success; no inventing fixture quotes.

## Failure injection (FR-018 subset)

| Injection | Expect |
|-----------|--------|
| Open-Meteo timeout | DP-503 or cache; slider available |
| Unknown point id | DP-404-POINT |
| ACK on CONFLICT | DP-409-ACK |
| Bad scenario body | DP-400-SCHEMA |

## Commands

Prefer when present: `make test`. Until then document every command actually run. Never claim green without running.

## Demo path

Video beats W1–W9 and optional aids are owned by [DEMO_WOW.md](../build/DEMO_WOW.md). Quality mapping:

| Demo | FR / E2E / test |
|------|-----------------|
| W1–W9 story | See [TRACEABILITY.md](../build/TRACEABILITY.md) Demo path table |
| Rain re-rank (W2) | E2E-02; T-RAIN-01 |
| CONFLICT null (W3) | E2E-03; E2E-06; T-OWN-CF-NULL; T-GOLD-PQ |
| HITL audit (W7) | E2E-04; T-HITL-UI |
| SYNTHETIC honesty (W6) | E2E-05; T-UI-SYN |
| MapHUD (M1) | E2E-07 (skippable without VERIFIED geo) |
| Anti-slop / Visual QA | T-VIS-AUDIT (UX §12 + §23) |

## References

- [LLD.md](../LLD.md) §10, §22
- [DEMO_WOW.md](../build/DEMO_WOW.md)
- [tests/eval/baseline_tournament.md](../../tests/eval/baseline_tournament.md)
- Spec Kit: tasks/analyze only after checklist readiness ([Agentic SDD](https://github.github.io/spec-kit/reference/agentic-sdd.html))
