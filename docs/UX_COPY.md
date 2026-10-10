# UX_COPY — DisputePoint product language SoT

**Status:** locked for product chrome. Phase 6 still wins on product conflicts.  
**Consumer:** [`frontend/src/lib/copy.ts`](../frontend/src/lib/copy.ts)

## Doctrine

Product language answers only:

1. WHAT HAPPENED?
2. WHAT NEEDS ATTENTION?
3. WHY IS IT DISPUTED?
4. WHAT DO I NEED TO DO?
5. WHAT WILL BE RECORDED?

Tone: short, specific, calm. No engineering/demo leak in normal chrome. DEMO/SCENARIO provenance is secondary. AWS = architecture only. Story progresses across screens (no six-screen repetition of the same warning).

Hard stops: CONFLICT ⇒ null agency / automatic assignment blocked; U ≠ severity; no invent SCADA/GPS; no personal phones.

## Vocabulary

| Concept | Canonical |
|---|---|
| Brand | DisputePoint |
| Descriptor | District incident coordination |
| Role | Incident Commander |
| Environment | New Delhi District · Operations |
| Queue | Incident queue |
| Attention | Awaiting review |
| Dispute | Responsibility disputed |
| Claims | Competing responsibility claims |
| Block | Automatic assignment blocked |
| Human | Human review / Responsibility decision |
| Confirmed | Officer confirmed |
| Evidence | Case evidence / What the evidence establishes / What remains unresolved |
| Next | Next action / Escalate for review |
| Rain | Rainfall / Rainfall scenario |
| Modes | Live · Scenario · Unavailable |
| Synthetic | Scenario |
| Map | Location context |
| AWS | Architecture only |

## Screen narrative

Command → Incident → Evidence → Coordination → Decision → Audit (one chapter each).

## String map

Format: KEY · CURRENT · ACTION · FINAL · SCREEN · RATIONALE

### Brand / shell

| KEY | CURRENT | ACTION | FINAL | SCREEN | RATIONALE |
|---|---|---|---|---|---|
| brand.name | DisputePoint | KEEP | DisputePoint | global | Memorable |
| brand.descriptor | (missing) | ADD | District incident coordination | TopBar | Product descriptor |
| brand.htmlTitle | DisputePoint | REWRITE | DisputePoint · District Incident Coordination | index.html | Tab context |
| brand.awsArchTitle | DisputePoint — AWS architecture (demo beat) | REWRITE | DisputePoint · Operational Architecture | aws-arch.html | AWS not in title |
| brand.awsArchSub | (missing) | ADD | Event-driven incident state, evidence, and audit | aws-arch.html | Architecture pitch |
| chrome.skip | Skip to queue | KEEP | Skip to queue | App | A11y |
| chrome.queueFail | Queue failed to load. | REWRITE | Incident queue unavailable. | App | Ops language |
| chrome.pointFail | Point failed to load. | REWRITE | Incident details unavailable. | App | Ops language |
| chrome.loadingIncident | Loading incident… | KEEP | Loading incident… | App | Fine |
| chrome.rainBanner | Rain source verified · Ownership… | REWRITE | RAINFALL · VERIFIED | App | Split concepts |
| chrome.footerDemo | Demo | REWRITE | DEMO MODE | App | Demo path label |
| chrome.footerJudges | Judges inspection | HIDE | (hidden default) | App | Debug only |
| chrome.awsHonesty | AWS · Ship It… | DELETE | (removed from product) | App | Architecture only |

### TopBar

| KEY | CURRENT | ACTION | FINAL | SCREEN | RATIONALE |
|---|---|---|---|---|---|
| topbar.role | INCIDENT COMMANDER | KEEP | INCIDENT COMMANDER | TopBar | Bone |
| topbar.sessionActor | Session actor | DELETE | — | TopBar | Dev leak |
| topbar.env | DISTRICT OPERATIONS · NEW DELHI DISTRICT | REWRITE | NEW DELHI DISTRICT · OPERATIONS | TopBar | Ops console |
| topbar.active | Active | REWRITE | ACTIVE | TopBar | Explicit |
| topbar.high | High | REWRITE | HIGH PRIORITY | TopBar | Explicit |
| topbar.disputed | Disputed | REWRITE | DISPUTED | TopBar | Explicit |
| topbar.awaiting | AWAITING YOU N | REWRITE | AWAITING REVIEW · N | TopBar | Ops queue |
| topbar.more | More/Less | KEEP | More/Less | TopBar | Disclosure |
| topbar.hideSynthetic | Hide synthetic | REWRITE | Hide scenario rows | TopBar | Provenance word |
| topbar.judgesLabel | Judges / source controls | HIDE | (judges only) | TopBar | Debug |

