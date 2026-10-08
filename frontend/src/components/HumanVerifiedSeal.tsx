import type { PointDetail } from "../api/client"

/** Visible after OVERRIDE or OFFICER_CONFIRMED — closes the accountability loop. */
export function HumanVerifiedSeal({ point }: { point: PointDetail }) {
  const confirmed = [...(point.audit ?? [])].reverse().find((row) => row.action === "OFFICER_CONFIRMED")
  const override = [...(point.audit ?? [])].reverse().find((row) => row.action === "OVERRIDE")
  const decision = point.decision_record
  if (!confirmed && !override && !decision) return null
  if (!point.human_selected_agency && !decision?.agency) return null

  const agency = String(decision?.agency ?? point.human_selected_agency)
  const auditId = String(decision?.auditId ?? `DP-AUD-${point.id.replace(/^dp-/, "").slice(0, 12).toUpperCase()}`)

  return (
    <section className="human-verified" data-testid="human-verified" aria-label="Officer confirmed">
      <p className="seal-title">OFFICER CONFIRMED</p>
      <p>
        <span className="claim-agency">{agency}</span>{" "}
        <span className="chip ok">HUMAN DECISION</span>
      </p>
      <p className="mono muted">AUDIT {auditId}</p>
      <p className="muted">System refused auto-assign; Incident Commander recorded operational responsibility.</p>
    </section>
  )
}
