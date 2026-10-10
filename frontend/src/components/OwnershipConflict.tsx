import type { PointDetail } from "../api/client"
import { copy } from "../lib/copy"

/**
 * Responsibility Assessment — signature component.
 * Equal-weight claims; no implied winner; data-state honest.
 */
export function OwnershipConflict({ point }: { point: PointDetail }) {
  if (point.ownership_state !== "CONFLICT") {
    if (point.officer_confirmed && point.responsible_agency) {
      return (
        <section
          className="responsibility-assessment"
          data-testid="ownership-confirmed"
          aria-label={copy.conflict.region}
        >
          <p className="responsibility-assessment-title">{copy.conflict.title}</p>
          <p className="dp-body">
            Recorded decision: <strong>{point.responsible_agency}</strong>
            {point.decision_record?.auditId
              ? ` · Audit ${String(point.decision_record.auditId)}`
              : ""}
          </p>
        </section>
      )
    }
    return null
  }

  const claims = point.agencies_claimed.filter(Boolean)
  const agencies = claims.join(" and ")

  return (
    <section
      className="responsibility-assessment ownership-conflict"
      data-testid="ownership-conflict"
      aria-label={copy.conflict.region}
    >
      <p className="responsibility-assessment-title">{copy.conflict.title}</p>

      <p className="dp-section" style={{ fontSize: 14, marginBottom: 8 }}>
        Competing claims
      </p>
      {claims.length === 0 ? (
        <p className="muted">No responsibility claims are recorded for this incident.</p>
      ) : (
        <div className="claim-grid" data-testid="claim-grid">
          {claims.map((agency) => (
            <div key={agency} className="claim-side">
              <span className="claim-agency">{agency}</span>
              <span className="muted">
                {point.claim_summaries?.[agency] ?? copy.conflict.claim}
              </span>
            </div>
          ))}
        </div>
      )}

      <hr className="assessment-divider" />

      <p className="section-h">{copy.conflict.whatEstablishes}</p>
      <p className="dp-body muted">
        {agencies
          ? copy.incident.competingClaimsLine(agencies)
          : copy.conflict.body}
      </p>

      <p className="section-h">{copy.conflict.whatUnresolved}</p>
      <p className="agency-null" data-testid="agency-null">
        <strong>{copy.conflict.operational}</strong>{" "}
        <span className="mono">{copy.conflict.none}</span>
      </p>
      <p className="dp-body muted">{copy.conflict.body}</p>

      <p className="no-auto" data-testid="no-auto-assign">
        {copy.conflict.noAutoAssign}
      </p>
      <p className="conflict-effect" data-testid="conflict-effect">
        {copy.conflict.next}
      </p>
    </section>
  )
}
