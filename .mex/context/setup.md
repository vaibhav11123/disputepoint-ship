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
last_updated: 2026-10-08
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
2. Plan gate is accepted. Next product step is WP-00 via `execution/START.md`.
3. Copy env only when a command needs it: `cp .env.example .env`
4. `make help` prints the stub targets. `make install` exits 1 until the API and UI trees exist.
5. After the scaffold is committed, `mex hub` serves the loopback Project Hub.

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
- `API_HOST`, `API_PORT`, `VITE_API_URL` (optional, commented) — local API and UI once Phase 7 exists.
- `AWS_PROFILE`, `AWS_REGION` (optional, commented) — only after G-CLOCK and G-AWS. Use `aws login` and roles. Do not put keys in `.env`.

<!-- mex:entity
id: mx_01M4D8EQ3QM94VNS9TGXCRQJJ6
type: guide
status: promoted
revision: 1
-->
## Common Commands

- `make help` — lists install, test, run, deploy and states that Phase 7 app code has not started
- `make install` — exits 1 with GAP-BOOT-01 until backend and frontend manifests exist
- `make test` — exits 1 until the backend tree exists, then pytest
- `make run` — exits 1 until the API and UI exist
- `mex check` — drift between this scaffold and the tree, no model call
- `mex doctor` — scaffold health
- `mex hub` — loopback Hub after `.mex/config.json` matches the committed HEAD

## Common Issues

**Make targets exit 1.** Expected. `Makefile` checks for the API and UI directories and stops. Create those trees only through the current work package, not by hand-dumping an app.

**`mex setup` skipped `.cursorrules`.** This repo already had `.cursorrules` (the DisputePoint Cursor anchor). Setup does not replace an existing tool file. Leave that anchor in place.
