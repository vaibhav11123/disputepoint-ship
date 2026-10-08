import type { ComponentType } from "react"
import type { PointDetail } from "../api/client"
import { AdvisoryBanner } from "../components/AdvisoryBanner"
import { EventRail } from "../components/EventRail"
import { IncidentNav } from "../components/IncidentNav"
import { OwnershipConflict } from "../components/OwnershipConflict"
import { ProvenanceFooter } from "../components/ProvenanceFooter"
import { ReadinessBlock } from "../components/ReadinessBlock"
import { AgencyBlock, StateChip } from "../components/StateChip"
import { TriageChip } from "../components/TriageChip"
import type { AppRoute } from "../lib/router"
import { motion } from "motion/react"

type ExplainProps = { point: PointDetail }
type ActionProps = { point: PointDetail }

const explainMods = import.meta.glob("../components/PriorityExplain.tsx", { eager: true }) as Record<
  string,
  { PriorityExplain?: ComponentType<ExplainProps> }
>
const actionMods = import.meta.glob("../components/ActionBlock.tsx", { eager: true }) as Record<
  string,
  { ActionBlock?: ComponentType<ActionProps> }
>
const PriorityExplain = Object.values(explainMods)[0]?.PriorityExplain
const ActionBlock = Object.values(actionMods)[0]?.ActionBlock

function decisionBrief(point: PointDetail, judges: boolean) {
  if (point.ownership_state === "CONFLICT") {
    return "RESPONSIBILITY DISPUTED — No auto-pick. Competing claims; escalate for Incident Commander review."
  }
  if (point.officer_confirmed && point.responsible_agency) {
    return `OFFICER CONFIRMED operational responsibility: ${point.responsible_agency}.`
  }
  if (point.ownership_state === "ASSIGNED" && point.responsible_agency) {
    if (judges) {
      return `Advisory: ${point.responsible_agency} (conf ${point.ownership_confidence.toFixed(2)}). Cell may ACK or OVERRIDE.`
    }
    return `Advisory: ${point.responsible_agency}. Cell may ACK or OVERRIDE.`
  }
  return judges
    ? "Evidence below θ 0.65 — need stronger cite or human research."
    : "Evidence below threshold — need stronger cite or human research."
}

export function IncidentScreen({
  point,
  route,
  hideSynthetic,
  judges,
}: {
  point: PointDetail
  route: AppRoute
  hideSynthetic: boolean
  judges: boolean
}) {
  const uncertain = point.ownership_state !== "ASSIGNED"

  return (
    <section className="incident-screen" aria-label="Point card">
      <IncidentNav id={point.id} route={route} title={point.name} />
      <AdvisoryBanner uncertain={uncertain} />
      <motion.article
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2 }}
        className="record-detail"
        data-testid="record-detail"
      >
        <EventRail point={point} />
        <p className="decision-meta">
          <TriageChip state={point.ownership_state} escalated={Boolean(point.escalated)} />{" "}
          <StateChip
            state={point.ownership_state}
            escalated={Boolean(point.escalated)}
            officerConfirmed={Boolean(point.officer_confirmed)}
          />{" "}
          <span className="muted">Agency: </span>
          <AgencyBlock agency={point.responsible_agency} claimed={point.agencies_claimed} />{" "}
          {point.id === "dp-purana-quila" ? <span className="chip">DEMO INCIDENT</span> : null}{" "}
          {judges ? <span className="mono muted">conf {point.ownership_confidence.toFixed(2)}</span> : null}
        </p>
        <p className="decision-brief" data-testid="decision-brief">
          {decisionBrief(point, judges)}
        </p>
        <OwnershipConflict point={point} />
        {point.agencies_claimed.length > 0 && point.ownership_state !== "CONFLICT" ? (
          <p className="claimed-row">
            <span className="muted">Claimed </span>
            <AgencyBlock agency={null} claimed={point.agencies_claimed} />
          </p>
        ) : null}
        <p className="next-action">
          <strong>Next: </strong>
          {point.recommended_action}
        </p>
        {judges && PriorityExplain ? <PriorityExplain point={point} /> : null}
        <ReadinessBlock readiness={point.readiness} hideSynthetic={hideSynthetic} />
        {ActionBlock ? <ActionBlock point={point} /> : null}
        <ProvenanceFooter point={point} />
      </motion.article>
    </section>
  )
}