### Rain / sources

| KEY | CURRENT | ACTION | FINAL | SCREEN | RATIONALE |
|---|---|---|---|---|---|
| rain.strike | Rain Strike | DELETE | — | RainControl | Hackathon name |
| rain.scenarioLine | RAINFALL SCENARIO · N mm | KEEP-ish | RAINFALL SCENARIO · N MM | RainControl | Deliberate |
| rain.label | Scenario mm | REWRITE | Rainfall | RainControl | Clean |
| rain.aria | Scenario rain millimetres | REWRITE | Rainfall millimetres | RainControl | Clean |
| rain.apply | Apply rain | REWRITE | APPLY SCENARIO | RainControl | Deliberate |
| rain.usingDemo | Using scenario rain · DEMO | REWRITE | SCENARIO RAINFALL · N MM | RainControl | Provenance secondary |
| rain.modes | Live/Cache/Slider/DEMO/IDLE | REWRITE | LIVE / SCENARIO / UNAVAILABLE | RainControl | Product modes |
| rain.liveFail | Live rain unavailable. | REWRITE | Live rainfall unavailable. | useRain | Ops |
| rain.scenarioFail | Rain scenario failed. | REWRITE | Rainfall scenario unavailable. | useRain | Ops |
| sources.volunteerScada | Volunteer ≠ SCADA | DELETE | — | LiveSources | Prototype joke |
| sources.block | Open-Meteo… | REWRITE | DATA STATUS (+ expand tech) | LiveSources | Progressive disclosure |
| sources.healthFail | Health failed. | REWRITE | Rainfall service unavailable | LiveSources | Clear |
| sources.evidenceFail | Evidence refresh failed. | REWRITE | Evidence could not be refreshed | LiveSources | Clear |
| sources.loading | Sources… | REWRITE | Sources | LiveSources | Clean |
| followStorm.* | Follow Storm… | HIDE | Demo Mode only | FollowStorm | Cinematic |

### Command / queue

| KEY | CURRENT | ACTION | FINAL | SCREEN | RATIONALE |
|---|---|---|---|---|---|
| command.region | Disputed points queue | REWRITE | Incident queue | Command | Product |
| command.hero | (missing) | ADD | District incident command | Command | Page title |
| command.heroSub | (missing) | ADD | Prioritize disputed waterlogging points and confirm who must act. | Command | One-line support |
| command.subtitle | triage strip counts | REWRITE | Cases requiring operational attention / Prioritized incidents requiring triage, review, or action. | Command | Kill prototype strip |
| command.viewDisputes | Open disputed | REWRITE | View disputes | Command | English |
| command.loading | Loading disputed points. | REWRITE | Loading incident queue… | Command | Ops |
| command.empty | No disputed points loaded. Check fixtures. | REWRITE | No disputed incidents require review. | Queue | No fixtures |
| command.queueFail | (error) | REWRITE | Incident queue unavailable. Retry. | Command | Fail path |
| queue.columns | Rank/Name/Triage/State/Agency/Priority/RainΔ | REWRITE | # / INCIDENT / STATUS / RESPONSIBILITY / PRIORITY / RAINFALL / NEXT ACTION | Queue | Drop Δ |
| triage.act | ACT | REWRITE | ACTION REQUIRED | TriageChip | Vocabulary |
| triage.adjudicate | ADJUDICATE | REWRITE | REVIEW REQUIRED | TriageChip | Vocabulary |
| triage.research | RESEARCH | REWRITE | EVIDENCE NEEDED | TriageChip | Vocabulary |
| triage.awaiting | AWAITING YOU | REWRITE | AWAITING DECISION | TriageChip | Vocabulary |
| state.officer | OFFICER CONFIRMED | KEEP | OFFICER CONFIRMED | StateChip | Bone |
| state.assigned | ASSIGNED | KEEP | ASSIGNED | StateChip | Bone |
| state.disputed | RESPONSIBILITY DISPUTED | KEEP | RESPONSIBILITY DISPUTED | StateChip | Bone |
| state.hintHuman | human review | REWRITE | REVIEW REQUIRED | StateChip | Vocabulary |
| state.hintMulti | multi-claim — no auto-pick | REWRITE | COMPETING CLAIMS · REVIEW REQUIRED | StateChip | Vocabulary |
| state.hintTheta | below θ 0.65 — escalate | DELETE | — | StateChip | Never show θ |
| map.region | District map context | REWRITE | Incident location | MapHUD | Ops |
| map.toggle | Hide/Show map | REWRITE | HIDE MAP / SHOW MAP | MapHUD | Caps OK |
| map.pin | Select name | REWRITE | VIEW INCIDENT | MapHUD | Action |
| map.credit | Positron… DEMO climax… | REWRITE | Map data · OpenStreetMap | MapHUD | Tiny footer |

