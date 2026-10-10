# Front-End Checklist — Critical/High gate (Command + Purana)

Scoped review after Ink · Stone · Forest Stages 1–4. SEO/PWA/cookie/i18n/dark-mode out of scope.

| Finding | Severity | File / component | In scope | Resolution | Verification |
|---------|----------|------------------|----------|------------|--------------|
| Visible focus on interactive controls | High | `tokens.css` `:focus-visible` | Yes | Brand outline (`--dp-brand`) | Visual + keyboard tab |
| Form labels on IC confirm | Critical | `ActionBlock.tsx` | Yes | `aria-label` + visible `.dp-label` on agency, rationale, evidence | E2E-04 |
| Unique IDs / no duplicate claim keys | High | `OwnershipConflict.tsx` | Yes | Agency name as React key in claim grid | Code review |
| Status not color-only | High | `TriageChip`, chips | Yes | Text labels; ACTION REQUIRED uses `.chip.action` not success-green | Visual |
| Reduced motion for map | High | `MapHUD.tsx` | Yes | `prefers-reduced-motion` → `jumpTo` | Code path |
| External links noopener | Medium | `EvidenceLedger.tsx` | Yes | `rel="noopener noreferrer"` | Code review |
| Skip link present | High | `App.tsx` | Yes | Existing skip to `#queue` | Present |
| Landmarks | High | shell / screens | Yes | `header`, `main`-equivalent sections with aria-labels | Snapshot |
| Horizontal overflow / queue|map | High | `tokens.css` `.command-layout` | Yes | 58/42 + `@media (max-width: 1100px)` stack | Layout CSS |
| Map CLS / min-height | High | `MapHUD`, `.command-map-hero` | Yes | `min-height: 280px` reserved | CSS |
| Confirm disabled until requirements | Critical | `ActionBlock.tsx` | Yes | UI gate; backend still enforces via API | E2E-04 + pytest HITL |
| Footer contradictory rain verified | High | `App.tsx` footer | Yes | Removed `RAINFALL · VERIFIED` when unavailable | Code |
| Claimant-as-assigned in queue | Critical | `StateChip.AgencyBlock` | Yes | Shows Disputed/Unresolved, never claim chips as agency | Code + E2E |
| Deferred: full axe CI | Medium | — | Partial | Manual FEC; no axe harness in repo | Defer |
| Deferred: skip-to-content beyond queue | Low | — | No | Existing skip sufficient for Command | Defer |
| Backend auth gaps | High | HITL APIs | Yes | Documented: frontend disabled ≠ auth; existing API role checks remain | pytest HITL |

**Skills note:** Anthropic Frontend Design / Vercel guidelines not vendored into repo this run; contract applied manually. Mutable upstream guidelines not fetched.
