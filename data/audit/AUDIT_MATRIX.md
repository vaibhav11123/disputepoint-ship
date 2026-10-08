# AUDIT_MATRIX — Data Ready

Filled 2026-10-06. Do not paste full article text here.

## A. Per source

| slug | fetch_status | relevance | usable_for_points | quote_ready | notes |
|------|--------------|-----------|-------------------|-------------|-------|
| livelaw-hc-mmh | ok | keep | dp-purana-quila, dp-mathura-rd-hc, dp-bharat-mandapam-tunnel | yes | COURT; needs_review=true; pypdf extract |
| toi-drains-hc | ok | weak | dp-bharat-mandapam-tunnel | no | HTML ok; no clean contiguous quote promoted |
| ie-barapullah | ok | keep | dp-barapullah | yes | PRESS ownership blame |
| newslaundry-five | ok | keep | dp-minto-bridge, dp-aiims-aurobindo, dp-lodhi-moolchand, dp-pragati-bhairon | yes | PRESS multi-agency |
| et-seven-hotspot | ok | keep | dp-zakhira, dp-who-ito-ring, dp-loni-rd, dp-pul-prahladpur | yes | seven-hotspot list |
| toi-confusion-hc | ok | keep | dp-maharani-bagh | yes | HC confusion / RWA |
| ht-cctv | ok | weak | dp-pul-prahladpur | weak | title-heavy; prefer ET |
| ht-308 | ok | keep | dp-zakhira | yes | PWD critical locations |
| toi-azad-market | ok | keep | dp-azad-market | yes | hotspot recurrence |
| theprint-dm71 | ok | keep | _(mandate only)_ | yes | DM-71 cite; not a point |

Fetch summary: **10 ok / 0 gated / 0 failed**. ROS mine: URL cites only (no bodies). Rain sample: ok (Open-Meteo CC-BY).

## B. Per point

| point_id | spine | evidence_count | ownership_signal | agency_signal | geo | sufficiency | ask |
|----------|-------|----------------|------------------|---------------|-----|-------------|-----|
| dp-purana-quila | yes | 2 | ok | ok | null_accept | GREEN | — |
| dp-bharat-mandapam-tunnel | no | 1 | ok | ok | null_accept | GREEN | — |
| dp-mathura-rd-hc | no | 1 | ok | thin | null_accept | GREEN | — |
| dp-barapullah | yes | 2 | ok | ok | null_accept | GREEN | — |
| dp-minto-bridge | yes | 2 | ok | ok | null_accept | GREEN | — |
| dp-aiims-aurobindo | no | 1 | ok | ok | null_accept | GREEN | — |
| dp-lodhi-moolchand | no | 1 | ok | ok | null_accept | GREEN | — |
| dp-maharani-bagh | no | 1 | thin | thin | null_accept | AMBER | optional better quote |
| dp-who-ito-ring | no | 1 | thin | ok | null_accept | AMBER | — |
| dp-zakhira | no | 2 | thin | ok | null_accept | GREEN | — |
| dp-pul-prahladpur | no | 1 | thin | ok | null_accept | AMBER | — |
| dp-azad-market | no | 1 | thin | missing | null_accept | AMBER | — |
| dp-pragati-bhairon | no | 1 | thin | ok | null_accept | AMBER | — |
| dp-loni-rd | no | 1 | thin | ok | null_accept | AMBER | — |

## Checkpoint log

- Phase 3 (2026-10-06): spine all GREEN; ≥3 spine quotes ready → **skip Phase 4 gap-fill**.
- Phase 5: promoted spine + stretch evidence; geo = null_accept (MapHUD skippable); no Nominatim re-hit.
- Phase 6: seed validate + §F Data Ready PASS.

## Handoff

Residual AMBER: maharani-bagh, who-ito-ring, pul-prahladpur, azad-market, pragati-bhairon, loni-rd (usable but thin). BLOCKED URLs: none. Next: **Phase 7 coding**. Still later: eval/gold, demo video, deploy/AWS, T-VIS-AUDIT. L0 bodies stay gitignored.

## C. Full-board v0.3 (2026-10-08)

- Gate A densified (≥4 evidence each) + `channel=VOLUNTEER_REPORTED` rows.
- Expansion B: ~21 press-named areas (demo volume; lat/lon null until VERIFIED).
- Total board ~35 points / ~120+ evidence. Not a 445-row dump; not DM-71.
- Generators: `scripts/build_fullboard_fixtures.py`, `scripts/fix_fullboard_spine.py`.
