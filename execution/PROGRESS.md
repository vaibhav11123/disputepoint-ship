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

### 2026-10-08 — WP-02 and WP-04, then G-OWNERSHIP

- OwnershipEngine: confidence is `min(1, top_weight_sum / 2.0)`. Below 0.65 the agency is null. A close pair (sums within 0.1 and both above 0.4) is CONFLICT with a null agency even when confidence is at least 0.65.
- Evidence loader validates fixture rows. Quote ⊆ source is checked against caller-supplied text. Gitignored L0 bodies were not opened.
- Package tests passed, then `make test` (18 passed). Schemas and OpenAPI were not edited.
- FR-002, FR-003, and FR-004 are VERIFIED. FR-001 stays DOCUMENTED pending G-GEO. FR-011 stays DOCUMENTED pending E2E-03. FR-019 stays DOCUMENTED until an audit-list check is named against committed sources.
- **G-OWNERSHIP is open.** WP-03 stays BLOCKED until a human reviews CONFLICT → `responsible_agency` null.

### 2026-10-08 — G-OWNERSHIP cleared

- Read-only review of `decide`: the CONFLICT branch returns `responsible_agency=None` and does not pass the top agency through.
- `DisputePoint` rejects CONFLICT or UNKNOWN when an agency is set.
- `pytest` on the conflict and null-agency cases: 6 passed.
- Gate closed. WP-03 is READY.
