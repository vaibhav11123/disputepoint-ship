"""OwnershipEngine. θ = 0.65, W_NORM = 2.0. CONFLICT always clears the agency.

Score agencies by evidence type weights (LLD §5). Do not import the evidence loader;
wave 2 packages stay path-separate.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.app.models.point import Agency, OwnershipState

THETA = 0.65
W_NORM = 2.0

TYPE_WEIGHTS = {
    "COURT_ORDER": 1.0,
    "GOV_ORDER": 0.85,
    "AGENCY_QUOTE": 0.7,
    "PRESS_REPORT": 0.55,
    "SPATIAL_HEURISTIC": 0.35,
}


@dataclass(frozen=True)
class EvidenceScore:
    type: str
    agency: str | None
    weight: float | None = None
    channel: str | None = None


@dataclass(frozen=True)
class OwnershipDecision:
    ownership_state: OwnershipState
    responsible_agency: Agency | None
    ownership_confidence: float
    scores: dict[str, float]


def decide(items: list[EvidenceScore]) -> OwnershipDecision:
    totals: dict[str, float] = {}
    for item in items:
        if item.agency is None:
            continue
        # Volunteer reports are conditions evidence, not jurisdiction claims.
        if item.channel == "VOLUNTEER_REPORTED":
            continue
        if item.type not in TYPE_WEIGHTS:
            raise ValueError(f"unknown evidence type {item.type}")
        totals[item.agency] = totals.get(item.agency, 0.0) + TYPE_WEIGHTS[item.type]

    if not totals:
        return OwnershipDecision(OwnershipState.UNKNOWN, None, 0.0, {})

    ranked = sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))
    top_agency, top_sum = ranked[0]
    second_sum = ranked[1][1] if len(ranked) > 1 else None
    confidence = min(1.0, top_sum / W_NORM)

    close_pair = (
        second_sum is not None
        and abs(top_sum - second_sum) <= 0.1
        and top_sum > 0.4
        and second_sum > 0.4
    )
    if close_pair:
        return OwnershipDecision(OwnershipState.CONFLICT, None, confidence, totals)
    if confidence >= THETA:
        return OwnershipDecision(OwnershipState.ASSIGNED, Agency(top_agency), confidence, totals)
    return OwnershipDecision(OwnershipState.UNKNOWN, None, confidence, totals)
