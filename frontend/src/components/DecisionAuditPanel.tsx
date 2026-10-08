import type { PointDetail } from "../api/client"

export function DecisionAuditPanel({ point }: { point: PointDetail }) {
  const latest = point.audit?.[point.audit.length - 1]
  return (
    <section aria-label="Decision audit" data-testid="decision-audit">
      <h3 style={{ fontSize: 14, margin: "12px 0 4px" }}>SYSTEM RECOMMENDED</h3>
      <p>{latest?.previous_recommendation ?? point.recommended_action ?? "—"}</p>
      <h3 style={{ fontSize: 14, margin: "12px 0 4px" }}>HUMAN DECISION</h3>
      {latest ? (
        <p>
          {latest.action} by {latest.reviewer}
          {point.human_selected_agency ? ` · ${point.human_selected_agency}` : ""}
          {point.override_reason ? ` · ${point.override_reason}` : ""}
          {point.escalate_reason ? ` · ${point.escalate_reason}` : ""}
        </p>
      ) : (
        <p className="muted">No human decision yet.</p>
      )}
    </section>
  )
}
