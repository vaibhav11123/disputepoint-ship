---
name: stack
description: Planned DisputePoint MVP stack. Application code is not in the tree yet.
triggers:
  - "stack"
  - "python"
  - "react"
  - "aws"
  - "fastapi"
edges:
  - target: context/architecture.md
    condition: when connecting a library choice to the request flow
  - target: context/decisions.md
    condition: when revisiting Ship It, Build It, or Bedrock
  - target: context/setup.md
    condition: when checking which commands exist today
grounds_to: []
last_updated: 2026-10-08
mex:
  id: mx_01M4D8EQ7VVRBD20W0YXVQSCQB
  type: architecture
  status: promoted
  revision: 3
  title: stack
  relations:
    - type: related_to
      target: mx_01M4D8EPSN5YTVEHAN19B65A7S
      note: when connecting a library choice to the request flow
    - type: related_to
      target: mx_01M4D8EQ6YSX62XR6H6BB2PM14
      note: when checking which commands exist today
---

# Stack

Details live in `docs/HLD.md` and the AWS notes under `docs/research/` and `docs/operations/AWS_OPERATOR.md`. Versions below are the locked direction. Pin exact app versions when WP-00 creates the projects.

## Core Technologies

- **Python + FastAPI** — local read API and engines. Not present until WP-00.
- **React + Vite** — queue and point-card UI. Styling is CSS variables, IBM Plex Sans and Mono.
- **Make** — root `Makefile` is the operator entry. Targets are stubs.
- **Node** — mex CLI only (this machine has Node 22). Not the product runtime.

## Key Libraries

- **Open-Meteo HTTP** — rain ingest. Use the locked URL. Do not add a second weather client for the demo.
- **JSON Schema + OpenAPI** — `docs/schemas/` and `docs/openapi.yaml` are the contracts. Do not introduce a parallel model layer that drifts from them.
- **pytest** — API tests once the backend tree exists. The Makefile already names pytest as the intended runner.
- **AWS services listed in architecture** — Ship It is the preferred deploy. SAM is the Build It fallback after day-1 recon, not the default.

## What We Deliberately Do NOT Use

- No ML ranking runtime and no Bedrock extraction in the MVP. Evidence is fixtures until a later gate says otherwise.
- No Carbon React package. UI kit is CSS variables plus React (`docs/UX.md`).
- No SNS or CloudFront as a required path.
- No live DM-71 or SCADA client as a source of truth.

## Version Constraints

Application language and framework versions are not pinned in this tree yet. Do not invent them. Mex on this machine is `mex-agent` 0.8.0. Node for mex is 22.17.0.
