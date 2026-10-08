---
name: agents
description: Always-loaded project anchor inside .mex. Secondary to root AGENTS.md and Phase 6.
last_updated: 2026-10-08
---

# DisputePoint

## What This Is

For a DM coordination cell officer, when monsoon rain threatens multi-agency disputed waterlogging points in Delhi, decide which point needs action first, which agency should act (or UNCERTAIN), and why — evidence-backed, HITL, not a flood heatmap.

## Non-Negotiables

- Phase 6 (`docs/PHASE6.md`) and root `AGENTS.md` hard stops win over this wiki.
- `ownership_state == CONFLICT` → `responsible_agency = null` always.
- U is coordination_uncertainty, not physical severity. No ML runtime in MVP.
- Never invent DM-71, SCADA, GPS, or quotes, and never mark synthetic as real.
- Build from `execution/START.md` one derived wave at a time. Do not one-shot the app.

## Commands

- `make help` · `make install` · `make test` · `make run` — stubs exit 1 until the API and UI trees exist.
- `mex check` · `mex doctor` · `mex hub` (loopback). Graph and wiki DBs stay gitignored.

## Code Graph
Use the smallest relevant structured resolver. For Inbox or Relay mutations, resolve only the intended action with `mex inbox contract --action <command-id> --json` or `mex relay contract --action <command-id> --json`; use `mex capabilities --json` only for broader capability discovery. If the user explicitly asks to create, save, or draft a checkout-local Inbox or Relay draft, preview and apply that exact draft without asking for redundant confirmation. Deleting a local draft, or publishing, approving, rejecting, withdrawing, marking stale, repairing, taking or acknowledging, or closing, requires fresh explicit confirmation after semantic preview. Treat Git commit, push, and pull as separate actions requiring their own authorization.

The repo is indexed into `.mex/graph.db`. Use it to avoid re-reading code you already have — it is one tool alongside Grep/Glob, not a replacement for them.
- If you know the symbol name, go straight to it: `mex graph query <who-calls|what-calls|where-defined> <symbol>` and `mex graph get <id>` are exact and cheap. This is the strongest part of the graph. Give it exact names — an approximate name can return a confident wrong match.
- Exploring an unfamiliar task? `mex graph scope "<task>"` returns bounded, source-backed JSONL context plus trustworthy execution flows. Scope matches on words, not meaning, so treat it as starting evidence rather than a complete answer.
- Treat source returned by the graph as ALREADY READ; do not re-open those files.
- Read the summary status and evidence. `status: "ok"` remains usable when `truncated: true`; only optional evidence was omitted. For `partial` or `degraded`, narrow the task or follow `suggestedNextCommands`.
- Use `mex graph get <id> --detail source` only when source is missing, you need exact expansion, or a partial/degraded summary suggests it. Do not expand nodes by quota.
- If the evidence is insufficient or the task wording does not match the code, use Grep/Glob instead. Do not re-run `scope` with reworded phrasing more than once.
- Before editing a symbol, run `mex impact <symbol|file>` to see affected callers and scaffold memory.
- During `mex sync`, adjudicate any AMBIGUOUS grounding; after repairs, ensure the refreshed grounding is re-emitted.

## Scaffold Growth
After meaningful work, run GROW:
- Ground: what changed in reality?
- Record: update `ROUTER.md` and relevant `context/` files
- Orient: create or update a `patterns/` runbook if this can recur
- Write: bump `last_updated` on changed scaffold files and run `mex log` when rationale matters

The scaffold grows from real work, not just setup. See the GROW step in `ROUTER.md` for details.

## Navigation
At the start of a build session, read root `AGENTS.md`, then `execution/START.md`. Use this file and `ROUTER.md` as secondary memory. Phase 6 still wins on product conflicts.

<!-- mex-agent:skills:start -->
## MEX context policy
- When MEX context materially influences an answer or implementation, include one concise acknowledgement: `MEX context used: <specific records/files/entities consulted>.`
- Do not claim an author, date, or historical event unless the retrieved data actually provides it.
- After a MEX write, say exactly what changed and its sharing boundary: a local draft is checkout-only and nothing is shared; a canonical artifact is written to the working tree and requires commit/push to share.
- Skill activation is not approval for canonical actions.
<!-- mex-agent:skills:end -->
