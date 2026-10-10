# DEMO_SCRIPT — read-aloud YouTube narration

**Purpose:** One-page spoken script for the ≤3 min WeMakeDevs video. Story IDs: [DEMO_WOW.md](DEMO_WOW.md). Record ops: [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md). Sources: [research/demo-win-tactics.md](../research/demo-win-tactics.md) · [research/video-win-pass-2026-10-10.md](../research/video-win-pass-2026-10-10.md) · [research/public-cost-of-waterlogging.md](../research/public-cost-of-waterlogging.md).

**Product SoT:** [PHASE6.md](../PHASE6.md). User = DM / incident commander. Spine = lived cost → queue → rain/priority separate from ownership → disputed null → evidence → human review → AWS → pilot. Not a flood map. Not a citizen inbox. Not a safe-route app.

**Word budget:** ~130–160 spoken words. Cut W5 / shorten AWS names if over 3:00.

**Voice:** People first (lost time, stranded journeys, recurring flood), then the coordination gap, then the product. Real places and cited FACT only. No unmeasured “fewer” / “faster” claims.

---

## Locked problem statement (0:00–0:30)

**Structure:** lived consequence → coordination gap → product for the commander (not HC as hero).

**VO (exact):**

> When heavy rain floods a road in Delhi, the consequences are immediate. People get stuck in traffic, vehicles get stranded, and even getting home can become difficult.
>
> And when a waterlogging incident needs attention, there’s another problem: figuring out which agency is responsible and getting the response coordinated.
>
> DisputePoint is built to help incident commanders work through that problem.

**On screen:** Incident queue (+ map if visible). Optional lower-third later for HC cite in write-up — not the first line of VO.

**FACT anchors (write-up / blog, not on-screen essay):** [HT Jul 2025](https://www.hindustantimes.com/cities/delhi-news/delhi-buckles-under-first-significant-monsoon-rain-spell-101752171973612.html) · [TOI / HC confusion](https://timesofindia.indiatimes.com/india/much-confusion-on-who-does-what-even-upkeep-of-drains-hc-to-delhi-government/articleshow/122963747.cms) · [LiveLaw](https://www.livelaw.in/high-court/delhi-high-court/delhi-high-court-government-flood-management-299427) · [LocalCircles survey](https://www.localcircles.com/a/press/page/gurugram-water-logging) (respondents, not all Delhi).

**30s pass/fail:** Stranger can answer (1) waterlogging hurts daily life, (2) response needs clear responsibility, (3) product helps commanders — does not invent an owner.

---

## Full timed VO

| Clock | VO (exact) | Click / show | W* |
|-------|------------|--------------|-----|
| **0:00–0:30** | Locked problem statement above | Queue (+ map); product on screen early | — |
| **0:30–0:55** | “Instead of starting with a flood map, we start with a queue of incidents. Some have an assigned agency. Some have competing responsibility claims. Others still need evidence. The officer can see what needs attention and where responsibility remains unresolved.” | Board mix: assigned / disputed / evidence-needed. Real places (Okhla, Samaypur, Minto…). | W1 |
| **0:55–1:15** | “Rainfall can change which incidents need attention first. But it doesn’t establish who owns a drain or road. We keep those decisions separate.” | Rain control; priority explanation if visible. Only if engine re-ranks — do not fake reorder. | W2 |
| **1:15–1:45** | “Let’s open Okhla. Here, responsibility remains disputed. We don’t pick an agency just to make the incident look resolved. The officer can examine the available evidence, see what it supports, and understand what is still missing.” | `/incident/dp-okhla-underpass` — DISPUTED / NO AUTO-ASSIGN + evidence (alt: Samaypur Badli). Never invent an owner. | W3 W4 |
| **1:45–2:10** | “When the evidence doesn’t settle the dispute, a human decision is required. The officer reviews the evidence, records the next step — escalate or override — and confirms only when a clear agency is already assigned. The decision stays auditable.” | ESCALATE or OVERRIDE + audit. ACK cutaway only on Mathura Rd / Bharat Mandapam if needed. Never ACK on CONFLICT. | W6 W7 |
| **2:10–2:35** | “Underneath, DisputePoint runs on AWS — API Gateway, Lambda, DynamoDB, and S3 — with EventBridge schedules and CloudWatch logs supporting the app. The aim is a structured, traceable decision process.” | Live UI or `/aws-arch.html` + `/health` | W9 |
| **2:35–3:00** | “We can’t fix Delhi’s drainage with a dashboard. And we can’t promise software will prevent the next flood. But we can make the response clearer: what needs attention, what the evidence says, and who confirmed the next action. Next: a ward pilot on time-to-responsibility decisions. DisputePoint: don’t guess. Coordinate.” | Close | W8 |

**Trigger idea (not a banner tour):** rainfall may change priority; ownership stays separate.

### Optional beat — Historical day (not cold-open)

On `/demo`, **HISTORICAL REPLAY · 29 July 2025** only if used: stored Safdarjung context + documented activations; gaps stay gaps; not live telemetry; do not call slider “29 July.”

---

## Script rules

- Lead with people; HC is supporting evidence for the coordination gap — not endorsement of DisputePoint.
- Say **DEMO / scenario** when slider drives rain; **LIVE** only when `/health` / banner says so.
- Never invent an agency under CONFLICT.
- Never claim measured response-time wins, prevented floods, or safe routes for commuters.
- Escalation ≠ confirmation; ACK only on ASSIGNED.
- Hard cutoff **3:00**.

---

## Anti-lines (do not say)

- “We prevent waterlogging / make Delhi flood-resilient.”
- “We eliminate traffic jams / tell you which roads are safe.”
- “AI assigns MCD automatically” / “shows the owner” on CONFLICT.
- “Fewer invisible handoffs” / “faster response” without measured pilot results.
- Invented SCADA / DM-71 / live flood-depth claims.
- “The High Court endorsed DisputePoint.”

---

## First-90s stranger test

1. Waterlogging costs people time and disrupts journeys  
2. Response also needs clear responsibility  
3. Product helps commanders coordinate — does not invent an owner  

---

## Live demo URLs

| Surface | URL |
|---------|-----|
| UI | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com |
| API | https://olnsv0shee.execute-api.ap-south-1.amazonaws.com |
| Arch | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html |
