# Live sources — constant retrieval (reliability first)

**Status:** M1–M2 implemented in product; M3–M4 gated on human access/validation.  
**Hard rule:** Live data may update **context** and, where documented, **priority**. It must **never** auto-assign agency or resolve CONFLICT.

Related: [live-source-integration-records.md](live-source-integration-records.md)

## Layers

1. **Source reliability** — `SourceState`, registry, provenance, non-blocking pollers  
2. **Live integrations** — Open-Meteo (+ evidence); NWDP/CWC / IMD / Google behind gates  
3. **Operator UI** — compact source-health in `LiveSources` (not a monitoring dashboard)

## Source states

| State | Meaning |
|-------|---------|
| LIVE | Valid observation within freshness limit |
| STALE | Usable observation older than limit, or refresh failed with cache kept |
| UNAVAILABLE | No usable observation |
| UNKNOWN | Access not established |
| SCENARIO | Synthetic demo (labelled) |

Retrieval health ≠ observation freshness. Failed refresh preserves last-good; never invent `0.0 mm`.

## Implemented now

| Source | Code | Poll | Effects |
|--------|------|------|---------|
| Open-Meteo rain | `rain.py` + scheduler | `RAIN_POLL_MINUTES` when polling on | `priority_rule` |
| Evidence URL verify | `evidence_live.py` | `DP_EVIDENCE_POLL_MINUTES` if `DP_LIVE_FETCH=1` | context |
| Source registry/health | `source_registry.py`, `source_health.py` | — | — |
| Lifespan pollers | `source_scheduler.py` | off unless `DP_LIVE_FETCH` / `DP_SOURCE_POLLING` | — |

**Startup fix:** `create_app` no longer synchronously hits Open-Meteo / Nominatim / evidence when `DP_LIVE_FETCH=1`. Background tasks only.

## Gated (adapters stubbed)

Gated sources remain in `GET /health` → `sources[]` for registry/tests, but are **not** shown in the Command DATA SOURCES strip (`LiveSources`) until access is validated. Operator UI surfaces only `open-meteo-rain` and `evidence-live`.

| Source | access_status until validated | Adapter |
|--------|-------------------------------|---------|
| NWDP/CWC Yamuna WL | investigating | `sources/nwdp_cwc.py` |
| IMD district rain/warn/AWS | key_required | `sources/imd.py` |
| Google Flood Yamuna | waitlist | `sources/google_flood.py` |

### IMD shortlist (when key present)

District rainfall → district warnings → AWS `sid=7` → current weather. Never block demo; never auto-combine with Open-Meteo for priority without a new documented rule.

### NWDP/CWC

Validate one real Delhi/Yamuna observation (station, units, timestamp) before setting LIVE. Contact: helpdesk-nwic@gov.in.

### Google Flood Forecasting

Pilot waitlist; months possible. Context-only; verified vs lower-confidence gauges; no underpass interpolation.

## Config

```dotenv
RAIN_POLL_MINUTES=15
DP_LIVE_FETCH=0
DP_SOURCE_POLLING=   # optional override; default follows DP_LIVE_FETCH
DP_EVIDENCE_POLL_MINUTES=60
DP_FLOOD_CONTEXT_ENABLED=0
DP_FLOOD_POLL_MINUTES=30
DP_SOURCE_TIMEOUT_SECONDS=10
DP_SOURCE_MAX_BACKOFF_SECONDS=900
IMD_API_KEY=
DP_NWDP_CWC_RESOURCE=
GOOGLE_FLOOD_API_KEY=
DP_GOOGLE_FLOOD_ENABLED=0
```

## Explicit non-goals

Auto-agency · flood heatmap · fake SCADA · unvalidated IMD+OM blend · Redis/Kafka scheduler · Google as demo dependency.
