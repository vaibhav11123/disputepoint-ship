import { useState } from "react"
import type { PointDetail } from "../api/client"
import { copy } from "../lib/copy"

const CHANNELS = [
  { role: "I&FC Flood Control Room", value: "011-21210867" },
  { role: "PWD helpline", value: "155305" },
  { role: "Disaster helpline", value: "1077" },
]

export function CoordinationBrief({ point }: { point: PointDetail }) {
  const escalated = (point.audit ?? []).some((a) => a.action === "ESCALATE") || Boolean(point.escalate_reason)
  const [copied, setCopied] = useState(false)
  const [openChannels, setOpenChannels] = useState(false)
  if (!escalated && point.ownership_state !== "CONFLICT") return null

  const brief = [
    copy.coordination.briefHeader,
    `Incident: ${point.name}`,
    `Status: ${copy.state.responsibilityDisputed}`,
    `Responsibility: ${point.agencies_claimed.join(" / ") || "—"}`,
    `Reason for review: ${point.escalate_reason || copy.coordination.fallbackReason}`,
    `Required action: Incident Commander to confirm operational responsibility.`,
    `Route: ${copy.coordination.routeBody}`,
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
    <section className="coordination-brief" data-testid="coordination-brief" aria-label={copy.coordination.briefAria}>
      <h3 className="section-h">{copy.coordination.title}</h3>
      <ul>
        <li>
          <strong>{copy.coordination.why}</strong>
          <br />
          {point.escalate_reason || copy.coordination.fallbackReason}
        </li>
        <li>
          <strong>{copy.coordination.route}</strong>
          <br />
          {copy.coordination.routeBody}
        </li>
        <li>
          <strong>{copy.coordination.next}</strong>
          <br />
          {copy.coordination.nextBody}
        </li>
        <li>
          <strong>{copy.coordination.point}</strong> {point.name} · {point.agencies_claimed.join(", ") || "—"}
        </li>
      </ul>
      <button type="button" data-testid="copy-brief" onClick={() => void copyBrief()}>
        {copied ? copy.coordination.copied : copy.coordination.copy}
      </button>
      <button type="button" className="linkish" onClick={() => setOpenChannels((v) => !v)} aria-expanded={openChannels}>
        {copy.coordination.channels} {openChannels ? "▾" : "▸"}
      </button>
      {openChannels ? (
        <ul className="channels" data-testid="official-channels">
          {CHANNELS.map((row) => (
            <li key={row.value}>
              <span className="muted">{row.role}</span> · <span className="mono">{row.value}</span>
            </li>
          ))}
          <li className="muted">{copy.coordination.verifiedContacts}</li>
        </ul>
      ) : null}
    </section>
  )
}
