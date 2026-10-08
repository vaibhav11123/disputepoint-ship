# How this project was researched and planned

**Audience:** Future you, teammates, GitHub visitors, Phase 7 coding agents.  
**Scope:** Capture the *process* used to get from hackathon brief → frozen Phase 6, so it can be reused for other problems — without dumping private chat logs.

Research originals live in `market-research/runs/environmental-hacks-deep-2026/`. This repo holds **copies** for product work.

---

## 1. What this repo is

| Layer | Purpose |
|-------|---------|
| `AGENTS.md` | Short agent README: project overview, hard stops, verify pointers, condensed priorities ([agents.md](https://agents.md/) style; keep under context/size caps) |
| `docs/agent/AGENT_CONSTITUTION.md` | Full engineering OS (B.1–B.32). Reusable on the next repo; replace the project overlay in root `AGENTS.md` per product. |
| `docs/phases/PHASE1–5.md` + `docs/PHASE6.md` | Research trail → **frozen** implementation contract |
| `docs/PRD.md` · `docs/HLD.md` · `docs/LLD.md` · `docs/UX.md` | Readable extracts of Phase 6. If an extract disagrees with Phase 6, follow Phase 6. |
| `docs/build/` | DATA_PLAYBOOK, GAPS (inventory + unlock recipes), LICENSE_AUDIT, TRACEABILITY, DEMO_WOW |
| `data/fixtures/` | L2 product corpus (points/evidence/readiness v0.2+; Data Ready PASS) |
| `data/audit/` | L1 audit matrices (committed); L0 source bodies gitignored — see `data/audit/README.md` |
| `docs/research/geocode-candidates.md` | Nominatim offline candidates; promote only after VERIFIED. |
| `docs/schemas/` | Data contracts coding agents must not silently change |
| `.mex/` (optional) | Secondary living memory (mex Hub loopback-only). Phase 6 + root AGENTS hard stops win on conflict. |
| `docs/research/` | ML/LLM gate, AWS/submission, UX anti-slop, API probes |
| `docs/archive/` | Earlier drafts (history, not SoT) |
| `docs/README.md` | Docs map |
| Code (Phase 7+) | Product implementation of DisputePoint |

**Product one-liner:** For a DM coordination cell, when rain threatens multi-agency disputed waterlogging points in Delhi, decide which point first, which agency (or UNCERTAIN), and why — evidence-backed, HITL, not a flood heatmap.

---

## 2. Phase pipeline (reusable)

```text
Phase 1  Opportunity landscape (many wedges, evidence-labeled)
   ↓
Phase 2  Due diligence (feasibility, data, competitors)
   ↓
Phase 3  Deep investigation (chosen family)
   ↓
Phase 4  Final selection + Gate A/B (cites, kill collisions)
   ↓
Phase 5  Build strategy (weights, θ_assign, UX, non-goals)
   ↓
Phase 6  Implementation plan + PRD/HLD/LLD + validation gates → FREEZE
   ↓
Phase 7  Code against frozen contract (agents OK; strategy reopen NOT OK)
   ↓
Phase 8–9 Judge-blind + submission package
```

**Hard rule after Phase 6 freeze:** Implementation may discover bugs and missing details; it may **not** reopen opportunity hunting or swap to a flood-prediction product.

### Evidence discipline (keep this for any future research)

- Label claims **FACT / DERIVED (or INFERENCE) / ASSUMPTION (or SPECULATION)**.
- Prefer primary URLs (court, gov, wire) over vibes.
- Never invent SCADA, GPS, or official lists that are not public.
- Synthetic fixtures must stay labeled forever.

### Decision tests that saved the product

| Test | Pass condition |
|------|----------------|
| Decision-delta | Beats verbal buck-passing with evidence-backed agency\|UNCERTAIN |
| Gate B collision | Not another Jal-Drishti / Pravah / FloodReady prediction map |
| Kill test A | Without evidence/ownership layer → not meaningfully ≠ flood dashboard |
| Kill test B | Without rain → still solves dispute→evidence→ownership→action |
| Unsupported ML | No fake XGBoost on n≈15 points |

---

## 3. Tools and how they were used

Built in **Cursor** with agents on the `market-research` Research OS run, then seeded into this product repo.

| Tool / surface | Used for | Notes for reuse |
|----------------|----------|-----------------|
| **Exa MCP** (`web_search_exa`, `web_fetch_exa`) | Live web research, hackathon rules, datasets, design sources | Prefer for current facts over model memory |
| **opencli / gh** | Reddit signals, GitHub crowding search | X/Twitter often blocked (`AUTH_REQUIRED`) — coverage gap |
| **HTTP probes** | Open-Meteo 🟢, IMD 🟡, Overpass, LiveLaw | Record in `docs/research/probe-log.md` |
| **Cursor plans** | Phase improve / ML gate / pre-freeze MUST FIX | Plan → confirm → execute; don’t edit plan files during exec |
| **Skills** | stop-slop (copy), Exa practices, frontend anti-AI-slop rules | Demo script + UI strings |
| **Agent transcripts** | Private Cursor session history | **Do not** commit raw transcripts; distill into docs like this |

### What we deliberately did *not* do

- Did not treat LLM as ownership authority.
- Did not force predictive ML onto 12–15 curated points.
- Did not ship Inter / purple-gradient / three-card SaaS UI for an ops queue.
- Did not invent DM-71 full geolist or live pump SCADA.

---

## 4. AI architecture (frozen stance)

```text
Documents → (deterministic | Bedrock/LLM extract) → validation
        → Evidence graph → Ownership (θ_assign, CONFLICT⇒null)
        → Explainable ranking (U = coordination_uncertainty)
        → HITL ACK / OVERRIDE / ESCALATE → audit
```

- **LLM:** extraction accelerator with quantitative AI Gate; fail → fixtures.
- **ML:** deferred until HITL labels exist (Phase 6 gate = no KEEP for MVP).
- **Primary KPI:** time-to-actionable-triage < 30s in demo.

Details: `docs/PHASE6.md`, `docs/research/ml-llm-opportunity-gate.md`.

---

## 5. How to reuse this for another hackathon / problem

1. **Copy the phase skeleton**, not the Delhi flood content.
2. Re-run Phase 1 with Exa + primary sources; keep FACT labels.
3. Gate B: search GitHub/Devpost for dashboard clones before locking.
4. Freeze a Phase 6-style contract (FRs, schemas, kill tests, video beat sheet) **before** coding.
5. Seed a clean product repo with `docs/` copies; implement outside a dirty research monorepo if needed.
6. Submission: public GitHub + ≤3 min YouTube + write-up; AWS visible in video (https://www.wemakedevs.org/aws/rules).

### Checklist to GitHub-enable *this* repo

- [ ] `LICENSE` chosen (MIT recommended for hackathon OSS attribution)
- [ ] Remote: see root README “Publish to GitHub”
- [ ] Branch protection on `main` after first code lands
- [ ] `.env.example` only — never commit `.env` / AWS keys
- [ ] `docs/build/LICENSE_AUDIT.md` before submission
- [ ] List AI coding tools used (Cursor) in README / write-up — required by tour rules

---

## 6. Reading order for newcomers

1. [docs/README.md](../README.md) (map) then this file
2. `docs/phases/PHASE4.md` (why this wedge)
3. `docs/phases/PHASE5.md` (product rules)
4. `docs/PHASE6.md` (build contract — **binding**)
5. `docs/research/*` gates
6. Then code.

---

## 7. Chat history policy

Full Cursor agent transcripts are **local and private**. They are not a substitute for docs.

When a session discovers something durable (probe result, gate verdict, MUST FIX), **write it into `docs/`** in the same session. That is how this repo stays usable months later without replaying chats.
