---
name: architecture
description: How DisputePoint pieces connect. Points at HLD and LLD. Does not replace Phase 6.
triggers:
  - "architecture"
  - "system design"
  - "ownership"
  - "priority"
  - "queue"
edges:
  - target: context/stack.md
    condition: when specific technology details are needed
  - target: context/decisions.md
    condition: when understanding why the architecture is structured this way
  - target: patterns/ownership-conflict-null.md
    condition: when implementing the CONFLICT null invariant
  - target: patterns/rain-ingest-open-meteo.md
    condition: when connecting rain into priority factor R
grounds_to: []
last_updated: 2026-10-10
mex:
  id: mx_01M4D8EPSN5YTVEHAN19B65A7S
  type: architecture
  status: promoted
  revision: 4
  title: architecture
  relations:
    - type: related_to
      target: mx_01M4D8EQ7VVRBD20W0YXVQSCQB
      note: when specific technology details are needed
    - type: related_to
      target: mx_01M4D8EQAVTWBYPZWZEJENVJ4Y
      note: when implementing the CONFLICT null invariant
    - type: related_to
      target: mx_01M4D8EQBNRR0BP5PYB5QR1DQV
      note: when connecting rain into priority factor R
---

# Architecture

Product source of truth is `docs/HLD.md` and `docs/LLD.md`. Phase 6 wins on conflict. No application modules exist yet. The flow below is the locked design, not running code.

## System Overview

```text
Fixtures (data/fixtures) + metro rain (Open-Meteo or scenario slider)
  → OwnershipEngine (θ=0.65; CONFLICT forces responsible_agency null)
  → PriorityEngine (weights R S C Q U G; U = coordination_uncertainty)
  → Read API (FastAPI locally, API Gateway + Lambda on AWS)
  → React queue-first list + point-card (not a flood heatmap)
  → HITL ACK / OVERRIDE / ESCALATE
  → DecisionAuditPanel writes an audit row the officer can see
```

Rain for the metro uses the Delhi-centroid Open-Meteo URL locked in `docs/LLD.md` Implementation locks and `docs/build/DATA_PLAYBOOK.md`. A failed fetch falls back to cache, then the scenario slider, with UI copy `Using scenario rain`.

<!-- mex:entity
id: mx_01M4D8EPRT2YBCA07QZ6EBKXRX
type: component
status: promoted
revision: 1
-->
## Key Components

- **OwnershipEngine** — scores agencies from evidence type weights (`W_NORM=2.0`). CONFLICT, or confidence under 0.65, yields `responsible_agency = null`. Depends on fixtures and the Evidence schema.
- **PriorityEngine** — ranks points with factors R, S, C, Q, U, G. U is coordination uncertainty. Depends on ownership output and the current rain observation.
- **Queue + point-card UI** — IBM Plex Sans and Mono. Officer acts from the card. ACK is allowed only for ASSIGNED + OPEN. Depends on the read API and UX locks in `docs/UX.md`.
- **HITL audit** — ACK, OVERRIDE, and ESCALATE persist a visible decision row. The model never silent-owns a point.

<!-- mex:entity
id: mx_01M4D8EPR005M4Y4W9FE819H7W
type: component
status: promoted
revision: 1
-->
## External Dependencies

- **Open-Meteo** — metro precipitation. Public HTTP. Attribute CC-BY 4.0. Not required to be up for the demo because the scenario slider is the fallback.
- **Fixtures and schemas** — `data/fixtures/` points 0.3.3 / evidence 0.3.6 and `docs/schemas/` plus `docs/openapi.yaml`. L0 audit bodies under `data/audit/sources/` stay gitignored.
- **AWS (Ship It, deployed 2026-10-10)** — EventBridge rain (15m) + evidence (1h) → Lambda `disputepoint-decision` → DynamoDB stamps + private evidence S3 (runtime SQLite snapshot) + public UI S3 website → API Gateway HTTPS; CloudWatch logs. Live Open-Meteo on cold start / invoke. Local `make run` remains the offline path.
- **IMD** — optional only when `IMD_API_KEY` is set. Demo must not block on it. Ship It leaves IMD as `key_required` (honest).

<!-- mex:entity
id: mx_01M4D8EPP1V5E6DADP4EM924PG
type: component
status: promoted
revision: 1
-->
## What Does NOT Exist Here

- No flood heatmap, ML ranking runtime, live SCADA, or DM-71 registry scrape.
- No Cognito / required CloudFront / WAF (MVP). HITL routes are demo-open with schema validation.
- MapHUD remains secondary; queue-first product. Geocode honesty rules still apply.
- No second product source of truth in `.mex/`. This file points at Phase 6.
