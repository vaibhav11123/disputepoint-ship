# AWS operator runbook

Live operator truth for DisputePoint AWS tooling. **Product SoT remains** [PHASE6.md](../PHASE6.md). If this file disagrees with Phase 6 product locks, follow Phase 6. Frozen Phase 6 recon tables (old CLI pins / “STS unverified”) are historical — use this page for day-1.

**Prefer Ship It.** Build It only if deploy is blocked. No product deploy before [G-CLOCK](../../execution/GATES.md) in a fresh submission repo. Tonight’s login / SAM / budget work is tooling only.

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

## Tonight prep status (2026-10-07)

| Item | Status |
|------|--------|
| SAM CLI `1.166.2` | Done on this laptop (`brew install aws-sam-cli`) |
| Docker for `sam local` | Present (`docker` 28.x) |
| Account (STS via toolkit) | `700002441889` — currently resolves as **root** ARN; prefer IAM/temp user for day-to-day after MFA check |
| Local CLI `aws login --profile disputepoint` | **OK 2026-10-07** — STS returns `arn:aws:iam::700002441889:root`. Re-run when local STS fails again |
| Promotional credits | **$120.00 USD remaining** (verified `billing:GetCredits` 2026-10-07): $100 AWS Free Tier + $20 Explore AWS Budgets promo; both ENABLED, unused so far; credit window through ~**2027-10-07**. Console free-plan note also mentions access until **Apr 07, 2027** or credit depletion |
| Cost budget | **`disputepoint-zero-spend`** — $1/month COST; **subscriber `scion2304@gmail.com` @ 80% ACTUAL** (API-confirmed). Check Gmail for AWS **verify email** link (required for new budget recipients) |
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

## G-AWS checklist (after WP-07 local green)

Human clears [G-AWS](../../execution/GATES.md). Then:

1. Choose **Ship It** (default) or **Build It** if blocked; record choice in submission `work-status` / notes.
2. Confirm budget alert email + no secrets in git.
3. `sam build` → `sam deploy` (or guided) under `infra/` once templates exist — **only in the submission repo after G-CLOCK**.
4. **Smoke** (Ship It):
   - Capture public API / UI URL
   - Invoke critical DecisionAPI routes (queue, point card, HITL ACK/OVERRIDE/ESCALATE as implemented)
   - Confirm DynamoDB read/write for points / audit
   - Confirm S3 access for fixtures/static as designed
   - Open CloudWatch log group for one successful invoke
5. **CORS:** from the real browser origin (Vite / hosted UI), not only `curl`. OPTIONS/preflight + methods/headers must succeed. Encode allowlist in SAM/IaC ([HTTP API CORS](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html)).
6. **Warm-up:** one GET against the demo path before recording (avoid cold-start stutter). Do **not** buy provisioned concurrency for MVP.
7. Architecture diagram artifact for video (same story as strategy ASCII: EventBridge → Lambda → DynamoDB/S3 → API Gateway → UI). Point DEMO_SCRIPT / DEMO_WOW AWS beat + [DEMO_REHEARSAL](../build/DEMO_REHEARSAL.md) dual path.
8. If Ship It fails: flip to Build It; fixtures still carry the spoken story.

---

## Oct 8 start sequence (locked)

| Step | Who | Action |
|------|-----|--------|
| 0 | Human | New Cursor session; `aws sts get-caller-identity --profile disputepoint` — re-`aws login` if expired |
| 1 | Human | **G-CLOCK**: declare clock → `CLOCK_STARTED=1 ./scripts/scaffold_submission.sh` → open Cursor on `/Users/vaibhavsingh/disputepoint-ship` only ([SUBMISSION_GIT](SUBMISSION_GIT.md)) |
| 2 | Human | **G-PLAN**: accept [PLAN_CHECK.md](../../execution/PLAN_CHECK.md) in the **submission** tree; set `plan_gate_accepted: true` in submission `execution/work-status.json` |
| 3 | Human | `gh repo create disputepoint-ship --source=. --remote=origin --private --push` |
| 4 | Agents | **WP-00** first, then local waves (engines → API → UI). Not morning Bedrock/MapHUD/blog |
| 5 | Early | Confirm `sam --version` on PATH (installed 2026-10-07 on planning laptop) |
| 6 | After WP-07 green | Human **G-AWS**: Ship It deploy; smoke + CORS + warm URL |
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
