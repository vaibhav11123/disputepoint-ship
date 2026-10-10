# AGENTS.md — DisputePoint

Agent README for this repository. Format follows [agents.md](https://agents.md/). Keep this file short. Full engineering rules live in [docs/agent/AGENT_CONSTITUTION.md](docs/agent/AGENT_CONSTITUTION.md). Docs map: [docs/README.md](docs/README.md).

## Project overview

**DisputePoint Response Intelligence** — for a DM coordination cell officer, when monsoon rain threatens multi-agency disputed waterlogging points in Delhi, decide which point needs action first, which agency should act (or UNCERTAIN), and why.

- Track: Heat and Water ([Environmental Hacks](https://www.wemakedevs.org/aws/env))
- Product shape: queue-first + point-card. **Not** a flood heatmap.
- Contract: [docs/PHASE6.md](docs/PHASE6.md) is frozen. Extracts: [docs/PRD.md](docs/PRD.md), [docs/HLD.md](docs/HLD.md), [docs/LLD.md](docs/LLD.md), [docs/UX.md](docs/UX.md).

## Read order (before coding)

1. **Build or continue the app:** read [execution/START.md](execution/START.md), then do what it says. Trust [execution/plan-check.yaml](execution/plan-check.yaml) and derived [execution/waves.yaml](execution/waves.yaml). Open only the sections the current work package names. Phase 6 still wins on product conflicts.
2. [docs/PHASE6.md](docs/PHASE6.md) — frozen contract (open only when a package or conflict requires it; do not reload the whole file every session).
3. Extract for the layer you change: PRD / HLD / LLD / UX. If an extract disagrees with Phase 6, **follow Phase 6**.
4. [docs/schemas/](docs/schemas/) + [docs/openapi.yaml](docs/openapi.yaml) — do not silently change.
5. [docs/quality/SPEC_READINESS.md](docs/quality/SPEC_READINESS.md) — Spec + **Data Ready PASS**. Entry product implementation: after Oct 8 clock in the submission repo — [SUBMISSION_GIT](docs/operations/SUBMISSION_GIT.md).
6. Quality pack as needed: [docs/quality/ACCEPTANCE_CRITERIA.md](docs/quality/ACCEPTANCE_CRITERIA.md), [TEST_STRATEGY.md](docs/quality/TEST_STRATEGY.md), [E2E_SCENARIOS.md](docs/quality/E2E_SCENARIOS.md); traceability: [docs/build/TRACEABILITY.md](docs/build/TRACEABILITY.md).
7. [docs/agent/HOWTO_REUSE.md](docs/agent/HOWTO_REUSE.md) — process boundaries.
8. Fixtures: [`data/fixtures/`](data/fixtures/) points **0.3.3** / evidence **0.3.4** + audit L1 [`data/audit/`](data/audit/). Recipes: [docs/build/DATA_PLAYBOOK.md](docs/build/DATA_PLAYBOOK.md). Gaps: [docs/build/GAPS.md](docs/build/GAPS.md). Geocode candidates: [docs/research/geocode-candidates.md](docs/research/geocode-candidates.md) — verify before promote; COURT `needs_review` remains until human validates. Never commit L0 under `data/audit/sources/`.
9. For multi-file, architectural, or debugging work: [docs/agent/AGENT_CONSTITUTION.md](docs/agent/AGENT_CONSTITUTION.md).

Prefer the smallest change that satisfies tests and FRs. Before the Oct 8 clock: planning docs in this tree only — no entry `backend/` / `frontend/` dump.

## Hard stops

- Do not reopen opportunity discovery or replace DisputePoint with a flood heatmap.
- Do not invent DM-71 / SCADA / GPS or mark synthetic as real.
- `ownership_state == CONFLICT` → `responsible_agency = null` always.
- U = coordination_uncertainty, not physical severity.
- No ML runtime in MVP (Phase 6 gate = no KEEP).
- LLM claims need schema + quote⊆source validation; never silent ownership.
- Do not expand scope to bypass blockers — escalate (GREEN / YELLOW / RED / BLOCKED).
- Never commit secrets, `.env`, or live `runs/`.
- Never commit L0 audit bodies under `data/audit/sources/` (or rain/geo/_work).
- **Git / submission:** follow [docs/operations/SUBMISSION_GIT.md](docs/operations/SUBMISSION_GIT.md) and [WeMakeDevs rules](https://www.wemakedevs.org/aws/rules). Before the clock: **planning/practice only** in this tree. Do **not** build the judged DisputePoint app for dump-into-day-1; do **not** create/push the public entry repo until the human says Oct 8 started. Never push unless asked; history must match event dates.

**Precedence:** Phase 6 + these hard stops win over `.mex/` wiki or Cursor anchors if they disagree.

## Hackathon kickoff

Two repos — details: [docs/operations/SUBMISSION_GIT.md](docs/operations/SUBMISSION_GIT.md).

1. **This folder** = planning SoT. Pre-clock: docs, schemas, fixtures, audit L1 — not the entry product implementation.
2. **At clock (Oct 8):** new empty git + new GitHub repo; **copy planning artifacts** (not old `.git`, not a pre-built app); implement product **in-event**; push; make public for submit.
3. Copy allow-list: Phase 6 + extracts, schemas/OpenAPI, fixtures, audit L1 (matrix/manifest/GAP_ASK/README), LICENSE / AGENTS / Makefile / `.env.example`.
4. Never upload: `.env`, keys, `runs/`, L0 source bodies, invented gov data marked real, pre-clock product dump.

## UI

- Queue-first + point-card.
- IBM Plex Sans + Mono.
- Pass anti-slop checklist in Phase 6 Part II-B / [docs/UX.md](docs/UX.md).
- HITL: ACK / OVERRIDE / ESCALATE + visible DecisionAuditPanel.

## Setup and verify

Use this repository’s commands when they exist. Do not invent a validation stack.

When present, prefer:

- `make install` · `make test` · `make run` · `make deploy` (optional)
- Backend: `pytest` (and project lint/type tools if configured)
- Frontend: package-script lint / test / build if configured

Until those land, document every command you actually ran. Never claim tests, builds, or live APIs passed unless you ran them.

After meaningful changes: run targeted tests; do not bypass failures; update docs if contracts change (version note).

## Engineering priorities (condensed)

In order: correctness → existing project requirements → safety and reliability → tests and verification → maintainability → simplicity → performance → elegance.

- A small correct change beats a large clever change.
- Prefer extending existing architecture; do not invent frameworks for résumé reasons.
- Stay in requested scope; record unrelated issues, do not silently expand.
- Never silently convert errors into success.
- Never fake verification. Distinguish **verified** from reasoned / not tested.
- Report using the completion template in [docs/agent/AGENT_CONSTITUTION.md](docs/agent/AGENT_CONSTITUTION.md) § B.31.

## Full operating system

[docs/agent/AGENT_CONSTITUTION.md](docs/agent/AGENT_CONSTITUTION.md) — Mission through Definition of Done (B.1–B.32). Read it before non-trivial work. It is not a second product source of truth; Phase 6 still wins on product conflicts.

## Secondary memory (mex)

After hard stops above: [`.mex/ROUTER.md`](.mex/ROUTER.md) for living wiki. Phase 6 + this file still win on conflict.
