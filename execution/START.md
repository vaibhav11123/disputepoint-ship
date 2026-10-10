# START — DisputePoint execution router

Read this file first when building or continuing the app. Do **not** follow `.mex/ROUTER.md` into a full wiki walk on a build session. Phase 6 wins on product conflicts. Open only the anchors named on the current package.

**Current (2026-10-10):** Product trees exist; **G-AWS cleared** (Ship It live — [AWS_OPERATOR.md](../docs/operations/AWS_OPERATOR.md)). Next human gates: **G-VIS** (human slots) · **G-VIDEO** · **G-FORM**.

## Session order

1. This file, then `execution/status.json`, `execution/work-status.json`, `execution/GATES.md`, `execution/RESIDUALS.md`.
2. Last screen of `execution/PROGRESS.md` and `git log -15`.
3. If a human gate in GATES.md is open, **stop** and name the gate.
4. If the human has not declared the Oct 8 clock, or this folder is still the **research** repo (`disputepoint` not `disputepoint-ship`), do **not** create `backend/` or `frontend/` application trees. You may only maintain these execution docs. Product work belongs in `/Users/vaibhavsingh/disputepoint-ship` after `CLOCK_STARTED=1 ./scripts/scaffold_submission.sh` ([docs/operations/SUBMISSION_GIT.md](../docs/operations/SUBMISSION_GIT.md)).
5. Gate order in the **submission** tree: **G-CLOCK** (script) → human **G-PLAN** (`plan_gate_accepted: true`) → WP-00. Trust `execution/plan-check.yaml` (must be `status: PASS`) and derived `execution/waves.yaml`. Do **not** trust a hand-edited wave list.
6. Launch only packages in the current derived wave whose `work-status` is `READY`, up to `scheduler.yaml` `max_parallel_builders` (3), each in its own git worktree / branch `wp/<id>`.
7. Before editing, **re-read that one package** from `execution/work-packages.yaml` (exact test command in the body). Optionally mirror prose in `TASKS.md`.
8. Builder: implement inside `owned_paths` only → run the package test command → commit the integration unit (one or more coherent commits allowed) → update `PROGRESS.md` and `work-status.json`.
9. Reviewer (no write): required per `scheduler.yaml` — LOW self-check; MEDIUM+ reviewer; HIGH+ barrier; CRITICAL+ human gate. Every integration barrier needs a reviewer.
10. On PASS, merge that branch only. Barrier runs `make test` + contract checks. Failed barrier blocks dependents. `failure.retry: false` — wait for the human.
11. Stop at a human gate, failed barrier, STALE package, or when no package is READY. Do not one-shot the app in one worktree.

## Spec vs plan vs state

| Layer | Files |
|-------|--------|
| Truth | PHASE6, schemas, OpenAPI, TRACEABILITY, AC, LLD, UX |
| Plan | `work-packages.yaml`, `ownership.yaml`, `contract-ownership.yaml`, `scheduler.yaml` |
| Derived | `plan-check.yaml`, `waves.yaml`, `dependency-graph.yaml` |
| State | `status.json` (requirements), `work-status.json` (packages), `PROGRESS.md` |

A package can be `SUCCEEDED` while an FR stays `DOCUMENTED` (e.g. FR-001 numeric lat waiting on human geocodes).

## Stale

On contract or artifact version bump, mark consumers and dependents `STALE` (`scheduler.yaml` `stale.propagate`). Re-read package + re-check → READY. Package text change = replan → human plan gate again.

## Convergence

When nothing is READY/RUNNING: write `execution/convergence/CONVERGENCE.md` (and `gaps.yaml` if needed). Max **3** rounds. Then PASS or REMAINING_GAPS with human acceptance. Do not invent geocodes or gold order to close gaps.

## Contracts

Schemas and OpenAPI are `HUMAN_REVIEW`. If a contract is insufficient, write `execution/changes/CHANGE-REQ-*.md` and **stop**. Do not edit the contract.

## Read list per package

Copy of plan anchors — re-read only the current WP:

- **WP-00** LLD §3; SUBMISSION_GIT; AC NFR-009
- **WP-01** DisputePointSeed + DisputePoint schemas; DATA_MODEL seed-to-runtime
- **WP-02** LLD §5; AC FR-003, FR-004
- **WP-03** LLD §6, §19, §24; AC FR-005, FR-013, FR-023
- **WP-04** Evidence schema; AC FR-002, FR-019; DATA_PLAYBOOK; `data/fixtures/evidence.json`
- **WP-05** LLD §9; DATA_MODEL; fixtures; AC FR-001; RESIDUALS
- **WP-06** RainObservation schema; OpenAPI rain; AC FR-006, FR-007
- **WP-07** LLD §7, §11; OpenAPI read/rain routes
- **WP-08** LLD §20; OpenAPI HITL; AC FR-012, FR-026
- **WP-09** LLD §8; UX queue/card; DESIGN_SYSTEM; AC FR-008…021
- **WP-10** UX rain; AC FR-006, FR-007
- **WP-11** UX HITL; AC FR-012
- **WP-12** LLD §19; UX palette; DEMO_WOW; AC FR-023, FR-024; E2E-08, E2E-09
- **WP-13** E2E-01…E2E-06; AC FR-017
- **WP-14** LLD §22; baseline_tournament; GAP-EVAL-02; AC FR-015
- **WP-15** TEST_STRATEGY failures; PHASE6 §16A only; AC FR-016, FR-018
- **WP-16** PHASE6 §39; DEMO_WOW W1–W9; DEMO_REHEARSAL (G-VIDEO)

Do not open Phase 1–5, research trail (except geocode verify), archive, whole PHASE6, whole PRD/HLD, AGENT_CONSTITUTION, or `.mex/ROUTER.md` on a build session.
