import type { ComponentType } from "react"
import { motion } from "motion/react"
import type { PointDetail } from "../api/client"
import { AdvisoryBanner } from "../components/AdvisoryBanner"
import { EventRail } from "../components/EventRail"
import { IncidentNav } from "../components/IncidentNav"
import { IncidentWorkspace } from "../components/IncidentWorkspace"
import { OwnershipConflict } from "../components/OwnershipConflict"
import { ProvenanceFooter } from "../components/ProvenanceFooter"
import { ReadinessBlock } from "../components/ReadinessBlock"
import { AgencyBlock, StateChip } from "../components/StateChip"
import { TriageChip } from "../components/TriageChip"
import { copy } from "../lib/copy"
import type { AppRoute } from "../lib/router"

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

function decisionBrief(point: PointDetail) {
  if (point.ownership_state === "CONFLICT") {
    return (
      <>
        {copy.incident.briefConflictBody}
        <br />
        {copy.incident.briefConflictNext}
      </>
    )
  }
  if (point.officer_confirmed && point.responsible_agency) {
    return copy.incident.briefOfficer(point.responsible_agency)
  }
  if (point.ownership_state === "ASSIGNED" && point.responsible_agency) {
    return copy.incident.briefAdvisory(point.responsible_agency)
  }
  return copy.incident.briefEvidenceLow
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
  const agencies = point.agencies_claimed.filter(Boolean).join(" and ")

  return (
    <section className="incident-screen" aria-label={copy.incident.region}>
      <IncidentWorkspace point={point}>
        <IncidentNav id={point.id} route={route} title={point.name} />
        <AdvisoryBanner uncertain={uncertain} />
        <motion.article
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
          className="record-detail"
          data-testid="record-detail"
        >
          <header className="incident-hero" data-testid="incident-hero">
            <h2 className="dp-incident-title">{point.name}</h2>
            {point.incident_summary ? (
              <p className="dp-body" data-testid="incident-summary">
                {point.incident_summary}
              </p>
            ) : null}
            {point.ownership_state === "CONFLICT" ? (
              <>
                <p className="chip warn">{copy.incident.briefConflictTitle}</p>
                {agencies ? <p className="muted">{copy.incident.competingClaimsLine(agencies)}</p> : null}
                <p className="dp-status-label">{copy.incident.autoBlocked}</p>
              </>
            ) : (
              <p className="decision-meta chip-budget">
                {point.ownership_state === "CONFLICT" || point.escalated ? (
                  <TriageChip
                    state={point.ownership_state}
                    escalated={Boolean(point.escalated)}
                    officerConfirmed={Boolean(point.officer_confirmed)}
                  />
                ) : (
                  <StateChip
                    state={point.ownership_state}
                    escalated={Boolean(point.escalated)}
                    officerConfirmed={Boolean(point.officer_confirmed)}
                  />
                )}{" "}
                <span className="muted">{copy.incident.agency} </span>
                <AgencyBlock agency={point.responsible_agency} claimed={point.agencies_claimed} />
              </p>
            )}
          </header>

          <EventRail point={point} />

          {point.ownership_state === "CONFLICT" ? (
            <p className="decision-brief" data-testid="decision-brief">
              {decisionBrief(point)}
            </p>
          ) : (
            <p className="decision-brief" data-testid="decision-brief">
              {decisionBrief(point)}
            </p>
          )}

          <OwnershipConflict point={point} />

          <p className="next-action">
            <strong>{copy.incident.next} </strong>
            {point.recommended_action}
          </p>
          {judges && PriorityExplain ? <PriorityExplain point={point} /> : null}
          <ReadinessBlock readiness={point.readiness} hideSynthetic={hideSynthetic} />
          {ActionBlock ? <ActionBlock point={point} /> : null}
          <details className="provenance-disclosure" open>
            <summary className="dp-meta">Location and provenance</summary>
            <ProvenanceFooter point={point} />
          </details>
        </motion.article>
      </IncidentWorkspace>
    </section>
  )
}
