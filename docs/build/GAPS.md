# Implementation gaps and solutions

**Purpose:** Inventory of weaknesses that can block Phase 7, plus web-researched unlock recipes.  
**SoT for product behavior:** [../PHASE6.md](../PHASE6.md). This file is not a second contract.  
**Last updated:** 2026-10-10 (corpus points 0.3.3 / evidence 0.3.6 board mix; prior Data Ready 2026-10-06).  
**Fixtures playbook:** [DATA_PLAYBOOK.md](DATA_PLAYBOOK.md) · **Audit:** [../../data/audit/](../../data/audit/) · **Geocode candidates:** [../research/geocode-candidates.md](../research/geocode-candidates.md)  
**Gate:** [SPEC_READINESS.md](../quality/SPEC_READINESS.md) Spec + Data Ready **PASS**. GAP-DATA-04 geocodes still READY (human VERIFIED).

Status values: **LOCKED** (prose closed) · **READY** (recipe + partial artifacts; finish in Phase 7) · **DEFERRED** (needs Phase 7 / human) · **OPEN** (should not remain).

---

## Inventory

| id | area | severity | symptom | owner | status | resolved_in |
|----|------|----------|---------|-------|--------|-------------|
| GAP-DATA-01 | data | P0 | No per-point extract recipe; agents invent quotes/coords | docs | LOCKED | [DATA_PLAYBOOK.md](DATA_PLAYBOOK.md) |
| GAP-DATA-02 | data | P0 | Fixture file layout / version unset | docs | LOCKED | DATA_PLAYBOOK § Files |
| GAP-DATA-03 | data | P0 | `data/fixtures/*.json` bytes missing | human+Phase7 | LOCKED | points 0.3.3 / evidence 0.3.6 (GOV_ORDER curated for ASSIGNED mix; advanced from v0.2 promote 2026-10-06); L0 audit gitignored; COURT needs_review |
| GAP-DATA-04 | data | P1 | `lat`/`lon` geocodes TBD for all 14 points | human | READY | [../research/geocode-candidates.md](../research/geocode-candidates.md) |
| GAP-DATA-05 | data | P1 | Row 15 DM-71 bulk mistaken for a demo point | docs | LOCKED | DATA_PLAYBOOK corpus note |
| GAP-DATA-06 | data | P2 | LICENSE_AUDIT rows incomplete for extracts | docs | LOCKED | URL rows for fixture sources filled 2026-10-06 |
| GAP-RAIN-01 | rain | P0 | Open-Meteo HTTP URL / params not copy-pasteable | docs | LOCKED | LLD § Implementation locks; live probe OK |
| GAP-RAIN-02 | rain | P0 | `normalize_rain` formula undefined | docs | LOCKED | LLD § Implementation locks |
| GAP-RAIN-03 | rain | P1 | Wet/dry demo precip pair for US-03 ambiguous | docs | LOCKED | wet=40 / dry=0 |
| GAP-RAIN-04 | rain | P1 | Poll interval / window_hours not locked in LLD | docs | LOCKED | 15 min / 6 h |
| GAP-RAIN-05 | rain | P2 | IMD path optional vs blocking unclear | docs | LOCKED | IMD COULD if env key; never block |
| GAP-SCORE-01 | scoring | P0 | `W_NORM` numeric value unset | docs | LOCKED | W_NORM=2.0 |
| GAP-SCORE-02 | scoring | P0 | `recurrence_to_unit` map incomplete | docs | LOCKED | chronic/recurring/occasional/unknown |
| GAP-SCORE-03 | scoring | P0 | `readiness_gap` + hide-synthetic G=0 unset | docs | LOCKED | LLD § Implementation locks |
| GAP-SCORE-04 | scoring | P1 | θ_assign still “calibrate later” soft language | docs | LOCKED | freeze 0.65 until gold |
| GAP-HITL-01 | HITL | P0 | ACK allowed on CONFLICT (“optional policy”) | docs | LOCKED | ACK only ASSIGNED+OPEN |
| GAP-HITL-02 | HITL | P0 | OVERRIDE from ACKED vs OPEN unclear | docs | LOCKED | OVERRIDE from OPEN only (MVP) |
| GAP-HITL-03 | HITL | P1 | RESOLVED path unspecified | docs | LOCKED | RESOLVED deferred MVP |
| GAP-UX-01 | UX micro | P0 | RainΔ sign / formula ambiguous | docs | LOCKED | UX §15; prev_rank − curr_rank |
| GAP-UX-02 | UX micro | P1 | MEDIUM band chip color/label unset | docs | LOCKED | `--dp-warn` + `MEDIUM` |
| GAP-UX-03 | UX micro | P1 | Counterfactual % rounding unset | docs | LOCKED | LLD locks |
| GAP-UX-04 | UX micro | P2 | Carbon vs CSS-vars still open in PRD | docs | LOCKED | CSS vars + React |
| GAP-EVAL-01 | eval | P1 | Fixture gold triage order missing | Phase7 | READY | `tests/eval/gold_order.example.json` |
| GAP-EVAL-02 | eval | P2 | Baseline tournament report path only | Phase7 | READY | `tests/eval/baseline_tournament.md` |
| GAP-BOOT-01 | bootstrap | P0 | Makefile / make install·test·run absent | Phase7 | READY | root `Makefile` stub |
| GAP-BOOT-02 | bootstrap | P0 | `.env.example` / OpenAPI / SAM not present | Phase7 | READY | `.env.example` + `docs/openapi.yaml` + `infra/README.md` |
| GAP-BOOT-03 | bootstrap | P1 | Hackathon clock-repo history vs research commits | process | LOCKED | AGENTS.md kickoff note |
| GAP-BOOT-04 | bootstrap | P2 | mex secondary memory not installed | docs+tooling | LOCKED | `.mex/` |
| GAP-OPEN-01 | open decisions | P0 | PRD §12 still lists open Qs as inventable | docs | LOCKED | PRD §12 status table |
| GAP-OPEN-02 | open decisions | P1 | Ship vs Build soft | docs | LOCKED | prefer Ship; day-1 recon gate |
| GAP-OPEN-03 | open decisions | P1 | Bedrock on/off | docs | LOCKED | off; fixtures-only |
| GAP-DRIFT-01 | cross-doc | P1 | PHASE6 still links `05-research-artifacts/` paths | docs | LOCKED | PHASE6 top redirect table (2026-10-06); legacy inline links may remain |
| GAP-DRIFT-02 | cross-doc | P2 | LLD seed list vs Gate A 14-row corpus | docs | LOCKED | seed → DATA_PLAYBOOK |
| GAP-DRIFT-03 | cross-doc | P2 | UX CONFLICT ACK optional vs LLD HITL table | docs | LOCKED | UX matrix + LLD §20 |

