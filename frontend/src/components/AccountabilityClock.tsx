import { useEffect, useState } from "react"
import type { PointDetail } from "../api/client"
import { copy } from "../lib/copy"

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
  const decided =
    Boolean(point.officer_confirmed) ||
    Boolean(point.human_selected_agency) ||
    Boolean(point.decision_record)
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    if (!escalate || decided) return
    const id = window.setInterval(() => setNow(Date.now()), 1000)
    return () => window.clearInterval(id)
  }, [escalate, decided])

  if (!escalate) return null

  const caseId = `CASE ${point.id.toUpperCase().replace(/^DP-/, "DP-")}`
  const next = nextCheckIso(escalate.timestamp, 30)
  const pending = !decided

  return (
    <section className="accountability-clock" data-testid="accountability-clock" aria-label={copy.clock.aria}>
      <h3 className="section-h">{copy.clock.title}</h3>
      <p className="case-line">
        <span className="mono">{caseId}</span>{" "}
        <span className="chip warn">{copy.clock.escalated}</span>
      </p>
      <p>
        <strong>{copy.clock.status}</strong>{" "}
        {pending ? (
          <span data-testid="owner-pending">{copy.clock.awaiting}</span>
        ) : (
          <span>{point.human_selected_agency ?? String(point.decision_record?.agency ?? "")}</span>
        )}
      </p>
      {pending ? (
        <p>
          <strong>{copy.clock.reviewAge}</strong> <span className="mono">{elapsedLabel(escalate.timestamp, now)}</span>
        </p>
      ) : null}
      <p>
        <strong>{copy.clock.nextReview}</strong>{" "}
        <span className="mono">{next === "—" ? "—" : next.replace("T", " ").slice(0, 16)}Z</span>
        <span className="muted"> (+30 min)</span>
      </p>
      <p className="muted">
        {copy.audit.auditId}: {escalate.timestamp}
      </p>
    </section>
  )
}
