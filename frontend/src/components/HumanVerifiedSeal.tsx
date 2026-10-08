import type { PointDetail } from "../api/client"

/** Visible after OVERRIDE (human assigns) — closes the accountability loop. */
export function HumanVerifiedSeal({ point }: { point: PointDetail }) {
  const override = [...(point.audit ?? [])].reverse().find((row) => row.action === "OVERRIDE")
  if (!override || !point.human_selected_agency) return null

  const auditId = `DP-AUD-${point.id.replace(/^dp-/, "").slice(0, 12).toUpperCase()}`

  return (
    <section className="human-verified" data-testid="human-verified" aria-label="Human verified">
      <p className="seal-title">HUMAN VERIFIED</p>
      <p>
        <span className="claim-agency">{point.human_selected_agency}</span>{" "}
        <span className="chip ok">HUMAN DECISION</span>
      </p>
      <p className="mono muted">AUDIT {auditId}</p>
      <p className="muted">System refused auto-assign; officer recorded ownership with reason.</p>
    </section>
  )
}
