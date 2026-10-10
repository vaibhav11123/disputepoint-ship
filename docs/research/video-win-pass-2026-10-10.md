# Video win pass — 2026-10-10

**Purpose:** Research OS + Exa cite log for ground-language DEMO_* rewrite. Promote only; do not edit `market-research/src/research_os/**`.

**Companion:** [demo-win-tactics.md](demo-win-tactics.md) · spoken VO [DEMO_SCRIPT.md](../build/DEMO_SCRIPT.md).

---

## Channels run

| Channel | Result |
|---------|--------|
| Research OS `scripts/smoke_channels.py` | **SMOKE OK** (~4m): PASS youtube (exa), jina_web, github; FAIL opencli_doctor + reddit (Browser Bridge not connected); SKIP x (same) |
| Exa `web_search_exa` — Delhi HC drain confusion | **FACT** reconfirmed: HC “enormous confusion” / “passing the buck”; LiveLaw PDF + TOI + DHC judgment PDF |
| Exa `web_search_exa` — hackathon demo tactics | AngelHack 30/90/30/30; one demoable path; problem-first; backup recording; name hard part |
| Live Ship It `GET /health` + `/points` | **FACT** 2026-10-10: `rain_source_state=LIVE`, `precip_mm=0.2`, 35 points, ownership CONFLICT 6 / UNKNOWN 23 / ASSIGNED 6; top-12 mix CONFLICT 5 / UNKNOWN 4 / ASSIGNED 3 |

---

## Voice bank (use in VO)

| Phrase | Label | Source |
|--------|-------|--------|
| “enormous confusion” / “passing the buck” | FACT | [LiveLaw PDF 28 Jul 2025](https://www.livelaw.in/pdf_upload/pms28072025cw131902024201344-613072.pdf) · [TOI](https://timesofindia.indiatimes.com/india/much-confusion-on-who-does-what-even-upkeep-of-drains-hc-to-delhi-government/articleshow/122963747.cms) · [DHC PDF 19 Aug 2025](https://delhihighcourt.nic.in/app/showFileJudgment/PMS19082025CW131902024_164406.pdf) |
| waterlogging, stormwater drain, sewer, MCD / PWD / DJB / DDA | FACT | Same HC orders (agency list) |
| Okhla underpass, Purana Quila, Samaypur Badli / Siraspur, Minto Bridge, Barapullah | FACT (fixtures) | `data/fixtures/points.json` + live `/points` |
| “we don’t guess” / honest null when agencies conflict | DERIVED | Product hard stop = Phase 6 CONFLICT→null |
| escalate / override for disputed points; confirm (ACK) only when already assigned | FACT (product) | HITL API: ACK only ASSIGNED+OPEN; Mathura Rd + Bharat Mandapam ACKED via seed |

## Reject in VO

| Phrase | Why |
|--------|-----|
| Death counts, “saved X hours,” flood depth predictions | Not in corpus; inventing impact |
| DM-71 / SCADA / GPS pumps as live | Hard stop |
| “Shows the responsible owner” on CONFLICT | Breaks null |
| Citizen inbox / chatbot assigns MCD | Not the product |
| “Board mix,” “HITL,” “corpus 0.3.4,” “θ” | Ops jargon — docs only |
| `_SHIP_IT_URL_` / example.com | Placeholders |

---

## FACT ledger (spoken claims → source)

| Spoken claim | Source | Label |
|--------------|--------|-------|
| User = DM / district coordination cell | Phase 6 / PRD | FACT (product) |
| HC: enormous confusion; agencies pass the buck | LiveLaw / TOI / DHC PDFs above | FACT |
| Thirty-plus places on the board | Live `/points` n=35 | FACT |
| Some clear agency, some disputed, some still need evidence | Live ownership counts 6/6/23; top-12 ≥3 each band | FACT |
| Purana Quila responsibility disputed; no auto-assign | `dp-purana-quila` CONFLICT, `responsible_agency` null | FACT |
| Okhla #1 disputed underpass | Live rank 1 CONFLICT | FACT |
| Mathura Rd / Bharat Mandapam can show officer confirm (ACK) | ASSIGNED + status ACKED on live API | FACT |
| Rain LIVE from Open-Meteo when banner says LIVE | `/health` `rain_source_state=LIVE` | FACT |
| Running on AWS: API Gateway, Lambda, DynamoDB, S3 | Ship It stack `disputepoint` | FACT |
| UI / API URLs | [AWS_OPERATOR.md](../operations/AWS_OPERATOR.md) | FACT |

ASSUMPTION never enters VO.

---

## Live pins (copy exactly)

| Surface | Value |
|---------|-------|
| API | https://olnsv0shee.execute-api.ap-south-1.amazonaws.com |
| UI | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com |
| Arch | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html |
| Fixtures | points **0.3.3** · evidence **0.3.4** |

---

## Judge tactics kept (AngelHack / Exa)

1. ~30s problem → ~90s working path → ~30s AWS → ~30s close  
2. One end-to-end path; no feature tour  
3. Name the hard part (ownership under conflict, honest null) while UI runs  
4. Fixtures for story + real AWS on camera  
5. Smoke twice; backup recording; signed-out YouTube check  

---

## Where this lands

DEMO_SCRIPT · DEMO_WOW · DEMO_REHEARSAL · AWS_DEMO_BEAT · BUILDER_BLOG · README · demo-win-tactics append.
