# AWS operator runbook

Live operator truth for DisputePoint AWS tooling. **Product SoT remains** [PHASE6.md](../PHASE6.md). If this file disagrees with Phase 6 product locks, follow Phase 6. Frozen Phase 6 recon tables (old CLI pins / “STS unverified”) are historical — use this page for day-1.

**Ship It is live (2026-10-10).** Build It only if the live URL dies mid-demo. Profile `disputepoint`, region `ap-south-1`. Pins below beat frozen Phase 6 recon tables.

---

## Locked identity

| Item | Value |
|------|-------|
| CLI profile | `disputepoint` |
| Deploy region | `ap-south-1` |
| Agent Toolkit configure region | `us-east-1` (toolkit default; does not change deploy region) |
| AWS CLI (verified 2026-10-07) | `aws-cli/2.37.10` at `~/.local/bin/aws` |
| SAM CLI (verified 2026-10-07) | `1.166.2` via Homebrew (`/opt/homebrew/bin/sam`) |
| Docker (Build It / `sam local`) | Present on this machine (`docker` 28.x) — required only for SAM Local failover |

```bash
export PATH="/opt/homebrew/bin:$HOME/.local/bin:$PATH"
export AWS_PROFILE=disputepoint
export AWS_REGION=ap-south-1
```

---

## Login and credential refresh

Session credentials from `aws login` expire. **Every session step 0:**

```bash
export PATH="/opt/homebrew/bin:$HOME/.local/bin:$PATH"
aws sts get-caller-identity --profile disputepoint
```

If that fails (`Unable to locate credentials` / expired):

```bash
aws login --profile disputepoint
aws sts get-caller-identity --profile disputepoint
```

Never hard-code access keys. Never commit `.env`, keys, or `runs/`. Prefer the SDK default provider chain / role credentials under profile `disputepoint`.

---

## IAM vs root

| Rule | Action |
|------|--------|
| Root | MFA on; **no root access keys**; root only for account tasks (billing, MFA, break-glass) |
| Day-to-day deploy | Profile `disputepoint` (IAM user / Identity Center / temp creds) |
| Lambda runtime | Execution role with least privilege (DynamoDB / S3 / logs as needed) — not root |
| Secrets | Env / SSM at runtime; never in git |

See [AWS root user best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).

---

## Ship It live (2026-10-10)

Stack **`disputepoint`** in **`ap-south-1`** via `make deploy` / SAM.

| Output | Value |
|--------|-------|
| API | https://olnsv0shee.execute-api.ap-south-1.amazonaws.com |
| UI | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com |
| DynamoDB | `disputepoint-PointsTable-OPB0M6XQFZH0` (invoke stamps) |
| Lambda | `disputepoint-decision` |
| EventBridge | `disputepoint-rain-15m` (15 min rain refresh) |

Smoked (live mode): `GET /health` → `live_fetch=true`, `rain_mode=live`, `rain_source_state=LIVE` (Open-Meteo); `evidence-live=LIVE` after evidence job; Dynamo stamps + S3 `runtime/disputepoint.sqlite` snapshot for cold-start continuity. Honest gates unchanged: IMD `key_required`, Google Flood `waitlist`, NWDP `investigating`.

**Demo board mix (2026-10-10):** fixtures `evidence.json` corpus **0.3.5** — honest `PRESS_REPORT` (never press typed as `GOV_ORDER`); ASSIGNED / CONFLICT / UNKNOWN under real engines (no DEMO MIX banner, no frontend rank rewrite). Dispute spine (Okhla, Samaypur, Barapullah, …) stays CONFLICT + null agency. `ensure_fixture_corpus` re-ingests when S3 sqlite lags package version; `DP_SEED_DEMO_ACK=1` ACKs Mathura Rd + Bharat Mandapam via the same HITL store path as the API.

---

## Tonight prep status (2026-10-07)

