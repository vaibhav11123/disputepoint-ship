# Docs map

DisputePoint documentation. **Phase 6 wins** if anything disagrees.

## Start here

1. [PHASE6.md](PHASE6.md) — frozen build contract  
2. Layer extract: [PRD.md](PRD.md) · [HLD.md](HLD.md) · [LLD.md](LLD.md) · [UX.md](UX.md) · product chrome: [UX_COPY.md](UX_COPY.md)  
3. Contracts: [schemas/](schemas/) · [openapi.yaml](openapi.yaml) · [contracts/DATA_MODEL.md](contracts/DATA_MODEL.md)  
4. Quality gate: [quality/SPEC_READINESS.md](quality/SPEC_READINESS.md) — Spec + **Data Ready both PASS**; Phase 7 may start  
5. Execution control plane: [`../execution/START.md`](../execution/START.md) — router; product ships; G-VIDEO still open for YouTube  
6. Fixtures / audit: [`../data/fixtures/`](../data/fixtures/) (points 0.3.3 · evidence 0.3.4) · [`../data/audit/`](../data/audit/) · [build/DATA_PLAYBOOK.md](build/DATA_PLAYBOOK.md) · [research/enrichment-source-pass.md](research/enrichment-source-pass.md) · [build/GAPS.md](build/GAPS.md)  
7. Demo video: [build/DEMO_SCRIPT.md](build/DEMO_SCRIPT.md) (spoken VO) · [build/DEMO_WOW.md](build/DEMO_WOW.md) · [build/DEMO_REHEARSAL.md](build/DEMO_REHEARSAL.md) · [build/AWS_DEMO_BEAT.md](build/AWS_DEMO_BEAT.md) · [research/demo-win-tactics.md](research/demo-win-tactics.md) · [research/video-win-pass-2026-10-10.md](research/video-win-pass-2026-10-10.md) · [build/BUILDER_BLOG.md](build/BUILDER_BLOG.md)  
8. Agents: root [AGENTS.md](../AGENTS.md) → [agent/AGENT_CONSTITUTION.md](agent/AGENT_CONSTITUTION.md)

## Layout

| Path | Role |
|------|------|
| [PHASE6.md](PHASE6.md) | Frozen SoT |
| [PRD.md](PRD.md) · [HLD.md](HLD.md) · [LLD.md](LLD.md) · [UX.md](UX.md) | Readable extracts of Phase 6 |
| [contracts/](contracts/) | DATA_MODEL index (schemas remain SoT for fields) |
| [design/](design/) | DESIGN_SYSTEM extract → UX §8–§12; Vite stack lock + library KEEP/REJECT (no Next/shadcn forks) |
| [quality/](quality/) | ACCEPTANCE_CRITERIA, TEST_STRATEGY, E2E_SCENARIOS, SPEC_READINESS |
| [operations/](operations/) | SECURITY, PERFORMANCE, [DEPLOYMENT](operations/DEPLOYMENT.md) (Ship It **live**), OBSERVABILITY, [AWS_OPERATOR](operations/AWS_OPERATOR.md) (URLs / login / cleanup), [SUBMISSION_GIT](operations/SUBMISSION_GIT.md) |
| [build/](build/) | DATA_PLAYBOOK, GAPS, [LICENSE_AUDIT](build/LICENSE_AUDIT.md), TRACEABILITY, [DEMO_SCRIPT](build/DEMO_SCRIPT.md), [DEMO_WOW](build/DEMO_WOW.md), [DEMO_REHEARSAL](build/DEMO_REHEARSAL.md), [BUILDER_BLOG](build/BUILDER_BLOG.md) |
| [`../data/`](../data/) | `fixtures/` (L2 product) · `audit/` (L1 decisions; L0 sources gitignored) |
| [phases/](phases/) | PHASE1–5 research trail + REPORT (history) |
| [agent/](agent/) | AGENT_CONSTITUTION, HOWTO_REUSE |
| [schemas/](schemas/) | JSON contracts — do not silently change |
| [research/](research/) | [demo-win-tactics](research/demo-win-tactics.md), [video-win-pass-2026-10-10](research/video-win-pass-2026-10-10.md), [full-corpus-evidence-audit](research/full-corpus-evidence-audit.md), [enrichment-source-pass](research/enrichment-source-pass.md), [delhi-2025-07-29 replay](research/delhi-2025-07-29-weather-timeline.md), [live-sources-constant-retrieval](research/live-sources-constant-retrieval.md), [geocode-candidates](research/geocode-candidates.md), [builder-center-blog-tactics](research/builder-center-blog-tactics.md), [aws-strategy notes](research/aws-strategy-and-submission-notes.md) |
| [openapi.yaml](openapi.yaml) | DecisionAPI HTTP contract (nine routes) |
| [archive/](archive/) | Drafts — not SoT |

## Reading order

Research trail (`phases/`) → **PHASE6** → extract for the layer you change → contracts/OpenAPI → fixtures + `docs/build/` demo stack → Ship It operator docs. App is shipped; G-VIDEO is the remaining human gate.
