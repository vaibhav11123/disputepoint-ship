# BUILDER_BLOG — AWS Builder Center article draft

**Purpose:** Paste-ready skeleton for Environmental Hacks **Top 5 blogs (AirPods)**. Tactics: [research/builder-center-blog-tactics.md](../research/builder-center-blog-tactics.md). Spoken video: [DEMO_SCRIPT.md](DEMO_SCRIPT.md). Product SoT: [PHASE6.md](../PHASE6.md).

**Not the short form.** Form still needs a separate short write-up (problem / build / AWS / Cursor). This article is the longer Builder Center post; paste its public URL into the submission.

**Timing:** Do **not** burn Thursday morning. Fill screenshots + “what fought back” + live links after **G-VIDEO** and Ship It URL. Human publishes at [builder.aws.com/create/content](https://builder.aws.com/create/content).

**Tags (≤5):** `Hackathon` · `Environmental Hacks` · `Serverless` · `DynamoDB` · `AWS`

---

## Title (paste)

DisputePoint: DM triage for disputed Delhi waterlogging points under rain (Environmental Hacks)

## Description (paste — 1–2 sentences)

A queue-first tool for a Delhi DM coordination cell: under monsoon rain, rank disputed waterlogging points, show who should act — or honest null when ownership conflicts — with evidence and human ACK/OVERRIDE.

---

## Article body (paste into Builder Center; replace placeholders)

### 1. Promise

Heat and Water track. User = DM cell officer, not a citizen inbox and not a citywide flood heatmap.

DisputePoint answers: which disputed point needs action first under rain, which agency should act (or UNCERTAIN / null), and why — with cited evidence and a visible audit trail.

### 2. The problem

During monsoon, multi-agency disputed waterlogging points stall while agencies pass the buck. Delhi’s High Court has called out enormous confusion over who does what on drains and related work (public record).

**Public FACT anchors (write-up, not invented stats):**

- [Delhi HC order PDF (LiveLaw)](https://www.livelaw.in/pdf_upload/pms28072025cw131902024201344-613072.pdf)
- [TOI — much confusion on who does what](https://timesofindia.indiatimes.com/india/much-confusion-on-who-does-what-even-upkeep-of-drains-hc-to-delhi-government/articleshow/122963747.cms)

We do not invent death counts. We do not invent a single owner when ownership conflicts.

### 3. What we built

Queue-first UI + point card:

1. Ranked queue of disputed points  
2. Rain context (live / cache / slider) re-ranks the list  
3. Ownership CONFLICT → `responsible_agency` stays **null**; quotes and source URLs stay visible  
4. Advisory next step; officer **ACK / OVERRIDE / ESCALATE** with **DecisionAuditPanel**

**Links (fill after deploy / record):**

- Public repo: `_REPO_URL_`  
- Ship It URL: `_SHIP_IT_URL_`  
- Demo video (≤3 min): `_YOUTUBE_URL_`

![Queue-first UI under rain — alt: DisputePoint ops queue showing ranked disputed points with rain mode banner](_SCREENSHOT_QUEUE_)

![Point card CONFLICT with responsible agency null — alt: point card showing ownership CONFLICT and null agency with evidence chips](_SCREENSHOT_CONFLICT_)

### 4. Safety invariant

| Rule | Behavior |
|------|----------|
| `ownership_state == CONFLICT` | `responsible_agency = null` always |
| U | Coordination uncertainty — not physical flood severity |
| Evidence | Quote ⊆ source; no silent ownership from LLM |
| Synthetic | Marked honest if readiness is synthetic |

### 5. Architecture (Ship It)

```text
Open-Meteo / fixtures
        ↓
   EventBridge          (rain poll / re-rank trigger)
        ↓
     Lambda             (decision API + rain refresh)
   ┌────┴────┐
DynamoDB    S3          (points + HITL audit | evidence + static UI)
   ↓
API Gateway → Frontend
(+ CloudWatch logs)
```

| Service | Role |
|---------|------|
| EventBridge | Schedule rain ingest / re-rank |
| Lambda | Decision engine + rain refresh |
| DynamoDB | Points, recommendations, HITL audit |
| S3 | Evidence corpus + static UI |
| API Gateway | HTTPS front door |
| CloudWatch | Logs / demo observability |

SAM CLI builds and deploys this stack. Cognito and map Location Service are out of MVP.

**Why these services (tradeoffs):** EventBridge beats a cron-on-laptop for a judge-visible schedule. Lambda keeps the decision path serverless and Free Tier–friendly. DynamoDB stores HITL audit without standing up RDS. S3 hosts evidence + static UI without Amplify auth surface. API Gateway is the only public HTTPS door. CloudWatch proves the invoke on camera. We cut Cognito (single-tenant demo), Location Service (queue-first product), and ML runtime (Phase 6 no-KEEP).

### Failure modes (what we degrade to)

| Failure | Behavior |
|---------|----------|
| Open-Meteo timeout | Cache then scenario slider; mode banner stays honest |
| AWS / Ship It down | Local FastAPI + fixtures still run the DEMO_SCRIPT story |
| Missing fixture point | Empty-state copy — never invent points or owners |
| CONFLICT ownership | `responsible_agency` stays **null**; quotes stay; human HITL only |

HITL: ACK / OVERRIDE / ESCALATE write an audit row the officer can see. No silent LLM ownership.

### 6. Golden path (matches the demo)

1. Open queue in `dry` — scattered workarounds become one ranked list.  
2. Trigger rain (`rain-spike` / slider) — ranks flash; mode banner shows live/cache/slider.  
3. Open a CONFLICT point (e.g. Purana Quila path) — agency null; evidence chips stay.  
4. Advisory next step → ACK or OVERRIDE → audit row visible.  
5. Show AWS: architecture diagram + Ship It URL or console invoke (API Gateway → Lambda → DynamoDB/S3).

Spoken script for the video: [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

### 7. What fought back

_Fill during the event with one real incident only:_

| Field | Fill |
|-------|------|
| Symptom | `_…_` |
| Root cause | `_…_` |
| Fix | `_…_` |
| Proof | `_test name or screenshot_` |

Do not invent a failure. If nothing painful shipped, write the hardest Phase 6 lock you had to keep (e.g. refusing to invent an owner under CONFLICT) and show the UI proof.

### 8. Limits and next

- Fixture-scale demo; not citywide hydraulic truth  
- No ML runtime in MVP (Phase 6 gate)  
- Geocodes / MapHUD only after human verify  
- Next: ward pilot on time-to-confirmation under real rain windows  

### 9. AI tools and credits

- AI coding tools: **Cursor** (and any others used — list all)  
- Data: Open-Meteo (CC-BY 4.0 attribution in UI); fixture evidence with source links  
- Third-party code/assets: see `docs/build/LICENSE_AUDIT.md` in the submission repo  

---

## Interview-surface acceptance (before G-VIDEO)

- [ ] Article (or README) states CONFLICT→null in plain language  
- [ ] AWS table has one-line **why** per service (not name-drop only)  
- [ ] Failure-modes table present (rain / AWS / empty / CONFLICT)  
- [ ] HITL + audit called out  
- [ ] Limits section does not claim production citywide truth  

## Publish checklist (human)

1. [ ] Ship It URL + YouTube live; smoke path twice ([DEMO_REHEARSAL.md](DEMO_REHEARSAL.md))  
2. [ ] Replace `_REPO_URL_`, `_SHIP_IT_URL_`, `_YOUTUBE_URL_`, screenshots, fought-back  
3. [ ] Interview-surface acceptance above PASS  
4. [ ] Builder Center: `+` → Create article → paste title/description/body → tags (≤5)  
5. [ ] Preview; alt text on images; Preview mobile-ish readability  
6. [ ] Publish → moderation → open URL **signed out**  
7. [ ] Paste article URL into hackathon form (separate from short write-up)  
8. [ ] Close residual **R-BLOG-BUILDER** when URL is live and linked  

---

## Short form (separate — for the submission form only)

Copy-edit after the article exists; keep short:

> **Problem:** DM cell officers lose time on disputed Delhi waterlogging points when agencies pass the buck under monsoon.  
> **Build:** DisputePoint — queue-first triage under rain; CONFLICT keeps responsible agency null; HITL ACK/OVERRIDE/ESCALATE with audit.  
> **AWS:** API Gateway, Lambda, DynamoDB, S3, EventBridge, CloudWatch (Ship It).  
> **AI tools:** Cursor.  
> **Builder Center article:** `_ARTICLE_URL_`
