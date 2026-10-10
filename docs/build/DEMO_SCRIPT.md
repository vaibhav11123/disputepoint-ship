# DEMO_SCRIPT — read-aloud YouTube narration

**Purpose:** One-page spoken script for the ≤3 min WeMakeDevs video. Story IDs: [DEMO_WOW.md](DEMO_WOW.md). Record ops: [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md). Sources: [research/demo-win-tactics.md](../research/demo-win-tactics.md).

**Product SoT:** [PHASE6.md](../PHASE6.md). User = DM cell officer. Spine = queue → rain → CONFLICT null → evidence → HITL → AWS. Not a flood map. Not a citizen inbox.

**Word budget:** ~130–150 spoken words. Cut W5 VO first if over 3:00.

---

## Locked problem statement (0:00–0:30)

**Structure:** named user → failure + public FACT → product promise that preserves null ownership.

**VO (exact):**

> You’re in a DM coordination cell. Under monsoon, disputed waterlogging points stall while agencies pass the buck — Delhi’s High Court called it enormous confusion. DisputePoint queues those points under rain: who acts, with evidence — or honest null when ownership conflicts.

**On screen:** Title + queue-first UI (not heatmap). Optional lower-third: `HC 2025 · agency buck-passing (public record)`. No fake death counts or invented stats.

**FACT anchors (cite in write-up, not as on-screen essay):** [Delhi HC order / LiveLaw PDF](https://www.livelaw.in/pdf_upload/pms28072025cw131902024201344-613072.pdf) · [TOI summary](https://timesofindia.indiatimes.com/india/much-confusion-on-who-does-what-even-upkeep-of-drains-hc-to-delhi-government/articleshow/122963747.cms).

**30s pass/fail:** Stranger can answer (1) user = DM cell, (2) pain = ownership confusion not rain data, (3) product will not invent an owner.

---

## Full timed VO

| Clock | VO (exact) | Click / show | W* |
|-------|------------|--------------|-----|
| **0:00–0:05** | (silent or ambient) | Earth Studio WORLD→PURANA QUILA → hard cut ([EARTH_STUDIO_SHOT.md](EARTH_STUDIO_SHOT.md)) | Mode C |
| **0:05–0:30** | Locked problem statement above | Title + calm queue (Mode A) | — |
| **0:30–0:45** | “Thirty-plus disputed areas on one board — assigned, disputed, and evidence-needed in the first screen. Volunteer reported rows fill the street view.” | Queue `dry` (full board mix: green ASSIGNED + olive CONFLICT + UNKNOWN); Volunteer reported chip. No DEMO MIX banner — fixtures drive engine order. | W1 |
| **0:45–1:05** | “Watch rain hit the board — mode banner updates; relative ranks stay engine-honest under citywide R.” | Slider or Open-Meteo; mode banner | W2 |
| **1:05–1:35** | “Purana Quila — DEMO INCIDENT. Responsibility disputed. We don’t guess. Competing claims, no auto-assign. Volunteer reports raise urgency — they do not pick an owner.” | Open `/incident/dp-purana-quila` — **focused place map + PlaceStrip must be on screen** beside RESPONSIBILITY DISPUTED / NO AUTO-ASSIGN; then Evidence tab (map stays sticky) + quotes | W3 W4 |
| **1:35–1:50** | “Why this rank — and what if rain drops.” | Counterfactual chips if shipped; else **skip VO** | W5 |
| **1:50–2:00** | “Advisory next step. Officer ACK or OVERRIDE — audit stays visible.” | Advisory + HITL + DecisionAuditPanel | W6 W7 |
| **2:00–2:30** | “Hard part: evidence-weighted ownership under conflict — no flood ML, no fake rain re-rank. On AWS: API Gateway, Lambda, DynamoDB, S3.” | Live UI or `/aws-arch.html` + `GET /health` LIVE — [AWS_DEMO_BEAT.md](AWS_DEMO_BEAT.md) | W9 |
| **2:30–3:00** | “Not another flood map — fewer invisible handoffs. Next: ward pilot on time-to-confirmation. DisputePoint: don’t guess. Coordinate.” | Summary; optional 5s heatmap vs queue contrast | W8 |

**Trigger sentence (only one):** “Watch rain hit the queue.”

### Optional beat — Historical day (not the judged cold-open path)

On `/demo`, operators may run **HISTORICAL REPLAY · 29 July 2025** (stored Safdarjung + documented activations). VO if used:

> We’re replaying published observations from 29 July 2025 — documented activations emerge over time; Safdarjung totals are station context (not 6h live R); gaps stay gaps. Not live telemetry. Not Purana Qila on that clock unless research says so.

Do **not** call the 42 mm stress-test “29 July.” Keep primary video on dry → APPLY SCENARIO unless judges choose the replay entry.

---

## Script rules

- Say **DEMO / scenario** when slider or fixtures drive rain (honesty = competence).
- Say **HISTORICAL REPLAY** when the 29 July stored day is running — never LIVE.
- Never invent an agency under `ownership_state == CONFLICT`.
- Never claim measured response-time wins or death counts.
- No “Hi we’re Team…”, no login, no feature tour, no citizen-inbox / Triage / Bedrock lines unless the product actually ships them (§14A default off).
- Mid-flow AWS breadcrumb allowed; dedicated AWS still in **2:00–2:30**.
- Rehearse with stopwatch; hard cutoff **3:00**.

---

## Anti-lines (do not say)

- “We predict flooding / water depth / risk for the whole city.”
- “AI assigns MCD automatically.”
- “Shows the responsible owner” when the card is CONFLICT null.
- Any invented SCADA / DM-71 GPS / live pump telemetry claim.

---

## First-90s stranger test

After watching 0:00–1:30 only, a stranger must name:

1. User (DM cell)
2. Trigger (rain on queue)
3. Aha (CONFLICT → null + evidence, not invent owner)

If they say “flood map” or “AI chatbot,” rewrite VO — do not add features.

---

## Ownership

| Item | Owner |
|------|--------|
| This script | WP-16 · G-VIDEO |
| Story IDs | [DEMO_WOW.md](DEMO_WOW.md) |
| Smoke / gates | [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md) |
