export function StateChip({ state, compact = false }: { state: string; compact?: boolean }) {
  if (state === "ASSIGNED") {
    return <span className="chip ok">ASSIGNED</span>
  }
  if (state === "CONFLICT") {
    return (
      <span className="state-with-hint">
        <span className="chip warn">CONFLICT</span>
        {compact ? null : <span className="chip-hint">multi-claim — no auto-pick</span>}
      </span>
    )
  }
  return (
    <span className="state-with-hint">
      <span className="chip warn">{state}</span>
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
