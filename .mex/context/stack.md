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
last_updated: 2026-10-10
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

- **Python + FastAPI + Mangum** — local uvicorn; Ship It Lambda ASGI adapter.
- **React + Vite** — queue and point-card UI. IBM Plex Sans and Mono.
- **Make** — `install` / `test` / `run` / `deploy` / `visual-qa`.
- **AWS SAM** — `infra/template.yaml` + `infra/stage_package.sh` + `infra/samconfig.toml`.
- **Node** — frontend build + mex CLI (Node 22 on this machine).

## Key Libraries

- **Open-Meteo HTTP** — rain ingest. Locked Delhi centroid URL.
- **JSON Schema + OpenAPI** — `docs/schemas/` and `docs/openapi.yaml`.
- **pytest** + Playwright (frontend e2e / visual-qa).
- **AWS Ship It** — API Gateway HTTP API, Lambda (python3.12 arm64), DynamoDB, S3 (UI website + private evidence), EventBridge schedules, CloudWatch. Build It / SAM Local remains failover only.

## What We Deliberately Do NOT Use

- No ML ranking runtime and no Bedrock extraction in the MVP. Evidence is fixtures until a later gate says otherwise.
- No Carbon React package. UI kit is CSS variables plus React (`docs/UX.md`).
- No SNS or CloudFront as a required path.
- No live DM-71 or SCADA client as a source of truth.

## Version Constraints

Python ≥3.11 (Lambda runtime 3.12). Mex on this machine is current `mex-agent`; Node for mex/frontend is 22.x. Prefer lockfiles in-repo over inventing versions.
