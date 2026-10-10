import { copy } from "../lib/copy"

export type TriageBand = "ACT" | "ADJUDICATE" | "RESEARCH" | "AWAITING YOU"

const LABEL: Record<TriageBand, string> = {
  ACT: copy.triage.actionRequired,
  ADJUDICATE: copy.triage.reviewRequired,
  RESEARCH: copy.triage.evidenceNeeded,
  "AWAITING YOU": copy.triage.awaitingDecision,
}

export function triageFor(state: string, escalated = false): TriageBand {
  if (escalated) return "AWAITING YOU"
  if (state === "ASSIGNED") return "ACT"
  if (state === "CONFLICT") return "ADJUDICATE"
  return "RESEARCH"
}

export function triageLabel(state: string, escalated = false): string {
  return LABEL[triageFor(state, escalated)]
}

export function TriageChip({ state, escalated = false }: { state: string; escalated?: boolean }) {
  const band = triageFor(state, escalated)
  // ACTION REQUIRED must never use success-green
  const klass = band === "ACT" ? "chip action" : "chip warn"
  return (
    <span className={klass} data-testid={band === "AWAITING YOU" ? "awaiting-you" : undefined}>
      {LABEL[band]}
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

export function nextActionLabel(state: string, escalated = false): string {
  const band = triageFor(state, escalated)
  if (band === "ADJUDICATE" || band === "AWAITING YOU") return copy.hitl.escalate
  if (band === "ACT") return copy.hitl.confirm
  return copy.triage.evidenceNeeded
}
