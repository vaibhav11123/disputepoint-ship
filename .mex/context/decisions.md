---
name: decisions
description: Locked product and engineering decisions. Point at PRD section 12 and LLD locks.
triggers:
  - "decision"
  - "ADR"
  - "θ_assign"
  - "Ship It"
  - "Bedrock"
edges:
  - target: context/architecture.md
    condition: when a decision changes system flow
  - target: context/stack.md
    condition: when a decision changes the stack
  - target: patterns/implement-work-package.md
    condition: when a decision changes how the next package may be built
grounds_to: []
last_updated: 2026-10-10
---

# Decisions

Do not re-litigate the Phase 6 freeze. Status table: `docs/PRD.md` section 12. Constants: `docs/LLD.md` Implementation locks. Inventory: `docs/build/GAPS.md`.

When a decision changes, mark the old entry superseded and add the new one above it.

## Decision Log

<!-- mex:entity
id: mx_01M4D8EQ2XV1P92TVFQ35VG2QJ
type: decision
status: promoted
revision: 1
-->
### Accept the execution plan in the submission tree
**Date:** 2026-10-08
**Status:** Active
**Decision:** `plan_gate_accepted` is true after `execution/plan-check.yaml` reported PASS.
**Reasoning:** G-PLAN is the human gate in front of WP-00. The machine report passed every check. Warnings on WP-14 and WP-15 do not fail the gate.
**Alternatives considered:** Starting WP-00 before acceptance (rejected — `execution/GATES.md` blocks all product work on G-PLAN).
**Consequences:** Wave 0 (`WP-00`) may start. Later packages stay blocked on their dependencies. A package-text change requires a replan and a new plan gate.

<!-- mex:entity
id: mx_01M4D8EQ2187NTANMWG13K8WYC
type: decision
status: promoted
revision: 1
-->
### Build the judged app in this submission tree after the clock
**Date:** 2026-10-08
**Status:** Active
**Decision:** Product implementation happens in `disputepoint-ship` after G-CLOCK. `clock_declared` is true.
**Reasoning:** `docs/operations/SUBMISSION_GIT.md` requires a new git history that matches the event clock. The first commit on 2026-10-08 is the planning scaffold, not a pre-built app.
**Alternatives considered:** Copying a pre-clock app from the research repo (rejected — that is a product dump).
**Consequences:** The API and UI trees are created by WP-00 onward in this tree. Push still needs an explicit ask (G-PUSH).

<!-- mex:entity
id: mx_01M4D8EQ15QB2A51DWZF6TTVAJ
type: decision
status: promoted
revision: 1
-->
### Data Ready PASS with null geocodes
**Date:** 2026-10-06
**Status:** Active
**Decision:** Spec package and Data Ready are PASS. Fixture `lat` and `lon` stay null until a human verifies candidates.
**Reasoning:** Recorded in `docs/quality/SPEC_READINESS.md`. Evidence floor is met. MapHUD and E2E-07 stay skippable.
**Alternatives considered:** Inventing coordinates so the map can render (rejected — hard stop).
**Consequences:** FR-001 numeric latitude stays short of VERIFIED until G-GEO. Do not close that gap with guessed decimals.

<!-- mex:entity
id: mx_01M4D8EQ0BFR45644T9J18MDR4
type: decision
status: promoted
revision: 1
-->
### CONFLICT clears responsible_agency
**Date:** 2026-10-06
**Status:** Active
**Decision:** `ownership_state == CONFLICT` always sets `responsible_agency` to null.
**Reasoning:** Phase 6 and root `AGENTS.md`. A close score is a coordination dispute, not a license to pick MCD or PWD.
**Alternatives considered:** Assigning the top agency whenever confidence is at least 0.65 (rejected — CONFLICT overrides ASSIGNED).
**Consequences:** API, engine, and UI must refuse ACK on CONFLICT. Tests of the form T-OWN-CF-NULL stay mandatory.

<!-- mex:entity
id: mx_01M4D8EPZGT5GMGQPTX2HXG8NT
type: decision
status: promoted
revision: 1
-->
### No ML runtime in the MVP
**Date:** 2026-10-06
**Status:** Active
**Decision:** Phase 6 gate is no KEEP. Ranking is the explainable weight formula. Bedrock extraction stays off. Evidence is fixtures.
**Reasoning:** The point set is a small curated corpus. A model would invent ownership.
**Alternatives considered:** XGBoost or LLM ownership (rejected in the ML/LLM gate).
**Consequences:** Do not add a model dependency in WP-00 or later MVP packages.

<!-- mex:entity
id: mx_01M4D8EPYSV0FCR7WXHMC9XGDW
type: decision
status: promoted
revision: 1
-->
### Ship It live path chosen (G-AWS)
**Date:** 2026-10-10
**Status:** Active
**Decision:** Deploy path is **Ship It** (not Build It). Stack name `disputepoint` in `ap-south-1`. Live rain (`DP_LIVE_FETCH=1`) + evidence batch job; CORS allowlist to UI origin; Swagger off on Lambda.
**Reasoning:** Account + SAM green; FR-016 video needs a live API/UI URL. Local `make run` remains the offline degrade path.
**Alternatives considered:** SAM Local Build It only (deferred — Ship It succeeded).
**Consequences:** Demo W9 uses live API Gateway + S3 UI + `aws-arch.html`. Cleanup with `sam delete` after video. Operator pins live in `docs/operations/AWS_OPERATOR.md`.

### Queue-first product, Ship It preferred
**Date:** 2026-10-06
**Status:** Active — consequences partially superseded by **Ship It live path chosen (G-AWS)** (2026-10-10)
**Decision:** The product is a queue plus point-card. Preferred deploy is Ship It. θ_assign stays 0.65 until fixture gold exists. UI kit is CSS variables and React.
**Reasoning:** Frozen in Phase 6. A flood heatmap collides with existing dashboards and fails the kill tests.
**Alternatives considered:** Heatmap product, Carbon React, required SAM Build It (rejected or deferred). Build It remains a day-1 recon fallback, not the default.
**Consequences:** Originally: G-AWS still open. **Now:** Ship It is deployed; keep Build It only as failover narration if the live URL dies mid-demo.
