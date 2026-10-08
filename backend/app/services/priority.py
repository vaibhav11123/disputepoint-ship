"""PriorityEngine. U is coordination uncertainty, not physical severity.

Locks: LLD §6, §19, §24. Weights must not be soft-changed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

WEIGHTS = {"R": 0.25, "S": 0.25, "C": 0.15, "Q": 0.15, "U": 0.15, "G": 0.05}
U_SEMANTICS = "U is coordination_uncertainty, not physical severity"

WHY_NOW = "Why now? Rain and/or coordination uncertainty increased triage urgency"
WHY_LOCATION = "Why this location? Chronic flooding + unresolved agency responsibility (coordination bottleneck)"
WHY_AGENCY = "Why this agency? Advisory only. CONFLICT means no auto-agency"


@dataclass(frozen=True)
class PriorityResult:
    score: float
    components: dict[str, float]
    explanation: list[str]
    counterfactuals: list[dict[str, Any]]


def normalize_rain(precip_mm: float) -> float:
    return min(1.0, max(0.0, precip_mm / 50.0))


def recurrence_to_unit(recurrence_class: str | None) -> float:
    return {
        "chronic": 1.0,
        "recurring": 0.7,
        "occasional": 0.4,
        "unknown": 0.2,
    }.get(recurrence_class or "unknown", 0.2)


def readiness_gap(readiness: dict[str, Any] | None, hide_synthetic: bool = False) -> float:
    if not readiness:
        return 0.5
    if hide_synthetic and readiness.get("is_synthetic"):
        return 0.0
    state = readiness.get("state", "UNKNOWN")
    return {"OK": 0.0, "GAP": 1.0, "UNKNOWN": 0.5}.get(state, 0.5)


def uncertainty_band(ownership_confidence: float) -> str:
    if ownership_confidence >= 0.85:
        return "HIGH"
    if ownership_confidence >= 0.65:
        return "MEDIUM"
    return "UNCERTAIN"


def _components(
    *,
    precip_mm: float,
    severity: float | None,
    is_arterial: bool,
    is_underpass: bool,
    recurrence_class: str | None,
    ownership_confidence: float,
    ownership_state: str,
    readiness: dict[str, Any] | None,
    hide_synthetic: bool,
    zero_q: bool = False,
    zero_g: bool = False,
    resolved_u: bool = False,
) -> dict[str, float]:
    r_value = normalize_rain(precip_mm)
    s_value = 0.0 if severity is None else float(severity)
    c_value = 1.0 if is_arterial or is_underpass else 0.4
    q_value = 0.0 if zero_q else recurrence_to_unit(recurrence_class)
    if resolved_u:
        u_value = 0.0
    else:
        u_value = 1.0 - ownership_confidence
        if ownership_state == "CONFLICT":
            u_value = max(u_value, 0.8)
    g_value = 0.0 if zero_g else readiness_gap(readiness, hide_synthetic)
    return {"R": r_value, "S": s_value, "C": c_value, "Q": q_value, "U": u_value, "G": g_value}


def _score(components: dict[str, float]) -> float:
    return sum(WEIGHTS[key] * components[key] for key in WEIGHTS)


def _explain(components: dict[str, float]) -> list[str]:
    lines = [f"{key}={components[key]:.2f}×{WEIGHTS[key]}" for key in WEIGHTS]
    lines.append(U_SEMANTICS)
    return lines


def _pct(before: float, after: float) -> int:
    return round(100 * (after - before) / max(before, 1e-6))


def priority(
    point: Any,
    precip_mm: float = 0.0,
    hide_synthetic: bool = False,
) -> PriorityResult:
    components = _components(
        precip_mm=precip_mm,
        severity=getattr(point, "severity", None),
        is_arterial=bool(getattr(point, "is_arterial", False)),
        is_underpass=bool(getattr(point, "is_underpass", False)),
        recurrence_class=getattr(point, "recurrence_class", None),
        ownership_confidence=float(point.ownership_confidence),
        ownership_state=str(getattr(point.ownership_state, "value", point.ownership_state)),
        readiness=getattr(point, "readiness", None),
        hide_synthetic=hide_synthetic,
    )
    score = _score(components)
    counterfactuals = _counterfactuals(point, precip_mm, score, hide_synthetic)
    return PriorityResult(score=score, components=components, explanation=_explain(components), counterfactuals=counterfactuals)


def _counterfactuals(point: Any, precip_mm: float, before: float, hide_synthetic: bool) -> list[dict[str, Any]]:
    variants = [
        ("zero_R", {"precip_mm": 0.0}),
        ("resolve_U", {"resolved_u": True}),
        ("zero_Q", {"zero_q": True}),
        ("zero_G", {"zero_g": True}),
    ]
    rows = []
    for name, flags in variants:
        components = _components(
            precip_mm=flags.get("precip_mm", precip_mm),
            severity=getattr(point, "severity", None),
            is_arterial=bool(getattr(point, "is_arterial", False)),
            is_underpass=bool(getattr(point, "is_underpass", False)),
            recurrence_class=getattr(point, "recurrence_class", None),
            ownership_confidence=float(point.ownership_confidence),
            ownership_state=str(getattr(point.ownership_state, "value", point.ownership_state)),
            readiness=getattr(point, "readiness", None),
            hide_synthetic=hide_synthetic,
            zero_q=bool(flags.get("zero_q")),
            zero_g=bool(flags.get("zero_g")),
            resolved_u=bool(flags.get("resolved_u")),
        )
        after = _score(components)
        rows.append(
            {
                "factor": name,
                "score_before": before,
                "score_after": after,
                "delta_pct": _pct(before, after),
                "copy": WHY_NOW if name == "zero_R" else WHY_LOCATION,
            }
        )
    return rows
