import type { PointDetail } from "../api/client"
import { copy } from "../lib/copy"

/** Visible after OFFICER_CONFIRMED — closes the accountability loop. */
export function HumanVerifiedSeal({ point }: { point: PointDetail }) {
  const confirmed = [...(point.audit ?? [])].reverse().find((row) => row.action === "OFFICER_CONFIRMED")
  const override = [...(point.audit ?? [])].reverse().find((row) => row.action === "OVERRIDE")
  const decision = point.decision_record
  if (!confirmed && !override && !decision) return null
  if (!point.human_selected_agency && !decision?.agency) return null

  const agency = String(decision?.agency ?? point.human_selected_agency)
  const auditId = String(decision?.auditId ?? `DP-AUD-${point.id.replace(/^dp-/, "").slice(0, 12).toUpperCase()}`)

  return (
    <section className="human-verified" data-testid="human-verified" aria-label={copy.audit.sealAria}>
      <p className="seal-title">{copy.audit.sealTitle}</p>
      <p>
        <span className="claim-agency">{agency}</span>{" "}
        <span className="chip ok">{copy.audit.humanDecision}</span>
      </p>
      <p className="mono muted">
        {copy.audit.auditId} {auditId}
      </p>
      <p className="muted">{copy.audit.sealBody}</p>
    </section>
  )
}
