# Visual / interaction / state gates — Command + Purana

Baseline commit: `b5fdca8` · Branch: `main` · Viewport target: 1440×900

## Preflight (six problems)

1. Generic visual identity — flat Carbon gray admin  
2. Uniform shout — all-caps labels  
3. Poor spatial rhythm — map below queue  
4. Disconnected map  
5. Competing yellow conflict panel  
6. Dev chrome (`cell-1`, RAINFALL · VERIFIED contradiction)

## Gate A — Visual

| Check | Result |
|-------|--------|
| Ink shell + Stone workspace + Forest selection | Pass (tokens + shell) |
| Command queue\|map side-by-side 58/42 | Pass (CSS grid) |
| Responsibility Assessment hierarchy (claims / findings / blocked) | Pass |
| No full yellow flood | Pass (late `.ownership-conflict` yellow wash removed) |
| Hierarchy: titles strong, meta quiet | Pass |
| Accidental blank / competing scroll | Pass at CSS level; measure in browser for polish |

## Gate B — Interaction / a11y

| Check | Result |
|-------|--------|
| Keyboard queue rows | Pass (E2E-01 focus) |
| Form labels / confirm requirements | Pass (E2E-04) |
| Focus ring brand | Pass (`:focus-visible`) |
| Reduced-motion map | Pass (code path) |
| Configure disclosure for rain | Pass (E2E-02) |
| Responsive &lt;1100 stack | Pass (CSS media) |

## Gate C — State integrity

| Check | Result |
|-------|--------|
| Claimants ≠ confirmed agency in queue | Pass (`AgencyBlock` → Disputed) |
| CONFLICT null agency in assessment | Pass (E2E-03) |
| Auto-assign blocked | Pass (E2E-03) |
| Confirm needs agency + rationale + evidence | Pass (UI + E2E-04) |
| Backend HITL enforcement | Pass (`make test` 47) |
| Unavailable ≠ verified evidence badge | Pass (`EvidenceLedger`) |
| Footer not VERIFIED when live unavailable | Pass |

## Automated verification

- `make test` → **47 passed**
- `CI=1 npx playwright test tests/e2e/queue.spec.ts` → **11 passed** (prior run)
- `npm run build` (frontend) → **pass** (prior run)
- `make visual-qa` → **pass** (V0–V7 PNGs + PASS.md in `runs/visual-qa/latest/`)

## Anomalies resolved

- CSS: removed late `.ownership-conflict` `--dp-warn-bg` yellow override; collapsed duplicate `.footer` / `.awaiting-next-strip` / stale `.command-map-hero` padding rules in `frontend/src/styles/tokens.css`.
- Playwright: `DP_E2E_FRESH=1` or `CI=1` forces fresh servers (no dirty sqlite reuse); `make visual-qa` exports both.
- Harness: `tests/e2e/visual-hackathon.spec.ts` rewritten for Ink·Stone·Forest (map open on Command, Configure→rain, Purana assessment, Escalate + Confirm IC path; no ACK/OVERRIDE).

## Backend gaps (documented)

- Disabled confirm button is not authorization; API enforces IC role and agency set.
- Frontend silent reviewer label `"Incident Commander"` replaces `cell-1` chrome; backend still records reviewer string.

## Refinement passes used

1 (structure + e2e alignment). No further decorative passes.
