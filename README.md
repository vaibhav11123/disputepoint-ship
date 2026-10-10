# DisputePoint Response Intelligence

DM coordination cell tool: under rain, rank disputed Delhi waterlogging points, show evidence-backed agency or UNCERTAIN, HITL ACK/OVERRIDE/ESCALATE — **not** a flood heatmap.

Hackathon context: [WeMakeDevs × AWS Environmental Hacks](https://www.wemakedevs.org/aws/env).

## Start here

1. **[docs/README.md](docs/README.md)** — docs map  
2. **[docs/PHASE6.md](docs/PHASE6.md)** — **frozen** build contract (binding for Phase 7)  
3. **[AGENTS.md](AGENTS.md)** — short agent README. Full OS: [docs/agent/AGENT_CONSTITUTION.md](docs/agent/AGENT_CONSTITUTION.md)  
4. **[docs/agent/HOWTO_REUSE.md](docs/agent/HOWTO_REUSE.md)** — how we researched / how to reuse

## Docs (thin index)

Full layout: [docs/README.md](docs/README.md).

| Need | Go to |
|------|--------|
| Frozen contract | [PHASE6](docs/PHASE6.md) |
| Requirements / system / modules / UI | [PRD](docs/PRD.md) · [HLD](docs/HLD.md) · [LLD](docs/LLD.md) · [UX](docs/UX.md) |
| Fixtures, gaps, license | [build/](docs/build/) |
| Research trail PHASE1–5 | [phases/](docs/phases/) |
| Schemas / OpenAPI | [schemas/](docs/schemas/) · [openapi.yaml](docs/openapi.yaml) |

## Status

- Phase 6 **frozen**. Do not reopen product strategy.
- PRD / HLD / LLD / UX are readable extracts. If an extract disagrees with Phase 6, follow Phase 6.
- Spec package + **Data Ready PASS** — [docs/quality/SPEC_READINESS.md](docs/quality/SPEC_READINESS.md) §F. Planning contracts ready; **entry product build starts at the Oct 8 clock** ([WeMakeDevs rules](https://www.wemakedevs.org/aws/rules)).
- Fixtures: [`data/fixtures/`](data/fixtures/) v0.2 (evidence promoted). L0 source bodies gitignored under [`data/audit/`](data/audit/) (L1 matrices committed).
- Geo: `lat`/`lon` null until human VERIFIED ([geocode-candidates](docs/research/geocode-candidates.md)); MapHUD skippable. COURT quotes may still have `needs_review=true`.
- App: queue-first UI + MapHUD + Rain Strike + Ownership Conflict + HITL. Demo chrome default; `?judges=1` for eval/θ.
- **Ship It (live):** `make deploy` → stack `disputepoint` / `ap-south-1`. URLs in [AWS_DEMO_BEAT](docs/build/AWS_DEMO_BEAT.md) · operator [AWS_OPERATOR](docs/operations/AWS_OPERATOR.md).
- Demo: [DEMO_SCRIPT](docs/build/DEMO_SCRIPT.md) · [EARTH_STUDIO_SHOT](docs/build/EARTH_STUDIO_SHOT.md) · [AWS_DEMO_BEAT](docs/build/AWS_DEMO_BEAT.md) · [DONOR_MATRIX](docs/build/DONOR_MATRIX.md)
- AI coding tools: Cursor (must be listed in hackathon write-up). AWS must show in the demo video (G-VIDEO still open).
- Optional secondary memory: `.mex/` (loopback Hub). Phase 6 + root AGENTS hard stops win on conflict.
- **Git:** policy [SUBMISSION_GIT](docs/operations/SUBMISSION_GIT.md) — keep history event-dated; make public before form submit.

## Engineering invariants (interview / judge surface)

| Topic | Choice |
|-------|--------|
| Ownership | `ownership_state == CONFLICT` → `responsible_agency = null` always — never invent MCD/PWD |
| Uncertainty U | Coordination uncertainty, not flood severity |
| HITL | ACK / OVERRIDE / ESCALATE with visible DecisionAuditPanel — model never silent-owns |
| AWS (Ship It) | EventBridge schedules rain; Lambda runs decisions; DynamoDB stores points/audit; S3 evidence/UI; API Gateway HTTPS; CloudWatch logs |
| Failure modes | Open-Meteo down → cache/slider; AWS down → local fixtures; missing fixtures → empty-state, do not invent points |
| Out of MVP | Cognito, map-as-home, ML KEEP, Bedrock unless §14A |

Demo VO: [docs/build/DEMO_SCRIPT.md](docs/build/DEMO_SCRIPT.md). Builder Center draft: [docs/build/BUILDER_BLOG.md](docs/build/BUILDER_BLOG.md).

## GitHub (two repos)

**Plan/practice here before the clock.** Do **not** use this research tree’s pre–Oct 8 history as the public entry.

| Tree | Path | Role |
|------|------|------|
| Research | `/Users/vaibhavsingh/disputepoint` | Planning only |
| Submission | `/Users/vaibhavsingh/disputepoint-ship` | Judged entry (create at clock) |

At clock:

```bash
cd /Users/vaibhavsingh/disputepoint
CLOCK_STARTED=1 ./scripts/scaffold_submission.sh
# then open Cursor on disputepoint-ship; G-PLAN; gh repo create disputepoint-ship ...
```

Policy: [docs/operations/SUBMISSION_GIT.md](docs/operations/SUBMISSION_GIT.md). History must match event dates or the team is disqualified.

Optional **private backup** of *this* research tree (not the judged entry):

```bash
cd /Users/vaibhavsingh/disputepoint
gh auth status
gh repo create disputepoint-research --private --source=. --remote=origin --push
```

Near submit on **submission** repo:

```bash
gh repo edit --visibility public
```

## Local secrets

```bash
cp .env.example .env
# fill only what you need; never commit .env
```

## License

MIT — see [LICENSE](LICENSE). Third-party data/quotes: [docs/build/LICENSE_AUDIT.md](docs/build/LICENSE_AUDIT.md).
