import type { ComponentType } from "react"
import { motion } from "motion/react"
import type { PointDetail } from "../api/client"
import { AccountabilityClock } from "../components/AccountabilityClock"
import { IncidentNav } from "../components/IncidentNav"
import { IncidentReplay } from "../components/IncidentReplay"
import type { AppRoute } from "../lib/router"

type AuditProps = { point: PointDetail }
const auditMods = import.meta.glob("../components/DecisionAuditPanel.tsx", { eager: true }) as Record<
  string,
  { DecisionAuditPanel?: ComponentType<AuditProps> }
>
const DecisionAuditPanel = Object.values(auditMods)[0]?.DecisionAuditPanel

export function AuditScreen({ point, route }: { point: PointDetail; route: AppRoute }) {
  return (
    <section className="audit-screen" aria-label="Decision audit" data-testid="audit-screen">
      <IncidentNav id={point.id} route={route} title={point.name} />
      <motion.div
        className="audit-timeline"
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.22 }}
      >
        {point.officer_confirmed ? (
          <p className="chip ok" data-testid="officer-confirmed-banner">
            OFFICER CONFIRMED
          </p>
        ) : null}
        {DecisionAuditPanel ? <DecisionAuditPanel point={point} /> : null}
        <AccountabilityClock point={point} />
        <IncidentReplay point={point} />
      </motion.div>
    </section>
  )
}
