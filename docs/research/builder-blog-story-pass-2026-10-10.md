# Builder blog story pass — market research (2026-10-10)

**Purpose:** Validate the pre-publish story brief (people-first + lessons-first; CONFLICT→null as thesis) against live Builder Center / WeMakeDevs signals before publishing.  
**Channels:** Exa `web_search_exa` + `agent_run_235d2549e4c54f719b896a8174d7098e`; prior tactics [builder-center-blog-tactics.md](builder-center-blog-tactics.md).  
**Hard stop:** Do not reopen Phase 6; do not drift to flood heatmap / citizen inbox / ML KEEP.

---

## Verdict on the brief

| Decision in brief | Research call |
|-------------------|---------------|
| Combine **people-first open** + **lessons-first heart** (CONFLICT refuses to guess) | **KEEP** — strongest distinctive claim on Builder Center vs flood-map peers |
| Title: *When Delhi's Roads Flood, Who Needs to Act? Building DisputePoint on AWS* | **KEEP** — problem + product + AWS; better than engineering-catalog titles |
| Project story with technical depth (not pure tutorial) | **KEEP** — matches JalDrishti / NER Landslide Guard tone |
| Tags including **Artificial Intelligence** | **REJECT** — MVP has no ML runtime; peers already own “AI flood” |
| Wait until repo / screenshots / demo tell the same story | **KEEP** — rules: if not on video, it doesn’t count; article must not overclaim |

**Central argument (locked):** DisputePoint makes responsibility and uncertainty visible so incident commanders can decide with evidence — it does not invent an owner when claims conflict.

---

## Competitive landscape on Builder Center (**FACT** / **DERIVED**)

| Post | Pattern | DisputePoint move |
|------|---------|-------------------|
| [Waterlog Watch](https://builder.aws.com/learn/topics/hackathon?tab=article) — “AI-verified flood alerts… live flood map and route checker” (Bedrock, Location) | Map / AI verify / citizen-facing flood surface | **Differentiate hard:** queue-first coordination, **not** another flood map; no Bedrock in MVP |
| [JalDrishti](https://builder.aws.com/content/3KQgBJLLDbf86A84W90dreaCC7m/building-jaldrishti-a-serverless-water-decision-support-platform-with-aws-lambda-and-dynamodb) | Transparent assumptions, serverless water decision-support, honest limits | Match **honesty tone**; differ on **inter-agency ownership conflict**, not water-balance forecasting |
| [NER Landslide Guard](https://builder.aws.com/content/3Jb5uz9WfQ7qHLMiDrnfWH5m29W/building-ner-landslide-guard-an-aws-powered-early-warning-platform-for-northeast-india) | Disaster workflow + prototype limitations | Match structure: problem → build → AWS → limits → next |
| [Sewa Sahayak / Reporting Wall](https://builder.aws.com/content/3BqNlwGSGMknFc1Kj5TiIRqrrMl/breaking-the-reporting-wall-automating-civic-action-with-amazon-bedrock-and-sagemaker) | Citizen reporting → agency portals | **Reject** citizen-inbox framing (Phase 6) |

Exa agent DERIVED: lead with one coordination failure + smallest working path + CONFLICT behavior; use negative scope (no heatmap / no inbox / no ML) as credibility.

---

## Angle scoring

| Angle | Fit for AirPods blog | Risk |
|-------|----------------------|------|
| People-first alone | High empathy | Looks like advocacy; weak “builder” signal |
| Engineering-first alone | High AWS checklist | Generic serverless write-up; loses Delhi hook |
| Lessons-first alone | Memorable thesis | Can feel abstract without lived-cost open |
| **People + lessons (recommended)** | Best | Must keep AWS section concrete (Ship It services only) |

Engineering-first title from Exa (“without becoming another flood map”) is a good **subtitle / H2**, not a replacement for the chosen title.

---

## Form metadata (publish)

**Title:** When Delhi’s Roads Flood, Who Needs to Act? Building DisputePoint on AWS  

**Description (prefer brief’s version):** Waterlogging is not just an infrastructure problem. Coordinating a response can also mean navigating incomplete evidence and competing claims of responsibility. This article explores how we built DisputePoint on AWS to help incident commanders review evidence, handle disputed ownership, and record decisions without manufacturing certainty.

**Tags (≤5) — use these:**

1. `Hackathon`  
2. `Environmental Hacks` (or closest available)  
3. `Serverless`  
4. `DynamoDB` (or `Architecture` if DynamoDB tag missing)  
5. `AWS`  

**Do not tag:** Artificial Intelligence / Bedrock / ML as headline tags.

**Cover:** `docs/assets/readme-queue.png` (queue with disputed states). No neon AI art.

**Workflow string (align with README):**  
`INCIDENT → PRIORITY → CLAIMS → EVIDENCE → DECISION → ACTION → AUDIT`

---

## Pre-publish gate

- [x] Public repo + Ship It URLs live  
- [x] Queue screenshot asset present  
- [x] Article thesis = CONFLICT → null + HITL  
- [ ] YouTube ≤3 min with AWS on camera (still open — article can ship first; form needs video)  
- [ ] Human Publish → signed-out URL → paste into form + `_ARTICLE_URL_`

---

## Citations

- Exa agent `agent_run_235d2549e4c54f719b896a8174d7098e`  
- [Hackathon topic articles](https://builder.aws.com/learn/topics/hackathon?tab=article)  
- WeMakeDevs [rules](https://www.wemakedevs.org/aws/env/rules) — AWS must show in video  
- Internal: [BUILDER_BLOG.md](../build/BUILDER_BLOG.md) · [builder-center-blog-tactics.md](builder-center-blog-tactics.md)
