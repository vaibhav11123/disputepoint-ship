# Replay package schema — `delhi-2025-07-29`

Path: [`data/replays/delhi-2025-07-29.json`](../../data/replays/delhi-2025-07-29.json)

## Top-level

| Field | Type | Notes |
|-------|------|-------|
| replay_id | string | `delhi-2025-07-29` |
| label | string | Human title |
| timezone | string | `Asia/Kolkata` |
| disclaimer | string | Honesty line |
| priority_uses | object | `{ station, rule }` — MVP: Safdarjung + `latest_completed_window_mm` |
| stations_context | string[] | Shown but do not drive R |
| steps | array | Ordered by `t` |
| gaps.points_without_day_evidence | string[] | Fixture IDs with no 29 Jul activation |

## Step kinds

### `weather`

| Field | Required |
|-------|----------|
| t, kind, station, precip_mm, period_start, period_end, source_url, is_synthetic, affects_priority | yes |

`affects_priority` must be true only when `station == priority_uses.station`.

### `incident_activate`

| Field | Required |
|-------|----------|
| t, kind, point_id, time_basis, source_url, note, is_synthetic | yes |

`point_id` must exist in fixtures. `time_basis`: `publication_earliest` | `reported_clock` | `unknown`.

## Time semantics

| Concept | Meaning |
|---------|---------|
| **Event time** | When waterlogging/incident occurred, if known |
| **Publication / observation time** | When a source reported it or a measurement window closed |
| `time_basis: publication_earliest` | Step `t` is earliest publication — **not** proof the event started then |
| `time_basis: reported_clock` | Step `t` is a clock stated in the source |
| `time_basis: unknown` | Do not invent a precise clock beyond the stored `t` used for ordering |

## Historical rain observation (runtime cache)

When seek materialises Safdarjung (or priority station) totals, the rain body is **display context**, not a 6h Open-Meteo observation:

- `source: historical_replay`
- `priority_uses: false` — do not feed mismatched periods into `R = min(1, mm/50)` as if they were 6h
- `period_start` / `period_end` from the weather step (e.g. 08:30–11:30 = 3h)
- `observation_type: reported_station_total`
- `window_hours: null`
- Station totals stay station-scoped (Ridge mm ≠ Purana Qila)

## Validation (runtime)

- Every step has `source_url` and `is_synthetic === false` for MVP package.  
- No interpolation steps.  
- Seek applies weather precip from latest Safdarjung weather step with `t <= seek_t` and `affects_priority` for **display**.  
- Seek activates points from incident steps with `t <= seek_t`.  
- Never mutates ownership / responsible_agency.
- Never label historical station totals as `MM / 6H`.
