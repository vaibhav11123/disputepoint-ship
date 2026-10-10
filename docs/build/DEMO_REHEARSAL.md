# DEMO_REHEARSAL — record ops + gates

**Purpose:** Make the YouTube reproducible. Story IDs: [DEMO_WOW.md](DEMO_WOW.md). **Spoken VO:** [DEMO_SCRIPT.md](DEMO_SCRIPT.md). Tactics: [research/demo-win-tactics.md](../research/demo-win-tactics.md). Blog (after video): [BUILDER_BLOG.md](BUILDER_BLOG.md). Gates: [execution/GATES.md](../../execution/GATES.md). Git: [operations/SUBMISSION_GIT.md](../operations/SUBMISSION_GIT.md).

**Rule:** Separate **story reliability** (fixtures) from **AWS eligibility proof** (Ship It or SAM on camera). Never claim AWS only in the write-up.

---

## Dual path

### A. Story path (deterministic)

| Scenario id | Intent | Seed / control |
|-------------|--------|----------------|
| `dry` | Baseline queue ranks | `precip_mm = 0` slider or dry fixture |
| `rain-spike` | Re-rank flash (W2) | Wet demo precip **40 mm** ([DEPLOYMENT](../operations/DEPLOYMENT.md)) |
| `conflict-open` | Okhla (or Samaypur) null agency (W3–W4) | Engine CONFLICT + `responsible_agency` null on spine (Okhla, Samaypur, Barapullah, Lodhi, Minto Bridge). Corpus evidence **0.3.5** — do not invent owners. |

Requirements:

- Visible rain **mode banner**: `live` | `cache` | `slider`
- Zero live typing of URLs or long forms; pre-seed ACK/OVERRIDE paths
- Open-Meteo timeout → cache then slider (R1); soft-fail still re-ranks
- Prefill everything AngelHack-style (bookmark demo URL; seeded data)

### B. AWS proof path (brief, real)

| Preferred | On screen ≥10s in **2:10–2:35** (and optional mid-flow) |
|-----------|--------------------------------------------------------|
| **Ship It primary** | API Gateway + Lambda + DynamoDB + S3 (+ EventBridge if used); live URL or console request for the rain/re-rank call |
| **Build It failover** | SAM local invoke of the **same** handler + architecture diagram naming AWS services/OSS |

Also show one architecture diagram (services named). Mid-flow breadcrumb (~1:00): mode banner or Network/CloudWatch showing the API hit after rain trigger.

---

## Shot list (AngelHack clock)

VO column = [DEMO_SCRIPT.md](DEMO_SCRIPT.md) (authoritative). Do not improvise the 0:00–0:30 problem line.

| Time | Camera / tab | Action | VO |
|------|--------------|--------|-----|
| 0:00–0:30 | UI | Queue (+ map); lived-cost open | DEMO_SCRIPT problem |
| 0:30–0:55 | UI | Board mix: assigned / disputed / evidence-needed | DEMO_SCRIPT queue |
| 0:55–1:15 | UI | Rain + priority (engine-honest); ownership separate | DEMO_SCRIPT rain |
| 1:15–1:45 | UI | Okhla (or Samaypur) disputed null + evidence | DEMO_SCRIPT aha |
| 1:45–2:10 | UI | ESCALATE/OVERRIDE + audit; ACK only if assigned cutaway | DEMO_SCRIPT HITL |
| 2:10–2:35 | Arch / health | AWS proof | DEMO_SCRIPT AWS |
| 2:35–3:00 | UI | Close + ward pilot (no unmeasured “faster”) | DEMO_SCRIPT close |

Hard cutoff **3:00**. Judges need not watch past three minutes.

---

## Smoke-before-record (must)

Run the **exact** recorded path twice with the same visible outcome:

1. [ ] `dry` → first viewport shows CONFLICT + UNKNOWN + ASSIGNED mix → `rain-spike` → open Okhla (or Samaypur) → evidence → ESCALATE or OVERRIDE → audit row
2. [ ] Second consecutive run matches (ranks, CONFLICT null agency, labels); ACK path only if cutting to seeded ASSIGNED (Mathura Rd / Bharat Mandapam)
3. [ ] Mode banner correct under forced Open-Meteo fail (R1)
4. [ ] No secrets/tokens on screen (grep fixtures + UI strings)
5. [ ] AWS proof shot rehearsed once (Ship It live — warm `/health` + arch tab)

Do not claim G-VIDEO until smoke passes twice.

