# Deployment

Hackathon deploy preference from Phase 6 / LLD locks: **prefer Ship It**. **Chosen and live (2026-10-10):** Ship It — not Build It. Operator truth (profile, login, URLs, cleanup): [AWS_OPERATOR.md](AWS_OPERATOR.md). Details: [HLD.md](../HLD.md), [infra/README.md](../../infra/README.md).

## Live Ship It (cleared G-AWS)

| Item | Value |
|------|-------|
| Path | **Ship It** |
| Stack / region | `disputepoint` / `ap-south-1` |
| Redeploy | `make deploy` (`AWS_PROFILE=disputepoint`) |
| API | https://olnsv0shee.execute-api.ap-south-1.amazonaws.com |
| UI | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com |
| Arch page | …/aws-arch.html |
| Live mode | `DP_LIVE_FETCH=1` — Open-Meteo rain LIVE; evidence batch LIVE |
| Security | CORS allowlist to UI origin; `/docs` off on Lambda — [SECURITY.md](SECURITY.md) |
| Demo beat | [AWS_DEMO_BEAT.md](../build/AWS_DEMO_BEAT.md) |
| Cleanup after video | `sam delete --stack-name disputepoint --region ap-south-1 --profile disputepoint` |

Smoke: `GET /health` → `ok`, `live_fetch`, `rain_source_state=LIVE`; `GET /points` → queue by `priority_rank`.

## Paths

| Path | Shape | When |
|------|-------|------|
| Local | FastAPI + Vite + SQLite fixtures | Default demo / offline (NFR-003) — `make run` |
| Ship It | S3 (static UI) → API Gateway → Lambda → DynamoDB; EventBridge rain + evidence; CloudWatch; private evidence S3 | **Live** — preferred for FR-016 / video |
| Build It | SAM Local / LocalStack (Lambda + Dynamo parity on laptop) | Failover only if Ship It URL dies mid-demo |

**Out of MVP:** SNS, Cognito, CloudFront required, Bedrock online.

## Local runbook

```text
make install
make test
make run
```

API `127.0.0.1:8000`; UI `127.0.0.1:5173`.

## Ship It runbook

```text
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
export AWS_PROFILE=disputepoint AWS_REGION=ap-south-1
aws sts get-caller-identity   # aws login --profile disputepoint if expired
make deploy
```

## Config locks

| Key | Value |
|-----|-------|
| `THETA_ASSIGN` / θ | 0.65 until fixture gold |
| `W_NORM` | 2.0 |
| Rain window | 6 hours |
| Poll interval | 15 minutes (EventBridge + local) |
| Wet demo precip | 40 mm |
| Dry demo precip | 0 mm |

## Degrade

| Failure | Behavior |
|---------|----------|
| Open-Meteo down | Cache or scenario slider |
| AWS down | Local URL for demo (`make run`) |
| Missing fixtures | Empty-state copy — do not invent points |

## References

- [AWS_OPERATOR.md](AWS_OPERATOR.md) — profile, region, login, budget, SAM, smoke/CORS/cleanup
- [SECURITY.md](SECURITY.md) — Ship It checks
- [HLD.md](../HLD.md) deploy sections
- [LLD.md](../LLD.md) §24 implementation locks
- [research/aws-strategy-and-submission-notes.md](../research/aws-strategy-and-submission-notes.md)
