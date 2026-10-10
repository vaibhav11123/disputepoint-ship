# Hackathon Visual Readiness Gate

Judge simulation: repo + ≤3 min YouTube + write-up. No live demo. Readiness means a **mute** stranger can read: WHERE → WHAT CHANGED → WHO DISAGREES → WHY → WHAT NEXT.

**Visual sentence:** Rain changes priority. The point becomes disputed. Evidence explains why. The system refuses to guess. A human takes ownership.

Automation: `make visual-qa` → PNGs + checklist stub in `runs/visual-qa/latest/` (gitignored). Human mute/thumbnail/AWS/Earth rows in `PASS.md` are **required** before G-VIDEO.

Wire: [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md) **G-VIS** = this gate green before **G-VIDEO**.

---

## V0–V7 PASS / FAIL

| ID | PASS | FAIL |
|----|------|------|
| **V0 Cold open** | Idle ≥5s: queue leads with **ACT · ASSIGNED** + agency; CONFLICT (Purana/Minto) mid-list as ADJUDICATE; map **collapsed**; no θ/Why/eval chrome on default demo | RESEARCH/UNKNOWN as #01; land already on CONFLICT; map open; purple glass / heatmap-first |
| **V1 Rain Strike** | BEFORE → Strike → DURING (flash/reorder) → AFTER; map **expands** + flyTo conflict; DEMO/scenario honesty visible | Silent reorder; map stays collapsed; fake “live storm” without honesty chip |
| **V2 Aha freeze** | Ownership Conflict card: claims duel · **NO AUTO-ASSIGN** · Agency **—** · EFFECT “does not establish exclusive responsibility”; **no** confidence % in demo | Conf % badge; invented responsible agency; soft “maybe both” copy |
| **V3 Evidence** | Trace: CLAIM → SOURCE → QUOTE → DECISION EFFECT; no spiderweb | Trace opens empty; quotes without effect line |
| **V4 Escalate** | CASE id · ESCALATED · **PENDING HUMAN** · Elapsed / next check (+30m) | Escalate with no clock; fake owner under CONFLICT |
| **V5 Human close** | After OVERRIDE: **HUMAN VERIFIED** seal + audit id | Seal without human action; agency invented without OVERRIDE reason |
| **V6 Replay** | Keep in video only if scrub proves lifecycle; else cut | Decorative scrub that changes nothing |
| **V7 AWS / Earth** | AWS: `frontend/public/aws-arch.html` or Ship It console (services we use). Earth: video-only per [EARTH_STUDIO_SHOT.md](EARTH_STUDIO_SHOT.md) | Decorative AWS soup; embedding Earth in product UI |

---

## Red-pixel kill list

- Flood heatmap as hero; Inter/Geist purple glass
- Confidence % or ML KEEP on demo chrome
- Auto-assigned agency under CONFLICT
- Fake DM-71 / SCADA / GPS marked real
- Secrets, `.env`, live tokens on screen
- θ / Why / EvalLink on default (non-`?judges=1`) chrome

---

## Thumbnail + stranger + mute

1. **Thumbnail:** pause at V2 aha; readable at ~20% zoom — NO AUTO-ASSIGN + Agency — visible.
2. **10s stranger (no audio):** can say “queue,” “rain changed order,” “two agencies claim,” “system won’t pick.”
3. **Mute full cut:** answers WHERE / WHAT CHANGED / WHO DISAGREES / WHY / WHAT NEXT without voiceover.

---

## Amazon-ready (condensed)

- [ ] AWS visible on camera (Ship It live URL ready — [AWS_DEMO_BEAT.md](AWS_DEMO_BEAT.md); still must appear in the recorded video)
- [ ] Architecture shows only services used (API GW, Lambda, DynamoDB/S3, EventBridge, CloudWatch)
- [ ] No secrets; AI tools listed in write-up
- [ ] YouTube ≤3:00; signed-out link works
- [ ] Public repo history matches event dates

---

## Commands

```bash
make visual-qa
# PNGs + PASS.md under runs/visual-qa/latest/
npx playwright test -c frontend/playwright.config.ts tests/e2e/queue.spec.ts
```

Human rows in `PASS.md` stay unchecked until you watch mute + stranger + AWS/Earth.
