---
name: setup
description: Dev environment setup and commands for the submission tree.
triggers:
  - "setup"
  - "install"
  - "environment"
  - "getting started"
  - "how do I run"
  - "local development"
edges:
  - target: context/stack.md
    condition: when specific technology versions are needed
  - target: context/architecture.md
    condition: when checking which processes should actually be running
  - target: patterns/implement-work-package.md
    condition: when setup is done and the next step is WP-00
grounds_to: []
last_updated: 2026-10-10
mex:
  id: mx_01M4D8EQ6YSX62XR6H6BB2PM14
  type: guide
  status: promoted
  revision: 4
  title: setup
  relations:
    - type: related_to
      target: mx_01M4D8EQ7VVRBD20W0YXVQSCQB
      note: when specific technology versions are needed
    - type: related_to
      target: mx_01M4D8EPSN5YTVEHAN19B65A7S
      note: when checking which processes should actually be running
    - type: related_to
      target: mx_01M4D8EQ9Y88HC70TFA0226418
      note: when setup is done and the next step is WP-00
---

# Setup

<!-- mex:entity
id: mx_01M4D8EQ65QNB4QD28VA01BY71
type: guide
status: promoted
revision: 1
-->
## Prerequisites

- This git tree: `/Users/vaibhavsingh/disputepoint-ship`
- Node 22 and global `mex` (`mex-agent` 0.8.0) for the scaffold
- Python, pytest, and a frontend package manager arrive with WP-00. They are not installed by the current Makefile

<!-- mex:entity
id: mx_01M4D8EQ5B0A5EMSN5MTKXK7Z0
type: guide
status: promoted
revision: 1
-->
## First-time Setup

1. Use this submission tree only. Clock is already declared (`execution/work-status.json`).
2. Plan gate is accepted. Product trees exist under `backend/` and `frontend/`.
3. Copy env only when a command needs it: `cp .env.example .env`
4. `make install` · `make test` · `make run` for local. Ship It: `aws login --profile disputepoint` then `make deploy`.
5. Live URLs and smoke notes: `docs/operations/AWS_OPERATOR.md` · `docs/build/AWS_DEMO_BEAT.md`.

<!-- mex:entity
id: mx_01M4D8EQ4G5F254YW1Q91F149G
type: guide
status: promoted
revision: 1
-->
## Environment Variables

From `.env.example`. No secret values belong in git.

- `IMD_API_KEY` (optional) — IMD path. Demo must not require it.
- `OPEN_METEO_BASE` (optional) — defaults to `https://api.open-meteo.com` in the example file.
- `RAIN_POLL_MINUTES` (optional) — example sets 15. Locked metro query is lat `28.6139`, lon `77.2090`, `past_hours=6`, timezone `Asia/Kolkata`.
- `API_HOST`, `API_PORT`, `VITE_API_URL` — local Vite proxy vs Ship It bake (`VITE_API_URL` + `VITE_AWS_MODE=ship` on `make deploy`).
- `DP_LIVE_FETCH`, `DP_SOURCE_POLLING` — live rain/evidence; Ship It Lambda sets these to `1`.
- `AWS_PROFILE=disputepoint`, `AWS_REGION=ap-south-1` — use `aws login`; never put keys in `.env`.

<!-- mex:entity
id: mx_01M4D8EQ3QM94VNS9TGXCRQJJ6
type: guide
status: promoted
revision: 1
-->
## Common Commands

- `make help` — install, test, run, deploy, visual-qa
- `make install` · `make test` · `make run` — local golden path
- `make deploy` — stage SAM package, `sam build`/`sam deploy`, build UI with API URL, sync S3, smoke `/health` + `/points`
- `mex check` — scaffold drift · `mex graph refresh` after large code moves
- `mex doctor` · `mex hub`

## Common Issues

**CLI session expired.** `aws login --profile disputepoint` (Chrome authorize + paste code if `--remote`).

**UI shows LIVE RAINFALL UNAVAILABLE.** Ship It must have `DP_LIVE_FETCH=1` and rain bootstrap; see `backend/app/lambda_handler.py`.

**`mex setup` skipped `.cursorrules`.** Leave the DisputePoint Cursor anchor in place.
