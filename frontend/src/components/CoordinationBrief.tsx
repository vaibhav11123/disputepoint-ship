import { useState } from "react"
import type { PointDetail } from "../api/client"

const CHANNELS = [
  { role: "I&FC flood control room", value: "011-21210867", asOf: "2026-10" },
  { role: "PWD helpline", value: "155305", asOf: "2026-10" },
  { role: "Disaster helpline", value: "1077", asOf: "2026-10" },
]

export function CoordinationBrief({ point }: { point: PointDetail }) {
  const escalated = (point.audit ?? []).some((a) => a.action === "ESCALATE") || Boolean(point.escalate_reason)
  const [copied, setCopied] = useState(false)
  const [openChannels, setOpenChannels] = useState(false)
  if (!escalated && point.ownership_state !== "CONFLICT") return null

  const brief = [
    `CASE: ${point.id}`,
    `Location: ${point.name}`,
    `State: RESPONSIBILITY DISPUTED / ${point.ownership_state}`,
    `Claims: ${point.agencies_claimed.join(" ↔ ") || "—"}`,
    `Reason: ${point.escalate_reason || "Competing agency claims; evidence does not establish exclusive responsibility"}`,
    `NEXT ACTION: Confirm operational responsibility (Incident Commander)`,
    `Route: District EOC → IC → Agency division → Engineering officer`,
  ].join("\n")

  async function copyBrief() {
    try {
      await navigator.clipboard.writeText(brief)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 2000)
    } catch {
      setCopied(false)
    }
  }

  return (
    <section className="coordination-brief" data-testid="coordination-brief" aria-label="Coordination brief">
      <h3 className="section-h">HUMAN REVIEW REQUIRED</h3>
      <ul>
        <li>
          <strong>Reason:</strong> {point.escalate_reason || "Competing agency claims + no exclusive responsibility"}
        </li>
        <li>
          <strong>Route:</strong> District EOC → Incident Commander → Agency division → Engineering officer
        </li>
        <li>
          <strong>NEXT ACTION:</strong> Confirm operational responsibility
        </li>
        <li>
          <strong>Point:</strong> {point.name} · {point.agencies_claimed.join(", ") || "—"}
        </li>
      </ul>
      <button type="button" data-testid="copy-brief" onClick={() => void copyBrief()}>
        {copied ? "COPIED" : "COPY BRIEF"}
      </button>
      <button type="button" className="linkish" onClick={() => setOpenChannels((v) => !v)} aria-expanded={openChannels}>
        Official coordination channels {openChannels ? "▾" : "▸"}
      </button>
      {openChannels ? (
        <ul className="channels" data-testid="official-channels">
          {CHANNELS.map((row) => (
            <li key={row.value}>
              <span className="muted">{row.role}</span> · <span className="mono">{row.value}</span>{" "}
              <span className="muted">as-of {row.asOf}</span>
            </li>
          ))}
        </ul>
      ) : null}
    </section>
  )
}
