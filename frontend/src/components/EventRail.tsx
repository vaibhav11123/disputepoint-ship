import type { PointDetail } from "../api/client"
import { copy } from "../lib/copy"

type Step = { id: string; label: string; done: boolean }

export function buildEventSteps(point: PointDetail): Step[] {
  const hasEvidence = (point.evidence?.length ?? 0) > 0
  const escalated = Boolean(point.escalate_reason) || (point.audit ?? []).some((a) => a.action === "ESCALATE")
  const confirmed =
    Boolean(point.officer_confirmed) || (point.audit ?? []).some((a) => a.action === "OFFICER_CONFIRMED")
  const assigned = point.ownership_state === "ASSIGNED" || confirmed
  const labels = copy.eventRail.steps
  return [
    { id: "received", label: labels[0], done: true },
    { id: "triaged", label: labels[1], done: point.priority_rank > 0 },
    { id: "conflict", label: labels[2], done: point.ownership_state === "CONFLICT" || confirmed },
    { id: "evidence", label: labels[3], done: hasEvidence },
    { id: "escalate", label: labels[4], done: escalated },
    { id: "confirmed", label: labels[5], done: confirmed },
    { id: "assigned", label: labels[6], done: assigned },
    { id: "resolved", label: labels[7], done: point.status === "CLOSED" },
  ]
}

export function EventRail({ point }: { point: PointDetail }) {
  const steps = buildEventSteps(point)
  return (
    <ol className="event-rail" data-testid="event-rail" aria-label={copy.eventRail.aria}>
      {steps.map((step) => (
        <li key={step.id} className={step.done ? "done" : "pending"}>
          <span className="rail-dot" aria-hidden="true" />
          <span>{step.label}</span>
        </li>
      ))}
    </ol>
  )
}
