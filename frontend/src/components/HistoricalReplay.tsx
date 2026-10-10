import { useEffect, useState } from "react"
import { exitReplay, getReplay, seekReplay, QUEUE_REFRESH, type ReplayState } from "../api/client"
import { copy } from "../lib/copy"

const REPLAY_ID = "delhi-2025-07-29"

export function HistoricalReplay({ onActivated }: { onActivated?: (ids: string[]) => void }) {
  const [milestones, setMilestones] = useState<string[]>(["start"])
  const [index, setIndex] = useState(0)
  const [state, setState] = useState<ReplayState | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [active, setActive] = useState(false)

  useEffect(() => {
    getReplay(REPLAY_ID)
      .then((pack) => {
        setMilestones(pack.milestones?.length ? pack.milestones : ["start"])
      })
      .catch((err: unknown) => setError(err instanceof Error ? err.message : "Replay unavailable"))
  }, [])

  async function goTo(nextIndex: number) {
    setBusy(true)
    setError(null)
    try {
      const clamped = Math.max(0, Math.min(nextIndex, milestones.length - 1))
      const projected = await seekReplay({ step_index: clamped }, REPLAY_ID)
      setIndex(clamped)
      setState(projected)
      setActive(true)
      onActivated?.(projected.activated_point_ids || [])
      window.dispatchEvent(
        new CustomEvent(QUEUE_REFRESH, {
          detail: { precip_mm: projected.precip_mm ?? undefined },
        }),
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : "Seek failed")
    } finally {
      setBusy(false)
    }
  }

  async function leave() {
    setBusy(true)
    setError(null)
    try {
      await exitReplay(REPLAY_ID)
      setActive(false)
      setState(null)
      setIndex(0)
      onActivated?.([])
      window.dispatchEvent(new CustomEvent(QUEUE_REFRESH, { detail: {} }))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Exit failed")
    } finally {
      setBusy(false)
    }
  }

  const gaps = state?.gaps?.points_without_day_evidence?.length ?? 0
  const clockLabel =
    !state || !state.clock || state.clock === "start"
      ? copy.historicalReplay.startDay
      : state.clock.replace("T", " ").replace("+05:30", " IST")

  return (
    <section className="historical-replay" data-testid="historical-replay" aria-label={copy.historicalReplay.aria}>
      <div className="brand-row" style={{ gap: 8, flexWrap: "wrap" }}>
        <span className="chip warn">{copy.historicalReplay.chip}</span>
        <span className="dp-section">{copy.historicalReplay.title}</span>
      </div>
      <p className="muted dp-body">{copy.historicalReplay.disclaimer}</p>
      <div className="actions rain-strip">
        <button type="button" disabled={busy} onClick={() => void goTo(0)}>
          {copy.historicalReplay.startDay}
        </button>
        <button type="button" disabled={busy || index <= 0} onClick={() => void goTo(index - 1)}>
          {copy.historicalReplay.back}
        </button>
        <button
          type="button"
          className="primary-action"
          data-testid="replay-advance"
          disabled={busy || index >= milestones.length - 1}
          onClick={() => void goTo(index + 1)}
        >
          {copy.historicalReplay.advance}
        </button>
        {active ? (
          <button type="button" data-testid="replay-exit" disabled={busy} onClick={() => void leave()}>
            {copy.historicalReplay.exit}
          </button>
        ) : null}
      </div>
      {active && state ? (
        <div className="source-health-detail mono muted" data-testid="replay-state">
          <p>
            Clock · {clockLabel} · step {index}/{milestones.length - 1}
          </p>
          <p>
            {copy.historicalReplay.priorityUses}
            {typeof state.precip_mm === "number"
              ? (() => {
                  const sj = (state.stations || []).find((s) => s.station === "Safdarjung")
                  const start = sj?.period_start
                  const end = sj?.period_end
                  let hours = ""
                  if (start && end) {
                    const ms = Date.parse(end) - Date.parse(start)
                    if (Number.isFinite(ms) && ms > 0) {
                      const h = ms / (1000 * 60 * 60)
                      hours = ` · ${Number.isInteger(h) ? h : h.toFixed(1)}h reported`
                    }
                  }
                  return ` · ${state.precip_mm} mm${hours}`
                })()
              : ` · ${copy.historicalReplay.noPrecip}`}
          </p>
          <p>
            {copy.historicalReplay.stations}:{" "}
            {(state.stations || [])
              .map((s) => {
                const start = s.period_start
                const end = s.period_end
                let suffix = ""
                if (start && end) {
                  const ms = Date.parse(end) - Date.parse(start)
                  if (Number.isFinite(ms) && ms > 0) {
                    const h = ms / (1000 * 60 * 60)
                    suffix = `/${Number.isInteger(h) ? h : h.toFixed(1)}h`
                  }
                }
                return `${s.station} ${s.precip_mm}mm${suffix}`
              })
              .join(" · ") || "—"}
          </p>
          <p>
            {copy.historicalReplay.activated}: {(state.activated_point_ids || []).join(", ") || "—"}
          </p>
          <p data-testid="replay-gaps">
            {copy.historicalReplay.endReview}: {gaps} points without 29 Jul evidence
          </p>
        </div>
      ) : null}
      {error ? (
        <span className="error" role="alert">
          {error}
        </span>
      ) : null}
    </section>
  )
}
