# Baseline tournament

LLD §22 methods. ML row is omitted (Phase 6 gate = no KEEP).

Measured on 2026-10-08 from `OwnershipEngine` + `PriorityEngine` over `data/fixtures/` at dry `precip_mm=0`. No coordinates were added. Severity is absent on the seed, so S is 0. Every current fixture row is `UNKNOWN` with `responsible_agency` null: tagged evidence weights do not clear θ 0.65 and do not form a close pair above 0.4.

## Methods

| Method | Role | In this run |
|--------|------|-------------|
| Random | Control | Not sampled. No gold order to score against. |
| Severity-only | Heuristic | S is 0 on every seed, so this order is a tie. |
| Rain-only | Heuristic | Dry precip is 0, so R is 0 for every point. |
| Static hotspot priority | Heuristic | Not a second list. Spine points are not reordered by hand. |
| Recurrence-only | Heuristic | Folded into Q of the weighted score below. |
| Nearest-agency heuristic | Weak ownership | Not run. No verified coordinates. |
| Weighted P | Target | Measured table below. |
| ML model | Only if KEEP | Out of MVP. |

## Measured weighted order (dry)

| Rank | Point | Score | State | Agency | U |
|------|-------|-------|-------|--------|---|
| 01 | dp-barapullah | 0.3850 | UNKNOWN | null | 1.00 |
| 02 | dp-maharani-bagh | 0.3850 | UNKNOWN | null | 1.00 |
| 03 | dp-minto-bridge | 0.3850 | UNKNOWN | null | 1.00 |
| 04 | dp-purana-quila | 0.3850 | UNKNOWN | null | 1.00 |
| 05 | dp-who-ito-ring | 0.3688 | UNKNOWN | null | 0.72 |
| 06 | dp-azad-market | 0.3400 | UNKNOWN | null | 1.00 |
| 07 | dp-lodhi-moolchand | 0.3400 | UNKNOWN | null | 1.00 |
| 08 | dp-mathura-rd-hc | 0.3100 | UNKNOWN | null | 0.50 |
| 09 | dp-aiims-aurobindo | 0.2988 | UNKNOWN | null | 0.72 |
| 10 | dp-pragati-bhairon | 0.2988 | UNKNOWN | null | 0.72 |
| 11 | dp-zakhira | 0.2988 | UNKNOWN | null | 0.72 |
| 12 | dp-bharat-mandapam-tunnel | 0.2650 | UNKNOWN | null | 0.50 |
| 13 | dp-loni-rd | 0.2537 | UNKNOWN | null | 0.72 |
| 14 | dp-pul-prahladpur | 0.2537 | UNKNOWN | null | 0.72 |

## Metrics vs gold

`gold_order.json` is not in the tree (G-GOLD). These cells stay blank. See GAP-EVAL-02.

| Metric | Weighted P | Severity-only | Rain-only | Random |
|--------|------------|---------------|-----------|--------|
| Top-k agreement | | | | |
| Spearman | | | | |
| Kendall | | | | |
| Ownership accuracy | | | | |
| False assignment rate | | | | |

False assignment on this fixture run, without gold: 0 points received a non-null agency.
