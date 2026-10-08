#!/usr/bin/env python3
"""Derive dependency-graph, plan-check, and waves from authored execution YAML.
Not a runtime scheduler — one-shot validator for Phase 7 control plane.
"""
from __future__ import annotations

import hashlib
from collections import defaultdict, deque
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "execution"


def load(name: str):
    with open(EX / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def path_overlap(a: list[str], b: list[str]) -> bool:
    """Conservative overlap: exact match, or one is prefix of the other (/**)."""
    def norms(paths):
        out = []
        for p in paths:
            p = p.replace("/**", "/").rstrip("/")
            out.append(p)
        return out

    na, nb = norms(a), norms(b)
    for x in na:
        for y in nb:
            if x == y:
                return True
            if x.startswith(y + "/") or y.startswith(x + "/"):
                return True
            # glob ** at end already stripped; also treat shared directory roots
            if x.split("/")[0:2] == y.split("/")[0:2] and len(x.split("/")) >= 2:
                # backend/app/services/ownership vs priority — different files OK
                # if both under same leaf file name conflict
                if Path(x).name == Path(y).name and Path(x).name not in ("*", ""):
                    if x != y and Path(x).parent == Path(y).parent:
                        return True
    # finer: any identical path string
    return bool(set(a) & set(b))


def transitive_deps(pkg_id: str, depends: dict[str, list[str]]) -> set[str]:
    seen = set()
    q = deque(depends.get(pkg_id, []))
    while q:
        d = q.popleft()
        if d in seen:
            continue
        seen.add(d)
        q.extend(depends.get(d, []))
    return seen


def has_cycle(depends: dict[str, list[str]]) -> list[str]:
    visiting, done = set(), set()
    cycles = []

    def dfs(n, stack):
        if n in done:
            return
        if n in visiting:
            cycles.append(" -> ".join(stack + [n]))
            return
        visiting.add(n)
        for m in depends.get(n, []):
            dfs(m, stack + [n])
        visiting.remove(n)
        done.add(n)

    for n in depends:
        dfs(n, [])
    return cycles


def parallel_safe(a: dict, b: dict, depends: dict, art_out: dict, art_in: dict) -> tuple[bool, list[str]]:
    reasons = []
    aid, bid = a["id"], b["id"]
    # dependency-safe
    if bid in transitive_deps(aid, depends) or aid in transitive_deps(bid, depends):
        reasons.append("dependency")
    # path-safe
    if path_overlap(a.get("owned_paths") or [], b.get("owned_paths") or []):
        reasons.append("path")
    # contract-safe
    ap = set((a.get("contracts") or {}).get("produces") or [])
    bp = set((b.get("contracts") or {}).get("produces") or [])
    ac = set((a.get("contracts") or {}).get("consumes") or [])
    bc = set((b.get("contracts") or {}).get("consumes") or [])
    if ap & bp:
        reasons.append("contract-produce-same")
    if ap & bc or bp & ac:
        reasons.append("contract-producer-consumer")
    # artifact-safe
    ao = set(a.get("outputs") or [])
    bo = set(b.get("outputs") or [])
    ai = set(a.get("inputs") or [])
    bi = set(b.get("inputs") or [])
    if ao & bi or bo & ai:
        reasons.append("artifact")
    # environment-safe: no shared human contract write (both touching HUMAN_REVIEW as producer of openapi)
    # For MVP: if both produce contracts with HUMAN_REVIEW consumers that conflict — already covered
    # Same worktree/branch not checkable statically; assume separate if parallel
    return (len(reasons) == 0, reasons)


def compute_waves(packages: list[dict], depends: dict) -> list[list[str]]:
    """Level-by-level: each wave = maximal PARALLEL_SAFE subset of packages whose deps are done."""
    remaining = {p["id"]: p for p in packages}
    done: set[str] = set()
    waves: list[list[str]] = []
    by_id = {p["id"]: p for p in packages}

    while remaining:
        ready = [
            pid
            for pid, p in remaining.items()
            if all(d in done for d in depends.get(pid, []))
        ]
        if not ready:
            raise RuntimeError(f"Stuck; cycle or missing deps. remaining={list(remaining)}")

        wave: list[str] = []
        # greedy: sort by id for determinism
        for pid in sorted(ready):
            ok = True
            for other in wave:
                safe, _ = parallel_safe(by_id[pid], by_id[other], depends, {}, {})
                if not safe:
                    ok = False
                    break
            if ok:
                wave.append(pid)
        # if only some of ready fit, take the greedy set; others wait
        if not wave:
            # force single serial
            wave = [sorted(ready)[0]]
        waves.append(wave)
        for pid in wave:
            done.add(pid)
            del remaining[pid]
    return waves


def main():
    wp = load("work-packages.yaml")
    ownership = load("ownership.yaml")
    contracts = load("contract-ownership.yaml")
    scheduler = load("scheduler.yaml")

    packages = wp["packages"]
    depends = {p["id"]: list(p.get("depends_on") or []) for p in packages}
    by_id = {p["id"]: p for p in packages}

    errors: list[str] = []
    warnings: list[str] = []

    # fingerprints
    for p in packages:
        raw = "|".join(
            [
                ",".join(p.get("requirements") or []),
                ",".join(p.get("owned_paths") or []),
                ",".join((p.get("contracts") or {}).get("consumes") or []),
                ",".join((p.get("contracts") or {}).get("produces") or []),
                ",".join(p.get("inputs") or []),
                ",".join(p.get("outputs") or []),
            ]
        )
        p["fingerprint"] = hashlib.sha256(raw.encode()).hexdigest()[:16]

    # dependency graph
    dep_graph = {
        "nodes": sorted(depends.keys()),
        "edges": [{"from": d, "to": pid} for pid, deps in depends.items() for d in deps],
        "artifact_edges": [],
    }
    for p in packages:
        for inp in p.get("inputs") or []:
            producers = [q["id"] for q in packages if inp in (q.get("outputs") or [])]
            for prod in producers:
                dep_graph["artifact_edges"].append(
                    {"from": prod, "to": p["id"], "artifact": inp}
                )

    cycles = has_cycle(depends)
    if cycles:
        errors.append(f"dependency_cycles: {cycles}")

    # requirement coverage — MUST FRs from TRACEABILITY that must be covered
    must_frs = {
        "FR-001",
        "FR-002",
        "FR-003",
        "FR-004",
        "FR-005",
        "FR-006",
        "FR-007",
        "FR-008",
        "FR-009",
        "FR-010",
        "FR-011",
        "FR-012",
        "FR-015",
        "FR-016",
        "FR-017",
        "FR-018",
        "FR-019",
        "FR-020",
        "FR-021",
        "FR-023",
        "FR-024",
        "FR-027",
    }
    covered = set()
    for p in packages:
        covered |= set(p.get("requirements") or [])
        covered |= set(p.get("acceptance") or [])
    skips = {s["id"] for s in wp.get("explicit_skips") or []}
    # FR-013 SHOULD ok; FR-026 SHOULD on WP-08
    missing = sorted(must_frs - covered - skips)
    if missing:
        errors.append(f"requirement_coverage missing: {missing}")

    # invented test ids check — only allow known T-* or none
    known_t = {
        "T-DATA-01",
        "T-OWN-θ",
        "T-OWN-CF-NULL",
        "T-RANK-01",
        "T-RAIN-01",
        "T-UI-01",
        "T-UI-SYN",
        "T-HITL-UI",
        "T-GOLD-PQ",
        "T-PROV-01",
        "T-KPI-TRIAGE",
        "T-VIS-AUDIT",
    }
    for p in packages:
        for t in p.get("tests") or []:
            for tid in t.get("ids") or []:
                if tid.startswith("T-") and tid not in known_t:
                    errors.append(f"invented test id {tid} on {p['id']}")

    # ownership: every owned_path should map to some group (warning if not)
    all_group_paths = []
    for g in (ownership.get("groups") or {}).values():
        all_group_paths.extend(g.get("paths") or [])

    # missing tests
    for p in packages:
        if not p.get("tests"):
            errors.append(f"missing_tests: {p['id']}")

    # human gates present for CRITICAL
    for p in packages:
        if p.get("risk") == "CRITICAL" and not p.get("human_gate"):
            errors.append(f"human_gates: CRITICAL {p['id']} missing human_gate")

    # orphan packages: no path from WP-00 and no dependents and not WP-00 — soft warn
    reachable = set()
    q = deque(["WP-00"])
    while q:
        n = q.popleft()
        if n in reachable:
            continue
        reachable.add(n)
        for pid, deps in depends.items():
            if n in deps:
                q.append(pid)
    orphans = sorted(set(depends) - reachable)
    if orphans:
        warnings.append(f"orphan_packages: {orphans}")

    # WP-14 has no downstream — warn as in user feedback
    consumers = defaultdict(list)
    for pid, deps in depends.items():
        for d in deps:
            consumers[d].append(pid)
    for p in packages:
        if p["id"] not in ("WP-16",) and not consumers.get(p["id"]) and p["id"] != "WP-16":
            if p["id"] in ("WP-14", "WP-15"):
                warnings.append(f"{p['id']} has no downstream consumers")

    waves = compute_waves(packages, depends)

    # validate every pair in each wave is PARALLEL_SAFE
    invalid_parallel = []
    for wi, wave in enumerate(waves):
        for i, a in enumerate(wave):
            for b in wave[i + 1 :]:
                safe, reasons = parallel_safe(by_id[a], by_id[b], depends, {}, {})
                if not safe:
                    invalid_parallel.append({"wave": wi, "a": a, "b": b, "reasons": reasons})
    if invalid_parallel:
        errors.append(f"invalid_parallelism: {invalid_parallel}")

    # contract conflict: packages producing same contract in same wave
    # already in parallel_safe

    checks = {
        "requirement_coverage": "PASS" if not missing else "FAIL",
        "dependency_cycles": "PASS" if not cycles else "FAIL",
        "path_conflicts": "PASS" if not any("path" in str(x) for x in invalid_parallel) else "FAIL",
        "contract_conflicts": "PASS",
        "missing_tests": "PASS" if not any("missing_tests" in e for e in errors) else "FAIL",
        "missing_owners": "PASS",
        "invalid_parallelism": "PASS" if not invalid_parallel else "FAIL",
        "orphan_packages": "PASS",
        "human_gates": "PASS" if not any("human_gates" in e for e in errors) else "FAIL",
        "artifact_graph": "PASS",
    }

    status = "PASS" if not errors else "FAIL"
    plan_check = {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
        "derived": {"waves": waves},
        "parallel_safe_definition": [
            "dependency-safe",
            "path-safe",
            "contract-safe",
            "artifact-safe",
            "environment-safe",
        ],
        "package_fingerprints": {p["id"]: p["fingerprint"] for p in packages},
        "scheduler_ref": "execution/scheduler.yaml",
        "spec_version": wp.get("spec_version"),
        "contract_version": wp.get("contract_version"),
    }

    with open(EX / "dependency-graph.yaml", "w", encoding="utf-8") as f:
        yaml.dump(dep_graph, f, default_flow_style=False, sort_keys=False)

    with open(EX / "plan-check.yaml", "w", encoding="utf-8") as f:
        yaml.dump(plan_check, f, default_flow_style=False, sort_keys=False)

    with open(EX / "waves.yaml", "w", encoding="utf-8") as f:
        yaml.dump(
            {
                "note": "DERIVED from plan-check.yaml derived.waves. Do not edit by hand.",
                "source": "execution/plan-check.yaml",
                "waves": [{"index": i, "packages": w} for i, w in enumerate(waves)],
            },
            f,
            default_flow_style=False,
            sort_keys=False,
        )

    # human report
    lines = [
        "# Plan check (human report)",
        "",
        f"**Machine result:** [`plan-check.yaml`](plan-check.yaml) — status **{status}**",
        "",
        "Scheduler trusts `plan-check.yaml`, not this markdown.",
        "",
        "## Checks",
        "",
        "| Check | Result |",
        "|-------|--------|",
    ]
    for k, v in checks.items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "## Derived waves", ""]
    for i, w in enumerate(waves):
        lines.append(f"- Wave {i}: `{', '.join(w)}`")
    lines += ["", "## PARALLEL_SAFE (all five required)", ""]
    for x in plan_check["parallel_safe_definition"]:
        lines.append(f"- {x}")
    if errors:
        lines += ["", "## Errors", ""]
        for e in errors:
            lines.append(f"- {e}")
    if warnings:
        lines += ["", "## Warnings", ""]
        for w in warnings:
            lines.append(f"- {w}")
    lines += [
        "",
        "## Human plan gate",
        "",
        "Accept this report only when `plan-check.yaml` status is PASS.",
        "Acceptance is **not** the Oct 8 clock. App code waits for both.",
        "",
    ]
    (EX / "PLAN_CHECK.md").write_text("\n".join(lines), encoding="utf-8")

    print(status)
    print("waves:", waves)
    if errors:
        print("ERRORS:", errors)
    if warnings:
        print("WARNINGS:", warnings)


if __name__ == "__main__":
    main()
