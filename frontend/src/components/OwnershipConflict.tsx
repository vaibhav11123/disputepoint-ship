import type { PointDetail } from "../api/client"
import { AgencyBlock } from "./StateChip"

export function OwnershipConflict({ point }: { point: PointDetail }) {
  if (point.ownership_state !== "CONFLICT") return null
  const left = point.agencies_claimed[0] ?? "MCD"
  const right = point.agencies_claimed[1] ?? "PWD"

  return (
    <section className="ownership-conflict" data-testid="ownership-conflict" aria-label="Responsibility disputed">
      <p className="ownership-conflict-title">RESPONSIBILITY DISPUTED · CLAIMS OVERLAP</p>
      <div className="claim-duel">
        <div className="claim-side">
          <span className="claim-agency">{left}</span>
          <span className="muted">CLAIM</span>
        </div>
        <div className="claim-vs" aria-hidden="true">
          ↔
        </div>
        <div className="claim-side">
          <span className="claim-agency">{right}</span>
          <span className="muted">CLAIM</span>
        </div>
      </div>
      <p className="claimed-row">
        <span className="muted">Claimed </span>
        <AgencyBlock agency={null} claimed={point.agencies_claimed} />
      </p>
      <p className="agency-null" data-testid="agency-null">
        <strong>Operational responsibility:</strong> <span className="mono">—</span>
        <span className="muted"> (no auto-assignment)</span>
      </p>
      <p className="no-auto" data-testid="no-auto-assign">
        NO AUTO-ASSIGN
      </p>
      <p className="conflict-effect" data-testid="conflict-effect">
        Evidence supports overlapping claims. It does not establish exclusive operational responsibility.
      </p>
      <div className="missing-evidence" data-testid="what-would-resolve">
        <p className="section-h">WHAT WOULD RESOLVE THIS?</p>
        <ul className="missing-list">
          <li>□ Current jurisdiction order</li>
          <li>□ Drain ownership record</li>
          <li>□ Recent maintenance responsibility</li>
          <li>□ Agency confirmation</li>
          <li>□ Field verification</li>
        </ul>
        <p className="muted">Competing claims present — exclusive responsibility not established.</p>
      </div>
    </section>
  )
}
