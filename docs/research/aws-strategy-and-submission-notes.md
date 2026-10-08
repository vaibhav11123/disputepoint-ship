# Phase 6 — AWS Strategy & Submission Notes

**Purpose:** Load-bearing AWS story, Ship It vs Build It decision criteria, license gate, video beat sheet, submission package.  
**Date:** 2026-10-06  
**Official:** [rules](https://www.wemakedevs.org/aws/rules) · [First Commit / judging](https://www.wemakedevs.org/aws/first-commit) · [Environmental Hacks](https://www.wemakedevs.org/aws/env)  
**Labels:** FACT / DERIVED / ASSUMPTION

---

## 1. Why AWS? (not decoration)

**FACT:** Built on AWS is judged; video must **show** AWS; write-up alone is insufficient.

| Service | Product role | If removed, what breaks? | Keep? |
|---------|--------------|--------------------------|-------|
| EventBridge | Schedule rain poll / re-rank trigger | No timed ingest in cloud | YES (Ship It) |
| Lambda | Decision API + rain refresh | No serverless API | YES |
| DynamoDB | Durable points, ACK/override audit | No persistent HITL trail | YES |
| S3 | Fixtures, evidence corpus, static UI | No durable evidence store / static host | YES |
| API Gateway | HTTPS front door | No public URL | YES |
| CloudWatch | Structured logs / demo observability | Harder AWS proof in video | YES |
| SNS | Top-priority alert (optional) | UI toast still works | SHOULD if time |
| Bedrock | Grounded document extraction | Manual fixtures still work | IF §14A eval green |
| Cognito | Auth | Not needed for single-tenant demo | **CUT** |
| Location Service | Maps | Queue-first product; avoid map collision | **CUT** |

**Judge line (DERIVED):**  
“AWS isn’t decoration: EventBridge drives rain ingest, Lambda runs the decision engine, DynamoDB stores recommendations and human overrides, S3 holds cited evidence, API Gateway serves the ops queue — optional Bedrock extracts claims that never become ownership without validation.”

```text
Open-Meteo / public evidence
        ↓
   EventBridge
        ↓
     Lambda
   ┌────┴────┐
DynamoDB    S3
   ↓         ↓
Decision   Evidence
   ↓
API Gateway → Frontend
(+ Bedrock extract IF gate; CloudWatch; SNS opt)
```

---

## 2. Ship It vs Build It

| Criterion | Ship It | Build It |
|-----------|---------|----------|
| AWS proof in video | Live URL + console/arch | SAM/LocalStack/Strands on laptop |
| Reliability | Needs deploy green | Local more controllable |
| Deploy risk | Higher | Lower |
| Demo quality | Cleaner for judges | Must screen-record local |
| Judge comprehension | “It’s on AWS” obvious | Must narrate OSS AWS tools |
| Time | Needs SAM + account | Faster if card/account blocked |
| Amazon signal | Strong if architecture clear | Valid if OSS is load-bearing |

**Default (DERIVED):** Prefer **Ship It** if Free Tier + SAM install succeed in Phase 7; else **Build It** with SAM Local / LocalStack for Lambda+Dynamo parity — still show AWS tooling in video. Grand prize leans Ship It (**FACT** First Commit page).

**Decision gate:** Record in Phase 7 day-1 recon; do not flip mid-demo without §40 escalation.

---

## 3. License / compliance hard gate

Every external asset gets a row before submission. Block ship if any `allowed_for_demo=false` or missing attribution when required.

| Asset class | Examples | Fields required |
|-------------|----------|-----------------|
| Datasets | Open-Meteo, OpenCity rainfall, IFI Zenodo | source, URL, retrieved_at, license/terms, attribution_required, allowed_for_demo, allowed_for_redistribution |
| Documents | LiveLaw, ThePrint, HC PDFs | Fair-use quotes in fixtures; link out; no wholesale copyrighted PDF redistrib without license |
| Geo | OSM/Overpass | ODbL attribution |
| Fonts | IBM Plex (@fontsource) | SIL OFL |
| Icons | Carbon / Lucide | Package license |
| Models | Bedrock model IDs | AWS ToS; no weight redistrib |
| Code deps | FastAPI, React, SAM | LICENSE files in repo |

Template CSV/Markdown table lives in product repo `docs/build/LICENSE_AUDIT.md` (Phase 7).

---

## 4. Video beat sheet (design before coding finishes)

**FACT:** No live demo; ≤3 min YouTube; if video doesn’t show it, it doesn’t count.

| Time | Beat | On-screen proof |
|------|------|-----------------|
| 0:00 | Problem — DM cell, multi-agency disputes | One sentence + Delhi context |
| 0:20 | Real disputed case | Purana Quila / Minto from Phase 4 |
| 0:40 | Rain event | Open-Meteo or slider; mode banner |
| 1:00 | Queue reprioritizes | Rank flash; not a heatmap |
| 1:20 | Open Purana Quila card | Ops queue → detail |
| 1:40 | Conflicting agencies + evidence | Quotes + URLs |
| 2:00 | Recommended action | Advisory banner |
| 2:20 | Human ACK / override | Audit fields visible |
| 2:35 | AWS architecture | Diagram + live URL / console |
| 2:50 | Impact / close | “Better than map: names owner + why” |

First-30s test: judge must grasp **user, problem, unique decision** (ownership under rain, not flood prediction).

---

## 5. Submission package skeleton

**FACT:** Public repo + YouTube ≤3 min + short write-up. **DERIVED (env prize):** also publish a longer [AWS Builder Center](https://builder.aws.com/) article for Top 5 blogs (AirPods) and link it in the form — draft [build/BUILDER_BLOG.md](../build/BUILDER_BLOG.md); tactics [builder-center-blog-tactics.md](builder-center-blog-tactics.md).

### Repository must include

- README (problem, user, setup, demo URL, AWS diagram)
- Architecture diagram
- Setup: lockfiles, `.env.example`, `make install|test|run`
- AWS explanation (why each service)
- AI coding tools used (Cursor/etc.) — rules require listing
- Data sources + LICENSE_AUDIT
- Data honesty (synthetic badges)
- Screenshots
- Demo link

### Write-up fields

**Short form (mandatory):** Problem · User · Why maps/dashboards fail · Solution · Architecture · AWS · AI tools listed · Limitations  

**Builder Center article (AirPods):** longer build story per BUILDER_BLOG — not a paste of the short form alone; publish after G-VIDEO

### Compliance

- New work after clock starts — git policy: [docs/operations/SUBMISSION_GIT.md](../operations/SUBMISSION_GIT.md) · official [rules](https://www.wemakedevs.org/aws/rules)
- OSS attribution
- Licenses allowing use
- AI tools listed
- AWS visible in video
---

## 6. Judge-blind + clean-room (pointers)

See Phase 6 §§38–41. Run before freeze submission:

1. Blind scorer with only repo/URL/video/write-up.  
2. Fresh clone → install → golden rain scenario.  
3. Ask: Would you put this in top 10? Why not?

---

## 7. Dual optimization reminder

| Output | Success look |
|--------|--------------|
| Judge | “Holy shit — this solves a real coordination problem.” |
| Amazon/engineer | Evidence, uncertainty, baselines, HITL, AWS tradeoffs. |