### Incident / conflict / HITL

| KEY | CURRENT | ACTION | FINAL | SCREEN | RATIONALE |
|---|---|---|---|---|---|
| incident.region | Point card | REWRITE | Incident | Incident | Vocabulary |
| incident.advisory | Advisory only… | REWRITE | OPERATIONAL STATUS · AWAITING HUMAN DECISION | Advisory | No apology |
| incident.ownershipUncertain | Ownership uncertain… | REWRITE | Operational responsibility is unresolved. Escalate for Incident Commander review. | Advisory | Responsibility not ownership |
| incident.brief.conflict | RESPONSIBILITY DISPUTED — No auto-pick… | REWRITE | Title + body + blocked lines (see copy.ts) | Incident | Professional |
| incident.conf | conf N | DELETE | — | Incident | No confidence UI |
| incident.demoChip | DEMO INCIDENT | REWRITE | SCENARIO | Incident | Provenance |
| conflict.title | RESPONSIBILITY DISPUTED · CLAIMS OVERLAP | REWRITE | COMPETING RESPONSIBILITY CLAIMS | OwnershipConflict | Stronger |
| conflict.noAuto | NO AUTO-ASSIGN | REWRITE | AUTO-ASSIGNMENT BLOCKED | OwnershipConflict | Polished |
| conflict.body | Evidence supports overlapping… | REWRITE | Evidence supports competing responsibility claims. No source establishes exclusive operational responsibility. | OwnershipConflict | Clear |
| conflict.next | Next: Escalate… | REWRITE | NEXT: INCIDENT COMMANDER REVIEW | OwnershipConflict | State |
| conflict.resolve | Drain ownership record… | REWRITE | Asset / maintenance checklist (see copy.ts) | OwnershipConflict | Responsibility |
| conflict.whatResolve | WHAT WOULD RESOLVE THIS? | KEEP | WHAT WOULD RESOLVE THIS? | OwnershipConflict | Bone |
| hitl.title | Actions | REWRITE | NEXT ACTION | ActionBlock | Stronger |
| hitl.escalate | ESCALATE FOR HUMAN REVIEW | REWRITE | ESCALATE FOR REVIEW | ActionBlock | Vocabulary |
| hitl.ack | ACK | DELETE | (hidden primary) | ActionBlock | Wrong model |
| hitl.override | OVERRIDE | DELETE | (hidden primary) | ActionBlock | Wrong model |
| hitl.decision | Human decision | REWRITE | RESPONSIBILITY DECISION | ActionBlock | Vocabulary |
| hitl.decisionSub | Confirm… (IC only). | REWRITE | Incident Commander decision / Confirm operational responsibility | ActionBlock | Split |
| hitl.confirmBtn | CONFIRM DECISION | REWRITE | CONFIRM RESPONSIBILITY | ActionBlock | Vocabulary |
| hitl.placeholder | Jurisdiction record… | DELETE | (empty) | ActionBlock | Never show placeholder |
| hitl.noEvidence | No evidence ids… | REWRITE | Evidence review required before confirmation. | ActionBlock | User need |
| hitl.disabled | Confirm disabled… | REWRITE | Incident Commander approval required | ActionBlock | Clean |
| hitl.fail | Action failed. | REWRITE | Decision could not be recorded. Try again. | ActionBlock | Trust |
| hitl.success | OFFICER CONFIRMED · a · id | REWRITE | OFFICER CONFIRMED / agency · Audit id | ActionBlock | Clean |
| eventRail.steps | RAIN/PRIORITY/… | REWRITE | RECEIVED…RESOLVED lifecycle | EventRail | Lifecycle |
| place.caption | Place context · OSM… | REWRITE | LOCATION CONTEXT · MAP DATA ONLY + jurisdiction note | PlaceStrip | Distinction |
| place.unverified | Coordinates not verified | REWRITE | Location not verified | PlaceStrip | Simple |
| place.mapEmpty | No verified geocode… | REWRITE | Location could not be verified. Map unavailable. | PointFocusMap | Clear |
| readiness.line | Readiness: synthetic fixture… | REWRITE | SCENARIO DATA · NOT LIVE TELEMETRY | ReadinessBlock | Provenance |
| readiness.chip | SYNTHETIC | REWRITE | SCENARIO | ReadinessBlock | Vocabulary |

