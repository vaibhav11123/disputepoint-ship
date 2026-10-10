import { copy } from "../lib/copy"
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
    return <span className="chip ok">{copy.state.officerConfirmed}</span>
  }
  if (escalated || state === "HUMAN_REVIEW") {
    return (
      <span className="state-with-hint">
        <span className="chip warn" data-testid="awaiting-you-chip">
          {copy.triage.awaitingDecision}
        </span>
        {compact ? null : <span className="chip-hint">{copy.state.hintReview}</span>}
      </span>
    )
  }
  if (state === "ASSIGNED") {
    return <span className="chip ok">{copy.state.assigned}</span>
  }
  if (state === "CONFLICT" || state === "RESPONSIBILITY_DISPUTED") {
    return (
      <span className="state-with-hint">
        <span className="chip warn">{copy.state.responsibilityDisputed}</span>
        {compact ? null : <span className="chip-hint">{copy.state.hintCompeting}</span>}
      </span>
    )
  }
  const life = lifecycleFromOwnership(state, escalated, officerConfirmed)
  return (
    <span className="state-with-hint">
      <span className="chip warn">{life === "TRIAGED" ? state : life}</span>
      {compact ? null : <span className="chip-hint">{copy.state.hintReview}</span>}
    </span>
  )
}

/** Responsibility column: confirmed agency only — never claimants as assigned. */
export function AgencyBlock({
  agency,
  claimed,
}: {
  agency: string | null
  claimed?: string[]
}) {
  if (agency) return <span className="responsibility-cell">{agency}</span>
  if ((claimed ?? []).filter(Boolean).length > 0) {
    return <span className="responsibility-cell disputed">Disputed</span>
  }
  return <span className="responsibility-cell unresolved">Unresolved</span>
}

/** Equal-weight claim chips for assessment only (not responsibility assignment). */
export function ClaimedAgencies({ claimed }: { claimed?: string[] }) {
  const chips = (claimed ?? []).filter(Boolean)
  if (chips.length === 0) return <span className="muted">No claims recorded</span>
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
