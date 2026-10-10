import type { PointDetail } from "../api/client"
import { copy } from "../lib/copy"
import { HumanVerifiedSeal } from "./HumanVerifiedSeal"

export function DecisionAuditPanel({ point }: { point: PointDetail }) {
  const latest = point.audit?.[point.audit.length - 1]
  const decision = point.decision_record
  const timeline = point.audit ?? []
  const conflict = point.ownership_state === "CONFLICT"

  return (
    <section aria-label={copy.audit.region} data-testid="decision-audit">
      <HumanVerifiedSeal point={point} />
      <h3 className="section-h">{copy.audit.systemFinding}</h3>
      <p>
        {conflict
          ? copy.audit.systemFindingBody
          : (latest?.previous_recommendation ?? point.recommended_action ?? "—")}
      </p>
      <h3 className="section-h">{copy.audit.humanDecision}</h3>
      {decision ? (
        <div className="decision-record" data-testid="decision-record">
          <p>
            <strong>{copy.audit.incident}</strong> {point.id}
          </p>
          <p>
            <strong>{copy.audit.decision}</strong> {copy.audit.confirmed(String(decision.agency))}
          </p>
          <p>
            <strong>{copy.audit.decisionMaker}:</strong> {String(decision.actorRole ?? "INCIDENT_COMMANDER")}
          </p>
          <p>
            <strong>{copy.audit.reason}</strong> {String(decision.reason)}
          </p>
          <p>
            <strong>{copy.audit.evidenceReviewed}</strong>{" "}
            {Array.isArray(decision.evidenceIds) ? decision.evidenceIds.length : 0} items
          </p>
          <p>
            <strong>{copy.audit.timestamp}</strong> {String(decision.timestamp ?? latest?.timestamp ?? "—")}
          </p>
          <p>
            <strong>{copy.audit.auditId}:</strong> <span className="mono">{String(decision.auditId)}</span>
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
        <p className="muted">{copy.audit.awaiting}</p>
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