### Evidence / coordination / audit / demo

| KEY | CURRENT | ACTION | FINAL | SCREEN | RATIONALE |
|---|---|---|---|---|---|
| evidence.lead | Decision effect: evidence informs… | REWRITE | WHAT THE EVIDENCE ESTABLISHES | Evidence | Clear |
| evidence.traceBtn | Trace | REWRITE | VIEW SOURCE | EvidenceLedger | Not dev tool |
| evidence.volunteer | Volunteer report | REWRITE | Volunteer report | EvidenceLedger | Compact chip; illustrative rows also `is_synthetic=true` |
| evidence.demoFixture | DEMO / fixture | REWRITE | SCENARIO | EvidenceLedger | Provenance |
| evidence.effect | Supports X claim · Does NOT… | REWRITE | Supports X's responsibility claim · Does not establish exclusive responsibility | EvidenceLedger | Keep meaning |
| coord.title | HUMAN REVIEW REQUIRED | KEEP | HUMAN REVIEW REQUIRED | Coordination | Bone |
| coord.labels | Reason/Route/NEXT ACTION | REWRITE | WHY THIS CASE IS HERE / ROUTE / NEXT ACTION | Coordination | Brief |
| coord.copy | COPY BRIEF | REWRITE | COPY COORDINATION BRIEF | Coordination | Unambiguous |
| coord.channels | Official coordination channels | REWRITE | OFFICIAL CONTACT CHANNELS | Coordination | Vocabulary |
| coord.asOf | as-of 2026-10 | REWRITE | Contact information verified October 2026 | Coordination | Professional |
| audit.system | SYSTEM RECOMMENDED | REWRITE | SYSTEM FINDING | DecisionAudit | Philosophy |
| audit.assignTo | ASSIGN TO agency | REWRITE | OPERATIONAL RESPONSIBILITY CONFIRMED · agency | DecisionAudit | Not tickets |
| audit.actor | Actor | REWRITE | Decision maker | DecisionAudit | Record |
| audit.audit | Audit | REWRITE | Audit ID | DecisionAudit | Record |
| audit.empty | No human decision yet. | REWRITE | AWAITING HUMAN DECISION | DecisionAudit | Vocabulary |
| audit.seal | System refused auto-assign… | REWRITE | Automatic assignment was blocked… final operational decision. | HumanVerifiedSeal | Perfect audit |
| clock.owner | Owner / PENDING HUMAN ASSIGNMENT | REWRITE | RESPONSIBILITY STATUS / AWAITING DECISION | AccountabilityClock | Not asset owner |
| clock.elapsed | Elapsed | REWRITE | REVIEW AGE | AccountabilityClock | Ops |
| clock.next | Next check | REWRITE | NEXT REVIEW | AccountabilityClock | Ops |
| demo.region | Demo signature | REWRITE | THE DISPUTEPOINT WORKFLOW | Demo | Product |
| demo.headline | Signature interaction… | REWRITE | WHEN RESPONSIBILITY IS UNCLEAR, DISPUTEPOINT DOESN'T GUESS. | Demo | Headline |
| demo.sub | — | ADD | It traces the evidence, routes the decision, and records who decided. | Demo | Subtitle |
| demo.enter | Enter command | REWRITE | START INCIDENT | Demo | CTA |
| demo.purana | Open Purana climax | REWRITE | VIEW PURANA QUILA CASE | Demo | CTA |
| replay.frames | RAIN / PRIORITY ↑ / … | REWRITE | RAINFALL → … → OFFICER CONFIRMED | IncidentReplay | Story |
| judges.eval | Judges: baseline tournament… | HIDE | Debug route only | Eval* | Not product |
| judges.priority | Why this rank… | HIDE | Debug / optional CASE BASIS | PriorityExplain | Not product |

## Implementation note

Code must import from `frontend/src/lib/copy.ts`. Do not invent new chrome strings in components.
