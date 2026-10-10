# Plan: Fix post-redesign test & style anomalies

**Status:** ready to execute (do not edit the Ink·Stone·Forest execution contract plan).  
**Scope:** Fix faults found in the full test run. Do not reopen product identity or Command+Purana composition.

## Fault inventory

| # | Fault | Severity | Root cause |
|---|--------|----------|------------|
| F1 | `visual-hackathon.spec.ts` fails | High | Spec asserts pre–Ink·Stone·Forest UI (collapsed map, old columns, ACK/OVERRIDE, old copy) |
| F2 | Later CSS undoes Responsibility Assessment look | High | Duplicate `.ownership-conflict` at ~L1108 sets full `--dp-warn-bg` yellow wash, overriding Stone + amber rail |
| F3 | Duplicate `.footer` / `.awaiting-next-strip` / `.command-*` rules | Medium | Stage-1 append left old rules; cascade is fragile |
| F4 | Dirty SQLite + `reuseExistingServer` flakes e2e | Medium | Local reuse skips `rm -f runs/disputepoint.sqlite` |
| F5 | Bundle size warning (~1.58 MB JS) | Low | MapLibre in main chunk; warning only |
| F6 | `visual-qa` PASS.md checklist text stale | Low | Template still describes collapsed map / NO AUTO-ASSIGN wording |

Already fixed (verify only): EventRail unused var · LiveSources `precip_mm` · MapHUD `attributionControl` typing.

---

## Approach

1. **Restore assessment surface** by deleting/rewriting the conflicting yellow `.ownership-conflict` block.  
2. **Deduplicate tokens.css** shell/command/assessment/footer rules into one Ink·Stone·Forest block.  
3. **Rewrite visual-hackathon harness** to the current product path (map always in Command workspace; escalate → confirm, not OVERRIDE).  
4. **Harden Playwright** so local runs get a fresh DB when `CI=1` or via an explicit `DP_E2E_FRESH=1`.  
5. **Optional defer:** MapLibre code-split — only if time; not required for green `make visual-qa`.

---

## Stage A — CSS integrity (F2, F3)

Files: [`frontend/src/styles/tokens.css`](frontend/src/styles/tokens.css)

1. Find all `.ownership-conflict` / `.responsibility-assessment` rules.  
2. Keep **one** assessment rule: Stone/white surface, 3px `--dp-review` rail, **no** full `--dp-review-bg` / warn-bg panel fill.  
3. Remove or neutralize the L1108 block that reintroduces yellow flood.  
4. Collapse duplicate `.footer` and `.awaiting-next-strip` to single definitions matching Ink shell + Stone workspace.  
5. Smoke: load Command + Purana; assessment must not look like a yellow alert.

**Verify:** visual check + `npm run build`.

---

## Stage B — Playwright / DB hygiene (F4)

Files: [`frontend/playwright.config.ts`](frontend/playwright.config.ts), optionally [`Makefile`](Makefile)

1. Keep `rm -f runs/disputepoint.sqlite` in API webServer command.  
2. Document in Makefile / VISUAL_GATE_REPORT: local flake fix = `CI=1` or kill ports 8000/5173 then re-run.  
3. Optional hardening: set `reuseExistingServer: false` when `process.env.DP_E2E_FRESH === "1"`, and wire `make visual-qa` / a `make e2e` target to export that.  
4. Prefer not to force `reuseExistingServer: false` always (slows day-to-day).

**Verify:** two sequential `CI=1` queue.spec runs without manual sqlite delete both pass.

---

## Stage C — Rewrite `visual-hackathon.spec.ts` (F1, F6)

File: [`tests/e2e/visual-hackathon.spec.ts`](tests/e2e/visual-hackathon.spec.ts)  
Target: `make visual-qa` green; screenshots still land in `runs/visual-qa/latest/`.

### Current UI mapping (use these, not old strings)

