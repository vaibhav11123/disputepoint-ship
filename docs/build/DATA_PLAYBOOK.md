# Data playbook — DisputePoint fixtures

**Purpose:** Minute-level recipes for curating the MVP point corpus. Agents and humans extract into JSON; they do not invent.  
**SoT:** [../PHASE6.md](../PHASE6.md) + Phase 4 Gate A. If this playbook disagrees with Phase 6, follow Phase 6.  
**Corpus:** Gate A rows **1–14** = conflict spine. **Expansion B** (~21 press-named areas) = demo volume only — not DM-71 bulk. Row 15 (DM-71) remains a **mandate cite**, not a point.  
**Numeric locks SoT:** [../LLD.md](../LLD.md) §24 (W_NORM, θ, rain window/poll, wet/dry precip) — do not soft-change here.

**Volunteer channel:** optional evidence field `channel: "VOLUNTEER_REPORTED"` (UI chip). Ownership `type` stays `PRESS_REPORT` (weight 0.55). Never treat volunteer rows as SCADA/live depths.
---

## Do not invent

- No DM-71 full coordinates or unnamed “spot 47”.
- No SCADA / pump GPS / live telemetry marked as real.
- No quote that is not a substring of the cited source after fetch.
- `is_synthetic=true` forever for readiness unless a public non-SCADA fact exists — and still never invent that fact.
- `lat` / `lon` stay `null` / `TBD_GEOCODE` in fixtures until a human marks a Nominatim candidate **VERIFIED**. Do not invent decimals. Procedure: [../research/geocode-candidates.md](../research/geocode-candidates.md).
- Expansion B stays null-geo until VERIFIED; do not invent decimals to fill the map.

---

## Geocode procedure (GAP-DATA-04)

1. One-shot Nominatim search (≤1 req/s, identifying User-Agent) — **offline only**, never from the demo runtime.
2. Record candidates in [../research/geocode-candidates.md](../research/geocode-candidates.md) with `CANDIDATE` / `FAILED`.
3. Human eyeballs map match → `VERIFIED`.
4. On promote: set `lat`/`lon` plus provenance `geo_source=nominatim`, `geo_query`, `geo_osm_id`; attribute OSM ODbL in UI/README.
5. Until verified, fixtures keep `lat`/`lon` null.
6. **MapHUD consumer:** VERIFIED `lat`/`lon` feed the secondary MapLibre HUD ([DEMO_WOW.md](DEMO_WOW.md) M1). Until then MapHUD stays collapsed/empty; do not invent coords to enable the map.

---

## Files

| Path | Role |
|------|------|
| `data/fixtures/points.json` | L2 seeds (points **0.3.3**; evidence corpus **0.3.5**); validate each item against [DisputePointSeed.schema.json](../schemas/DisputePointSeed.schema.json); `evidence_ids` when promoted |
| `data/fixtures/evidence.json` | L2 Evidence rows (short quote⊆source only) |
| `data/fixtures/readiness.json` | Readiness objects keyed by `point_id` |
| `data/audit/` | L1: `FETCH_MANIFEST.json`, `AUDIT_MATRIX.md`, `GAP_ASK.md`, `README.md` (committed). L0: `sources/`, `rain/`, `geo/`, `_work/` (**gitignored**) |
| Promote path | AUDIT_MATRIX keep + quote⊆source verify → L2 fixtures (never commit full articles/PDFs) |
| `version` | Semver on each fixture file root |

Suggested fixture root shape:

```json
{
  "version": "0.2.0",
  "points": [ ]
}
```

Agency allowlist (schema): `PWD`, `MCD`, `NDMC`, `IFC`, `DDA`, `DJB`, `RAILWAYS`, `CPWD`, `OTHER`, `UNKNOWN`.  
Map Gate A “I&FC” → `IFC`.

---

## Rain (locked)

```text
GET https://api.open-meteo.com/v1/forecast
  ?latitude=28.6139
  &longitude=77.2090
  &hourly=precipitation
  &past_hours=6
  &forecast_hours=0
  &timezone=Asia%2FKolkata
```

| Field | Mapping |
|-------|---------|
| `precip_mm` | sum of `hourly.precipitation` over returned hours |
| `window_hours` | `6` |
| `source` | `open-meteo` |
| `is_synthetic` | `false` when HTTP 200 |
| failure | use last cache, else scenario slider; UI copy `Using scenario rain` |

Demo pair: wet `precip_mm=40`, dry `0`. Poll every **15 minutes**.  
IMD: COULD only if `IMD_API_KEY` set; never block the demo.

`normalize_rain(precip_mm) = min(1.0, max(0.0, precip_mm / 50.0))` — ASSUMPTION (see LLD locks).

---

## Extract checklist (every evidence row)

