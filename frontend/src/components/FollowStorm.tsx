import { useState } from "react"
import { postClearScenario, postScenario, QUEUE_REFRESH } from "../api/client"

/** Tier A: ≤10s radar→priority cascade demo, then calm. Not permanent radar. */
export function FollowStorm({ onDone }: { onDone?: () => void }) {
  const [running, setRunning] = useState(false)
  const [status, setStatus] = useState<string | null>(null)

  async function run() {
    if (running) return
    setRunning(true)
    setStatus("FOLLOW RAIN — front approaching")
    const steps = [
      { mm: 12, msg: "Point corridor A — priority ↑" },
      { mm: 28, msg: "Point corridor B — priority ↑" },
      { mm: 42, msg: "Conflict corridor C — ownership dispute urgent" },
    ]
    try {
      for (const step of steps) {
        await postScenario(step.mm)
        window.dispatchEvent(new Event(QUEUE_REFRESH))
        setStatus(step.msg)
        await new Promise((r) => window.setTimeout(r, 2200))
      }
      setStatus("Returning to calm queue")
      const cleared = await postClearScenario()
      window.dispatchEvent(
        new CustomEvent(QUEUE_REFRESH, {
          detail: { precip_mm: typeof cleared.precip_mm === "number" ? cleared.precip_mm : undefined },
        }),
      )
      await new Promise((r) => window.setTimeout(r, 800))
      setStatus(null)
      onDone?.()
    } catch {
      setStatus("Follow Storm failed — use Rain Strike")
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="follow-storm" data-testid="follow-storm">
      <button type="button" disabled={running} aria-busy={running} onClick={() => void run()}>
        {running ? "Following…" : "Follow Storm"}
      </button>
      {status ? <span className="muted follow-status">{status}</span> : null}
    </div>
  )
}
