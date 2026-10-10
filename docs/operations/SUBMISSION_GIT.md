# Submission git — two repos (WeMakeDevs-aligned)

**Purpose:** Where to commit, what to copy into the judged GitHub repo, and what never to upload. Binding with root [`AGENTS.md`](../../AGENTS.md). Phase 6 still wins on product conflicts.

## Official rules (binding)

| Source | Link |
|--------|------|
| Tour rules (all six hacks) | [wemakedevs.org/aws/rules](https://www.wemakedevs.org/aws/rules) (updated 2026-09-16) |
| Environmental Hacks | [wemakedevs.org/aws/env](https://www.wemakedevs.org/aws/env) |
| Env schedule | [wemakedevs.org/aws/env/schedule](https://www.wemakedevs.org/aws/env/schedule) |

**Quotes that govern this file:**

1. Learning, planning, and practice before the clock are fine and encouraged. **Project work starts when the clock does.**
2. Old projects do not count. If you began the project before the hackathon opened, it does **not** qualify, **even if you rewrote it.**
3. A repository whose **history does not match the event dates** disqualifies the whole team.
4. Kickoff day: teams form, tracks get picked, **repos get made.**
5. AI coding tools are allowed — **list them in the write-up.** AWS must appear in the **demo video** (name-only in write-up is not enough).
6. Boilerplate, starter templates, OSS libs, public APIs are fine; judges care what you **added during the event.**

If unclear: ask organizers before the clock (`contact@wemakedevs.org`), not after.

**Event:** Oct 8–11 2026 · Heat and Water track · Submission = **public** GitHub repo + ≤3 min YouTube + short write-up.

---

## Locked names (do not improvise)

| Role | Path / name |
|------|-------------|
| Research tree (planning SoT) | sibling `disputepoint` — **never** the form URL |
| Submission local folder | this repo (`disputepoint-ship`) |
| GitHub repo | `disputepoint-ship` (new empty repo under your GitHub user) |
| Default branch | `main` |

Product work after clock: open Cursor on **`disputepoint-ship` only**. Do not add `backend/` / `frontend/` app trees to the research tree for dump-into-day-1.

---

## Two folders

| Role | This research tree | Submission tree (create at clock) |
|------|--------------------|-----------------------------------|
| Path | sibling `disputepoint` | this repo `disputepoint-ship` |
| Job | Planning SoT: Phase 6, extracts, schemas, fixtures, audit L1, execution plane | **Judged** product + git history during the event |
| Before Oct 8 | Planning/practice commits OK; optional private backup remote | **Do not** create or fill |
| Public entry URL | **Never** | **Yes** — public before submit |

Do **not** `git clone` this research repo into the submission folder. **Copy allow-list files** into a fresh `git init`, then commit on Oct 8+.

---

## Tiers: what before vs after the clock

| Tier | When | Allowed |
|------|------|---------|
| **Planning** | Before clock | Phase 6 + extracts; schemas/OpenAPI; quality + build docs; LICENSE_AUDIT; fixtures; audit L1; execution plane; Makefile / `.env.example`; research notes that are **not** a pre-built app |
| **Product (entry)** | **Only after clock** in `disputepoint-ship` | API, ranking/ownership, queue UI, infra deploy |
| **Never** | Anytime in any judged push | Secrets, L0 audit bodies, invented gov data marked real, pre-clock **git history** as the entry |

---

## Before clock (now → Oct 7)

**Do:** plan/practice in research tree; keep secrets out of git; keep [`scripts/scaffold_submission.sh`](../../scripts/scaffold_submission.sh) ready (script **refuses** to create DST until clock).

**Do not:** create `disputepoint-ship` or the public submission repo; begin entry app implementation meant for judges; push L0 bodies.

---

## At clock start (Oct 8) — locked order

1. Human declares clock aloud.
2. From research tree:

```bash
cd /path/to/disputepoint   # research/planning tree
CLOCK_STARTED=1 ./scripts/scaffold_submission.sh
```

   Script creates sibling `disputepoint-ship`, allow-list rsync only, `git init -b main`, first commit, sets `clock_declared: true` in submission `execution/work-status.json`.

3. Open Cursor on **`disputepoint-ship` only**.
4. **G-PLAN:** read `execution/PLAN_CHECK.md`; set `plan_gate_accepted: true` in submission `execution/work-status.json` and commit (human).
5. Create remote (human):

```bash
cd /path/to/disputepoint-ship
gh repo create disputepoint-ship --source=. --remote=origin --private --push
```

6. **WP-00** per [`execution/START.md`](../../execution/START.md). No morning Bedrock / MapHUD / Builder Center blog.
7. Near deadline: public visibility + YouTube (AWS visible) + short write-up + Builder Center article URL + form.

Manual fallback (if script broken): `mkdir` + `git init -b main` + rsync allow-list below + same commits — **still never copy `.git`**.

---

## Copy into submission at clock (allow)

| Include | Why |
|---------|-----|
| `docs/PHASE6.md` + PRD/HLD/LLD/UX + `docs/README.md` | Product contract |
| `docs/schemas/`, `docs/openapi.yaml`, `docs/contracts/` | Planning contracts |
| `docs/quality/`, `docs/build/` (incl. LICENSE_AUDIT), `docs/design/`, `docs/operations/`, `docs/agent/` | Gates + demo + ops |
| Selected `docs/research/*` (aws-strategy, demo-win-tactics, builder-center-blog-tactics, geocode-candidates) | Weekend tactics |
| `data/fixtures/` | Seed points/evidence/readiness |
| `data/audit/` **L1 only**: `AUDIT_MATRIX.md`, `FETCH_MANIFEST.json`, `GAP_ASK.md`, `README.md` | Audit trail (not `sources/**`) |
| `execution/` | Waves, gates, work-packages, START |
| `AGENTS.md`, root `README.md`, `LICENSE`, `Makefile`, `.env.example`, `.gitignore` | Run + license |
| `.cursorrules`, `infra/README.md` | Optional thin pointers |

**Exact paths** are encoded in [`scripts/scaffold_submission.sh`](../../scripts/scaffold_submission.sh) — prefer the script over hand copy.

**Do not copy:** research `.git`; `.env`; `data/audit/sources|rain|geo|_work`; `runs/`; finished `backend/` / `frontend/` built before the clock; full `docs/phases/` / archive unless you intentionally trim-in.

---

## Never upload (deny)

| Never | Why |
|-------|-----|
| `.env`, `*.pem`, `.aws/`, credentials | Secrets |
| `runs/`, live deploy state | Ephemeral / may leak |
| `data/audit/sources/**`, `rain/`, `geo/`, `_work/` | L0 bodies |
| Pre-clock **git history** as the entry | DQ |
| Pre-built product dumped as “day 1” | Old project rule |
| Invented “live” gov feeds marked real | Hard stop |

---

## Submission package checklist

- [ ] Public GitHub repo `disputepoint-ship` (history dated Oct 8–11)
- [ ] Demo video ≤3 min on YouTube (public or unlisted); **AWS visible** in the video
- [ ] Short write-up: problem, build, where AWS fits; **AI tools listed** (e.g. Cursor)
- [ ] README has **Failure modes / ownership invariant / AWS why** (interview surface)
- [ ] **Builder Center article** published; URL linked in form — [BUILDER_BLOG.md](../build/BUILDER_BLOG.md)
- [ ] Form submitted before env deadline
- [ ] No secrets / no L0 bodies in the repo

---

## Commit / push rules (agents)

1. **Never** `git push` unless the human asked — and know **which** remote (research backup vs submission).
2. **Never** create or push the **judged** submission repo before the human says the Oct 8 clock started.
3. Before the clock: do **not** implement the entry product into a tree meant to become the public repo.
4. Prefer small commits during the event; message = why.
5. Before any push: `git status` — no `.env`, no L0 under `data/audit/sources/`.
6. List Cursor (and other AI tools) in the hackathon write-up.

---

## One-line rule

**Plan and practice before Oct 8; scaffold with `CLOCK_STARTED=1 ./scripts/scaffold_submission.sh`; build the entry only in `disputepoint-ship` whose history matches the event; never push secrets or L0.**
