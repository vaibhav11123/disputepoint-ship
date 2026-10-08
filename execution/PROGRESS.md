# Progress log

Append-only. Sessions add dated entries. Do not rewrite history.

## Header

- Control plane created from Phase 7 execution plan.
- `plan-check.yaml` status: PASS (derived waves in `waves.yaml`).
- Product app code: **not started** (waits for G-PLAN + G-CLOCK).

## Log

### 2026-10-06 — control plane authored

- Authored: work-packages, ownership, contract-ownership, scheduler, START, TASKS, GATES, RESIDUALS, status, work-status.
- Derived: dependency-graph, plan-check, PLAN_CHECK, waves.
- AGENTS.md read order points at `execution/START.md`.
- Next human: accept PLAN_CHECK (G-PLAN); at Oct 8 declare clock (G-CLOCK) then WP-00 alone.

### 2026-10-08 — WP-00 toolchain

- G-PLAN accepted on main before this package (`plan-check.yaml` PASS).
- Branch `wp/WP-00`: Makefile install/test/run, root `pyproject.toml` and npm workspace, Vite shell, toolchain `create_app` until `backend/app/main.py` exists.
- `make install`, `make test` (no `tests/` yet), and `make run` (API `127.0.0.1:8000`, UI `127.0.0.1:5173`) passed.
- NFR-009 set to VERIFIED. WP-01 is READY. `make deploy` still exits 1 (G-AWS).

### 2026-10-08 — WP-01 models

- `DisputePointSeed` accepts fixture null lat/lon. `DisputePoint` rejects null lat/lon and empty `evidence_ids`.
- CONFLICT or UNKNOWN with a non-null `responsible_agency` fails validation.
- `pytest tests/test_models.py -q`: 9 passed. Fixture file was not given coordinates.
- FR-001 stays DOCUMENTED (numeric lat still waits on G-GEO).
- Same-session MEDIUM review: schema required fields and bbox match the JSON Schema; no schema file edited.
- WP-02 and WP-04 are READY.
