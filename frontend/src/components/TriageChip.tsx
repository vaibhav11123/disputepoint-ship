import { copy } from "../lib/copy"

export type TriageBand = "CONFIRMED" | "ACT" | "ADJUDICATE" | "RESEARCH" | "AWAITING YOU"

const LABEL: Record<TriageBand, string> = {
  CONFIRMED: copy.state.officerConfirmed,
  ACT: copy.triage.actionRequired,
  ADJUDICATE: copy.triage.reviewRequired,
  RESEARCH: copy.triage.evidenceNeeded,
  "AWAITING YOU": copy.triage.awaitingDecision,
}

export function triageFor(
  state: string,
  escalated = false,
  officerConfirmed = false,
): TriageBand {
  // Human-verified IC path — green seal state on the queue, not ACTION REQUIRED.
  if (officerConfirmed || state === "OFFICER_CONFIRMED") return "CONFIRMED"
  if (state === "ASSIGNED") return "ACT"
  if (escalated) return "AWAITING YOU"
  if (state === "CONFLICT") return "ADJUDICATE"
  return "RESEARCH"
}

export function triageLabel(
  state: string,
  escalated = false,
  officerConfirmed = false,
): string {
  return LABEL[triageFor(state, escalated, officerConfirmed)]
}

export function TriageChip({
  state,
  escalated = false,
  officerConfirmed = false,
}: {
  state: string
  escalated?: boolean
  officerConfirmed?: boolean
}) {
  const band = triageFor(state, escalated, officerConfirmed)
  // ACTION REQUIRED must never use success-green; officer-confirmed does.
  const klass =
    band === "CONFIRMED" ? "chip ok" : band === "ACT" ? "chip action" : "chip warn"
  return (
    <span
      className={klass}
      data-testid={
        band === "AWAITING YOU" ? "awaiting-you" : band === "CONFIRMED" ? "officer-confirmed-chip" : undefined
      }
    >
      {LABEL[band]}
    </span>
  )
}

export function triageSummary(
  rows: { ownership_state: string; escalated?: boolean; officer_confirmed?: boolean }[],
) {
  let act = 0
  let adjudicate = 0
  let research = 0
  let awaiting = 0
  let confirmed = 0
  for (const row of rows) {
    const band = triageFor(
      row.ownership_state,
      Boolean(row.escalated),
      Boolean(row.officer_confirmed),
    )
    if (band === "CONFIRMED") confirmed += 1
    else if (band === "ACT") act += 1
    else if (band === "AWAITING YOU") awaiting += 1
    else if (band === "ADJUDICATE") adjudicate += 1
    else research += 1
  }
  return { act, adjudicate, research, awaiting, confirmed, disputed: adjudicate + awaiting }
}

export function nextActionLabel(
  state: string,
  escalated = false,
  officerConfirmed = false,
): string {
  const band = triageFor(state, escalated, officerConfirmed)
  if (band === "CONFIRMED") return copy.audit.sealTitle
  if (band === "ADJUDICATE" || band === "AWAITING YOU") return copy.hitl.escalate
  if (band === "ACT") return copy.hitl.confirm
  return copy.triage.evidenceNeeded
}
