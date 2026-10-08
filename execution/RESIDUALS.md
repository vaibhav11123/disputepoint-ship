# Residuals — geocode / runtime lat-lon

Seeds allow null `lat`/`lon` ([docs/schemas/DisputePointSeed.schema.json](../docs/schemas/DisputePointSeed.schema.json)).

Runtime [docs/schemas/DisputePoint.schema.json](../docs/schemas/DisputePoint.schema.json) and OpenAPI `DisputePointPublic` require numeric Delhi-bbox coordinates.

[docs/quality/SPEC_READINESS.md](../docs/quality/SPEC_READINESS.md) and [docs/contracts/DATA_MODEL.md](../docs/contracts/DATA_MODEL.md) accept null geocodes for MapHUD skip and forbid loosening the runtime schema.

## Rules (every package inherits)

1. Never write a coordinate that is not already on the seed.
2. Never edit schemas or OpenAPI to allow null `lat`.
3. MapHUD stays collapsed while geocodes are null (LLD §3, FR-020). E2E-07 skipped.
4. Strict runtime schema validation runs only for points whose seed `lat` and `lon` are both numbers.
5. FR-001’s “≥12 items validate as runtime DisputePoint with numeric lat/lon” stays **DOCUMENTED** (not VERIFIED) until a human verifies geocodes (gate G-GEO). Queue length still comes from the seed file. An agent must not turn that red test green by inventing coordinates.

Convergence must not invent coordinates or a gold order to close this residual.

---

## Demo / video / clock residuals

Operational packaging for flashier-winner / AWS-video / git-dump / blog-prize risks. Story IDs: [docs/build/DEMO_WOW.md](../docs/build/DEMO_WOW.md). Ops: [docs/build/DEMO_REHEARSAL.md](../docs/build/DEMO_REHEARSAL.md). Blog: [docs/build/BUILDER_BLOG.md](../docs/build/BUILDER_BLOG.md). Sources: [docs/research/demo-win-tactics.md](../docs/research/demo-win-tactics.md) · [docs/research/builder-center-blog-tactics.md](../docs/research/builder-center-blog-tactics.md).

| Id | Risk | Open until | Owner |
|----|------|------------|--------|
| **R-DEMO-WOW** | Weak wow vs flashy prediction demos | Cold-open / AngelHack script rehearsed; first-90s stranger test pass on a dry-run recording | WP-16 · G-KPI · DEMO_WOW |
| **R-DEMO-DETERMINISM** | Flaky live deps kill the video | Fixture scenarios smoke twice; dual AWS/fixture path proven; R1 labeled failover | WP-16 · DEMO_REHEARSAL |
| **R-GIT-CLOCK** | Pre-clock product dump / wrong history = DQ | Human G-CLOCK; fresh submission repo; allow-list copy only; event-dated history | G-CLOCK · [SUBMISSION_GIT](../docs/operations/SUBMISSION_GIT.md) |
| **R-BLOG-BUILDER** | Miss Top 5 blogs (AirPods) / only short form | Builder Center article published; URL opens signed-out; linked in form (separate from short write-up) | Human after G-VIDEO · [BUILDER_BLOG](../docs/build/BUILDER_BLOG.md) |

Agents must not mark W9 / FR-016 VERIFIED until G-VIDEO (AWS on screen). Do not invent demo metrics or geocodes to close these residuals. Do not burn day-1 build time closing R-BLOG-BUILDER.
