---
name: router
description: Session bootstrap and navigation hub. Secondary to root AGENTS.md, Phase 6, and execution/START.md on build sessions.
edges:
  - target: context/architecture.md
    condition: when working on system design or how components connect
  - target: context/stack.md
    condition: when working with specific technologies or making tech decisions
  - target: context/conventions.md
    condition: when writing or reviewing code
  - target: context/decisions.md
    condition: when making architectural choices or checking a lock
  - target: context/setup.md
    condition: when setting up the environment or running the project
  - target: patterns/INDEX.md
    condition: when starting a task — check for a matching pattern
  - target: patterns/implement-work-package.md
    condition: when implementing the current derived wave package
  - target: patterns/ownership-conflict-null.md
    condition: when implementing or testing ownership CONFLICT null
  - target: patterns/add-fixture-point.md
    condition: when curating points, evidence, or readiness fixtures
  - target: patterns/rain-ingest-open-meteo.md
    condition: when implementing rain ingest or the scenario slider
last_updated: 2026-10-08
---

# Session Bootstrap

**Precedence:** root `AGENTS.md` hard stops and `docs/PHASE6.md` win over this router. On a build session, follow `execution/START.md` and open only the anchors named on the current package.

## Current Project State

**Working:**
- Frozen Phase 6 contract plus PRD, HLD, LLD, and UX extracts
- Schemas, OpenAPI, fixtures v0.2, and audit L1. Spec package and Data Ready PASS (2026-10-06)
- Submission tree: `clock_declared` true, `plan_gate_accepted` true, `plan-check.yaml` status PASS
- Derived wave 0 is `WP-00` and its work-status is READY. Later packages stay BLOCKED on dependencies
- Makefile stubs and `.env.example` exist. Mex scaffold is under `.mex/` with Cursor selected

**Not yet built:**
- API and UI application trees (WP-00 onward)
- WP-01 through WP-16
- VERIFIED geocode promotes (latitude and longitude stay null; MapHUD skippable)
- Gold order file and tournament metric cells
- Live AWS deploy (G-AWS still open)

**Known issues:**
- `make install`, `make test`, `make run`, and `make deploy` exit 1 until app directories exist
- Code graph is thin: indexed files are docs and planning scripts, not product engines
- Plan-check warnings: WP-14 and WP-15 have no downstream consumers
- Phase 6 still cites some legacy research paths; prefer `docs/schemas/` and `docs/research/`

## Routing Table

Prefer product docs over rewriting the source of truth into this wiki.

| Task type | Load |
|-----------|------|
| Build or continue the app | `execution/START.md`, then the current package in `execution/work-packages.yaml` |
| Product contract / FRs | `docs/PHASE6.md`, then the matching extract |
| Understanding system shape | `context/architecture.md` → `docs/HLD.md` |
| Stack / deploy | `context/stack.md` |
| Writing or reviewing code | `context/conventions.md` |
| Design decision | `context/decisions.md` |
| Setup / run | `context/setup.md` |
| Recurring task | `patterns/INDEX.md` |
| Current work package | `patterns/implement-work-package.md` |
| Curate fixtures | `patterns/add-fixture-point.md` |
| Ownership / CONFLICT | `patterns/ownership-conflict-null.md` |
| Rain ingest | `patterns/rain-ingest-open-meteo.md` |

## Behavioural Contract

1. **CONTEXT** — Root AGENTS, then Phase 6 or the current package anchors, then this routing table and any matching pattern.
2. **BUILD** — Smallest change inside the package `owned_paths`. Do not invent data or edit schemas.
3. **VERIFY** — Run the package test command. Use the Verify Checklist in `context/conventions.md`. Never claim an unverified pass.
4. **DEBUG** — Check `patterns/INDEX.md` for a debug path. Escalate RED, BLOCKED, or FAILED. `failure.retry` is false.
5. **GROW** — After meaningful work, update Current Project State and any stale `context/` or pattern file. Point at docs. Do not fork Phase 6. Bump `last_updated` on files you change.
