# Delhi 29 July 2025 — weather timeline

Clock: **Asia/Kolkata**. Values locked per [source discrepancies](delhi-2025-07-29-source-discrepancies.md).

## Timeline

| t (IST) | Station | precip_mm | period_start | period_end | affects_priority | Source |
|---------|---------|----------:|--------------|------------|------------------|--------|
| 2025-07-29T11:30:00+05:30 | Safdarjung | 63.5 | 08:30 | 11:30 | **yes** | ThePrint/PTI, TOI |
| 2025-07-29T11:30:00+05:30 | Ridge | 129.4 | 08:30 | 11:30 | no | ThePrint/PTI, TOI |
| 2025-07-29T11:30:00+05:30 | Pragati Maidan | 44.4 | 08:30 | 11:30 | no | ThePrint/PTI, TOI |
| 2025-07-29T11:30:00+05:30 | Lodhi Road | 64.5 | 08:30 | 11:30 | no | ThePrint/PTI, TOI |
| 2025-07-29T11:30:00+05:30 | Pusa | 37.5 | 08:30 | 11:30 | no | ThePrint/PTI, TOI |
| 2025-07-29T11:30:00+05:30 | Ayanagar | 23.0 | 08:30 | 11:30 | no | ThePrint/PTI, TOI |
| 2025-07-29T17:30:00+05:30 | Safdarjung | 68.1 | 08:30 | ~17:30 | **yes** | Indian Express day wrap |

## Notes

- Step timestamp `t` = end of reporting window (when the total becomes available for ops).  
- Spatial variance is the point: Ridge ≫ Safdarjung ≫ Pragati on the same 3h window.  
- This is **not** Open-Meteo 6h Delhi-centroid rain; do not label LIVE.  
- CP 100.2 mm / 2h (NDTV) omitted from priority series (see discrepancies).

## Priority rule (product)

`priority_uses = { station: Safdarjung, rule: latest_completed_window_mm }`  
After morning step, priority precip = **63.5**. After evening step, **68.1**.
