# Design system extract

Ops UI tokens and rules for DisputePoint. **Authoritative visual copy:** [UX.md](../UX.md) §8–§12. This file is the agent-facing extract so front-end work does not skip UX.

**Product shape:** queue-first + point-card. Not a flood heatmap. Not a marketing landing page.

## Foundations

| Kind | Rule |
|------|------|
| Type | IBM Plex Sans (UI) + IBM Plex Mono (scores, ranks) |
| Radius | `0` or `2px` |
| Border | 1px `--dp-border` |
| Elevation | One subtle shadow max on detail panel |
| Spacing | `--dp-space-*`: 4 / 8 / 12 / 16 px |
| Touch | Controls ≥44×44px, ≥8px gap; queue rows may be ~40px with full-row hit |
| Motion | Max 2 UI effects (rank flash 200 ms; rain pulse). MapHUD `flyTo` is camera. Honor `prefers-reduced-motion` — see [UX.md](../UX.md) §8 |

## Color tokens

Source of truth for values: UX §8. Implement as CSS variables in `tokens.css` (Phase 7).

| Token | Hex | Role |
|-------|-----|------|
| `--dp-bg` | `#f5f6f8` | App background |
| `--dp-surface` | `#ffffff` | Tables / panels |
| `--dp-text` | `#161616` | Primary text |
| `--dp-text-2` | `#525252` | Secondary |
| `--dp-ink` | `#1c2541` | Actions / links |
| `--dp-border` | `#e0e0e0` | Rules |
| `--dp-warn` | `#b28600` | CONFLICT / UNCERTAIN |
| `--dp-danger` | `#a2191f` | Underpass severity |
| `--dp-ok` | `#198038` | ACKED / OK readiness |
| `--dp-synthetic` | `#8a3ffc` | SYNTHETIC badge only |

## Typography

| Role | Face | Size / weight |
|------|------|---------------|
| UI body | IBM Plex Sans | 14px / 400 |
| Section | IBM Plex Sans | 16–20px / 600 |
| Meta / scores | IBM Plex Mono | 13–14px / 500 tabular |
| Rank index | IBM Plex Mono | 12px / 600 |

Fonts: `@fontsource/ibm-plex-sans`, `@fontsource/ibm-plex-mono`.

## UI kit lock

CSS variables + React. **No `@carbon/react`** unless a later ADR. Do not substitute Inter / Geist / Roboto / system-ui-only stacks.

## Stack lock

Phase 7 frontend is **Vite + React + TypeScript** with `tokens.css` (`--dp-*`) talking to **FastAPI** ([openapi.yaml](../openapi.yaml)).

- **Not** Next.js App Router, RSC `HydrationBoundary`, or a multi-page SaaS admin shell.
- **Not** a fork of Kiranism / Nellavio / other shadcn+Tailwind dashboard starters (steal TanStack patterns only; do not import their chrome).
- Visual SoT remains this file + [UX.md](../UX.md) §8–§12 (light workbench `#f5f6f8`), not dark `slate-950` SOC templates.

## Library KEEP / ADAPT / REJECT

Guidance for Phase 7 agents. Do not install packages in this docs pass.

