# Infra / deploy notes

**Product SoT:** [docs/PHASE6.md](../docs/PHASE6.md). Prefer **Ship It**. Day-1 recon may choose **Build It** if account/SAM is blocked.

**Operator runbook:** [docs/operations/AWS_OPERATOR.md](../docs/operations/AWS_OPERATOR.md) — profile `disputepoint`, region `ap-south-1`, login refresh, Free Tier budget, SAM/Docker, G-AWS smoke/CORS/cleanup. Phase 6 frozen recon tables are historical; use AWS_OPERATOR for live pins.

## Ship It (preferred)

Hosted path when Free Tier login + SAM work: static frontend on S3 (or equivalent) + API Gateway + Lambda + DynamoDB + EventBridge rain schedule + CloudWatch. Keep demo runnable locally with fixtures if deploy fails. No product deploy before G-CLOCK in the submission repo.

## Build It (SAM Local failover)

If Ship It is blocked at G-AWS, use SAM Local / LocalStack for Lambda + Dynamo parity (Docker required for `sam local`):

- Tutorial: [Deploy a Hello World application with AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)
- Typical flow: `sam init` → Hello World or Serverless API → `sam build` → `sam deploy --guided` (or `sam local` when staying offline)
- Do not invent DM-71 / live SCADA into Lambda payloads; use `data/fixtures/`.

SAM CLI on the planning laptop (2026-10-07): `1.166.2` via Homebrew. Verify: `sam --version`.

## Local first

```text
cp .env.example .env
make install   # when Phase 7 apps exist
make test
make run
```

Until Phase 7 code exists, `make` targets exit with a pointer to [docs/build/GAPS.md](../docs/build/GAPS.md).

## Out of MVP

SNS and CloudFront are out unless a later written ADR. Bedrock stays off (fixtures-only evidence).
