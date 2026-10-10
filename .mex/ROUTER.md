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
  - target: patterns/ship-it-deploy.md
    condition: when redeploying or smoking Ship It AWS
last_updated: 2026-10-10
---

# Session Bootstrap

**Precedence:** root `AGENTS.md` hard stops and `docs/PHASE6.md` win over this router. On a build session, follow `execution/START.md` and open only the anchors named on the current package.

## Current Project State

**Working:**
- Frozen Phase 6 contract plus PRD, HLD, LLD, and UX extracts
- Schemas, OpenAPI, fixtures points 0.3.3 / evidence 0.3.6, and audit L1. Spec package and Data Ready PASS
- Submission tree: `clock_declared` true, `plan_gate_accepted` true; waves WP-00–WP-16 product code landed
- Local: `make install` · `make test` · `make run` (API `127.0.0.1:8000`, UI `127.0.0.1:5173`)
- **Ship It live (2026-10-10)** stack `disputepoint` / `ap-south-1`: API Gateway → Lambda → DynamoDB + S3 + EventBridge + CloudWatch; `DP_LIVE_FETCH=1`; Open-Meteo rain LIVE; evidence LIVE batch; CORS allowlist; `/docs` off
- Live URLs in [docs/build/AWS_DEMO_BEAT.md](../docs/build/AWS_DEMO_BEAT.md) and [docs/operations/AWS_OPERATOR.md](../docs/operations/AWS_OPERATOR.md)
- Redeploy: `make deploy` (profile `disputepoint`)

**Not yet done (submission / gates):**
- G-VIDEO (YouTube ≤3 min with AWS on screen) · G-VIS human slots · form write-up · public repo if still private
- IAM day-to-day user (CLI may still resolve as root) · post-video `sam delete` cleanup
- Gold order / tournament metric cells (optional)

**Known issues / residual:**
- **G-VIDEO** still open (YouTube + AWS on camera); Builder `_ARTICLE_URL_` after publish
- Phase 6 still cites some legacy research paths; prefer `docs/schemas/` and `docs/research/`
- G-AWS cleared 2026-10-10 — Ship It live

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
| Ship It deploy / smoke | `patterns/ship-it-deploy.md` |

## Behavioural Contract

1. **CONTEXT** — Root AGENTS, then Phase 6 or the current package anchors, then this routing table and any matching pattern.
2. **BUILD** — Smallest change inside the package `owned_paths`. Do not invent data or edit schemas.
3. **VERIFY** — Run the package test command. Use the Verify Checklist in `context/conventions.md`. Never claim an unverified pass.
4. **DEBUG** — Check `patterns/INDEX.md` for a debug path. Escalate RED, BLOCKED, or FAILED. `failure.retry` is false.
5. **GROW** — After meaningful work, update Current Project State and any stale `context/` or pattern file. Point at docs. Do not fork Phase 6. Bump `last_updated` on files you change.
