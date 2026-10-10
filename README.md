# DisputePoint Response Intelligence

**When Delhi floods, who is responsible for acting?**

Rain creates the emergency. Disputed responsibility creates the delay. DisputePoint helps incident commanders turn fragmented evidence into accountable action.

DisputePoint is an incident-coordination system for waterlogging response. It helps district incident commanders prioritize reported locations, examine competing agency claims, review supporting evidence, and record who must act.

The problem isn't just finding water on a map. It's getting the right agency to act when responsibility is unclear.

**Built for [WeMakeDevs × AWS Environmental Hacks](https://www.wemakedevs.org/aws/env).**

[Live Demo](http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com)
· [AWS Architecture](http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html)
· [Demo Video](#demo-video)

![DisputePoint incident queue — disputed underpasses ranked for coordination](docs/assets/readme-queue.png)

*Live queue: real Delhi waterlogging places (Okhla, Samaypur Badli, Minto…). Disputed responsibility stays visible — the system does not invent an owner.*

---

## The problem

During intense monsoon rainfall, waterlogging can disrupt roads, underpasses, and essential transport corridors across Delhi.

Responding to an incident involves more than identifying its location. Teams must establish which agency is responsible, determine what the available evidence supports, and coordinate an accountable response.

When multiple agencies make competing claims, responsibility can remain unresolved precisely when a quick decision matters most. Delhi’s High Court has described this as **enormous confusion** among civic agencies that leads them to **pass the buck** ([LiveLaw order PDF](https://www.livelaw.in/pdf_upload/pms28072025cw131902024201344-613072.pdf) · [TOI](https://timesofindia.indiatimes.com/india/much-confusion-on-who-does-what-even-upkeep-of-drains-hc-to-delhi-government/articleshow/122963747.cms)).

Existing maps can show where a problem is. DisputePoint focuses on the operational question that follows:

**Who needs to act, what evidence supports that decision, and what happens next?**

## What DisputePoint does

DisputePoint gives an incident commander one queue for prioritizing incidents and coordinating responsibility decisions.

- **Prioritize incidents:** Review waterlogging locations in a queue ordered by operational priority (including rainfall urgency).
- **Resolve responsibility disputes:** Examine competing agency claims without automatically assigning responsibility when the evidence conflicts.
- **Trace the evidence:** Inspect available supporting material, sources, and verification status.
- **Keep humans in control:** Require an authorized officer to escalate, override, or confirm — the model never silently owns a disputed point.
- **Preserve accountability:** Record decisions and actions in an auditable workflow.
- **Coordinate through a map:** Inspect incident locations alongside the operational queue.

DisputePoint is **not** a citizen complaint inbox or simply another flood visualization dashboard. It is a coordination layer between incident evidence and accountable action.

## How it works

Operational workflow:

`INCIDENT → PRIORITY → CLAIMS → EVIDENCE → DECISION → ACTION → AUDIT`

### 1. Triage

The incident commander reviews the queue and identifies locations requiring attention.

### 2. Examine responsibility

Each incident has an ownership state:

| State | Meaning | System behavior |
|-------|---------|-----------------|
| `ASSIGNED` | Evidence supports a responsible agency | The responsible agency is displayed |
| `CONFLICT` | Competing claims remain unresolved | **No** responsible agency is assigned automatically (`responsible_agency` stays `null`) |
| `UNKNOWN` | Available evidence does not establish responsibility | Further evidence is needed |

### 3. Review evidence

The officer examines the available evidence, its source, verification status, and relevance to the responsibility decision.

### 4. Make an accountable decision

Where responsibility is disputed, the system preserves the conflict until an authorized human reviews the evidence and confirms a decision (escalate / override). Confirmation (ACK) applies when a point already has a clear assigned agency.

### 5. Maintain an audit trail

Decisions and subsequent actions remain part of the incident’s operational history.

## What makes it different

### Uncertainty is a state, not a reason to guess

A system that always names an agency can look decisive while being wrong.

DisputePoint explicitly represents unresolved responsibility. If claims conflict, the system does not manufacture a single answer just to complete the workflow:

**`ownership_state == CONFLICT` → `responsible_agency = null` always.**

### Evidence and decisions stay connected

The goal is not merely to display documents. It is to help an officer understand what the available evidence supports and what remains unresolved.

### Rainfall does not determine ownership

Rainfall can influence operational urgency. It cannot establish which agency is responsible for an asset.

Priority and responsibility are treated as separate decisions.

### Human confirmation is part of the workflow

Disputed responsibility requires an authorized officer’s decision rather than an automatic assignment based on incomplete or conflicting evidence.

## AWS architecture

DisputePoint is deployed on AWS (Ship It). The operational workflow above is what the product is; AWS is how it runs in production.

| Service | Role in this deploy |
|---------|---------------------|
| **Amazon API Gateway** | HTTPS API for the UI (`/points`, `/health`, HITL routes, rain controls) |
| **AWS Lambda** | Runs the FastAPI decision app (Mangum) |
| **Amazon DynamoDB** | Invoke / audit stamps for the Ship It path |
| **Amazon S3** | Private evidence/runtime storage + **static website** for the UI |
| **Amazon EventBridge** | Schedules rain refresh (15 min) and evidence verification (1 hour) |
| **Amazon CloudWatch** | Lambda logs for the decision function |

[Open the architecture diagram](http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html) · Operator notes: [`docs/operations/AWS_OPERATOR.md`](docs/operations/AWS_OPERATOR.md)

## Demo

| Surface | URL |
|---------|-----|
| **Live application** | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com |
| **Backend API** | https://olnsv0shee.execute-api.ap-south-1.amazonaws.com |
| **AWS architecture** | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html |

### Demo video

YouTube link will be added when the ≤3 min recording is published. Spoken walkthrough: [`docs/build/DEMO_SCRIPT.md`](docs/build/DEMO_SCRIPT.md).

The demonstration follows an incident from queue prioritization through evidence review, responsibility handling (honest null under conflict), human escalate/override, and audit — with AWS visible on camera.

## Run locally

### Prerequisites

- Python 3.12+
- Node.js and npm
- AWS credentials only if you intend to deploy

### Installation

```bash
git clone https://github.com/vaibhav11123/disputepoint-ship.git
cd disputepoint-ship

cp .env.example .env
make install
```

Configure only the variables you need. Never commit credentials or `.env`.

### Tests

```bash
make test
```

### Start the application

```bash
make run
```

Development UI: `http://127.0.0.1:5173` · API: `http://127.0.0.1:8000` (`DP_LIVE_FETCH=1` by default in `make run`).

### Deploy

```bash
make deploy
```

Uses the repository’s AWS SAM + S3 workflow (profile `disputepoint`, region `ap-south-1`). Read [`docs/operations/AWS_OPERATOR.md`](docs/operations/AWS_OPERATOR.md) before deploying.

## Project status and limitations

DisputePoint is a hackathon-stage prototype focused on incident triage, responsibility disputes, evidence review, and human-in-the-loop coordination.

The repository includes a **35-location** Delhi incident corpus and supporting evidence fixtures used for demos and evaluation. Fixture data, illustrative volunteer rows, and live-source observations are distinguished by provenance in the data model (for example synthetic readiness flags and evidence channels). Assigned agencies appear only when the ownership engine supports them from fixture evidence — not from invented official orders or fake telemetry.

The application is not a substitute for official emergency-management systems, verified jurisdiction records, or an authorized officer’s judgment.

It does **not** claim live flood-depth measurements, CCTV intelligence, SCADA telemetry, DM-71 GPS, or predictive flood warnings.

AI coding tools used in development: **Cursor** (disclose in the hackathon write-up).

## Repository guide

| Resource | Purpose |
|----------|---------|
| [`docs/README.md`](docs/README.md) | Documentation index |
| [`docs/PHASE6.md`](docs/PHASE6.md) | Frozen product and engineering contract |
| [`AGENTS.md`](AGENTS.md) | Engineering constraints and hard stops |
| [`docs/agent/AGENT_CONSTITUTION.md`](docs/agent/AGENT_CONSTITUTION.md) | Agent operating rules |
| [`docs/build/DEMO_SCRIPT.md`](docs/build/DEMO_SCRIPT.md) | Demo walkthrough (spoken VO) |
| [`docs/build/AWS_DEMO_BEAT.md`](docs/build/AWS_DEMO_BEAT.md) | AWS demonstration sequence |
| [`docs/operations/AWS_OPERATOR.md`](docs/operations/AWS_OPERATOR.md) | Deployment and operations |
| [`docs/research/`](docs/research/) | Research, evidence audits, and source notes |
| [`infra/`](infra/) | SAM / Ship It infrastructure |

## License

MIT. See [`LICENSE`](LICENSE).

Third-party data and quotation notes: [`docs/build/LICENSE_AUDIT.md`](docs/build/LICENSE_AUDIT.md).
