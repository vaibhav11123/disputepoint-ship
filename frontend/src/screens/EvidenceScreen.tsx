import { motion } from "motion/react"
import type { PointDetail } from "../api/client"
import { EvidenceLedger } from "../components/EvidenceLedger"
import { IncidentNav } from "../components/IncidentNav"
import type { AppRoute } from "../lib/router"

export function EvidenceScreen({ point, route }: { point: PointDetail; route: AppRoute }) {
  return (
    <section className="evidence-screen" aria-label="Evidence ledger" data-testid="evidence-screen">
      <IncidentNav id={point.id} route={route} title={point.name} />
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
        <p className="muted evidence-effect">
          Decision effect: evidence informs coordination uncertainty — not auto-assignment.
        </p>
        <EvidenceLedger items={point.evidence ?? []} ownershipState={point.ownership_state} />
      </motion.div>
    </section>
  )
}
