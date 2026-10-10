# DEMO_SCRIPT — read-aloud YouTube narration

**Purpose:** One-page spoken script for the ≤3 min WeMakeDevs video. Story IDs: [DEMO_WOW.md](DEMO_WOW.md). Record ops: [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md). Sources: [research/demo-win-tactics.md](../research/demo-win-tactics.md) · [research/video-win-pass-2026-10-10.md](../research/video-win-pass-2026-10-10.md).

**Product SoT:** [PHASE6.md](../PHASE6.md). User = DM coordination cell officer. Spine = queue → rain → disputed null → evidence → officer escalate/override → AWS. Not a flood map. Not a citizen inbox.

**Word budget:** ~130–150 spoken words. Cut W5 VO first if over 3:00.

**Voice:** Ground language of people stuck when underpasses flood and agencies pass the buck — and the cell officer who must decide. Real places and public FACT only. No death counts, fake sensors, or placeholder URLs.

---

## Locked problem statement (0:00–0:30)

**Structure:** named user → failure + public FACT → product promise that preserves null ownership.

**VO (exact):**

> You’re in a DM coordination cell. When the monsoon hits, disputed waterlogging points stall — underpasses, drains — while agencies pass the buck. Delhi’s High Court called it enormous confusion. DisputePoint puts those places on one queue under rain: who clears this, with evidence — or honest null when ownership still fights.

**On screen:** Title + queue-first UI (not heatmap). Optional lower-third: `HC 2025 · agency buck-passing (public record)`. No fake death counts or invented stats.

**FACT anchors (cite in write-up, not as on-screen essay):** [Delhi HC order / LiveLaw PDF](https://www.livelaw.in/pdf_upload/pms28072025cw131902024201344-613072.pdf) · [TOI summary](https://timesofindia.indiatimes.com/india/much-confusion-on-who-does-what-even-upkeep-of-drains-hc-to-delhi-government/articleshow/122963747.cms) · [DHC judgment PDF](https://delhihighcourt.nic.in/app/showFileJudgment/PMS19082025CW131902024_164406.pdf).

**30s pass/fail:** Stranger can answer (1) user = DM cell, (2) pain = ownership confusion not rain data, (3) product will not invent an owner.

---

## Full timed VO

| Clock | VO (exact) | Click / show | W* |
|-------|------------|--------------|-----|
| **0:00–0:05** | (silent or ambient) | Earth Studio WORLD→PURANA QUILA → hard cut ([EARTH_STUDIO_SHOT.md](EARTH_STUDIO_SHOT.md)) | Mode C |
| **0:05–0:30** | Locked problem statement above | Title + calm queue (Mode A) | — |
| **0:30–0:45** | “Thirty-plus waterlogging places on one board — Okhla, Samaypur, Minto. Some already have a clear agency. Some are still disputed. Some still need evidence. Volunteer reports show the street — they do not pick the owner.” | Full board: green assigned + disputed + evidence-needed in the first screen. No DEMO MIX banner. | W1 |
| **0:45–1:05** | “Watch rain hit the board — the mode banner updates. We do not invent who owns the drain.” | Slider or Open-Meteo; mode banner `live` \| `cache` \| `slider` | W2 |
| **1:05–1:35** | “Purana Quila — responsibility disputed. We don’t guess. Competing claims stay on screen. No auto-assign.” | Open `/incident/dp-purana-quila` — place map + RESPONSIBILITY DISPUTED / NO AUTO-ASSIGN; Evidence tab + quotes | W3 W4 |
| **1:35–1:50** | “Why this rank — and what if rain drops.” | Counterfactual chips if shipped; else **skip VO** | W5 |
| **1:50–2:00** | “Next step for the officer: escalate or override — the audit stays on screen. When a point already has a clear agency — Mathura Road, Bharat Mandapam — they can confirm.” | CONFLICT: ESCALATE or OVERRIDE + audit. Optional cutaway: seeded ASSIGNED ACK on Mathura Rd / Bharat Mandapam. Never ACK on CONFLICT. | W6 W7 |
| **2:00–2:30** | “Hard part: evidence-weighted ownership under conflict — no flood ML, no fake rain tricks. Live on AWS: API Gateway, Lambda, DynamoDB, S3.” | Live UI or `/aws-arch.html` + `GET /health` — [AWS_DEMO_BEAT.md](AWS_DEMO_BEAT.md) | W9 |
| **2:30–3:00** | “Not another flood map — fewer invisible handoffs when the road is underwater. Next: ward pilot on time-to-confirmation. DisputePoint: don’t guess. Coordinate.” | Summary; optional 5s heatmap vs queue contrast | W8 |

**Trigger sentence (only one):** “Watch rain hit the board.”

### Optional beat — Historical day (not the judged cold-open path)

On `/demo`, operators may run **HISTORICAL REPLAY · 29 July 2025** (stored Safdarjung + documented activations). VO if used:

> We’re replaying published observations from 29 July 2025 — documented activations emerge over time; Safdarjung totals are station context (not 6h live R); gaps stay gaps. Not live telemetry. Not Purana Qila on that clock unless research says so.

Do **not** call the 42 mm stress-test “29 July.” Keep primary video on dry → APPLY SCENARIO unless judges choose the replay entry.

---

## Script rules

- Say **DEMO / scenario** when slider or fixtures drive rain (honesty = competence).
- Say **HISTORICAL REPLAY** when the 29 July stored day is running — never LIVE.
- Say **LIVE** only when the mode banner / `/health` shows live Open-Meteo.
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
- “ACK” on a disputed / CONFLICT card.
- Any invented SCADA / DM-71 GPS / live pump telemetry claim.

---

## First-90s stranger test

After watching 0:00–1:30 only, a stranger must name:

1. User (DM cell)
2. Trigger (rain on queue)
3. Aha (CONFLICT → null + evidence, not invent owner)

If they say “flood map” or “AI chatbot,” rewrite VO — do not add features.

---

## Live demo URLs (real pins)

| Surface | URL |
|---------|-----|
| UI | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com |
| API | https://olnsv0shee.execute-api.ap-south-1.amazonaws.com |
| Arch | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html |

---

## Ownership

| Item | Owner |
|------|--------|
| This script | WP-16 · G-VIDEO |
| Story IDs | [DEMO_WOW.md](DEMO_WOW.md) |
| Smoke / gates | [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md) |
| Cite log | [video-win-pass-2026-10-10.md](../research/video-win-pass-2026-10-10.md) |
