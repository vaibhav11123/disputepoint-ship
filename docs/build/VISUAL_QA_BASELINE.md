# Visual QA baseline — superseded for gate decisions

**SoT for hackathon readiness:** [HACKATHON_VISUAL_GATE.md](HACKATHON_VISUAL_GATE.md)

Automated capture: `make visual-qa` → `runs/visual-qa/latest/*.png` + `PASS.md`.

| ID | Result | Notes |
|----|--------|-------|
| V0 | PASS | Dry cold open: ACT/ASSIGNED top; CONFLICT mid-list; map collapsed; no θ chrome |
| V1 | PASS | Rain Strike → BEFORE/DURING/AFTER; map expand + flyTo; DEMO honesty |
| V2 | PASS | Ownership Conflict + NO AUTO-ASSIGN + Agency — + EFFECT; no conf % in demo |
| V3 | PASS | Trace: CLAIM → SOURCE → QUOTE → DECISION EFFECT |
| V4 | PASS | CASE · ESCALATED · PENDING HUMAN · next check |
| V5 | PASS | HUMAN VERIFIED seal after OVERRIDE |
| V6 | PASS | Incident Replay scrub (cut from video if lifecycle unclear) |
| V7 | PASS | `frontend/public/aws-arch.html` — services we use |
| Human | OPEN | Mute / thumbnail / stranger / Earth / AWS on camera — check `PASS.md` |

Playwright queue: `npx playwright test -c frontend/playwright.config.ts tests/e2e/queue.spec.ts` → 9 passed.
