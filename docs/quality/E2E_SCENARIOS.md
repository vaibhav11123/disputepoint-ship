# E2E scenarios

Critical-path scenarios for the DM coordination demo. Queue-first + point-card. IDs are E2E-* (not inventing Phase 6 T-* beyond LLD §10).

**Fixtures:** prefer playbook spine (`dp-purana-quila`, `dp-minto-bridge`, `dp-barapullah`, …). Do not invent coordinates or quotes.

---

## E2E-01 — Cold start queue (FR-008, FR-020, FR-021)

| Step | Action | Expect |
|------|--------|--------|
| 1 | Open app | Home is QueueTable, not map-only |
| 2 | Wait load | Loading state then ≥12 rows or empty-state copy if fixtures missing |
| 3 | Keyboard | Tab focus: queue rows then card |
| 4 | Select top row | PointCard opens with advisory banner |

## E2E-02 — Rain re-rank (FR-006, FR-007, US-03)

| Step | Action | Expect |
|------|--------|--------|
| 1 | Note dry ranks | Capture order at precip~0 / cached dry |
| 2 | Set scenario `precip_mm=40` | RainObservation `scenario_slider`, synthetic |
| 3 | Observe queue | Rank flash (≤200 ms) on moved rows; order may change |
| 4 | Kill live rain path (if testing fallback) | Slider + using-scenario copy available |

Maps: T-RAIN-01 (subset).

## E2E-03 — CONFLICT null agency (FR-011, FR-004, FR-017)

| Step | Action | Expect |
|------|--------|--------|
| 1 | Open `dp-purana-quila` (or fixture CONFLICT) | State CONFLICT |
| 2 | Agency cell | Blank / null — no silent single agency |
| 3 | Agencies | Multiple claimed agencies visible |
| 4 | Escalate copy | Ownership uncertain / escalate messaging |

Maps: T-OWN-CF-NULL, T-GOLD-PQ (partial).

## E2E-04 — HITL ACK / OVERRIDE / ESCALATE (FR-012, US-07)

| Step | Action | Expect |
|------|--------|--------|
| 1 | ASSIGNED + OPEN point | ACK enabled |
| 2 | ACK | Status ACKED; audit panel SYSTEM + HUMAN |
| 3 | CONFLICT point | ACK disabled or 409; OVERRIDE/ESCALATE available |
| 4 | OVERRIDE | Agency + reason + reviewer; panel shows recommended vs human |
| 5 | ESCALATE | Reason recorded; coordination handoff visible |

Maps: T-HITL-UI.

## E2E-05 — Synthetic honesty (FR-010, US-06)

| Step | Action | Expect |
|------|--------|--------|
| 1 | Point with `readiness.is_synthetic=true` | SYNTHETIC badge |
| 2 | Copy | Not live SCADA |
| 3 | Optional hide-synthetic | G contribution zeroed when toggle on (FR-013) |

Maps: T-UI-SYN.

## E2E-06 — Golden Purana Quila spine (FR-017, FR-027)

Ordered demo path (≤30 s triage KPI):

1. Load app → queue visible.
2. Select Purana Quila → CONFLICT + null agency + evidence quotes.
3. Wet rain 40 mm → re-rank visible.
4. Escalate or Override with reason → DecisionAuditPanel updated.
5. Provenance footer present.

Maps: T-GOLD-PQ, T-KPI-TRIAGE.

## E2E-07 — MapHUD secondary (FR-020) — **skippable**

Skip until ≥1 fixture point has human **VERIFIED** lat/lon (GAP-DATA-04). Demo ships without this scenario.

| Step | Action | Expect |
|------|--------|--------|
| 1 | Open app with null coords | Queue usable; MapHUD collapsed/empty |
| 2 | After VERIFIED promote: expand MapHUD | Markers for points with lat/lon; OSM attribution |
| 3 | Select Purana Quila row | Map `flyTo` / highlight; PointCard still primary |
| 4 | Click marker | Same `selectedPointId` as row click |
| 5 | Collapse MapHUD | Home still queue-first — not map-only |

## E2E-08 — Cmd+K point jump (J1)

| Step | Action | Expect |
|------|--------|--------|
| 1 | Press ⌘K / Ctrl+K | CommandPalette opens |
| 2 | Type part of a point name | Fuzzy match list |
| 3 | Enter on a result | PointCard matches selection; palette closes |
| 4 | Confirm | No Billing/Settings items |

## E2E-09 — Eval link or drawer (FR-015 / J2)

| Step | Action | Expect |
|------|--------|--------|
| 1 | Click footer “Judges: baseline tournament” | Opens markdown report and/or EvalDrawer |
| 2 | If metrics still TBD | Skeleton / TBD visible — **no invented Spearman** |
| 3 | Confirm | Markdown path remains SoT; UI is judges aid only |

## Out of scope for E2E MVP

- Map-primary navigation / flood heatmap home
- Live Bedrock extraction (off)
- RESOLVED status transitions
- Multi-user auth flows

## References

- [UX.md](../UX.md) regions and copy
- [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md)
- [LLD.md](../LLD.md) §2 golden sequence
- [build/DEMO_WOW.md](../build/DEMO_WOW.md)
