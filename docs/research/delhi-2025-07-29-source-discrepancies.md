# Delhi 29 July 2025 — source discrepancies

**Purpose:** Resolve conflicting press/IMD figures before locking replay weather rows.  
**Retrieved:** 2026-10-09 · research for DisputePoint historical replay (stored data only).

## Locked vs discarded

| Observation | Decision | Rationale |
|-------------|----------|-----------|
| Safdarjung **63.5 mm**, 08:30–11:30 IST | **LOCK** (`affects_priority`) | Consistent across ThePrint/PTI, TOI, NewsArenaIndia |
| Ridge **129.4 mm**, 08:30–11:30 IST | **LOCK** (context only) | Same PTI cluster; morning window |
| Pragati Maidan **44.4 mm**, 08:30–11:30 IST | **LOCK** (context) | Same PTI cluster |
| Lodhi Road **64.5 mm**, 08:30–11:30 IST | **LOCK** (context) | Same PTI cluster |
| Pusa **37.5 mm**, 08:30–11:30 IST | **LOCK** (context) | Same PTI cluster |
| Ayanagar **23 mm**, 08:30–11:30 IST | **LOCK** (context) | Same PTI cluster |
| Safdarjung **68.1 mm** (day total / longer window) | **LOCK** as separate row | Indian Express 30 Jul wrap; period treated as through evening (~08:30–17:30 class), **not** substituted for 3h total |
| Ridge **129.8 mm** (IE day wrap) | **DISCARD as duplicate** | Likely rounding / end-of-day reprint of Ridge morning total; prefer 129.4 with explicit 3h window |
| Pragati Maidan **45.6 mm** (IE) | **DISCARD** | Conflicts with 44.4 morning RMC figure; keep 44.4 |
| LiveMint alternate Safdarjung **55.0 mm** list | **DISCARD** | Inconsistent with RMC 63.5 in same article’s other table |
| NDTV Connaught Place **100.2 mm / 2 h** | **CONTEXT ONLY** (unmapped fixture) | Different metric/place; no `dp-*` for CP plaza; do not convert to 6h metro precip |
| IMD PR “very light to light” past 24h to 08:30 | **NOT a day total for the event** | Pre-event bulletin; heavy rain was daytime 29 Jul |

## Period rules (hard)

- Do **not** invent a 6-hour Open-Meteo-equivalent total from 3h or ~9h station windows.
- Product priority uses **Safdarjung** only (`priority_uses.station = Safdarjung`).
- Ridge / Pragati / Lodhi / Pusa / Ayanagar = multi-station **context strip**, `affects_priority: false`.

## Primary sources

1. [ThePrint / PTI](https://theprint.in/india/red-alert-issued-as-heavy-rain-batters-delhi-causes-waterlogging-and-traffic-snarls/2705877/) — 29 Jul 2025  
2. [Times of India](https://timesofindia.indiatimes.com/city/delhi/heavy-rainfall-disrupts-delhi-air-india-and-igi-airport-issue-travel-advisories/articleshow/122965653.cms) — 29 Jul 2025  
3. [Indian Express](https://indianexpress.com/article/cities/delhi/delhi-downpour-triggers-waterlogging-traffic-chaos-and-political-sparring-10158311/) — 30 Jul 2025 wrap  
4. [NewsArenaIndia](https://newsarenaindia.com/states/delhi-on-red-alert-amid-heavy-showers-waterlogging/51661) — traffic list mirror  
5. [NDTV](https://www.ndtv.com/delhi-news/delhi-rain-video-delhis-connaught-place-other-areas-flooded-after-heavy-rain-8972439) — CP / underpass advisories  

## Confidence

- Weather morning window (RMC via PTI): **high**  
- Day-end Safdarjung 68.1: **medium** (period less precisely stated than 08:30–11:30)  
- Traffic-police named underpasses: **high** for activation mapping  
- Generic “ITO waterlogging” photos/politics: **medium** (maps to `dp-who-ito-ring`, not exclusive ownership proof)