| Old assertion | New assertion |
|---------------|---------------|
| `td.nth(3)` = ASSIGNED | Status = `td.nth(1)` → ACTION REQUIRED / REVIEW REQUIRED / …; Responsibility = `td.nth(2)` → agency name or Disputed |
| Map collapsed / Show map | Map open in `.command-map-hero`; `.maplibregl-map` count ≥ 1 |
| `rain-strike` always visible | Open Configure (`scenario-strip` → Configure) then click `rain-strike` |
| `Using scenario rain` | `rain-mm` / `rain-scenario-label` contain `RAINFALL SCENARIO` · 42 |
| Rain auto-opens conflict card on command | After rain, open Purana via queue row or View disputes; then assert assessment |
| `NO AUTO-ASSIGN` | `/AUTO.*ASSIGNMENT BLOCKED/` on `no-auto-assign` |
| Button `Trace` | `VIEW SOURCE` (`copy.evidence.viewSource`) |
| Trace text one line with arrows | Match actual ledger: contains `CLAIM` and `SOURCE` (and decision effect), not exact old string |
| Button `ESCALATE` | `Escalate for review` / `getByTestId("escalate-human-review")` |
| `PENDING HUMAN` | `copy.clock.awaiting` = `AWAITING DECISION` on `owner-pending` |
| OVERRIDE flow | **Removed** — use Confirm path: agency + rationale + evidence checkbox + `confirm-decision` |
| `HUMAN VERIFIED` | `OFFICER CONFIRMED` / seal copy from `HumanVerifiedSeal` / `human-verified` |

### Revised beat sequence (keep V0–V7 filenames)

1. **V0-cold** — Command 1440×900; 35 rows; page title District incident command; queue|map both visible; no θ.  
2. **V1-rain-*** — Configure → apply scenario; assert scenario label; screenshot before/during/after; do **not** require conflict panel on Command itself.  
3. **V2-conflict** — Open Purana; ownership-conflict; no-auto-assign; agency-null; claim-grid.  
4. **V3-evidence** — Evidence tab or VIEW SOURCE; assert evidence ledger / trace path.  
5. **V4-escalate-*** — Escalate for review → audit; accountability-clock visible.  
6. **V5-human** — Confirm responsibility (IC path) → human-verified / officer confirmed.  
7. **V6-replay** — incident-replay scrub if present.  
8. **V7-aws** — `/aws-arch.html` unchanged.

Update `writePassTemplate` checklist bullets to match the new beats.

**Verify:** `make visual-qa` → exit 0; PNGs in `runs/visual-qa/latest/`.

---

## Stage D — Bundle warning (F5) — optional / defer

Only if Stage A–C done and time remains:

- Dynamic-import MapHUD / maplibre worker so Command cold path does not force full map chunk on first paint.  
- Or raise `build.chunkSizeWarningLimit` with a one-line comment that MapLibre is intentional.  

Do **not** block visual-qa on this.

---

## Stage E — Docs sync

- Update [`docs/build/VISUAL_GATE_REPORT.md`](docs/build/VISUAL_GATE_REPORT.md) with visual-qa result.  
- Note CSS dedupe + harness rewrite under “Anomalies resolved”.  
- Do not invent new product copy; keep [`frontend/src/lib/copy.ts`](frontend/src/lib/copy.ts) SoT.

---

## Verification matrix (Definition of done)

| Check | Pass criteria |
|-------|----------------|
| `make test` | 47/47 |
| `npx tsc --noEmit` (frontend) | exit 0 |
| `npm run build` | exit 0 |
| `CI=1` queue.spec.ts | 11/11 |
| `make visual-qa` | exit 0 + V0–V7 PNGs |
| Purana assessment | Not full yellow panel (Stone + amber rail only) |
| No product invariant regression | CONFLICT still null agency; confirm still IC-gated |

---

## Explicit non-goals

- New palette / Tailwind / skill installs  
- Reopening Command 58/42 composition  
- Restoring ACK/OVERRIDE  
- Full MapLibre performance project  
- Editing the master Ink·Stone·Forest execution contract plan file  

---

## Suggested execution order

```
A (CSS) → B (Playwright hygiene) → C (visual-hackathon rewrite) → E (docs) → [optional D]
```

After each stage: run the smallest relevant verify. After C: full matrix above.
