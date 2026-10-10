# DEMO_WOW — video story checklist

**Purpose:** Freeze the ≤3 min YouTube wow so agents and humans build toward one path. **Spoken VO:** [DEMO_SCRIPT.md](DEMO_SCRIPT.md). Companion: [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md) · Phase 6 §39 · [UX.md](../UX.md) · [research/demo-win-tactics.md](../research/demo-win-tactics.md).

**Product SoT:** [PHASE6.md](../PHASE6.md) wins on conflict. Wow = **who acts under rain, with evidence** — not flood prediction or AI theater.

**Constraint:** WeMakeDevs has **no live demo**. The YouTube **is** the product. If it is not on screen, it does not count.

---

## AngelHack clock (locked)

| Clock | Job | On screen / voice |
|-------|-----|-------------------|
| **0:00–0:30** | Problem + promise | **Read [DEMO_SCRIPT.md](DEMO_SCRIPT.md)** — lived cost of waterlogging → coordination gap → commander tool |
| **0:30–2:10** | Working path (~half runtime) | Before → trigger → aha → HITL (W1–W8); VO in DEMO_SCRIPT |
| **2:10–2:35** | Tech hard part + **AWS** | W9: live Ship It UI + `/aws-arch.html` or `GET /health` LIVE — [AWS_DEMO_BEAT.md](AWS_DEMO_BEAT.md) |
| **2:35–3:00** | Impact / next | Triage clarity; “not another flood map”; optional 5s competitor contrast |

**First-90s pass/fail:** A stranger can answer: who is the user, what decision, why not a flood map. Full VO checklist: [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

---

## Before → trigger → aha (spoken script)

**Authoritative read-aloud:** [DEMO_SCRIPT.md](DEMO_SCRIPT.md) (lived-cost open + timed VO). Summary only:

| Beat | Script (≤1 sentence each) | Must show |
|------|---------------------------|-----------|
| **Problem** | Flooded roads cost people time; response also needs clear responsibility | Queue (+ map) |
| **Before** | Queue of incidents — assigned / disputed / evidence-needed | Board mix |
| **Trigger** | Rain may change priority; does not set ownership | Rain control + priority (engine-honest) |
| **Aha** | Okhla (or Samaypur) disputed — no invented owner; evidence stays | Incident + ledger |
| **Proof** | Escalate or override; audit visible; ACK only if already assigned | HITL + audit |
| **Hard part** | Ownership under conflict on AWS — no flood ML | AWS beat |
| **Close** | Can’t stop rain with a dashboard; clearer response; ward pilot | Close |

---

## Critical story — W1–W9 (must show)

| ID | Moment | FR / note | §39 / AngelHack slot |
|----|--------|-----------|----------------------|
| W1 | Ranked queue, named points | FR-001, FR-008 | ~0:30–0:40 |
| W2 | Rain → re-rank, flash ≤200 ms | FR-006, FR-007 | ~0:40–1:00 |
| W3 | Okhla / Samaypur CONFLICT + null agency | FR-011, FR-017 | ~1:15–1:45 |
| W4 | Evidence quotes + URLs | FR-002, FR-009 | ~1:20–1:40 |
| W5 | Why / counterfactual chips | FR-023 | ~1:40–1:55 |
| W6 | Advisory + SYNTHETIC honesty labels | FR-010 | ~1:55–2:05 |
| W7 | OVERRIDE/ESCALATE on CONFLICT → DecisionAuditPanel; optional ACK cutaway on seeded ASSIGNED | FR-012 | ~2:05–2:20 (may spill into tech block) |
| W8 | Triage &lt;30s feel on golden path | FR-027 | Close + KPI feel |
| W9 | AWS visible in video | FR-016 | **2:10–2:35** (plus optional mid-flow breadcrumb) |

MapHUD / Cmd+K / eval are **not** W* story beats — see C7–C9 / J1–J2.

---

## Craft — C1–C9

| ID | Rule |
|----|------|
| C1 | IBM Plex Sans/Mono + tabular scores |
| C2 | ~65/35 queue+card; no hero / map-first home |
| C3 | Max **2** UI motions: rank flash + rain pulse. Map `flyTo` is camera, not a third UI motion |
| C4 | Loading / empty / error non-blank |
| C5 | Rain mode `live` \| `cache` \| `slider` visible |
| C6 | Pass anti-slop checklist ([UX §12](../UX.md), [DESIGN_SYSTEM](../design/DESIGN_SYSTEM.md)) |
| C7 | MapHUD: BUILD IF STABLE; light basemap; OSM attribution; no heatmap |
| C8 | Cmd+K via `cmdk` + `--dp-*`; not shadcn Command |
| C9 | Eval: footer link and/or drawer; never product home |

## Judges aids — J1–J2 (optional cutaways)

| ID | Aid | Rule |
|----|-----|------|
| J1 | Cmd+K point jump | Same `selectedPointId` as row click |
| J2 | Eval link or drawer | Mirrors `tests/eval/baseline_tournament.md`; **no invented metrics** |

## Reliability — R1

| ID | Moment |
|----|--------|
| R1 | Open-Meteo fail → slider/cache still re-ranks; mode banner labeled |

## Map — M1 (gated, not critical story)

| ID | Moment | Rule |
|----|--------|------|
| M1 | MapHUD marker + flyTo | Prefer VERIFIED geocodes; MapHUD is in play on Ship It (Rain Strike expand). Do not invent coords. |

---

## Anti-flash traps (fail the video if present)

- City heatmap or map-first cold open
- “AI-powered” / “smart city” / Inter-Geist purple glass SaaS shell
- Bedrock or LLM wallpaper without schema + quote⊆source validation
- Invented owner when `ownership_state == CONFLICT`
- Claiming synthetic readiness or fixtures as live SCADA/GPS/DM-71
- Feature tour that delays the working decision past ~90s

---

## Optional 5s competitor contrast (2:30–3:00)

Split or cutaway: generic flood heatmap (stock or labeled mock) vs DisputePoint queue naming owner / UNCERTAIN. Voice: “Maps show water. This shows who must act.”

Do not spend build time on a real competitor product.

---

## Memorability checklist (pre-record)

- [ ] Citation chip names agency or shows CONFLICT null
- [ ] Rain mode banner honest
- [ ] ≤2 motions (C3)
- [ ] AWS on screen (W9) — not write-up only
- [ ] First-90s stranger test pass
- [ ] Anti-flash traps absent

---

## Ownership

| Artifact | Package / gate |
|----------|----------------|
| W1–W8 golden path | WP-09…WP-13, WP-16 / G-KPI |
| W5 counterfactuals | WP-12 |
| W9 AWS beat | WP-15 + **G-VIDEO** |
| Rehearsal ops | [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md) · WP-16 |
| Visual anti-slop | **G-VIS** before G-VIDEO |
