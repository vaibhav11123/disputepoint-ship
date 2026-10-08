import { useEffect, useState } from "react"
import type { PointDetail } from "../api/client"

function nextCheckIso(from: string, minutes = 30): string {
  const t = Date.parse(from)
  if (Number.isNaN(t)) return "—"
  return new Date(t + minutes * 60_000).toISOString()
}

function elapsedLabel(from: string, now: number): string {
  const t = Date.parse(from)
  if (Number.isNaN(t)) return "00:00:00"
  const sec = Math.max(0, Math.floor((now - t) / 1000))
  const h = String(Math.floor(sec / 3600)).padStart(2, "0")
  const m = String(Math.floor((sec % 3600) / 60)).padStart(2, "0")
  const s = String(sec % 60).padStart(2, "0")
  return `${h}:${m}:${s}`
}

export function AccountabilityClock({ point }: { point: PointDetail }) {
  const escalate = [...(point.audit ?? [])].reverse().find((row) => row.action === "ESCALATE")
  const override = [...(point.audit ?? [])].reverse().find((row) => row.action === "OVERRIDE")
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    if (!escalate || override) return
    const id = window.setInterval(() => setNow(Date.now()), 1000)
    return () => window.clearInterval(id)
  }, [escalate, override])

  if (!escalate) return null

  const caseId = `CASE ${point.id.toUpperCase().replace(/^DP-/, "DP-")}`
  const next = nextCheckIso(escalate.timestamp, 30)
  const pending = !override && !point.human_selected_agency

  return (
    <section className="accountability-clock" data-testid="accountability-clock" aria-label="Accountability clock">
      <h3 className="section-h">Coordination case</h3>
      <p className="case-line">
        <span className="mono">{caseId}</span>{" "}
        <span className="chip warn">ESCALATED</span>
      </p>
      <p>
        <strong>Owner:</strong>{" "}
        {pending ? <span data-testid="owner-pending">PENDING HUMAN ASSIGNMENT</span> : <span>{point.human_selected_agency}</span>}
      </p>
      {pending ? (
        <p>
          <strong>Elapsed:</strong> <span className="mono">{elapsedLabel(escalate.timestamp, now)}</span>
        </p>
      ) : null}
      <p>
        <strong>Next check:</strong>{" "}
        <span className="mono">{next === "—" ? "—" : next.replace("T", " ").slice(0, 16)}Z</span>
        <span className="muted"> (+30 min)</span>
      </p>
      <p className="muted">Audit: {escalate.timestamp}</p>
    </section>
  )
}
