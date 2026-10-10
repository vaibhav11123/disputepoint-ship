# Live source integration records

Schema for each provider before (and after) product wiring.

```text
source_id
source_name
endpoint_or_resource
access_status          # investigating | key_required | waitlist | active | blocked
source_state           # LIVE | STALE | UNAVAILABLE | UNKNOWN | SCENARIO
station_or_location
observation_time
retrieved_at
units
freshness_limit
last_success
last_error_category    # auth | network | empty | stale | parse | coverage | waitlist
allowed_effects        # context | priority_rule | none
```

## Registry (initial)

| source_id | access_status | allowed_effects | Notes |
|-----------|---------------|-----------------|-------|
| open-meteo-rain | active | priority_rule | Primary rain; Open-Meteo CC-BY |
| evidence-live | active | context | URL fetch + quote⊆source |
| imd-district-rainfall | key_required | context | Needs `IMD_API_KEY` |
| imd-district-warning | key_required | context | Needs key |
| imd-aws | key_required | context | `sid=7` DELHI when key |
| nwdp-cwc-yamuna-wl | investigating | context | Validate station before LIVE |
| google-flood-yamuna | waitlist | context | Pilot access |

Runtime values are exposed on `GET /health` → `sources[]`.

## Validation checklist (per new source)

- [ ] Authenticated/independent retrieval succeeds  
- [ ] `observation_time` and `retrieved_at` both stored  
- [ ] Freshness limit matches publication cadence  
- [ ] Failure leaves app usable; last-good preserved  
- [ ] UI shows LIVE/STALE/UNAVAILABLE/UNKNOWN/SCENARIO honestly  
- [ ] `allowed_effects` enforced (no silent priority/agency)  
- [ ] Sanitized fixture saved for tests (no secrets)
