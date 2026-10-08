import { lifecycleFromOwnership } from "../lib/lifecycle"

export function StateChip({
  state,
  compact = false,
  escalated = false,
  officerConfirmed = false,
}: {
  state: string
  compact?: boolean
  escalated?: boolean
  officerConfirmed?: boolean
}) {
  if (officerConfirmed || state === "OFFICER_CONFIRMED") {
    return <span className="chip ok">OFFICER CONFIRMED</span>
  }
  if (escalated || state === "HUMAN_REVIEW") {
    return (
      <span className="state-with-hint">
        <span className="chip warn" data-testid="awaiting-you-chip">
          AWAITING YOU
        </span>
        {compact ? null : <span className="chip-hint">human review</span>}
      </span>
    )
  }
  if (state === "ASSIGNED") {
    return <span className="chip ok">ASSIGNED</span>
  }
  if (state === "CONFLICT" || state === "RESPONSIBILITY_DISPUTED") {
    return (
      <span className="state-with-hint">
        <span className="chip warn">RESPONSIBILITY DISPUTED</span>
        {compact ? null : <span className="chip-hint">multi-claim — no auto-pick</span>}
      </span>
    )
  }
  const life = lifecycleFromOwnership(state, escalated, officerConfirmed)
  return (
    <span className="state-with-hint">
      <span className="chip warn">{life === "TRIAGED" ? state : life}</span>
      {compact ? null : <span className="chip-hint">below θ 0.65 — escalate</span>}
    </span>
  )
}

export function AgencyBlock({
  agency,
  claimed,
}: {
  agency: string | null
  claimed?: string[]
}) {
  if (agency) return <span>{agency}</span>
  const chips = (claimed ?? []).filter(Boolean)
  if (chips.length > 0) {
    return (
      <span className="claimed-chips" title={chips.join(" · ")}>
        {chips.map((name) => (
          <span key={name} className="chip claimed">
            {name}
          </span>
        ))}
      </span>
    )
  }
  return <span>—</span>
}
