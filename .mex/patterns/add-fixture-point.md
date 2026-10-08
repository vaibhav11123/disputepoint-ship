---
name: add-fixture-point
description: Curate one DisputePoint fixture from DATA_PLAYBOOK without inventing quotes or coordinates.
triggers:
  - "fixture"
  - "evidence"
  - "DATA_PLAYBOOK"
  - "Gate A"
edges:
  - target: context/conventions.md
    condition: when checking the agency allowlist and synthetic flags
  - target: context/architecture.md
    condition: when checking how fixtures feed ownership and priority
grounds_to: []
last_updated: 2026-10-08
mex:
  id: mx_01M4D8EQ8PYAE240CFT14ES4HP
  type: pattern
  status: promoted
  revision: 3
  title: add-fixture-point
  relations:
    - type: related_to
      target: mx_01M4D8EPXXZMJTD6EKC17082AD
      note: when checking the agency allowlist and synthetic flags
    - type: related_to
      target: mx_01M4D8EPSN5YTVEHAN19B65A7S
      note: when checking how fixtures feed ownership and priority
---

# Add fixture point

## Context

Load the recipe row in `docs/build/DATA_PLAYBOOK.md` for the `dp-*` id. Validate shape against `docs/schemas/`. Root AGENTS hard stops apply. The code graph has no fixture-loader symbol yet, so read the recipe and schema directly.

## Steps

1. Open the recipe row and fetch each cited source URL.
2. Copy a quote of at least 10 characters that appears verbatim in the source.
3. Fill evidence with type, an allowlisted agency or null, `retrieved_at`, and `is_synthetic`.
4. Leave `lat` and `lon` null until a human geocode. Do not invent decimals.
5. Readiness stays UNKNOWN with `is_synthetic=true` unless a public non-SCADA fact is copied.
6. Validate against the seed schema when a validator exists.

## Gotchas

- A DM-71 bulk mention is not a point.
- A sentence that SCADA or CCTV is "planned" is not live readiness.
- CONFLICT evidence pairs still force a null agency at runtime.

## Verify

- [ ] quote ⊆ source
- [ ] agency is allowlisted or null
- [ ] no invented coordinates
- [ ] synthetic rows are labeled

## Debug

If a quote fails the subset check, delete the paraphrase and copy from the source again. Do not relax the schema.

## Update Scaffold

- [ ] Update `.mex/ROUTER.md` Current Project State if fixture readiness changed
- [ ] Update any `.mex/context/` file that is now stale
- [ ] If this task grew a new gotcha, add it here
