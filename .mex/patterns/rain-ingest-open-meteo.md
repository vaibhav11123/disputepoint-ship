---
name: rain-ingest-open-meteo
description: Wire metro rain with the locked Open-Meteo URL and the failure fallback.
triggers:
  - "rain"
  - "Open-Meteo"
  - "precip"
  - "scenario slider"
edges:
  - target: context/architecture.md
    condition: when connecting rain to priority factor R
  - target: context/setup.md
    condition: when documenting env or the poll schedule
grounds_to: []
last_updated: 2026-10-08
mex:
  id: mx_01M4D8EQBNRR0BP5PYB5QR1DQV
  type: pattern
  status: promoted
  revision: 3
  title: rain-ingest-open-meteo
  relations:
    - type: related_to
      target: mx_01M4D8EPSN5YTVEHAN19B65A7S
      note: when connecting rain to priority factor R
    - type: related_to
      target: mx_01M4D8EQ6YSX62XR6H6BB2PM14
      note: when documenting env or the poll schedule
---

# Rain ingest (Open-Meteo)

## Context

Locked URL and mapping are in `docs/LLD.md` Implementation locks and `docs/build/DATA_PLAYBOOK.md`. Env names are in `.env.example`. No rain client symbol exists in the code graph yet.

## Steps

1. GET the locked Open-Meteo forecast URL (Delhi centroid, `past_hours=6`, timezone `Asia/Kolkata`).
2. Sum `hourly.precipitation` into `precip_mm`. Set `window_hours=6`, `source=open-meteo`, `is_synthetic=false`.
3. On a non-200 response, use cache, then the scenario slider. UI copy is `Using scenario rain`.
4. `normalize_rain = min(1, max(0, precip_mm / 50))`.
5. Poll every 15 minutes once a scheduler exists. Demo pair is wet 40 and dry 0.

## Gotchas

- Do not block the demo on IMD.
- Do not invent per-point rain until geocodes exist. Metro rain is one observation.

## Verify

- [ ] Request URL matches the lock
- [ ] Failure path shows `Using scenario rain`
- [ ] Slider rows are synthetic. Live Open-Meteo rows are not

## Debug

If the queue looks dry during a demo outage, check the fallback copy before changing weights. A missing observation must become the scenario, not a silent zero treated as live.

## Update Scaffold

- [ ] Update `.mex/ROUTER.md` if live rain is now running
- [ ] Update `.mex/context/setup.md` if env names change
- [ ] Ground this pattern once a rain client function exists in the graph
