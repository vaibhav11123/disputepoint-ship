import type { ComponentType } from "react"
import type { PointDetail } from "../api/client"
import { AgencyBlock, StateChip } from "./StateChip"
import { AccountabilityClock } from "./AccountabilityClock"
import { CoordinationBrief } from "./CoordinationBrief"
import { EventRail } from "./EventRail"
import { EvidenceLedger } from "./EvidenceLedger"
import { IncidentReplay } from "./IncidentReplay"
import { OwnershipConflict } from "./OwnershipConflict"
import { ProvenanceFooter } from "./ProvenanceFooter"
import { ReadinessBlock } from "./ReadinessBlock"
import { TriageChip } from "./TriageChip"

type ExplainProps = { point: PointDetail }
type ActionProps = { point: PointDetail }
type AuditProps = { point: PointDetail }

const explainMods = import.meta.glob("./PriorityExplain.tsx", { eager: true }) as Record<string, { PriorityExplain?: ComponentType<ExplainProps> }>
const actionMods = import.meta.glob("./ActionBlock.tsx", { eager: true }) as Record<string, { ActionBlock?: ComponentType<ActionProps> }>
const auditMods = import.meta.glob("./DecisionAuditPanel.tsx", { eager: true }) as Record<string, { DecisionAuditPanel?: ComponentType<AuditProps> }>

const PriorityExplain = Object.values(explainMods)[0]?.PriorityExplain
const ActionBlock = Object.values(actionMods)[0]?.ActionBlock
const DecisionAuditPanel = Object.values(auditMods)[0]?.DecisionAuditPanel

function decisionBrief(point: PointDetail, judges: boolean) {
  if (point.ownership_state === "CONFLICT") {
    return "Multiple agencies claim this corridor. No auto-pick — escalate or OVERRIDE."
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

export function PointCard({
  point,
  hideSynthetic,
  judges,
}: {
  point: PointDetail
  hideSynthetic: boolean
  judges: boolean
}) {
  return (
    <article>
      <h2 style={{ fontSize: 16, fontWeight: 600, margin: "0 0 8px" }}>{point.name}</h2>
      <EventRail point={point} />
      <p className="decision-meta">
        <TriageChip state={point.ownership_state} />{" "}
        <StateChip state={point.ownership_state} />{" "}
        <span className="muted">Agency: </span>
        <AgencyBlock agency={point.responsible_agency} />{" "}
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
      <EvidenceLedger items={point.evidence ?? []} ownershipState={point.ownership_state} />
      <ReadinessBlock readiness={point.readiness} hideSynthetic={hideSynthetic} />
      <CoordinationBrief point={point} />
      {ActionBlock ? <ActionBlock point={point} /> : null}
      <AccountabilityClock point={point} />
      {DecisionAuditPanel ? <DecisionAuditPanel point={point} /> : null}
      <IncidentReplay point={point} />
      <ProvenanceFooter point={point} />
    </article>
  )
}
