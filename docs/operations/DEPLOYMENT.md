# Deployment

Hackathon deploy preference from Phase 6 / LLD locks: **prefer Ship It**; day-1 recon may choose Build It if account/SAM blocked. Operator truth (profile, login, G-AWS): [AWS_OPERATOR.md](AWS_OPERATOR.md). Details: [HLD.md](../HLD.md), [infra/README.md](../../infra/README.md).

## Paths

| Path | Shape | When |
|------|-------|------|
| Local | FastAPI + Vite + SQLite fixtures | Default demo / offline (NFR-003) |
| Ship It | S3 (static UI / fixtures) → API Gateway → Lambda → DynamoDB; EventBridge rain schedule; CloudWatch | Prefer for video eligibility (FR-016) |
| Build It | SAM Local / LocalStack (Lambda + Dynamo parity on laptop); still show AWS tooling on video | If Ship It blocked |

**Out of MVP:** SNS, Cognito, CloudFront required, Bedrock online.

## Local runbook (when Makefile present)

```text
make install
make test
make run
```

Until targets exist, document commands actually run. Never invent a stack.

## Config locks

| Key | Value |
|-----|-------|
| `THETA_ASSIGN` / θ | 0.65 until fixture gold |
| `W_NORM` | 2.0 |
| Rain window | 6 hours |
| Poll interval | 15 minutes |
| Wet demo precip | 40 mm |
| Dry demo precip | 0 mm |

## Degrade

| Failure | Behavior |
|---------|----------|
| Open-Meteo down | Cache or scenario slider |
| AWS down | Local URL for demo |
| Missing fixtures | Empty-state copy — do not invent points |

## References

- [AWS_OPERATOR.md](AWS_OPERATOR.md) — profile, region, login, budget, SAM, G-AWS smoke/CORS/cleanup
- [HLD.md](../HLD.md) deploy sections
- [LLD.md](../LLD.md) §24 implementation locks
- [research/aws-strategy-and-submission-notes.md](../research/aws-strategy-and-submission-notes.md)
