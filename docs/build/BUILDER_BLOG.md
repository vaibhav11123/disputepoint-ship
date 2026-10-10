# BUILDER_BLOG — AWS Builder Center article draft

**Purpose:** Paste-ready article for Environmental Hacks **Top 5 blogs (AirPods)**. Story arc: civic problem → engineering decision → lessons. Public-cost cites: [research/public-cost-of-waterlogging.md](../research/public-cost-of-waterlogging.md). Spoken video: [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

**Not the short form.** Form still needs a separate short write-up. Publish at [builder.aws.com/create/content](https://builder.aws.com/create/content).

**Tags (≤5):** `Hackathon` · `Environmental Hacks` · `Serverless` · `DynamoDB` · `AWS`  
*(Do not use Artificial Intelligence / Bedrock as headline tags — MVP has no ML runtime. Story research: [research/builder-blog-story-pass-2026-10-10.md](../research/builder-blog-story-pass-2026-10-10.md).)*

**Central argument:** Make responsibility and uncertainty visible — do not invent an owner when claims conflict (`CONFLICT` → `responsible_agency` null).

**Hackathon note (sidebar / author line, not the lede):** Built for WeMakeDevs × AWS Environmental Hacks (Heat and Water). AI coding tools: Cursor (disclose; not the product thesis).

---

## Title (paste)

When Delhi’s Roads Flood, Who Needs to Act? Building DisputePoint on AWS

## Description (paste — 1–2 sentences)

Waterlogging is not just an infrastructure problem. Coordinating a response can also mean navigating incomplete evidence and competing claims of responsibility. This article explores how we built DisputePoint on AWS to help incident commanders review evidence, handle disputed ownership, and record decisions without manufacturing certainty.

---

## Article body (paste)

# When Delhi’s Roads Flood, Who Needs to Act? Building DisputePoint on AWS

When a road floods during Delhi’s monsoon, the consequences are immediate. Commuters lose time, vehicles can become stranded, and residents may face recurring disruption.

Responding to a waterlogging incident can involve multiple agencies with different responsibilities. When responsibility is unclear, the response team needs to establish what is known, what remains disputed, and who should take the next action.

In July 2025, the Delhi High Court highlighted coordination problems among civic agencies dealing with drainage and flooding. Later proceedings also recorded coordination between agencies and residents over drainage-related issues. These proceedings provide context for the problem we wanted to explore with DisputePoint. They do **not** establish that every waterlogging incident is caused by an ownership dispute, and they do not endorse this product. ([TOI](https://timesofindia.indiatimes.com/india/much-confusion-on-who-does-what-even-upkeep-of-drains-hc-to-delhi-government/articleshow/122963747.cms) · [LiveLaw](https://www.livelaw.in/high-court/delhi-high-court/delhi-high-court-government-flood-management-299427) · [Delhi High Court order, 19 Aug 2025](https://delhihighcourt.nic.in/app/showFileJudgment/PMS19082025CW131902024_164406.pdf))

**DisputePoint is a prototype for coordinating waterlogging incidents, reviewing responsibility claims, and recording decisions in one operational workflow.**

## The problem we wanted to solve

A map can show where an incident is reported. The response team still needs to answer:

- Which incidents need attention first?
- What evidence is available?
- Which agency is responsible, if that can be established?
- What should happen when available claims conflict?
- How can a decision and its rationale be recorded?

We focused on the coordination problem rather than building another citywide flood visualization. On Builder Center, flood-map and AI-alert projects already occupy that lane — DisputePoint is deliberately **not** a heatmap, citizen inbox, or flood predictor.

The prototype is designed for an incident commander or coordination officer who needs to review incidents, understand responsibility claims, and coordinate the next action.

The objective is not to replace an official’s judgment. It is to make the information and decisions surrounding that judgment easier to inspect.

## What we built

DisputePoint brings an incident queue, a map, an evidence view, and a responsibility workflow into one interface.

The workflow is:

`INCIDENT → PRIORITY → CLAIMS → EVIDENCE → DECISION → ACTION → AUDIT`

The application distinguishes three ownership states:

| State | Meaning |
|-------|---------|
| `ASSIGNED` | Responsibility is assigned to an agency |
| `CONFLICT` | Competing claims remain unresolved |
| `UNKNOWN` | Available evidence does not establish responsibility |

These states are not just labels. They determine what the system is allowed to do next.

### Designing for uncertainty instead of hiding it

One design decision shaped the rest of DisputePoint: when evidence supports competing responsibility claims, the system must not automatically select an agency.

In our ownership model, `CONFLICT` means the responsible agency remains unassigned (`responsible_agency = null`). The incident can still be prioritized, the available evidence can still be reviewed, and an officer can still take the next step. What the system cannot do is pretend that the disagreement has already been resolved.

For example, open Okhla (or Samaypur Badli) in the live queue. Responsibility remains disputed. Competing claims and source material stay visible. An authorized officer can escalate or override after review; confirmation applies when a clear agency is already assigned. The decision and rationale stay in the audit trail.

This distinction matters because an operational interface can look complete while concealing uncertainty. We wanted the unresolved state to remain visible until an authorized human decision is recorded.

The result is a workflow that represents uncertainty explicitly rather than treating every incident as a classification problem with a mandatory answer.

The system does not use an AI-generated answer to silently resolve conflicting ownership claims.

## Keeping priority separate from responsibility

Rainfall matters to waterlogging response, but it answers a different question from asset ownership.

Rainfall can be relevant to how urgently an incident needs attention. It cannot, by itself, establish who maintains a drain or road.

DisputePoint treats priority and responsibility as separate decisions. When live Open-Meteo observations are available, or when an operator applies a rainfall scenario, the backend recalculates priority scores from the configured model inputs (including rainfall). The mode banner shows whether rain is live, cached, or scenario-driven so that a demonstration scenario is not mistaken for a historical flood measurement.

A higher position in the queue has not been validated against emergency-response outcomes. It is a prototype ranking for triage, not a certified urgency score.

## Connecting evidence to decisions

The evidence view is intended to help an officer examine what supports a claim and what remains missing — source, quotation, verification status, and relationship to the decision.

A source existing is not the same as a claim being verified. A quotation being accurately extracted is not the same as that quotation establishing jurisdiction over a particular asset. Court quotations may still need human review of context and legal meaning before anyone treats them as settling ownership.

The current prototype contains a **35-location** Delhi incident corpus and supporting evidence fixtures. The corpus demonstrates the workflow. It should not be interpreted as a comprehensive or independently verified account of every incident or agency responsibility in Delhi. Illustrative volunteer rows and synthetic readiness labels stay marked as such.

## Deploying the prototype on AWS

We deployed the DisputePoint frontend as a static web application on S3 and exposed the backend through API Gateway and Lambda. DynamoDB stores invoke stamps and workflow-related audit records; S3 also holds the private evidence/runtime snapshot used on cold start. EventBridge schedules rain refresh (every 15 minutes) and evidence-verification batches (hourly). CloudWatch receives Lambda logs for the decision function.

We chose this serverless shape to build and deploy the prototype without managing a fleet of application servers. The current deployment demonstrates the application’s workflow. It does not establish production readiness for a citywide emergency-management system.

- **Repository:** https://github.com/vaibhav11123/disputepoint-ship  
- **Live application:** http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com  
- **Backend API:** https://olnsv0shee.execute-api.ap-south-1.amazonaws.com  
- **Architecture:** http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html  

*(Upload screenshot: `docs/assets/readme-queue.png` — alt: DisputePoint incident queue showing waterlogging places with disputed responsibility visible.)*

When Open-Meteo is unavailable, the UI can fall back to cache or a labeled scenario slider. When ownership conflicts, the agency field stays empty until a human decision is recorded. Missing fixture points produce an empty state — we do not invent owners.

## Three lessons from building DisputePoint

### 1. A system should be able to say “we don’t know yet”

Many interfaces are designed around selecting a single result. In a responsibility workflow, forcing a result can conceal the most important fact: the available evidence is inconclusive.

Representing uncertainty explicitly allows the system to remain useful without pretending to know more than it does.

### 2. Related signals should not become interchangeable

Rainfall, priority, evidence quality, and responsibility all matter, but each answers a different question.

Keeping them separate makes the system easier to reason about and reduces the risk of an unsupported signal determining an unrelated decision.

### 3. Human decisions need enforceable rules and an audit trail

A human-in-the-loop label is not enough by itself. The backend must enforce who can make a decision, which state transitions are allowed, and what must be recorded — for example, confirmation only when ownership is already assigned; escalate/override when disputed.

The interface should make the workflow understandable, while the backend protects its invariants.

## What remains to be proven

DisputePoint is a hackathon-stage prototype, not a validated citywide emergency-management system.

Its current corpus is limited in size and coverage. The application does not establish live flood depth, provide a validated flood-prediction model, or prove that its queue improves real-world response times.

The next step would be a ward-level pilot with relevant response teams and verified asset and jurisdiction records.

We would measure:

- Time from incident intake to a documented responsibility decision  
- Time from responsibility confirmation to an acknowledged action  
- The proportion of disputed incidents resolved with documented evidence  
- The proportion of incidents that remain unresolved because required evidence is missing  

These are proposed evaluation metrics, not results demonstrated by the current prototype.

The larger question is whether making incident priority, responsibility, and evidence more visible helps response teams coordinate their work more effectively. That needs to be tested with the people who would use the system.

## Try the prototype

Explore the [live DisputePoint application](http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com) or inspect the [AWS architecture](http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html). Source: [github.com/vaibhav11123/disputepoint-ship](https://github.com/vaibhav11123/disputepoint-ship).

**AI tools and credits:** Cursor. Rain observations via Open-Meteo (CC-BY 4.0). Third-party quotation notes: `docs/build/LICENSE_AUDIT.md` in the repository.

**For builders:** How would you model conflicting responsibility claims in an operational workflow? Would you use explicit ownership states, an evidence graph, or another approach?

I’d be interested in how others would handle the boundary between automated prioritization and a decision that must remain with an authorized human.

---

## Short form (submission form only)

> **Problem:** When Delhi roads flood, people lose time and get stranded; response teams also struggle when agencies disagree on who must act.  
> **Build:** DisputePoint — queue-first incident coordination; CONFLICT keeps agency null; evidence + human escalate/override with audit.  
> **AWS:** API Gateway, Lambda, DynamoDB, S3, EventBridge, CloudWatch.  
> **AI tools:** Cursor.  
> **Builder Center article:** `_ARTICLE_URL_`

---

## Publish checklist (human)

1. [ ] Confirm live `/health` rain mode wording matches the article (live vs scenario)  
2. [ ] Okhla / Samaypur path: CONFLICT null + evidence visible; no ACK on conflict  
3. [ ] Upload `docs/assets/readme-queue.png` with alt text  
4. [ ] Add YouTube when recorded ([DEMO_SCRIPT.md](DEMO_SCRIPT.md))  
5. [ ] Publish on Builder Center; open signed-out; paste URL into form  
