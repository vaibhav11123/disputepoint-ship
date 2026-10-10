import { motion } from "motion/react"
import type { PointDetail } from "../api/client"
import { EvidenceLedger } from "../components/EvidenceLedger"
import { IncidentNav } from "../components/IncidentNav"
import { IncidentWorkspace } from "../components/IncidentWorkspace"
import { copy } from "../lib/copy"
import type { AppRoute } from "../lib/router"

export function EvidenceScreen({ point, route }: { point: PointDetail; route: AppRoute }) {
  return (
    <section className="evidence-screen" aria-label={copy.evidence.region} data-testid="evidence-screen">
      <IncidentWorkspace point={point}>
        <IncidentNav id={point.id} route={route} title={point.name} />
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
          <h2 className="dp-section evidence-effect">{copy.evidence.lead}</h2>
          <EvidenceLedger items={point.evidence ?? []} ownershipState={point.ownership_state} />
        </motion.div>
      </IncidentWorkspace>
    </section>
  )
}
