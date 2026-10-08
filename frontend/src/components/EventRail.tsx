import type { PointDetail } from "../api/client"

type Step = { id: string; label: string; done: boolean }

export function buildEventSteps(point: PointDetail): Step[] {
  const hasEvidence = (point.evidence?.length ?? 0) > 0
  const escalated = Boolean(point.escalate_reason) || (point.audit ?? []).some((a) => a.action === "ESCALATE")
  const human = (point.audit?.length ?? 0) > 0
  return [
    { id: "rain", label: "RAIN", done: (point.rain_delta ?? 0) !== 0 },
    { id: "priority", label: "PRIORITY", done: point.priority_rank > 0 },
    { id: "conflict", label: "CONFLICT", done: point.ownership_state === "CONFLICT" },
    { id: "evidence", label: "EVIDENCE", done: hasEvidence },
    { id: "escalate", label: "ESCALATE", done: escalated },
    { id: "human", label: "HUMAN", done: human },
  ]
}

export function EventRail({ point }: { point: PointDetail }) {
  const steps = buildEventSteps(point)
  return (
    <ol className="event-rail" data-testid="event-rail" aria-label="Case event rail">
      {steps.map((step) => (
        <li key={step.id} className={step.done ? "done" : "pending"}>
          <span className="rail-dot" aria-hidden="true" />
          <span>{step.label}</span>
        </li>
      ))}
    </ol>
  )
}