---

## Five rehearsal passes

| Pass | Check |
|------|-------|
| 1 | Time ≤3:00 stopwatch with [DEMO_SCRIPT.md](DEMO_SCRIPT.md) |
| 2 | Speak **0:00–0:30 problem** aloud; stranger hears lived cost → coordination gap → honest null |
| 3 | Live/fixture path (no dead clicks); people-first open matches DEMO_SCRIPT |
| 4 | Backup: early full-path screen recording on disk |
| 5 | Blind stranger: first-90s test from DEMO_SCRIPT |

Feature freeze ~**4 hours** before final take. Cut features; do not stretch the clock.

---

## Final-hour checklist (before record)

- [ ] Slot length confirmed: ≤3:00 YouTube
- [ ] Demo data seeded; scenarios load in one click
- [ ] Demo URL bookmarked (no typing)
- [ ] Slow steps pre-warmed (API hot, fixtures loaded)
- [ ] G-VIS done (T-VIS-AUDIT / UX §12) — **before** record
- [x] G-AWS path chosen (Ship It) documented — live URLs in AWS_DEMO_BEAT / AWS_OPERATOR
- [x] Architecture diagram file open in a tab (`/aws-arch.html` on UI bucket + `frontend/public/aws-arch.html`)
- [ ] Screen resolution / font contrast checked
- [ ] No `.env` or keys in shared screen
- [ ] After upload: YouTube **public or unlisted**; open link in **signed-out** browser

---

## Gate checklists

### G-CLOCK (before WP-00 in submission repo)

- [ ] Human declared Oct 8 clock
- [ ] New folder; `git init`; **no** research `.git`
- [ ] Allow-list copy only ([SUBMISSION_GIT](../operations/SUBMISSION_GIT.md))
- [ ] No pre-built `backend/` / `frontend/` dump from research tree
- [ ] First commit dated event day
- [ ] `clock_declared: true` in submission `execution/work-status.json`

### G-VIS (before G-VIDEO)

**SoT:** [HACKATHON_VISUAL_GATE.md](HACKATHON_VISUAL_GATE.md) — do not call the video hackathon-ready until this gate is green.

- [ ] `make visual-qa` produces `runs/visual-qa/latest/V0`…`V7` PNGs + `PASS.md`
- [ ] Automated V0–V5 asserts green (NO AUTO-ASSIGN, Agency —, Rain Strike map expand, CASE/PENDING HUMAN, HUMAN VERIFIED)
- [ ] Human mute + thumbnail + 10s stranger checked in `PASS.md`
- [ ] IBM Plex; queue-first; no Inter/Geist purple glass heatmap-first
- [ ] T-VIS-AUDIT / UX §12 pass
- [ ] Video framing starts on **queue**, not map collage
- [ ] AWS / Earth human slots done or explicitly cut from cut list

### G-AWS

- [x] Ship It path chosen and runnable for the W9 shot (API Gateway + S3 UI live 2026-10-10)
- [x] Secrets held out of git and video (CORS allowlist; `/docs` off on Lambda)

### G-VIDEO (before submit)

- [ ] Recording ≤3:00
- [ ] AWS **visible** on screen (W9)
- [ ] AI tools listed in write-up (e.g. Cursor)
- [ ] Signed-out YouTube link works
- [ ] Smoke-before-record passed twice
- [ ] Public repo history matches event dates
- [ ] After G-VIDEO: fill + publish [BUILDER_BLOG.md](BUILDER_BLOG.md) on Builder Center; paste article URL in form (closes **R-BLOG-BUILDER**)

### G-KPI (human timed)

- [ ] Golden path feels &lt;30s triage (FR-027) on dry run
- Measured seconds: not recorded. Do not invent a time.

---

## Weekend timebox (60/20/20)

| Share | Focus |
|-------|--------|
| 60% | Core golden path (W1–W8) |
| 20% | UX anti-slop (G-VIS) |
| 20% | Video + short write-up + AWS proof (G-VIDEO) + Builder Center blog after video |

Do not invent day-4 features at the expense of the 20% presentation slot. Do not spend Thursday morning on the blog before the golden path.

---

## Ownership

| Item | Owner |
|------|--------|
| This file + recording | WP-16 |
| AWS path / diagram | WP-15 · G-AWS |
| Visual polish stop | G-VIS |
| Clock DQ | G-CLOCK · human |
| Story IDs | [DEMO_WOW.md](DEMO_WOW.md) |
