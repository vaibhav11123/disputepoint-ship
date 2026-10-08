# Human gates

Agents stop here. Clearing a gate is a human action (or an explicit human-started read-only review). See [`START.md`](START.md).

| Id | When | What you do | Blocks |
|----|------|-------------|--------|
| G-PLAN | Before any app code | Accept [`PLAN_CHECK.md`](PLAN_CHECK.md) while [`plan-check.yaml`](plan-check.yaml) is PASS | All WP product work |
| G-CLOCK | Before WP-00 in submission repo | Declare Oct 8 clock; `git init` new folder; copy allow-list (no `.git`) | Product implementation |
| G-PUSH | Any push | Explicit ask; name research vs submission remote | Push |
| G-OWNERSHIP | After WP-02 SUCCEEDED | Review CONFLICT → `responsible_agency` null (read-only) | Dependents past ownership gate |
| G-HITL-API | After WP-08 | Review ACK/OVERRIDE/ESCALATE API + audit rows | WP-11 consumers of HITL |
| G-HITL-UI | After WP-11 | Review HITL UI + DecisionAuditPanel | WP-13 if HITL UI failing |
| G-GEO | Optional for map | Verify lat/lon; promote fixtures | E2E-07 / MapHUD; FR-001 numeric-lat VERIFIED |
| G-GOLD | Optional for eval metrics | Supply `gold_order.json` | FR-015 metric cells |
| G-QUOTES | As needed | Accept/reject `needs_review` evidence | Honest promotion of quotes |
| G-AWS | Before deploy / Ship vs Build | Choose §16A path; hold secrets/SAM/account | Live deploy |
| G-VIS | Before video | Run T-VIS-AUDIT (anti-slop, contrast) | NFR-007, NFR-008 VERIFIED |
| G-KPI | During WP-16 | Time Purana Quila path &lt;30s | FR-027 VERIFIED |
| G-VIDEO | Before submit | Record ≤3 min video (AWS visible); list AI tools | Submission |
| G-FORM | Submit | Public repo + form | Release |
| G-RED | On RED/BLOCKED/FAILED | Decide retry, fallback, or cut | That package |
| G-SCHEMA | Contract insufficient | Phase 6 amendment only | Affected STALE packages |
| G-CONVERGE | After max 3 converge rounds | Accept REMAINING_GAPS or PASS | Release |

## Risk → review (from scheduler.yaml)

| Risk | Required |
|------|----------|
| LOW | Builder self-verification |
| MEDIUM | Builder + reviewer |
| HIGH | Builder + reviewer + integration barrier |
| CRITICAL | Builder + reviewer + barrier + human gate |
| Any integration barrier | Independent reviewer |

## Not gates between every WP

After a gate is cleared, the orchestrator continues derived waves until the next gate or failure.
