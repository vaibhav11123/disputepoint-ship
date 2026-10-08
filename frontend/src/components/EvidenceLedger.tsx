import { useState } from "react"
import type { EvidenceItem } from "../api/client"

function decisionEffect(ownershipState: string, type: string): string {
  if (ownershipState === "CONFLICT") {
    return `Supports ${type.includes("PWD") ? "PWD" : "agency"} claim · Does NOT establish exclusive responsibility`
  }
  return "Supports claim · Review for exclusive responsibility"
}

export function EvidenceLedger({
  items,
  ownershipState,
}: {
  items: EvidenceItem[]
  ownershipState: string
}) {
  const [traceId, setTraceId] = useState<string | null>(null)

  if (items.length === 0) return <p className="muted">No evidence rows on this point.</p>

  return (
    <section className="evidence-ledger" data-testid="evidence-ledger" aria-label="Case evidence">
      <h3 className="section-h">CASE EVIDENCE</h3>
      {ownershipState === "CONFLICT" ? (
        <p className="evidence-effect muted" data-testid="claims-overlap">
          CLAIMS OVERLAP → NO AUTO-ASSIGN → HUMAN REVIEW
        </p>
      ) : null}
      <ul className="evidence-list">
        {items.map((item) => {
          const active = traceId === item.id
          const stale = item.live_status === "STALE" || item.live_status === "UNAVAILABLE"
          return (
            <li key={item.id} className={active ? "evidence-row tracing" : "evidence-row"} data-testid="evidence-card">
              <button
                type="button"
                className="evidence-trace-btn"
                onClick={() => setTraceId(active ? null : item.id)}
                aria-expanded={active}
              >
                Trace
              </button>
              <div>
                <p className="evidence-type">
                  {item.type}{" "}
                  {item.channel === "VOLUNTEER_REPORTED" ? (
                    <span className="chip warn" data-testid="volunteer-reported">
                      Volunteer reported
                    </span>
                  ) : null}{" "}
                  {item.live_verified ? (
                    <span className="chip ok">VERIFIED</span>
                  ) : (
                    <span className="chip">DEMO / fixture</span>
                  )}
                  {stale ? <span className="chip warn">SOURCE UNAVAILABLE</span> : null}
                </p>
                <p>
                  <q>{item.quote}</q>{" "}
                  <a href={item.url} target="_blank" rel="noreferrer">
                    source
                  </a>
                </p>
                <p className="decision-effect" data-testid="decision-effect">
                  {decisionEffect(ownershipState, item.type)}
                </p>
                {active ? (
                  <p className="trace-path mono" data-testid="evidence-trace">
                    CLAIM → SOURCE → EXTRACT → POINT → DECISION EFFECT
                    {ownershipState === "CONFLICT" ? " (no exclusive responsibility)" : ""}
                  </p>
                ) : null}
              </div>
            </li>
          )
        })}
      </ul>
    </section>
  )
}