### Weakness classes

| Class | Covered by |
|-------|------------|
| Data / fixtures | GAP-DATA-* |
| Rain ingest | GAP-RAIN-* |
| Scoring constants | GAP-SCORE-* |
| HITL transitions | GAP-HITL-* |
| Eval / gold | GAP-EVAL-* |
| Bootstrap / tooling | GAP-BOOT-* |
| Open product decisions | GAP-OPEN-* |
| UX micro + cross-doc drift | GAP-UX-*, GAP-DRIFT-* |

### Phase 6 path drift (GAP-DRIFT-01 — redirect done)

PHASE6 top **Path redirects** table maps legacy `05-research-artifacts/phase6/*` → `docs/schemas/`, `docs/research/*`, and phase5 → `docs/phases/PHASE5.md`. Inline legacy links may remain; agents prefer product-repo paths when 404. **Data Ready PASS** (spine evidence + null_accept geo) — see [SPEC_READINESS.md](../quality/SPEC_READINESS.md) §F. Residual: human COURT review; optional VERIFIED geocode promote for MapHUD.

### Do not invent

Closing a gap must not invent DM-71 full list, SCADA GPS, pump telemetry, or real coordinates. Mark synthetic forever labeled. Escalate BLOCKED rather than fabricate FACT. Geocode candidates are **not** verified FACT until human marks `VERIFIED`.

---

## Unlock recipes (web-researched)

Recipe status: **READY** = recipe complete, execution can proceed · **BLOCKED** = waiting on human/Phase 7 artifacts.

### GAP-DATA-03 — fixture JSON bytes

| Field | Value |
|-------|-------|
| Method | Curate shells from [DATA_PLAYBOOK.md](DATA_PLAYBOOK.md); fill evidence via fetch→verbatim quote⊆source |
| Constraints | No invented quotes; schema validate against `docs/schemas/` |
| Done when | `data/fixtures/{points,evidence,readiness}.json` validate and each point has ≥1 evidence quote |
| Owner | human + Phase 7 Agent D |
| Status | LOCKED — corpus points 0.3.3 / evidence 0.3.6 shipped; COURT `needs_review` residual |

**Extract checklist**

1. Open playbook recipe for `dp-*`.
2. Fetch each source URL; set `retrieved_at`.
3. Copy quote ≥10 chars that appears verbatim in the source.
4. Set `agency` from allowlist or `null`.
5. Schema-validate; never invent lat/lon here (see GAP-DATA-04).

