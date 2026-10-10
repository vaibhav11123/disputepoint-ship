---
name: implement-work-package
description: Implement one READY package from the current derived wave, inside its owned paths.
triggers:
  - "work package"
  - "WP-00"
  - "wave"
  - "START.md"
edges:
  - target: context/conventions.md
    condition: when checking owned paths and the verify list
  - target: context/setup.md
    condition: when a package adds install or run commands
  - target: context/decisions.md
    condition: when a package would change a locked decision
grounds_to: []
last_updated: 2026-10-08
mex:
  id: mx_01M4D8EQ9Y88HC70TFA0226418
  type: pattern
  status: promoted
  revision: 3
  title: implement-work-package
  relations:
    - type: related_to
      target: mx_01M4D8EPXXZMJTD6EKC17082AD
      note: when checking owned paths and the verify list
    - type: related_to
      target: mx_01M4D8EQ6YSX62XR6H6BB2PM14
      note: when a package adds install or run commands
---

# Implement one work package

## Context

`execution/START.md` is the build router. Trust `execution/plan-check.yaml` (PASS) and derived `execution/waves.yaml`. Current gate state is in `execution/work-status.json`: clock declared, plan gate accepted, WP-00 READY.

## Steps

1. Re-read `execution/status.json`, `execution/work-status.json`, `execution/GATES.md`, and `execution/RESIDUALS.md`.
2. Launch only READY packages in the current derived wave, up to `max_parallel_builders` (3), each on branch `wp/<id>`.
3. Re-read that one package in `execution/work-packages.yaml`, including its test command.
4. Edit only `owned_paths`. Run the package test command.
5. Update `execution/PROGRESS.md` and `execution/work-status.json` after the integration unit.
6. Stop at the next human gate, a failed barrier, a STALE package, or when nothing is READY.

## Gotchas

- Do not create the API or UI trees outside the package that owns them.
- Do not hand-edit the wave list. A package-text change means replan and a new human plan gate.
- `failure.retry` is false. Wait for the human on RED, BLOCKED, or FAILED.
- Schemas and OpenAPI are HUMAN_REVIEW. An insufficient contract becomes `execution/changes/CHANGE-REQ-*.md`, then stop.

## Verify

- [ ] Package was READY in the current derived wave
- [ ] Diff stays inside `owned_paths`
- [ ] The package test command was run
- [ ] No schema or OpenAPI edit slipped in

## Debug

If Make fails, read the Makefile message. `make deploy` needs a live `aws login --profile disputepoint`. If a dependent package is BLOCKED, finish its dependency first. Do not mark it READY by hand.

## Update Scaffold

- [ ] Update `.mex/ROUTER.md` Current Project State when a package succeeds
- [ ] Update `.mex/context/setup.md` when real install, test, or run commands land
- [ ] Add a tighter pattern only after a package teaches a gotcha this file does not cover