1. Fetch source; keep `retrieved_at` ISO-8601.
2. Copy a `quote` ≥10 characters that appears **verbatim** in the source (quote ⊆ source).
3. Set `agency` from allowlist or `null` if the excerpt does not name one.
4. Record dispute / ownership signal in `location_span` or quote context.
5. Set `type` from enum; weight follows type default (COURT 1.0 … HEURISTIC 0.35).
6. `needs_review=true` until human validates COURT_ORDER / GOV_ORDER.
7. Never mark invented readiness as non-synthetic.

---

## Recurrence map (locked)

| Gate A signal language | `recurrence_class` | Q unit |
|------------------------|--------------------|--------|
| chronic / judicial notice of flooding / chronic hotspot | `chronic` | 1.0 |
| recurring / repeated / ≥4 floods/year / top recurring | `recurring` | 0.7 |
| occasional / named in plan without chronic language | `occasional` | 0.4 |
| unclear | `unknown` | 0.2 |

---

## Recipes (Gate A #1–#14)

### 1 — `dp-purana-quila`

| Field | Value |
|-------|-------|
| Display name | Purana Quila Rd storm drain (India Gate→Yamuna) |
| `agencies_claimed` | NDMC, PWD, MCD, IFC (six sections) |
| Sources | [LiveLaw HC PDF](https://www.livelaw.in/pdf_upload/mmh08042024cw75942018185925-533124.pdf) |
| Dispute signal | Multi-agency slope/level failure; HC judicial notice of flooding |
| `recurrence_class` | `chronic` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote naming multi-section / multi-agency drain ownership along Purana Quila corridor |

### 2 — `dp-bharat-mandapam-tunnel`

| Field | Value |
|-------|-------|
| Display name | Bharat Mandapam / Purana Quila tunnel |
| `agencies_claimed` | PWD |
| Sources | Same HC PDF; [TOI HC](https://timesofindia.indiatimes.com/city/delhi/assign-upkeep-of-all-drains-to-1-dept-hc/articleshow/109207116.cms) |
| Dispute signal | Flooded/closed in 2023 monsoon alongside corridor |
| `recurrence_class` | `recurring` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote tying tunnel/corridor flooding to PWD (or L&T under PWD) |

### 3 — `dp-mathura-rd-hc`

| Field | Value |
|-------|-------|
| Display name | Mathura Rd / High Court pool bungalows |
| `agencies_claimed` | PWD (corridor; multi-agency context) |
| Sources | LiveLaw HC PDF |
| Dispute signal | Flooding of carriageway & bungalows |
| `recurrence_class` | `chronic` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote on Mathura Road / bungalow flooding from HC record |

### 4 — `dp-barapullah`

| Field | Value |
|-------|-------|
| Display name | Barapullah drain (outfall / wall breach) |
| `agencies_claimed` | PWD, MCD, IFC |
| Sources | [IE](https://indianexpress.com/article/cities/delhi/breach-in-barapullah-drain-wall-led-to-south-new-delhi-flooding-9421799/) |
| Dispute signal | Back-flow blamed; agencies denied/unclear ownership |
| `recurrence_class` | `chronic` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote on wall breach / ownership handoff confusion |

### 5 — `dp-minto-bridge`

| Field | Value |
|-------|-------|
| Display name | Minto Bridge / Minto Road underpass |
| `agencies_claimed` | NDMC, MCD, PWD, RAILWAYS |
| Sources | [Newslaundry](https://www.newslaundry.com/2024/06/29/whos-responsible-for-delhis-rain-mess-answers-from-5-of-the-worst-hit-spots); [ET seven-hotspot](https://economictimes.indiatimes.com/news/india/new-drains-sumps-automated-pump-house-delhi-pwds-plan-to-tackle-waterlogging-at-seven-hotspots/articleshow/121268671.cms) |
| Dispute signal | Chronic hotspot; each agency blames other; in PWD 7-hotspot plan |
| `recurrence_class` | `chronic` |
| Readiness | `GAP` or `UNKNOWN`, `is_synthetic=true` (do not invent pump house facts) |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote on multi-agency blame at Minto underpass |

### 6 — `dp-aiims-aurobindo`

| Field | Value |
|-------|-------|
| Display name | AIIMS / Aurobindo Marg |
| `agencies_claimed` | PWD, NDMC, MCD |
| Sources | Newslaundry (same five-spots piece) |
| Dispute signal | NDMC claims MCD drains not cleaned caused NDMC-area flooding |
| `recurrence_class` | `recurring` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote naming NDMC vs MCD drain blame |

### 7 — `dp-lodhi-moolchand`

| Field | Value |
|-------|-------|
| Display name | Lodhi Rd / Moolchand Ring Rd |
| `agencies_claimed` | PWD, CPWD, MCD |
| Sources | Newslaundry; [HT CCTV](https://www.hindustantimes.com/cities/delhi-news/cctvs-in-delhi-underpasses-to-keep-eye-on-waterlogging-101746813831570.html) |
| Dispute signal | Multi-owner drainage blame; CCTV/SCADA **planned** (not live — do not invent GPS) |
| `recurrence_class` | `recurring` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote on multi-owner drainage / underpass monitoring plan |

### 8 — `dp-maharani-bagh`

| Field | Value |
|-------|-------|
| Display name | Maharani Bagh / Taimur Nagar drain / Ring Rd wells |
| `agencies_claimed` | PWD, MCD, DJB |
| Sources | [TOI](https://timesofindia.indiatimes.com/india/much-confusion-on-who-does-what-even-upkeep-of-drains-hc-to-delhi-government/articleshow/122963747.cms) |
| Dispute signal | HC 2025 “enormous confusion,” buck-passing; site inspection ordered |
| `recurrence_class` | `chronic` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote on confusion / who-does-what for drains |

### 9 — `dp-who-ito-ring`

| Field | Value |
|-------|-------|
| Display name | Ring Road opposite WHO (ITO) |
| `agencies_claimed` | PWD |
| Sources | ET seven-hotspot plan |
| Dispute signal | Chronic; short-term pumps + new drains planned |
| `recurrence_class` | `chronic` |
| Readiness | `GAP`, `is_synthetic=true` (planned pumps ≠ live SCADA) |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote naming WHO / ITO / Azad Bhawan interconnection hotspot |

### 10 — `dp-zakhira`

| Field | Value |
|-------|-------|
| Display name | Zakhira flyover underpass |
| `agencies_claimed` | PWD |
| Sources | ET; [HT 308](https://www.hindustantimes.com/cities/delhi-news/delhi-marks-100-new-flooding-spots-many-along-ring-road-101719339431895.html) |
| Dispute signal | Recurring ≥4 floods/year class; desilt + long-term drain plan |
| `recurrence_class` | `recurring` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote on Zakhira underpass recurrence / drains |

### 11 — `dp-pul-prahladpur`

| Field | Value |
|-------|-------|
| Display name | Pul Prahladpur underpass |
| `agencies_claimed` | PWD |
| Sources | ET; HT CCTV |
| Dispute signal | Readiness capital spent (pump/sump cited in press); still monitored; CCTV planned |
| `recurrence_class` | `occasional` |
| Readiness | Prefer quote-backed `OK` **only** if press states installed capacity; else `UNKNOWN`. Always `is_synthetic=true` unless a public non-SCADA fact is copied verbatim — never invent HP/litre numbers. |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote on pump house / sump / monitoring — copy numbers only if present in source |

### 12 — `dp-azad-market`

| Field | Value |
|-------|-------|
| Display name | Azad Market underpass |
| `agencies_claimed` | OTHER / multi civic (use `OTHER` or null until cite names one) |
| Sources | [TOI 445](https://timesofindia.indiatimes.com/city/delhi/number-of-waterlogging-hotspots-up-set-to-challenge-delhis-preparedness/articleshow/120652175.cms) |
| Dispute signal | Top recurring underpass class 2024; multi-MLA jurisdictions |
| `recurrence_class` | `recurring` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote placing Azad Market among recurring underpass hotspots |

### 13 — `dp-pragati-bhairon`

| Field | Value |
|-------|-------|
| Display name | Pragati Maidan / Bhairon corridor tunnel |
| `agencies_claimed` | PWD |
| Sources | Newslaundry; HT 308 |
| Dispute signal | Repeated closures; flood watchlist around new corridor |
| `recurrence_class` | `recurring` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote on corridor / tunnel closures (label design-defect claims as press narrative, not COURT) |

### 14 — `dp-loni-rd`

| Field | Value |
|-------|-------|
| Display name | Loni Rd roundabout |
| `agencies_claimed` | PWD |
| Sources | ET; HT |
| Dispute signal | Named in 7-hotspot / 24h monitor set |
| `recurrence_class` | `occasional` |
| Readiness | `UNKNOWN`, `is_synthetic=true` |
| `lat`/`lon` | `TBD_GEOCODE` |
| Extract focus | Quote naming Loni Road in PWD hotspot / monitor set |

---

## Mandate cite (not a point)

**DM-71** — use in README / copy / DM mandate banner only:

- [ThePrint/PTI](https://theprint.in/india/delhi-govt-directs-district-magistrates-to-fix-71-waterlogging-spots-ahead-of-monsoon/2663818/)
- Do **not** create `dp-dm-71-*` placeholder points without named locations and sources.

---

## Priority demo spine (must appear in fixtures)

From LLD seed intent + this corpus: at minimum include `dp-purana-quila`, `dp-minto-bridge`, `dp-barapullah`, `dp-aiims-aurobindo`, `dp-maharani-bagh`, `dp-who-ito-ring`, `dp-zakhira`, `dp-pul-prahladpur`, `dp-azad-market`. Prefer shipping all 14 when extracts are ready.
