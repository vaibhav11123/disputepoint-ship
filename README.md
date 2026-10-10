# DisputePoint Response Intelligence

When monsoon rain hits Delhi, disputed waterlogging points stall while agencies pass the buck. DisputePoint is for a **DM coordination cell officer**: one queue under rain — which place needs action first, which agency (or honest null when ownership still fights), with evidence. **Not** a flood heatmap. **Not** a citizen complaint inbox.

Hackathon: [WeMakeDevs × AWS Environmental Hacks](https://www.wemakedevs.org/aws/env).

## Start here

1. **[docs/README.md](docs/README.md)** — docs map  
2. **[docs/PHASE6.md](docs/PHASE6.md)** — **frozen** build contract  
3. **[AGENTS.md](AGENTS.md)** — agent hard stops. Full OS: [docs/agent/AGENT_CONSTITUTION.md](docs/agent/AGENT_CONSTITUTION.md)  
4. **[docs/agent/HOWTO_REUSE.md](docs/agent/HOWTO_REUSE.md)** — how we researched / how to reuse  
5. **Demo VO:** [docs/build/DEMO_SCRIPT.md](docs/build/DEMO_SCRIPT.md) · cite log [docs/research/video-win-pass-2026-10-10.md](docs/research/video-win-pass-2026-10-10.md)

## Setup

```bash
make install   # .venv + npm
make test      # pytest
make run       # API :8000 + UI :5173 (DP_LIVE_FETCH=1)
make deploy    # Ship It — SAM + S3 UI (profile disputepoint, ap-south-1)
```

```bash
cp .env.example .env   # never commit .env
```

## Ship It (live)

| Surface | URL |
|---------|-----|
| UI | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com |
| API | https://olnsv0shee.execute-api.ap-south-1.amazonaws.com |
| Arch | http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html |

Operator: [docs/operations/AWS_OPERATOR.md](docs/operations/AWS_OPERATOR.md) · demo beat: [docs/build/AWS_DEMO_BEAT.md](docs/build/AWS_DEMO_BEAT.md).

## Status

- Phase 6 **frozen**. Product ships in this repo (judged entry).
- Fixtures: points **0.3.3** (35 places) · evidence **0.3.4** — assigned / disputed / evidence-needed under real ownership + priority engines (no DEMO MIX banner, no fake rank rewrite).
- Queue-first UI + MapHUD + rain modes + ownership CONFLICT→null + HITL. `?judges=1` for eval chrome.
- G-AWS cleared (Ship It). **G-VIDEO** still open until ≤3 min YouTube passes smoke twice.
- AI coding tools: **Cursor** (list in write-up). AWS must appear on camera.
- Git: [docs/operations/SUBMISSION_GIT.md](docs/operations/SUBMISSION_GIT.md) — event-dated history; make public before form submit.

## Engineering invariants

| Topic | Choice |
|-------|--------|
| Ownership | `ownership_state == CONFLICT` → `responsible_agency = null` always |
| Uncertainty U | Coordination uncertainty, not flood severity |
| HITL | ACK only when ASSIGNED; OVERRIDE / ESCALATE when disputed — audit visible |
| AWS | API Gateway → Lambda → DynamoDB + S3; EventBridge rain; CloudWatch |
| Out of MVP | Cognito, map-as-home, ML KEEP, Bedrock unless §14A |

## Docs map

| Need | Go to |
|------|--------|
| Frozen contract | [PHASE6](docs/PHASE6.md) |
| PRD / HLD / LLD / UX | [docs/](docs/) |
| Demo video | [DEMO_SCRIPT](docs/build/DEMO_SCRIPT.md) · [DEMO_WOW](docs/build/DEMO_WOW.md) · [DEMO_REHEARSAL](docs/build/DEMO_REHEARSAL.md) |
| Research | [demo-win-tactics](docs/research/demo-win-tactics.md) · [video-win-pass](docs/research/video-win-pass-2026-10-10.md) |
| Builder blog draft | [BUILDER_BLOG](docs/build/BUILDER_BLOG.md) |

## License

MIT — [LICENSE](LICENSE). Third-party data/quotes: [docs/build/LICENSE_AUDIT.md](docs/build/LICENSE_AUDIT.md).
