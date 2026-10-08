import type { PointDetail } from "../api/client"

export function CoordinationBrief({ point }: { point: PointDetail }) {
  const escalated = (point.audit ?? []).some((a) => a.action === "ESCALATE") || Boolean(point.escalate_reason)
  if (!escalated && point.ownership_state !== "CONFLICT") return null

  return (
    <section className="coordination-brief" data-testid="coordination-brief" aria-label="Coordination brief">
      <h3 className="section-h">Coordination brief</h3>
      <ul>
        <li>
          <strong>Point:</strong> {point.name}
        </li>
        <li>
          <strong>State:</strong> {point.ownership_state} · agency null until human
        </li>
        <li>
          <strong>Claims:</strong> {point.agencies_claimed.join(", ") || "—"}
        </li>
        <li>
          <strong>Ask:</strong> DM cell confirms exclusive owner or keeps UNCERTAIN with next check
        </li>
      </ul>
    </section>
  )
}
