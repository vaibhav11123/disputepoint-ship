import { useState } from "react"
import type { EvidenceItem } from "../api/client"
import { copy } from "../lib/copy"
import { evidenceChip, evidenceChipTone } from "../lib/evidenceStatus"

function decisionEffect(ownershipState: string, agency: string | null | undefined): string {
  if (ownershipState === "CONFLICT") {
    if (agency && agency.trim()) return copy.evidence.effectConflict(agency.trim())
    return copy.evidence.effectConflictUnknown
  }
  return copy.evidence.effectOk
}

export function EvidenceLedger({
  items,
  ownershipState,
}: {
  items: EvidenceItem[]
  ownershipState: string
}) {
  const [traceId, setTraceId] = useState<string | null>(null)

  if (items.length === 0) return <p className="muted">{copy.evidence.empty}</p>

  return (
    <section className="evidence-ledger" data-testid="evidence-ledger" aria-label={copy.evidence.caseAria}>
      <h3 className="dp-section">{copy.evidence.heading}</h3>
      {ownershipState === "CONFLICT" ? (
        <p className="evidence-effect muted" data-testid="claims-overlap">
          {copy.evidence.conflictBanner}
        </p>
      ) : null}
      <ul className="evidence-list">
        {items.map((item) => {
          const active = traceId === item.id
          const chip = evidenceChip(item)
          const tone = evidenceChipTone(item)
          return (
            <li key={item.id} className={active ? "evidence-row tracing" : "evidence-row"} data-testid="evidence-card">
              <button
                type="button"
                className="evidence-trace-btn"
                onClick={() => setTraceId(active ? null : item.id)}
                aria-expanded={active}
              >
                {copy.evidence.viewSource}
              </button>
              <div>
                <p className="evidence-type">
                  {item.type}{" "}
                  <span
                    className={tone === "ok" ? "chip ok" : tone === "warn" ? "chip warn" : "chip"}
                    data-testid="evidence-status-chip"
                  >
                    {chip}
                  </span>
                </p>
                {item.title ? <p className="dp-section" style={{ fontSize: 13 }}>{item.title}</p> : null}
                {(item.publisher || item.source_date) && (
                  <p className="dp-meta">
                    {[item.publisher, item.source_date].filter(Boolean).join(" · ")}
                  </p>
                )}
                <p>
                  <q>{item.quote}</q>{" "}
                  <a href={item.url} target="_blank" rel="noopener noreferrer">
                    {copy.evidence.source}
                  </a>
                  <span className="dp-meta visually-hidden">{item.id}</span>
                </p>
                {item.establishes ? (
                  <p className="dp-body muted" data-testid="evidence-establishes">
                    Establishes: {item.establishes}
                  </p>
                ) : null}
                {item.does_not_establish ? (
                  <p className="dp-body muted" data-testid="evidence-does-not">
                    Does not establish: {item.does_not_establish}
                  </p>
                ) : null}
                <p className="decision-effect" data-testid="decision-effect">
                  {decisionEffect(ownershipState, item.agency)}
                </p>
                {active ? (
                  <div className="trace-path mono" data-testid="evidence-trace">
                    <p className="dp-label">{copy.evidence.trace}</p>
                    <p>CLAIM</p>
                    <p>↓</p>
                    <p>SOURCE</p>
                    <p>↓</p>
                    <p>EXTRACT</p>
                    <p>↓</p>
                    <p>DECISION EFFECT{ownershipState === "CONFLICT" ? copy.evidence.noExclusive : ""}</p>
                  </div>
                ) : null}
              </div>
            </li>
          )
        })}
      </ul>
      {ownershipState === "CONFLICT" ? (
        <p className="section-h" data-testid="what-remains-unresolved">
          {copy.evidence.unresolved}
        </p>
      ) : null}
    </section>
  )
}
