import { useState } from "react"
import type { EvidenceItem } from "../api/client"

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
    <section className="evidence-ledger" data-testid="evidence-ledger" aria-label="Evidence ledger">
      <h3 className="section-h">Evidence</h3>
      {ownershipState === "CONFLICT" ? (
        <p className="evidence-effect muted">
          EFFECT: quotes establish competing claims — exclusive responsibility is not established.
        </p>
      ) : null}
      <ul className="evidence-list">
        {items.map((item) => {
          const active = traceId === item.id
          return (
            <li key={item.id} className={active ? "evidence-row tracing" : "evidence-row"}>
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
                    <span className="chip ok">live verified</span>
                  ) : (
                    <span className="chip">fixture cache</span>
                  )}
                </p>
                <p>
                  <q>{item.quote}</q>{" "}
                  <a href={item.url} target="_blank" rel="noreferrer">
                    source
                  </a>
                </p>
                {active ? (
                  <p className="trace-path mono" data-testid="evidence-trace">
                    CLAIM → SOURCE → QUOTE → DECISION EFFECT
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
