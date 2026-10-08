---
name: conventions
description: Coding and data conventions. Defer to Phase 6, LLD locks, and root AGENTS hard stops.
triggers:
  - "convention"
  - "style"
  - "ownership_state"
  - "synthetic"
  - "HITL"
edges:
  - target: context/architecture.md
    condition: when a convention depends on module boundaries
  - target: context/decisions.md
    condition: when a convention traces to a locked decision
  - target: patterns/ownership-conflict-null.md
    condition: when applying the CONFLICT null rule in code or tests
  - target: patterns/add-fixture-point.md
    condition: when naming points or labeling synthetic rows
grounds_to: []
last_updated: 2026-10-08
mex:
  id: mx_01M4D8EPXXZMJTD6EKC17082AD
  type: convention
  status: promoted
  revision: 4
  title: conventions
  relations:
    - type: related_to
      target: mx_01M4D8EPSN5YTVEHAN19B65A7S
      note: when a convention depends on module boundaries
    - type: related_to
      target: mx_01M4D8EQAVTWBYPZWZEJENVJ4Y
      note: when applying the CONFLICT null rule in code or tests
    - type: related_to
      target: mx_01M4D8EQ8PYAE240CFT14ES4HP
      note: when naming points or labeling synthetic rows
---

# Conventions

These rules are already enforced in schemas, fixtures, and the frozen contract. Application code must follow them when it lands.

<!-- mex:entity
id: mx_01M4D8EPX0DF90MWGBAA2G68NF
type: convention
status: promoted
revision: 1
-->
## Naming

- Point ids use the `dp-*` form from `docs/build/DATA_PLAYBOOK.md`.
- JSON fields are snake_case (`ownership_state`, `responsible_agency`, `is_synthetic`, `precip_mm`).
- Agency allowlist: `PWD`, `MCD`, `NDMC`, `IFC`, `DDA`, `DJB`, `RAILWAYS`, `CPWD`, `OTHER`, `UNKNOWN`.
- Work packages and branches: package id `WP-00` style, branch `wp/<id>` per `execution/START.md`.

<!-- mex:entity
id: mx_01M4D8EPW37HPJNY5MGMWYK4MD
type: convention
status: promoted
revision: 1
-->
## Structure

- Product behavior stays in `docs/PHASE6.md`, extracts, schemas, and OpenAPI. `.mex/` points at those files.
- Owned edits stay inside the current package `owned_paths` in `execution/work-packages.yaml`.
- Fixtures live in `data/fixtures/`. L0 source bodies stay under gitignored `data/audit/sources/`, `data/audit/rain/`, `data/audit/geo/`, and `data/audit/_work/`.
- Tests are named by the package body. API tests are pytest once the backend tree exists. Do not put a second test stack beside Make.

<!-- mex:entity
id: mx_01M4D8EPV8JGXPEYWSFZTXPJ7B
type: convention
status: promoted
revision: 1
-->
## Patterns

CONFLICT always clears the agency, even when the top score is above θ:

```text
# Correct
ownership_state = CONFLICT
responsible_agency = null

# Wrong
ownership_state = CONFLICT
responsible_agency = "MCD"
```

Synthetic readiness stays labeled and does not count as a live fact:

```text
# Correct
is_synthetic = true
readiness = UNKNOWN

# Wrong
is_synthetic = false
readiness = OPERATIONAL   # copied from a "planned SCADA" sentence
```

ACK is only for `ASSIGNED` + `OPEN`. CONFLICT and UNKNOWN use OVERRIDE or ESCALATE.

<!-- mex:entity
id: mx_01M4D8EPTEKDD38QT8WW59B95F
type: convention
status: promoted
revision: 1
-->
## Verify Checklist

Before presenting code or fixture edits:

- [ ] Schemas and OpenAPI were not silently edited
- [ ] CONFLICT still forces `responsible_agency = null`
- [ ] U was not treated as flood severity
- [ ] Synthetic rows stay `is_synthetic=true`; quotes are verbatim subsets of the source
- [ ] No invented lat, lon, DM-71 row, or SCADA reading
- [ ] The package test command was run, or the gap is stated as not tested
- [ ] Edits stayed inside the current package `owned_paths`
