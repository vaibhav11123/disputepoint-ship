---
name: ownership-conflict-null
description: Implement or test ownership so CONFLICT always yields responsible_agency null.
triggers:
  - "CONFLICT"
  - "ownership"
  - "θ_assign"
  - "T-OWN-CF-NULL"
edges:
  - target: context/conventions.md
    condition: when HITL ACK rules depend on ownership_state
  - target: context/decisions.md
    condition: when the θ_assign lock is questioned
  - target: context/architecture.md
    condition: when placing the rule in the engine flow
grounds_to: []
last_updated: 2026-10-08
mex:
  id: mx_01M4D8EQAVTWBYPZWZEJENVJ4Y
  type: pattern
  status: promoted
  revision: 3
  title: ownership-conflict-null
  relations:
    - type: related_to
      target: mx_01M4D8EPXXZMJTD6EKC17082AD
      note: when HITL ACK rules depend on ownership_state
    - type: related_to
      target: mx_01M4D8EPSN5YTVEHAN19B65A7S
      note: when placing the rule in the engine flow
---

# Ownership CONFLICT to null

## Context

`docs/LLD.md` OwnershipEngine and Implementation locks. Phase 6 FR-004 and test T-OWN-CF-NULL. No ownership function is in the code graph yet (`mex graph scope` returned no source-backed nodes).

## Steps

1. Score agencies with type weights. Confidence is `min(1, sum / W_NORM)` with `W_NORM=2.0`.
2. If the top two scores are within 0.1 and both are above 0.4, set CONFLICT and `responsible_agency` null.
3. Otherwise, if confidence is at least 0.65, set ASSIGNED. Else set UNKNOWN and null.
4. Keep a unit test that CONFLICT never assigns an agency even when the top score is at least θ.

## Gotchas

- CONFLICT overrides ASSIGNED. A high top score does not win.
- The UI must not offer ACK on CONFLICT or UNKNOWN. Those states use OVERRIDE or ESCALATE.

## Verify

- [ ] A T-OWN-CF-NULL style assertion exists
- [ ] The API cannot return an agency under CONFLICT
- [ ] The UI disables ACK for CONFLICT and UNKNOWN

## Debug

If an agency appears on a CONFLICT row, the bug is in the final assignment, not in the score weights. Force null after the CONFLICT branch and re-run the test.

## Update Scaffold

- [ ] Update `.mex/ROUTER.md` Current Project State if the engine now exists
- [ ] Update `.mex/context/architecture.md` only to point at the new module path
- [ ] Ground this pattern to the real function once the graph has a node id and fingerprint