| Decision | Library / pattern | Notes |
|----------|-------------------|--------|
| KEEP | Headless [TanStack Table](https://tanstack.com/table/latest) | QueueTable logic only; markup + styles from `--dp-*` (Carbon→TanStack direction) |
| ADAPT | TanStack Query | Optional for `/points`, rain, HITL; query keys + invalidate; not mandatory day-1 |
| ADAPT | Lucide icons | Sparingly; no emoji chrome |
| ADAPT | Radix Slider | Optional for rain control if styled with `--dp-*` |
| ADAPT | [react-map-gl/maplibre](https://visgl.github.io/react-map-gl/) + MapLibre | **Secondary MapHUD only** (BUILD IF STABLE); point markers after VERIFIED geocodes; FR-020 home without map |
| ADAPT | [`cmdk`](https://github.com/dip/cmdk) | CommandPalette — same-screen point jump; style with `--dp-*` |
| REJECT | shadcn/ui + Tailwind kits as design system | Fights anti-slop / IBM Plex tokens |
| REJECT | shadcn Command chrome / Next+Clerk billing starters | Wrong product shape; Cognito/auth out of MVP |
| REJECT | BlueprintJS / Tremor as SoT | Density inspiration only; theme takeover |
| REJECT | Flood heatmap / globe-first / map-as-home | Gate B; FR-020 |
| REJECT | AI chat UI (AI Elements, assistant-ui, CopilotKit) | Not a chat product |
| REJECT | Dark SOC three-pane / emoji mission-control layouts | Ban dark neon + wrong IA |
| REJECT | Ownership “blame meter” / agency share stacked bars | CONFLICT → `responsible_agency = null` always |
| REJECT | react-pdf / Mark.js dual-pane MVP | Quote + url provenance; PDF viewer deferred |

## Phase 7 wiring (prose)

When the UI is built (separate plan):

- Queue order comes from server `priority_rank` — do not recompute PriorityEngine in the client.
- Types mirror [schemas/](../schemas/) and OpenAPI (`OPEN` \| `ACKED`, `ownership_state`, null agency on CONFLICT) — do not invent `DisputeIncident` / `uncertainAgencyShares`.
- HITL uses existing ACK / OVERRIDE / ESCALATE routes; optimistic ACK only when `ASSIGNED` + `OPEN`; roll back on `DP-409-ACK`.
- Rain scenario: POST then refetch queue; rank change flash ≤200 ms (UX motion lock).
- Fonts: `font-display: swap` (or optional) for IBM Plex to avoid FOIT.
- Queue region: reserve min-height while loading so the shell does not collapse to a blank band.
- MapHUD: **unmounted or `height: 0` when collapsed** — no reserved empty strip; select ↔ flyTo (or jump if reduced-motion) when VERIFIED coords exist; OSM attribution required.
- CommandPalette: ⌘K sets `selectedPointId` — no Billing/Settings routes; Esc restores focus.
- Eval: footer link to `tests/eval/baseline_tournament.md` and/or optional drawer; never invent metrics ([build/DEMO_WOW.md](../build/DEMO_WOW.md)).
- HITL: disable confirm + `aria-busy` while request in flight; error near form.

## Required copy (exact)

- `Advisory only — not an official agency assignment.`
- `Ownership uncertain — escalate to coordination cell.`
- `Readiness: synthetic fixture (not live SCADA).`
- `No disputed points loaded. Check fixtures.`

## Component map (LLD §8)

| Region | Job |
|--------|-----|
| AdvisoryBanner | Global honesty |
| TopBar | Title, RainControl, HideSyntheticToggle |
| QueueTable | Ranked rows — home |
| MapHUD | Secondary collapsible map (BUILD IF STABLE); markers only with VERIFIED coords |
| CommandPalette | ⌘K fuzzy jump to point |
| EvalDrawer / EvalLink | Judges tournament aid — link-out OK while TBD |
| PointCard | Evidence, priority explain, HITL, DecisionAuditPanel |
| DecisionAuditPanel | SYSTEM RECOMMENDED vs HUMAN DECISION |

## Banned (fail design review)

Inter/Geist/Roboto-only; purple/indigo/pink gradients; centered hero + three feature cards; `rounded-2xl` + glass chrome; glow pills; “AI-powered” / “smart city” copy. Full list: UX §10. Pre-demo checklist: UX §12.

## Accessibility

Extract of [UX.md](../UX.md) §11 (SoT). Do not diverge.

- Skip link → queue; focus ring 2px `--dp-ink`
- Controls ≥44×44; color+text on State / SYNTHETIC / severity
- Contrast-check text, text-2, warn, synthetic on surface
- Aria on MapHUD toggle, ⌘K trigger, icon-only controls
- HITL busy/disabled + inline error; Esc closes palette/drawer
- Visual gate: UX §12 + §23 (`T-VIS-AUDIT`)

## References

- [UX.md](../UX.md) §8–§12 — authoritative
- [Design System Doc Spec](https://designsystemdocspec.org/) — structure inspiration only; we keep markdown + CSS variables, not DSDS YAML
- [research/ux-anti-slop-research.md](../research/ux-anti-slop-research.md)
- [TanStack Table](https://tanstack.com/table/latest) · [tanstack-carbon](https://github.com/carbon-design-system/tanstack-carbon) — headless table + design-system chrome direction
