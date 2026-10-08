# Baseline tournament

LLD §22 methods. ML row is omitted (Phase 6 gate = no KEEP).

Measured on 2026-10-08 from `OwnershipEngine` + `PriorityEngine` over `data/fixtures/` at dry `precip_mm=0`. All fourteen points carry cited Nominatim coordinates. Severity is absent on the seed, so S is 0. Spine CONFLICT (Purana, Minto, Barapullah, Lodhi) keeps null agency. Seven ASSIGNED rows are PWD where cited press/court weight clears θ. Three UNKNOWN rows remain true gaps (Maharani, Azad, AIIMS).

## Methods

| Method | Role | In this run |
|--------|------|-------------|
| Random | Control | Not sampled. No gold order to score against. |
| Severity-only | Heuristic | S is 0 on every seed, so this order is a tie. |
| Rain-only | Heuristic | Dry precip is 0, so R is 0 for every point. |
| Static hotspot priority | Heuristic | Not a second list. Spine points are not reordered by hand. |
| Recurrence-only | Heuristic | Folded into Q of the weighted score below. |
| Nearest-agency heuristic | Weak ownership | Not run as a separate scorer. Coordinates exist on 14 points. |
| Weighted P | Target | Measured table below. |
| ML model | Only if KEEP | Out of MVP. |

## Measured weighted order (dry)

| Rank | Point | Score | State | Agency | U |
|------|-------|-------|-------|--------|---|
| 01 | dp-maharani-bagh | 0.3850 | UNKNOWN | null | 1.00 |
| 02 | dp-barapullah | 0.3550 | CONFLICT | null | 0.80 |
| 03 | dp-minto-bridge | 0.3550 | CONFLICT | null | 0.80 |
| 04 | dp-purana-quila | 0.3550 | CONFLICT | null | 0.80 |
| 05 | dp-azad-market | 0.3400 | UNKNOWN | null | 1.00 |
| 06 | dp-lodhi-moolchand | 0.3100 | CONFLICT | null | 0.80 |
| 07 | dp-aiims-aurobindo | 0.2988 | UNKNOWN | null | 0.72 |
| 08 | dp-who-ito-ring | 0.2863 | ASSIGNED | PWD | 0.17 |
| 09 | dp-mathura-rd-hc | 0.2350 | ASSIGNED | PWD | 0.00 |
| 10 | dp-bharat-mandapam-tunnel | 0.2238 | ASSIGNED | PWD | 0.22 |
| 11 | dp-pragati-bhairon | 0.2162 | ASSIGNED | PWD | 0.17 |
| 12 | dp-zakhira | 0.2162 | ASSIGNED | PWD | 0.17 |
| 13 | dp-loni-rd | 0.1712 | ASSIGNED | PWD | 0.17 |
| 14 | dp-pul-prahladpur | 0.1712 | ASSIGNED | PWD | 0.17 |

## Metrics vs gold

`gold_order.json` is not in the tree (G-GOLD). These cells stay blank. See GAP-EVAL-02.

| Metric | Weighted P | Severity-only | Rain-only | Random |
|--------|------------|---------------|-----------|--------|
| Top-k agreement | | | | |
| Spearman | | | | |
| Kendall | | | | |
| Ownership accuracy | | | | |
| False assignment rate | | | | |

False assignment on this fixture run, without gold: ASSIGNED rows are PWD only where quotes name PWD; CONFLICT rows keep `responsible_agency = null`.
