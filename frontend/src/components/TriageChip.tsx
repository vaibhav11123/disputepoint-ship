export type TriageBand = "ACT" | "ADJUDICATE" | "RESEARCH"

export function triageFor(state: string): TriageBand {
  if (state === "ASSIGNED") return "ACT"
  if (state === "CONFLICT") return "ADJUDICATE"
  return "RESEARCH"
}

export function TriageChip({ state }: { state: string }) {
  const band = triageFor(state)
  const klass = band === "ACT" ? "chip ok" : "chip warn"
  return <span className={klass}>{band}</span>
}

export function triageSummary(rows: { ownership_state: string }[]) {
  let act = 0
  let adjudicate = 0
  let research = 0
  for (const row of rows) {
    const band = triageFor(row.ownership_state)
    if (band === "ACT") act += 1
    else if (band === "ADJUDICATE") adjudicate += 1
    else research += 1
  }
  return { act, adjudicate, research }
}
