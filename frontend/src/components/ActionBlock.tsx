import { useState } from "react"
import { postAck, postEscalate, postOverride, QUEUE_REFRESH, type PointDetail } from "../api/client"

const AGENCIES = ["MCD", "PWD", "NDMC", "DJB", "PWD_FLOOD", "NHAI", "DMRC", "OTHER"]

export function ActionBlock({ point }: { point: PointDetail }) {
  const [reviewer, setReviewer] = useState("cell-1")
  const [agency, setAgency] = useState("PWD")
  const [overrideReason, setOverrideReason] = useState("")
  const [escalateReason, setEscalateReason] = useState("")
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const open = point.status === "OPEN"
  const ackEnabled = open && point.ownership_state === "ASSIGNED"

  async function run(work: () => Promise<unknown>) {
    setBusy(true)
    setError(null)
    try {
      await work()
      window.dispatchEvent(new Event(QUEUE_REFRESH))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Action failed.")
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="actions" aria-busy={busy} data-testid="hitl-actions">
      <label className="field">
        Reviewer
        <input aria-label="Reviewer" value={reviewer} onChange={(event) => setReviewer(event.target.value)} />
      </label>
      <button type="button" disabled={!ackEnabled || busy || reviewer.length === 0} onClick={() => run(() => postAck(point.id, reviewer))}>
        ACK
      </button>
      <label className="field">
        Agency
        <select aria-label="Override agency" value={agency} onChange={(event) => setAgency(event.target.value)}>
          {AGENCIES.map((name) => (
            <option key={name} value={name}>{name}</option>
          ))}
        </select>
      </label>
      <label className="field">
        Override reason
        <input aria-label="Override reason" value={overrideReason} onChange={(event) => setOverrideReason(event.target.value)} />
      </label>
      <button
        type="button"
        disabled={!open || busy || overrideReason.trim().length === 0 || reviewer.length === 0}
        onClick={() => run(() => postOverride(point.id, agency, overrideReason.trim(), reviewer))}
      >
        OVERRIDE
      </button>
      <label className="field">
        Escalate reason
        <input aria-label="Escalate reason" value={escalateReason} onChange={(event) => setEscalateReason(event.target.value)} />
      </label>
      <button
        type="button"
        disabled={busy || escalateReason.trim().length === 0 || reviewer.length === 0}
        onClick={() => run(() => postEscalate(point.id, escalateReason.trim(), reviewer))}
      >
        ESCALATE
      </button>
      {error ? <p className="error" role="alert">{error}</p> : null}
    </div>
  )
}
