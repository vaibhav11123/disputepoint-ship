# Acceptance criteria

Given / When / Then for every **MUST** FR (and key SHOULD where HITL/demo depends). Format follows Gherkin API practice: one behavior per scenario; happy + error + edge where the FR needs it ([Gherkin API patterns](https://testquality.com/gherkin-api-testing-patterns-and-examples/)).

**SoT:** [PRD.md](../PRD.md). Do not invent new FR ids. Mapped Phase 6 test ids from [LLD.md](../LLD.md) §10 noted where present.

---

## FR-001 — Load ≥12 DisputePoints

```gherkin
Scenario: Queue loads curated points from seed
  Given fixture points validate against DisputePointSeed.schema.json
  And at least 12 seed points load
  And for each seed point with non-null lat and non-null lon, values lie within Delhi bbox
  When GET /points (after ingest)
  Then response 200 with items length >= 12
  And every item.id matches ^dp-[a-z0-9-]+$
  And runtime items conform to DisputePoint.schema.json (numeric lat/lon; evidence_ids minItems 1)
```

Null `lat`/`lon` on seed is allowed until human VERIFIED geocode ([DATA_PLAYBOOK.md](../build/DATA_PLAYBOOK.md)). Do not weaken runtime DisputePoint / OpenAPI to accept null geo.

## FR-002 — Evidence url + quote

```gherkin
Scenario: Each point has evidence with url and quote
  Given fixtures for all loaded points
  When evidence is validated
  Then each point has >= 1 Evidence with url and quote minLength 10
```

## FR-003 — Ownership states

```gherkin
Scenario: Ownership yields only allowed states
  Given OwnershipEngine runs on seed fixtures
  When ownership_state is computed
  Then each value is ASSIGNED or CONFLICT or UNKNOWN
```

## FR-004 — θ and CONFLICT null agency

```gherkin
Scenario: Below theta forces null agency
  Given ownership_confidence < 0.65
  When ownership result is published
  Then responsible_agency is null
  And escalate copy is eligible for UI

Scenario: CONFLICT forces null agency
  Given ownership_state is CONFLICT
  When the point card is returned
  Then responsible_agency is null
```

Maps: T-OWN-θ, T-OWN-CF-NULL.

## FR-005 — Priority factors include U

```gherkin
Scenario: Priority components expose U
  Given a ranked point
  When GET /points/{id}
  Then components includes R, S, C, Q, U, G
  And U means coordination_uncertainty not physical severity
```

## FR-006 — Live rain re-rank

```gherkin
Scenario: Open-Meteo rain updates R and re-ranks
  Given rain refresh succeeds from Open-Meteo
  When POST /rain/refresh then GET /points
  Then RainObservation.source is open-meteo or cache
  And priority_rank order may change vs dry baseline
```

Maps: T-RAIN-01.

## FR-007 — Scenario slider fallback

```gherkin
Scenario: Slider rain when live fails
  Given Open-Meteo is unavailable
  When POST /rain/scenario with precip_mm 40
  Then 200 RainObservation source scenario_slider is_synthetic true
  And UI may show Using scenario rain
```

## FR-008 — Queue by priority_rank

```gherkin
Scenario: Home queue is ranked
  Given points are scored
  When the officer opens the app
  Then home shows QueueTable ordered by priority_rank ascending
```

Maps: T-UI-01.

## FR-009 — Point card content

```gherkin
Scenario: Point card shows required blocks
  Given a selected point
  When the detail pane opens
  Then agency or blank-agency, confidence, evidence, actions, and advisory banner are visible
```

## FR-010 — SYNTHETIC badge

```gherkin
Scenario: Synthetic readiness is badged
  Given readiness.is_synthetic is true
  When the point card renders
  Then SYNTHETIC badge is visible
  And copy does not claim live SCADA
```

Maps: T-UI-SYN.

## FR-011 — CONFLICT multi-agency, no silent pick

```gherkin
Scenario: CONFLICT never silent-picks agency
  Given ownership_state CONFLICT with multiple agencies_claimed
  When GET /points/{id}
  Then responsible_agency is null
  And UI shows multiple agencies not a single preferred pick
```

Maps: T-OWN-CF-NULL.

## FR-012 — HITL + audit panel

```gherkin
Scenario: ACK only ASSIGNED+OPEN
  Given point ownership_state ASSIGNED and status OPEN
  When POST /points/{id}/ack with reviewer
  Then 200 and status ACKED
  And DecisionAuditPanel shows SYSTEM vs HUMAN

Scenario: ACK rejected on CONFLICT
  Given ownership_state CONFLICT and status OPEN
  When POST /points/{id}/ack
  Then 409 DP-409-ACK

Scenario: OVERRIDE from OPEN records audit
  Given status OPEN
  When POST /points/{id}/override with agency, reason, reviewer
  Then 200 with recommended_agency and human_selected_agency
  And audit panel is visible in UI
```

Maps: T-HITL-UI.

## FR-015 — Baseline tournament (no ML)

```gherkin
Scenario: Eval runs non-ML baselines
  Given seed fixtures and gold order template
  When baseline tournament runs
  Then methods include Random, Severity, Rain, Recurrence, Nearest, Static, Weighted
  And ML row is skipped for MVP
  And the markdown report at tests/eval/baseline_tournament.md remains the MUST deliverable

Scenario: Optional judges UI does not invent metrics
  Given GAP-EVAL-01 or GAP-EVAL-02 still open
  When the officer opens the eval footer link or drawer
  Then TBD or link-out to the markdown report is shown
  And no invented Spearman or top-k values appear
```

## FR-016 — AWS path documented

```gherkin
Scenario: Eligibility architecture path exists
  Given HLD Ship It or Build It path
  When submission materials are reviewed
  Then an AWS path is documented for the video plan
```

## FR-017 — Golden Purana Quila

```gherkin
Scenario: Golden PQ end-to-end
  Given dp-purana-quila fixtures and wet rain precip_mm 40
  When the officer follows the demo spine
  Then CONFLICT null agency, evidence, re-rank, and escalate/override path succeed
```

Maps: T-GOLD-PQ. Detail: [E2E_SCENARIOS.md](E2E_SCENARIOS.md).

## FR-018 — Failure-injection subset

```gherkin
Scenario: Failure suite subset runs
  Given Phase 6 Part I §24 failure list
  When the subset is executed
  Then Open-Meteo fail → slider path and CONFLICT null are covered
```

## FR-019 — Provenance fields

```gherkin
Scenario: Provenance on sources
  Given fixtures and LICENSE_AUDIT
  When contract validation runs
  Then provenance fields exist and sources are audit-listed
```

Maps: T-PROV-01.

## FR-020 — No map-only primary nav

```gherkin
Scenario: Home is queue not map
  Given a fresh session
  When the app loads
  Then primary navigation is the queue not a map-only shell

Scenario: Secondary MapHUD is optional
  Given fixtures with null lat/lon
  When the app loads
  Then the queue and point card are usable without a map
  And MapHUD is collapsed or empty

Scenario: MapHUD never replaces home
  Given at least one VERIFIED lat/lon
  When MapHUD is expanded
  Then selecting a queue row still drives the point card
  And the map remains secondary (not map-only primary nav)
```

## Cmd+K point jump (UX craft J1)

```gherkin
Scenario: Command palette selects a point
  Given the queue is loaded
  When the officer presses Meta+K or Control+K and chooses a point
  Then selectedPointId matches that point as if the row were clicked
  And no Billing or Settings route is offered
```

## FR-021 — Keyboard + states

```gherkin
Scenario: Focus and shell states
  Given the app is loaded
  When the officer tabs
  Then focus order is queue then card
  And loading, empty, and error states are non-blank
```

## FR-023 — Counterfactuals

```gherkin
Scenario: Counterfactual chips on card
  Given a scored point
  When GET /points/{id}
  Then counterfactuals array is present
  And UI shows Why chips with deltas
```

## FR-024 — Uncertainty bands

```gherkin
Scenario: UNCERTAIN is success
  Given ownership band UNCERTAIN
  When the card renders
  Then band chip shows UNCERTAIN
  And UI does not treat it as a hard error
```

## FR-027 — Time-to-triage KPI

```gherkin
Scenario: Demo triage under 30s
  Given warm local stack and fixtures
  When officer runs golden path to actionable triage
  Then elapsed time is under 30 seconds
```

Maps: T-KPI-TRIAGE.

---

## SHOULD (implement if in scope)

| FR | Minimal AC |
|----|------------|
| FR-013 | hide-synthetic zeros G; ranks change accordingly |
| FR-014 | Optional geometry validates for PQ-class when present |
| FR-025 | LLM path only after schema + quote⊆source; Bedrock off in MVP |
| FR-026 | Each HITL decision writes a feedback dataset row |

## NFR anchors (verify in ops + e2e)

| NFR | Check |
|-----|-------|
| NFR-001 | GET /points local &lt; 300 ms |
| NFR-002 | Rank 15 points &lt; 50 ms |
| NFR-003 | Offline shell + fixtures works without network |
| NFR-004 | No secrets in git |
| NFR-006 | JSON logs with request_id |
| NFR-007 / NFR-008 | UX checklist + contrast |
| NFR-009 | `make install` · `make test` · `make run` |
| NFR-010 | LICENSE_AUDIT complete |

## References

- [PRD.md](../PRD.md) FR text
- [LLD.md](../LLD.md) §10 test matrix
- [Gherkin API testing patterns](https://testquality.com/gherkin-api-testing-patterns-and-examples/)
