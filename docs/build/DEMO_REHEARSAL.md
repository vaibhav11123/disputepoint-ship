# DEMO_REHEARSAL — record ops + gates

**Purpose:** Make the YouTube reproducible. Story IDs: [DEMO_WOW.md](DEMO_WOW.md). **Spoken VO:** [DEMO_SCRIPT.md](DEMO_SCRIPT.md). Tactics: [research/demo-win-tactics.md](../research/demo-win-tactics.md). Blog (after video): [BUILDER_BLOG.md](BUILDER_BLOG.md). Gates: [execution/GATES.md](../../execution/GATES.md). Git: [operations/SUBMISSION_GIT.md](../operations/SUBMISSION_GIT.md).

**Rule:** Separate **story reliability** (fixtures) from **AWS eligibility proof** (Ship It or SAM on camera). Never claim AWS only in the write-up.

---

## Dual path

### A. Story path (deterministic)

| Scenario id | Intent | Seed / control |
|-------------|--------|----------------|
| `dry` | Baseline queue ranks | Live rain or clear scenario |
| `rain-spike` | **Optional** W2 — scenario label + scores (not required reorder) | Wet demo precip **42 mm** Strike if used |
| `conflict-open` | Okhla null agency (W3–W4) | Engine CONFLICT + `responsible_agency` null. Corpus evidence **0.3.6** — do not invent owners. |

Requirements:

- Visible rain **mode banner**: `live` | `cache` | `slider` / scenario
- Bookmark **root** UI URL; navigate to Command in-app (S3 `/command` curl 404 is expected SPA ErrorDocument)
- Open-Meteo timeout → cache then slider (R1)
- Prefill escalate reason; ACK only on seeded ASSIGNED cutaway if needed

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
| 0:00–0:30 | UI | Root → Command; lived-cost open | DEMO_SCRIPT problem |
| 0:30–0:55 | UI | Okhla disputed / Azadpur evidence / Karala PWD | DEMO_SCRIPT queue |
| 0:55–1:15 | UI | **Optional** Rain Strike or verbal urgency≠ownership | DEMO_SCRIPT rain |
| 1:15–1:45 | UI | Okhla disputed null + six evidence items | DEMO_SCRIPT aha |
| 1:45–2:10 | UI | ESCALATE + audit (agency still null); never ACK on CONFLICT | DEMO_SCRIPT HITL |
| 2:10–2:35 | Arch / health | `/aws-arch.html` (S3 website) + `/health` | DEMO_SCRIPT AWS |
| 2:35–3:00 | UI | Queue close + ward pilot | DEMO_SCRIPT close |

Hard cutoff **3:00**. Judges need not watch past three minutes.

---

## Live acceptance (2026-10-11 Ship It) — escalate transaction

Verified against `https://olnsv0shee.execute-api.ap-south-1.amazonaws.com` + S3 website UI:

| Check | Result |
|-------|--------|
| Okhla evidence ×6 | PASS — quotes/URLs; DDA vs PWD `establishes` / `does_not_establish`; 2 illustrative volunteer rows labeled synthetic / sample |
| ACK on CONFLICT | PASS — `409 DP-409-ACK` |
| Escalate Okhla | PASS — `ESCALATE`, reason stored, `lifecycle_state=HUMAN_REVIEW`, `escalated=true` |
| Agency after escalate | PASS — still `responsible_agency: null`, `ownership_state=CONFLICT` |
| Audit fields present | PASS — `action`, `reviewer`, `timestamp`, `point_id`, `previous_recommendation`, `final_decision.reason` (no `auditId` until confirm/`decision_record`) |
| Refresh re-fetch | PASS — state + audit persist |
| Rain scenario 42 mm | PASS optional — `scenario_slider` / `is_synthetic`; scores update; **do not require reorder on camera** |
| `/command` curl | Expected SPA 404 + index body; record via root → Command |
| UI audit after escalate | PASS — `ESCALATE by demo-eoc-operator`, timeline, responsibility awaiting decision; diagram live **UI (S3 website)** |
| `/health` at record prep | `rain_mode=live`, `rain_source_state=LIVE`, `scenario_active=false` |

Narrate audit fields visible on screen after escalate (`ESCALATE`, reviewer, timestamp/timeline). Full reason string is on the point (`escalate_reason`); say it if shown. Do not invent a separate DecisionRecord `auditId` unless confirm was used.

**Human still owed:** two stopwatch dry-runs ≤3:00 with [DEMO_SCRIPT.md](DEMO_SCRIPT.md) before G-VIDEO.

---

## Smoke-before-record (must)

Run the **exact** recorded path twice with the same visible outcome:

1. [x] API + one UI path: Okhla evidence → ESCALATE → audit (agency null). Rain optional. *(Human: repeat full timed path.)*
2. [ ] Second consecutive **timed** run matches (CONFLICT null agency, escalate audit); ACK path only if cutting to seeded ASSIGNED
3. [x] Mode banner honest (LIVE vs scenario) at prep
4. [ ] No secrets/tokens on screen (human share-screen check)
5. [x] AWS proof: `/aws-arch.html` shows **S3 website**; `/health` LIVE

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
