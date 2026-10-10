import type { ComponentType } from "react"
import { motion } from "motion/react"
import type { PointDetail } from "../api/client"
import { CoordinationBrief } from "../components/CoordinationBrief"
import { IncidentNav } from "../components/IncidentNav"
import { IncidentWorkspace } from "../components/IncidentWorkspace"
import { copy } from "../lib/copy"
import type { AppRoute } from "../lib/router"

type ActionProps = { point: PointDetail }
const actionMods = import.meta.glob("../components/ActionBlock.tsx", { eager: true }) as Record<
  string,
  { ActionBlock?: ComponentType<ActionProps> }
>
const ActionBlock = Object.values(actionMods)[0]?.ActionBlock

export function CoordinationScreen({ point, route }: { point: PointDetail; route: AppRoute }) {
  return (
    <section className="coordination-screen" aria-label={copy.coordination.region} data-testid="coordination-screen">
      <IncidentWorkspace point={point}>
        <IncidentNav id={point.id} route={route} title={point.name} />
        <motion.div
          className="coordination-form"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          <h2 className="dp-incident-title" style={{ fontSize: 22, marginBottom: 12 }}>
            {point.name}
          </h2>
          <CoordinationBrief point={point} />
          {ActionBlock ? <ActionBlock point={point} /> : null}
        </motion.div>
      </IncidentWorkspace>
    </section>
  )
}