| Item | Status |
|------|--------|
| SAM CLI `1.166.2` | Done on this laptop (`brew install aws-sam-cli`) |
| Docker for `sam local` | Present (`docker` 28.x) |
| Account (STS via toolkit) | Profile `disputepoint` / region `ap-south-1` — prefer IAM user (not root) for day-to-day after MFA check |
| Local CLI `aws login --profile disputepoint` | **OK 2026-10-07** — re-run `aws sts get-caller-identity --profile disputepoint` when local STS fails |
| Promotional credits | Track Free Tier / promo credits in the Billing console; credit window noted locally through ~**2027-10-07** |
| Cost budget | **`disputepoint-zero-spend`** — $1/month COST; subscriber is the operator inbox @ 80% ACTUAL. Confirm budget email verify link in the Billing console |
| Free Tier usage alert | Defaults to root email; confirm under Billing → Billing preferences / Free Tier in **your** browser (embedded Cursor browser hit “Unable to load content”) |
| Root MFA on; no root access keys | **Still human** — Security credentials in your browser (MFA assign if missing; access keys list empty) |

## Free Tier alert + budget (human — before first deploy)

~**$125** promotional credits cover a normal Ship It weekend if you stay on the locked stack (APIGW / Lambda / DynamoDB / S3 / EventBridge / CloudWatch) and clean up after video. Credits ≠ unlimited free; they do not waive Free Tier quantity limits or surprise SKUs.

Do this **before G-AWS**:

1. Console → Billing → **Credits** / **Free Tier** — confirm ~$125 remaining and expiry if shown.
2. Confirm (or enable) the automatic Free Tier usage alert (AWS documents alerts near 85% of a limit).
3. **Budgets** → `disputepoint-zero-spend` already exists at **$1/month** as an early alarm; **add your email** as subscriber; optionally add a second budget near **$100** if you want a “credits almost gone” warning.
4. Record **budget owner** (who watches email) here when set: `_owner: _________`

Docs: [Tracking Free Tier](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/tracking-free-tier-usage.html) · [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html).

---

## Agent Toolkit (Cursor)

| Piece | Where |
|-------|--------|
| Project rules | [`.cursor/rules/aws-agent-toolkit.mdc`](../../.cursor/rules/aws-agent-toolkit.mdc) |
| MCP | Cursor `aws-mcp`; proxy profile env `AWS_MCP_PROXY_PROFILES=disputepoint` when set |
| Skills | `~/.cursor/skills` (AWS Agent Toolkit install) |

**Precedence:** root [AGENTS.md](../../AGENTS.md) + Phase 6 win over toolkit wording. Prefer AWS MCP for AWS CLI-style work when available; do not treat toolkit setup as permission to dump judged product code before the clock.

---

## Install / verify toolchain

### AWS CLI

Already on PATH via `~/.local/bin`. Refresh:

```bash
aws --version
aws sts get-caller-identity --profile disputepoint
```

### SAM CLI

```bash
brew install aws-sam-cli   # or see AWS SAM install docs
sam --version              # expect ≥ 1.166 on this laptop after 2026-10-07
```

