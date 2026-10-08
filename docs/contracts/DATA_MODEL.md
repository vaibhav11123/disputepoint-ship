# Data model index

Machine-readable contracts and where truth lives. Values and field rules stay in JSON Schema / OpenAPI — this file is the **index** (pointer pattern: document meaning here, do not duplicate full schemas).

**SoT precedence:** [PHASE6.md](../PHASE6.md) → [schemas/](../schemas/) → [openapi.yaml](../openapi.yaml) → [LLD.md](../LLD.md).

## Entities

| Entity | Schema | OpenAPI component | Persistence (local / AWS) | Notes |
|--------|--------|-------------------|---------------------------|-------|
| DisputePointSeed | [DisputePointSeed.schema.json](../schemas/DisputePointSeed.schema.json) | — (fixture only) | `data/fixtures/points.json` | Null lat/lon OK; `evidence_ids` may be empty |
| DisputePoint | [DisputePoint.schema.json](../schemas/DisputePoint.schema.json) | `DisputePointPublic`, `PointCardResponse` | SQLite `points` / DynamoDB `POINT#id` META | Runtime API; strict numeric lat/lon; `evidence_ids` ≥1 |
| Evidence | [Evidence.schema.json](../schemas/Evidence.schema.json) | `Evidence` | SQLite `evidence` / `POINT#id` EV# | quote⊆source validation |
| RainObservation | [RainObservation.schema.json](../schemas/RainObservation.schema.json) | `RainObservation` | SQLite `rain_cache` / CONFIG RAIN | live, cache, or scenario_slider |
| PriorityScore | [PriorityScore.schema.json](../schemas/PriorityScore.schema.json) | `PriorityComponents` (+ card extras) | Derived at rank time | R,S,C,Q,U,G |
| Incident / Audit | LLD §20 | `IncidentResponse`, `AuditDecisionResponse` | SQLite `audit` / AUDIT#ts | HITL trail |
| Honesty meta | LLD §21 | `HonestyMetaResponse` | Config / constants | θ, W_NORM, U semantics |

## Seed → ingest → runtime

```text
DisputePointSeed (fixtures)
        ↓ FixtureLoader + Evidence attach + OwnershipEngine
DisputePoint (API / queue / card)
```

Validate fixture **points** against **DisputePointSeed** only. Do not loosen runtime DisputePoint or OpenAPI to match seed null-geo / empty evidence.

## Ownership of truth

| Fact | Owner | Must not |
|------|-------|----------|
| Field types / enums | `docs/schemas/*.json` | Silently diverge OpenAPI from schemas |
| HTTP paths / status / DP-* codes | [openapi.yaml](../openapi.yaml) + LLD §7/§11 | Add routes without Phase 6 amendment |
| CONFLICT → `responsible_agency = null` | Phase 6 / AGENTS hard stop | Prefer one agency on CONFLICT |
| U meaning | Coordination uncertainty | Treat U as physical severity |
| Fixture quotes / coords | DATA_PLAYBOOK + verified sources | Invent DM-71 / SCADA / GPS |

## Relationships (logical)

```text
DisputePoint 1──* Evidence          (evidence_ids)
DisputePoint 1──1 PriorityScore     (computed)
DisputePoint 1──* AuditDecision     (HITL)
RainObservation ──▶ PriorityScore.R (global rain context)
```

## Hard invariants

1. `ownership_state == CONFLICT` ⇒ `responsible_agency` is always `null`.
2. ACK only when `ownership_state == ASSIGNED` and `status == OPEN`.
3. OVERRIDE only from `OPEN`; records recommended vs human agency.
4. Agency values ∈ allowlist: PWD, MCD, NDMC, IFC, DDA, DJB, RAILWAYS, CPWD, OTHER, UNKNOWN.
5. Evidence `quote` minLength 10; type weights per LLD §13.
6. Rain scenario responses set `source: scenario_slider`, `is_synthetic: true`.

## EVENT_CONTRACTS

**N/A for MVP.** There is no product event bus. EventBridge (if used) is schedule-only for rain poll — not a domain event contract surface. Pact / CDCT deferred (single FastAPI + Vite app).

## References

- [Design System Doc Spec — pointer vs copy](https://designsystemdocspec.org/) (index schemas; do not fork field tables here)
- [openapi.yaml](../openapi.yaml) — HTTP shapes
- [LLD.md](../LLD.md) §4, §9, §13–§15 — field dictionaries
