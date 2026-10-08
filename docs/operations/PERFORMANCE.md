# Performance

Targets from [PRD.md](../PRD.md) NFRs and [HLD.md](../HLD.md) §15.

| ID | Requirement | Target | Architecture response |
|----|-------------|--------|----------------------|
| NFR-001 | GET /points latency (local) | &lt; 300 ms | Pure-function rank over ~15 points; no remote fan-out on GET |
| NFR-002 | Rank 15 points | &lt; 50 ms | In-process PriorityEngine |
| NFR-005 | Free Tier cost | Within hackathon credits | EventBridge poll 5–15 min; Bedrock off; tiny fixtures |
| FR-027 | Time-to-actionable-triage | &lt; 30 s demo path | Warm local stack + fixture spine |

## Design locks that protect latency

- No ML runtime in MVP.
- Rain refresh is separate from GET /points (POST `/rain/refresh`).
- Scenario slider is local synthetic — no upstream wait.
- UI motion budget: max 2 effects (rank flash 200 ms).

## How to verify

1. Unit: rank microbench for 15 points (NFR-002).
2. Integration: time GET /points under fixture load (NFR-001).
3. Demo stopwatch on E2E-06 (FR-027).

Do not claim numbers without measurement.

## References

- [PRD.md](../PRD.md) §8
- [TEST_STRATEGY.md](../quality/TEST_STRATEGY.md)
