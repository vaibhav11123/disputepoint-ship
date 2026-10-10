# Docs map

DisputePoint documentation. **Phase 6 wins** if anything disagrees.

## Start here

1. [PHASE6.md](PHASE6.md) — frozen build contract  
2. Layer extract: [PRD.md](PRD.md) · [HLD.md](HLD.md) · [LLD.md](LLD.md) · [UX.md](UX.md) · product chrome: [UX_COPY.md](UX_COPY.md)  
3. Contracts: [schemas/](schemas/) · [openapi.yaml](openapi.yaml) · [contracts/DATA_MODEL.md](contracts/DATA_MODEL.md)  
4. Quality gate: [quality/SPEC_READINESS.md](quality/SPEC_READINESS.md) — Spec + **Data Ready both PASS**; Phase 7 may start  
5. Execution control plane: [`../execution/START.md`](../execution/START.md) — router; plan check must PASS before app code; clock still Oct 8  
6. Fixtures / audit: [`../data/fixtures/`](../data/fixtures/) · [`../data/audit/`](../data/audit/) (AUDIT_MATRIX, FETCH_MANIFEST; L0 bodies gitignored) · [build/DATA_PLAYBOOK.md](build/DATA_PLAYBOOK.md) · [build/DATA_ENRICHMENT.md](build/DATA_ENRICHMENT.md) · [research/enrichment-source-pass.md](research/enrichment-source-pass.md) · [build/GAPS.md](build/GAPS.md) · [build/TRACEABILITY.md](build/TRACEABILITY.md)  
7. Demo video: [build/DEMO_SCRIPT.md](build/DEMO_SCRIPT.md) (spoken VO) · [build/DEMO_WOW.md](build/DEMO_WOW.md) (W1–W9) · [build/DEMO_REHEARSAL.md](build/DEMO_REHEARSAL.md) (smoke/gates) · [build/BUILDER_BLOG.md](build/BUILDER_BLOG.md) (Builder Center / AirPods) · [research/demo-win-tactics.md](research/demo-win-tactics.md) · [research/builder-center-blog-tactics.md](research/builder-center-blog-tactics.md)  
8. Agents: root [AGENTS.md](../AGENTS.md) → [agent/AGENT_CONSTITUTION.md](agent/AGENT_CONSTITUTION.md)

## Layout

| Path | Role |
|------|------|
| [PHASE6.md](PHASE6.md) | Frozen SoT |
| [PRD.md](PRD.md) · [HLD.md](HLD.md) · [LLD.md](LLD.md) · [UX.md](UX.md) | Readable extracts of Phase 6 |
| [contracts/](contracts/) | DATA_MODEL index (schemas remain SoT for fields) |
| [design/](design/) | DESIGN_SYSTEM extract → UX §8–§12; Vite stack lock + library KEEP/REJECT (no Next/shadcn forks) |
| [quality/](quality/) | ACCEPTANCE_CRITERIA, TEST_STRATEGY, E2E_SCENARIOS, SPEC_READINESS |
| [operations/](operations/) | SECURITY, PERFORMANCE, DEPLOYMENT, OBSERVABILITY, [AWS_OPERATOR](operations/AWS_OPERATOR.md) (profile/region/login/SAM/G-AWS), [SUBMISSION_GIT](operations/SUBMISSION_GIT.md) (two-repo commit/push + upload allow/deny) |
| [build/](build/) | DATA_PLAYBOOK, GAPS, [LICENSE_AUDIT](build/LICENSE_AUDIT.md), TRACEABILITY, [DEMO_SCRIPT](build/DEMO_SCRIPT.md), [DEMO_WOW](build/DEMO_WOW.md), [DEMO_REHEARSAL](build/DEMO_REHEARSAL.md), [BUILDER_BLOG](build/BUILDER_BLOG.md) |
| [`../data/`](../data/) | `fixtures/` (L2 product) · `audit/` (L1 decisions; L0 sources gitignored) |
| [phases/](phases/) | PHASE1–5 research trail + REPORT (history) |
| [agent/](agent/) | AGENT_CONSTITUTION, HOWTO_REUSE |
| [schemas/](schemas/) | JSON contracts — do not silently change |
| [research/](research/) | ML/LLM gate, AWS notes, UX anti-slop, probes, geocode candidates, [full-corpus-evidence-audit](research/full-corpus-evidence-audit.md), [delhi-2025-07-29 replay](research/delhi-2025-07-29-weather-timeline.md), [live-sources-constant-retrieval](research/live-sources-constant-retrieval.md), [live-source-integration-records](research/live-source-integration-records.md), [demo-win-tactics](research/demo-win-tactics.md), [builder-center-blog-tactics](research/builder-center-blog-tactics.md) |
| [openapi.yaml](openapi.yaml) | DecisionAPI HTTP contract (nine routes) |
| [archive/](archive/) | Drafts — not SoT |

## Reading order

Research trail (`phases/`) → **PHASE6** → extract for the layer you change → contracts/OpenAPI → **SPEC_READINESS** (Spec + Data Ready **PASS**) → `data/fixtures` + `data/audit` / `build/` for residuals → **Phase 7 coding** (app still to build).
