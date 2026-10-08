import type { ComponentType } from "react"
import type { PointDetail } from "../api/client"
import { AgencyBlock } from "./AgencyBlock"
import { EvidenceList } from "./EvidenceList"
import { ProvenanceFooter } from "./ProvenanceFooter"
import { ReadinessBlock } from "./ReadinessBlock"
import { StateChip } from "./StateChip"

type ExplainProps = { point: PointDetail }
type ActionProps = { point: PointDetail }
type AuditProps = { point: PointDetail }

const explainMods = import.meta.glob("./PriorityExplain.tsx", { eager: true }) as Record<string, { PriorityExplain?: ComponentType<ExplainProps> }>
const actionMods = import.meta.glob("./ActionBlock.tsx", { eager: true }) as Record<string, { ActionBlock?: ComponentType<ActionProps> }>
const auditMods = import.meta.glob("./DecisionAuditPanel.tsx", { eager: true }) as Record<string, { DecisionAuditPanel?: ComponentType<AuditProps> }>

const PriorityExplain = Object.values(explainMods)[0]?.PriorityExplain
const ActionBlock = Object.values(actionMods)[0]?.ActionBlock
const DecisionAuditPanel = Object.values(auditMods)[0]?.DecisionAuditPanel

export function PointCard({ point, hideSynthetic }: { point: PointDetail; hideSynthetic: boolean }) {
  const uncertain = point.ownership_state !== "ASSIGNED"
  return (
    <article>
      <h2 style={{ fontSize: 16, fontWeight: 600, margin: "0 0 8px" }}>{point.name}</h2>
      <p>
        <StateChip state={point.ownership_state} />{" "}
        <AgencyBlock agency={point.responsible_agency} />{" "}
        <span className="mono muted">conf {point.ownership_confidence.toFixed(2)}</span>{" "}
        {point.uncertainty_band ? <span className="chip warn">{point.uncertainty_band}</span> : null}
      </p>
      {uncertain ? <p>Ownership uncertain — escalate to coordination cell.</p> : null}
      <p className="muted">Claimed: {point.agencies_claimed.join(", ") || "—"}</p>
      <p>{point.recommended_action}</p>
      {PriorityExplain ? <PriorityExplain point={point} /> : null}
      <EvidenceList items={point.evidence ?? []} />
      <ReadinessBlock readiness={point.readiness} hideSynthetic={hideSynthetic} />
      {ActionBlock ? <ActionBlock point={point} /> : null}
      {DecisionAuditPanel ? <DecisionAuditPanel point={point} /> : null}
      <ProvenanceFooter point={point} />
    </article>
  )
}