Official: [Install SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

### Docker (Build It / `sam local` only)

Needed if G-AWS flips to Build It and you run `sam local`. Verify:

```bash
docker info
```

Install Docker Desktop if `docker info` fails and Build It is the backup path.

---

## Target shapes

| Path | Shape | When |
|------|-------|------|
| **Ship It** (preferred) | API Gateway → Lambda → DynamoDB + S3; EventBridge rain schedule; CloudWatch; static UI on S3 (or equivalent) | Free Tier + SAM + login green |
| **Build It** (failover) | SAM Local / LocalStack on laptop; still show AWS tooling on video | Ship It blocked at G-AWS |
| **Local** | FastAPI + Vite + SQLite fixtures | Default offline / story path (NFR-003) |

Out of MVP: Cognito, required CloudFront, SNS unless time, Bedrock unless §14A green. Details: [aws-strategy](../research/aws-strategy-and-submission-notes.md), [DEPLOYMENT.md](DEPLOYMENT.md), [infra/README.md](../../infra/README.md).

---

## G-AWS checklist — **cleared 2026-10-10 (Ship It)**

Recorded in `execution/work-status.json` (`WP-15.gate_open: false`). Replay anytime:

1. [x] Path = **Ship It** (not Build It)
2. [x] No secrets in git; CORS allowlist; `/docs` off on Lambda — [SECURITY.md](SECURITY.md)
3. [x] `make deploy` / SAM under `infra/`
4. [x] **Smoke:** `/health` LIVE · `/points` queue · Dynamo stamps · S3 UI · EventBridge rain+evidence
5. [x] **CORS** from S3 website origin (not `*`)
6. [ ] **Warm-up** once immediately before recording (human — G-VIDEO)
7. [x] Architecture diagram: `frontend/public/aws-arch.html` + hosted `/aws-arch.html`
8. Failover: if live URL dies, Build It / `make run` + honest narration

---

## Oct 8 start sequence (locked)

| Step | Who | Action |
|------|-----|--------|
| 0 | Human | New Cursor session; `aws sts get-caller-identity --profile disputepoint` — re-`aws login` if expired |
| 1 | Human | **G-CLOCK**: declare clock → `CLOCK_STARTED=1 ./scripts/scaffold_submission.sh` → open Cursor on this submission tree only ([SUBMISSION_GIT](SUBMISSION_GIT.md)) |
| 2 | Human | **G-PLAN**: accept [PLAN_CHECK.md](../../execution/PLAN_CHECK.md) in the **submission** tree; set `plan_gate_accepted: true` in submission `execution/work-status.json` |
| 3 | Human | `gh repo create disputepoint-ship --source=. --remote=origin --private --push` |
| 4 | Agents | **WP-00** first, then local waves (engines → API → UI). Not morning Bedrock/MapHUD/blog |
| 5 | Early | Confirm `sam --version` on PATH (installed 2026-10-07 on planning laptop) |
| 6 | After WP-07 green | Human **G-AWS**: Ship It deploy; smoke + CORS + warm URL — **done 2026-10-10** |
| 7 | WP-15 | Document public URL + architecture diagram for demo AWS beat |
| 8 | Near end | G-VIS → **G-VIDEO** (AWS visible) → public repo + form → Builder Center blog ([BUILDER_BLOG](../build/BUILDER_BLOG.md)) → **cleanup** |

### Thu hour box (IST — adjust if kickoff call shifts)

| Window | Focus | Hard stop |
|--------|--------|-----------|
| 09:00–10:00 | G-CLOCK script + G-PLAN + `gh repo create` | No product features yet |
| 10:00–13:00 | WP-00 → ownership/rank engines | No Bedrock, no MapHUD, no blog |
| 13:00–18:00 | API + queue/card golden path | Keep CONFLICT→null honest |
| 18:00–21:00 | HITL + polish + fixture smoke | Still local-first |
| Evening | Only if API green: skim G-AWS prep | Do not block story on deploy day-1 |

**Day-1 effort split:** ~60% golden path (queue / rain / CONFLICT→null / HITL), ~20% UX anti-slop, ~20% AWS proof + video prep. Blog = after G-VIDEO (**R-BLOG-BUILDER**).

**AWS identity note:** profile may resolve as root for a solo hackathon; prefer IAM user/role before any long-lived keys. Never create root access keys.

---

## Cleanup (after video)

Owner: same as budget owner (fill above).

```bash
# When a SAM stack exists and recording is done:
sam delete --stack-name <stack> --region ap-south-1 --profile disputepoint
```

Tear nonessential resources; leave only what you still need for a public demo URL if judges may click through. Avoid surprise spend after the event.

---

## LICENSE_AUDIT

Submission copy should include [docs/build/LICENSE_AUDIT.md](../build/LICENSE_AUDIT.md) per [SUBMISSION_GIT](SUBMISSION_GIT.md) / [HOWTO_REUSE](../agent/HOWTO_REUSE.md). Create or refresh that table in the Phase 7 submission repo before form submit — do not invent licenses; row every external asset.

---

## References

- [DEPLOYMENT.md](DEPLOYMENT.md) · [SECURITY.md](SECURITY.md) · [SUBMISSION_GIT.md](SUBMISSION_GIT.md)
- [infra/README.md](../../infra/README.md)
- [DEMO_SCRIPT.md](../build/DEMO_SCRIPT.md) · [DEMO_REHEARSAL.md](../build/DEMO_REHEARSAL.md) · [DEMO_WOW.md](../build/DEMO_WOW.md)
- [aws-strategy-and-submission-notes.md](../research/aws-strategy-and-submission-notes.md)
- [execution/GATES.md](../../execution/GATES.md) · [execution/START.md](../../execution/START.md)