Scaffold files may ship with empty `evidence[]` and `lat`/`lon` null.

### GAP-DATA-04 — lat/lon geocodes

| Field | Value |
|-------|-------|
| Method | **Offline one-shot** Nominatim search → [../research/geocode-candidates.md](../research/geocode-candidates.md); copy into fixtures only after `VERIFIED` |
| URLs | https://nominatim.openstreetmap.org/search ; policy https://operations.osmfoundation.org/policies/nominatim/ |
| Constraints | ≤1 req/s; User-Agent `DisputePoint/0.1 (hackathon; contact via repo)`; ODbL attribution; **no runtime Nominatim in the demo app** |
| Done when | Demo points have `VERIFIED` coords (or explicit FAILED). **VERIFIED coords unlock MapHUD** (BUILD IF STABLE secondary markers — [DEMO_WOW.md](DEMO_WOW.md) M1). Until then MapHUD stays collapsed/empty; E2E-07 skippable; queue-first demo ships without map (FR-020) |
| Owner | human (verify) |
| Status | READY (candidates) |

Wrong matches stay `CANDIDATE` until human OK (e.g. Minto → nearby Shivaji Bridge node).

### GAP-DATA-06 — LICENSE_AUDIT

| Field | Value |
|-------|-------|
| Method | Fill rows from Open-Meteo CC-BY 4.0, India fair dealing §52, OSM ODbL — see [LICENSE_AUDIT.md](LICENSE_AUDIT.md) |
| URLs | https://open-meteo.com/en/licence · https://open-meteo.com/en/terms · Copyright Act §52 fair dealing summaries |
| Done when | No empty license cells for rain/geo/quotes; `allowed_for_demo` set |
| Owner | human (final ship check) |
| Status | READY |

### GAP-EVAL-01 — fixture gold triage order

| Field | Value |
|-------|-------|
| Method | After fixtures exist, human ranks points under wet demo (`precip_mm=40`); store as `tests/eval/gold_order.json` (start from `.example.json`) |
| Done when | Gold list length matches fixture corpus; used by Spearman/Kendall tests |
| Owner | Phase 7 |
| Status | READY (template) |
| UI note | Judges EvalDrawer/link must **not invent** gold or Spearman while this gap is open — link-out / TBD cells only ([DEMO_WOW.md](DEMO_WOW.md) J2) |

### GAP-EVAL-02 — baseline tournament report

| Field | Value |
|-------|-------|
| Method | Fill [../../tests/eval/baseline_tournament.md](../../tests/eval/baseline_tournament.md) metrics vs LLD §22 baselines |
| Done when | Report committed with measured numbers (not placeholders) |
| Owner | Phase 7 |
| Status | READY (skeleton) |
| UI note | Footer link to markdown is enough until filled; optional drawer may mirror TBD — never fake metrics for demo polish |

### GAP-BOOT-01 — Makefile

| Field | Value |
|-------|-------|
| Method | Root `Makefile` with `install` `test` `run` `deploy`; fail clearly until Phase 7 apps exist |
| Pattern | FastAPI + Vite monorepo Makefile as Phase 7 grows |
| Done when | `make install && make test && make run` work offline with fixtures |
| Owner | Phase 7 Agent A |
| Status | READY (stub) |

### GAP-BOOT-02 — .env.example / OpenAPI / SAM

| Field | Value |
|-------|-------|
| Method | Commit `.env.example` + `docs/openapi.yaml` stub; Ship It preferred; Build It via [AWS SAM Hello World](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html) — see [../../infra/README.md](../../infra/README.md) |
| Done when | Env template documented; OpenAPI matches live routes; SAM or Ship path smoke-tested day-1 |
| Owner | Phase 7 |
| Status | READY (stubs) |

### GAP-DRIFT-01 — Phase 6 `05-research-artifacts` links

| Field | Value |
|-------|-------|
| Method | Prefer `docs/schemas/` and `docs/research/` when legacy paths 404; do not mass-edit Phase 6 in this pass |
| Done when | Optional later cleanup PR rewriting links only |
| Owner | docs |
| Status | DEFERRED (cleanup) |

### Rain lock re-verify (LOCKED, for confidence)

Live probe of locked Open-Meteo URL returned 6 hourly precipitation values for Delhi centroid (`past_hours=6&forecast_hours=0`). Free tier is non-commercial ≤10k calls/day; UI must attribute Open-Meteo (CC-BY 4.0). See LLD § Implementation locks.
