import type { PointDetail } from "../api/client"
import { HumanVerifiedSeal } from "./HumanVerifiedSeal"

export function DecisionAuditPanel({ point }: { point: PointDetail }) {
  const latest = point.audit?.[point.audit.length - 1]
  const decision = point.decision_record
  const timeline = point.audit ?? []

  return (
    <section aria-label="Decision audit" data-testid="decision-audit">
      <HumanVerifiedSeal point={point} />
      <h3 className="section-h">SYSTEM RECOMMENDED</h3>
      <p>{latest?.previous_recommendation ?? point.recommended_action ?? "—"}</p>
      <h3 className="section-h">HUMAN DECISION</h3>
      {decision ? (
        <div className="decision-record" data-testid="decision-record">
          <p>
            <strong>Incident:</strong> {point.id}
          </p>
          <p>
            <strong>Decision:</strong> ASSIGN TO {String(decision.agency)}
          </p>
          <p>
            <strong>Actor:</strong> {String(decision.actorRole ?? "INCIDENT_COMMANDER")}
          </p>
          <p>
            <strong>Reason:</strong> {String(decision.reason)}
          </p>
          <p>
            <strong>Evidence reviewed:</strong>{" "}
            {Array.isArray(decision.evidenceIds) ? decision.evidenceIds.length : 0} items
          </p>
          <p>
            <strong>Timestamp:</strong> {String(decision.timestamp ?? latest?.timestamp ?? "—")}
          </p>
          <p>
            <strong>Audit:</strong> <span className="mono">{String(decision.auditId)}</span>
          </p>
        </div>
      ) : latest ? (
        <p>
          {latest.action} by {latest.reviewer}
          {point.human_selected_agency ? ` · ${point.human_selected_agency}` : ""}
          {point.override_reason ? ` · ${point.override_reason}` : ""}
          {point.escalate_reason ? ` · ${point.escalate_reason}` : ""}
        </p>
      ) : (
        <p className="muted">No human decision yet.</p>
      )}
      {timeline.length > 0 ? (
        <ol className="audit-timeline" data-testid="audit-timeline">
          {timeline.map((row, index) => (
            <li key={`${row.timestamp}-${index}`}>
              <span className="mono">{row.timestamp?.slice(11, 19) ?? "—"}</span> {row.action} · {row.reviewer}
            </li>
          ))}
        </ol>
      ) : null}
    </section>
  )
}
