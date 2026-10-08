export type TriageBand = "ACT" | "ADJUDICATE" | "RESEARCH" | "AWAITING YOU"

export function triageFor(state: string, escalated = false): TriageBand {
  if (escalated) return "AWAITING YOU"
  if (state === "ASSIGNED") return "ACT"
  if (state === "CONFLICT") return "ADJUDICATE"
  return "RESEARCH"
}

export function TriageChip({ state, escalated = false }: { state: string; escalated?: boolean }) {
  const band = triageFor(state, escalated)
  const klass = band === "ACT" ? "chip ok" : "chip warn"
  return (
    <span className={klass} data-testid={band === "AWAITING YOU" ? "awaiting-you" : undefined}>
      {band}
    </span>
  )
}

export function triageSummary(rows: { ownership_state: string; escalated?: boolean }[]) {
  let act = 0
  let adjudicate = 0
  let research = 0
  let awaiting = 0
  for (const row of rows) {
    const band = triageFor(row.ownership_state, Boolean(row.escalated))
    if (band === "ACT") act += 1
    else if (band === "AWAITING YOU") awaiting += 1
    else if (band === "ADJUDICATE") adjudicate += 1
    else research += 1
  }
  return { act, adjudicate, research, awaiting, disputed: adjudicate + awaiting }
}
