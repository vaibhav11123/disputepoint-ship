# Observability

MVP logging and demo break-glass. From [HLD.md](../HLD.md) cross-cutting + NFR-006.

## Goals

1. Structured logs with `request_id` always (NFR-006).
2. Locate failing stage in under ~30 seconds during demo (Phase 6 §26 intent).
3. CloudWatch when on AWS; else stdout JSON lines locally.

## Log fields (minimum)

| Field | Meaning |
|-------|---------|
| `request_id` | Correlate request |
| `stage` | e.g. rain_refresh, rank, ack, override |
| `point_id` | When applicable |
| `level` | info / warn / error |
| `code` | DP-* when error |

Example shape (illustrative):

```json
{"request_id":"…","stage":"ack","point_id":"dp-…","level":"warn","code":"DP-409-ACK"}
```

## What to watch in demo

| Symptom | First check |
|---------|-------------|
| Empty queue | Fixtures load / schema validate |
| Stale ranks | Rain mode: live vs cache vs slider (`GET /health`) |
| ACK fails | ownership_state + status; expect DP-409 on CONFLICT |
| Rain fail | Open-Meteo timeout → slider path |
| Ship It “LIVE RAINFALL UNAVAILABLE” | `GET {ApiUrl}/health` — expect `live_fetch=true`, `rain_source_state=LIVE`; CloudWatch log group `/aws/lambda/disputepoint-decision` |

## Ship It (2026-10-10)

- Lambda: `disputepoint-decision` · HTTP API `olnsv0shee` · region `ap-south-1`
- Dynamo stamps: `_shipit_api_invoke`, `_shipit_rain_live`, `_shipit_evidence_live`
- Warm one `/health` before recording (cold start)

## Non-goals

- Full OpenTelemetry traces (optional later)
- PagerDuty / on-call
- Log shipping of secrets or full evidence quotes at debug in production-like deploys

## References

- [HLD.md](../HLD.md) §7, §15
- [SECURITY.md](SECURITY.md) API8/API9 inventory via OpenAPI
