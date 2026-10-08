import { useMemo, useState } from "react"
import type { PointDetail } from "../api/client"
import { buildEventSteps } from "./EventRail"

type Frame = { t: string; label: string; stepId: string }

function framesFor(point: PointDetail): Frame[] {
  const steps = buildEventSteps(point)
  const base = "09:41"
  const labels: Record<string, string> = {
    rain: "RAIN",
    priority: "PRIORITY ↑",
    conflict: "RESPONSIBILITY DISPUTED",
    evidence: "EVIDENCE · WE DON’T GUESS",
    escalate: "HUMAN REVIEW",
    human: "OFFICER CONFIRMED",
  }
  const done = steps.filter((s) => s.done)
  return done.map((step, index) => {
    const minute = 41 + index
    return {
      t: `09:${String(minute).padStart(2, "0")}`,
      label: labels[step.id] ?? step.label,
      stepId: step.id,
    }
  })
}

export function IncidentReplay({ point }: { point: PointDetail }) {
  const frames = useMemo(() => framesFor(point), [point])
  const [index, setIndex] = useState(() => Math.max(0, frames.length - 1))
  if (frames.length === 0) return null

  const frame = frames[Math.min(index, frames.length - 1)]
  return (
    <section className="incident-replay" data-testid="incident-replay" aria-label="Incident replay">
      <div className="replay-head">
        <h3 className="section-h">Incident replay</h3>
        <span className="chip">MODE B</span>
      </div>
      <label className="replay-scrub">
        <span className="mono">
          {frame.t} · {frame.label}
        </span>
        <input
          type="range"
          min={0}
          max={frames.length - 1}
          value={Math.min(index, frames.length - 1)}
          aria-label="Replay case"
          onChange={(event) => setIndex(Number(event.target.value))}
        />
      </label>
      <ol className="replay-frames">
        {frames.map((f, i) => (
          <li key={f.stepId} className={i <= index ? "done" : "pending"}>
            <span className="mono">{f.t}</span> {f.label}
          </li>
        ))}
      </ol>
    </section>
  )
}
