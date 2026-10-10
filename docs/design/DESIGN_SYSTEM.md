# Design system — Ink · Stone · Forest

Ops UI tokens for DisputePoint. **Product copy:** [UX_COPY.md](../UX_COPY.md). Visual contract: Ink · Stone · Forest redesign plan.

**Product shape:** queue-first + point-card. Not a flood heatmap. Not a marketing landing page.

## Foundations

| Kind | Rule |
|------|------|
| Type | IBM Plex Sans (UI) + IBM Plex Mono (ids, timestamps, scores) |
| Radius | Panels 6–10px; controls slightly tighter |
| Border | 1px `--dp-border` |
| Elevation | Restrained; selective borders over shadows |
| Spacing | 4 / 8 / 12 / 16 / 24 / 32 / 40 / 48 / 64 |
| Selection | `--dp-brand-tint` + 3px brand/ink rail — not solid green wash |
| Density | Productive ops density (queue + map in one viewport) |
| Motion | Restrained map camera; honor `prefers-reduced-motion` |

## Color tokens

| Token | Hex | Role |
|-------|-----|------|
| `--dp-ink` | `#17211F` | Shell, primary actions |
| `--dp-ink-raised` | `#22312D` | Raised Ink |
| `--dp-canvas` | `#F4F3EE` | Workspace (Stone) |
| `--dp-surface` | `#FFFFFF` | Panels |
| `--dp-surface-subtle` | `#EBEEE8` | Secondary surfaces |
| `--dp-border` | `#DCE1DA` | Borders |
| `--dp-brand` | `#176B55` | Forest — brand / selection / active nav only |
| `--dp-brand-hover` | `#125641` | Brand hover |
| `--dp-review` | `#95620B` | Unresolved responsibility / review |
| `--dp-review-bg` | `#FFF4D6` | Restrained review wash |
| `--dp-success` | `#26734A` | Confirmed / resolved only |
| `--dp-critical` | `#B93832` | Justified urgency |
| `--dp-text` | `#202925` | Primary text |
| `--dp-text-muted` | `#66716A` | Secondary |
| `--dp-scenario` | neutral gray | Scenario / unavailable chrome |

**Rules:** Forest ≠ success. Amber ≠ whole-incident flood. ACTION REQUIRED never success-green. Status always includes text. Validate contrast on Ink shell and amber chips.

## Typography roles

| Class | Use |
|-------|-----|
| `.dp-page-title` | Command page title (~28/600) |
| `.dp-incident-title` | Incident name (~26/600) |
| `.dp-section` | Section headings (~16/600) |
| `.dp-body` | Body / evidence (~14/1.45) |
| `.dp-meta` | Quiet metadata |
| `.dp-status-label` | Scarce uppercase status chips |

Uppercase only for short chips: `RESPONSIBILITY DISPUTED`, `OFFICER CONFIRMED`, `AUTOMATIC ASSIGNMENT BLOCKED`.

## Layout targets (1440 × 900)

| Region | Target |
|--------|--------|
| Navigation | 64 px |
| Operational summary | 68 px |
| Scenario strip | 40 px when needed |
| Horizontal margin | 28 px |
| Queue/map gap | 18 px |
| Queue/map | 58% / 42% of content width |
| Queue header / row | 40 px / 48 px |

Shell = stable desktop composition (not clipping). Narrow: queue-first + map toggle.

## Stack lock

Vite + React + TypeScript + `tokens.css` (`--dp-*`) + FastAPI. **No** Tailwind, shadcn, Carbon React, or new aesthetic direction from skills.

## Signature component

**Responsibility Assessment** — claims (equal weight) → what evidence establishes → what remains unresolved → automatic assignment blocked. Not a yellow alert flood.
