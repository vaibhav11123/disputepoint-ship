/** Top-bar rainfall availability — derived from health source state, not mm thresholds. */

export type RainStatusInput = {
  scenarioActive?: boolean
  replayActive?: boolean
  rainSourceState?: string | null
  rainMode?: string | null
  precipMm?: number | null
  /** Historical station total — never treat as 6h LIVE R. */
  priorityUses?: boolean | null
  station?: string | null
  periodStart?: string | null
  periodEnd?: string | null
  windowHours?: number | null
}

/** Hours between ISO period bounds; null if unknown. */
export function periodHoursBetween(start?: string | null, end?: string | null): number | null {
  if (!start || !end) return null
  const a = Date.parse(start)
  const b = Date.parse(end)
  if (!Number.isFinite(a) || !Number.isFinite(b) || b <= a) return null
  return (b - a) / (1000 * 60 * 60)
}

export function rainAvailabilityLabel(input: RainStatusInput): string {
  if (input.replayActive || input.rainMode === "replay") {
    return "HISTORICAL REPLAY"
  }
  if (input.scenarioActive || input.rainMode === "slider") {
    return "SCENARIO APPLIED"
  }
  if (input.rainSourceState === "LIVE") return "LIVE DATA AVAILABLE"
  if (input.rainSourceState === "STALE") return "USING LAST OBSERVATION"
  if (input.rainSourceState === "SCENARIO" && !input.replayActive) return "SCENARIO APPLIED"
  return "LIVE RAINFALL UNAVAILABLE"
}

export function rainScenarioStripLine(
  input: RainStatusInput,
  scenarioLine: (mm: number) => string,
  sourceStatus: string,
  replayLine?: (mm: number, meta?: { station?: string; periodHours?: number | null }) => string,
): string {
  if (input.replayActive || input.rainMode === "replay" || input.priorityUses === false) {
    const mm = typeof input.precipMm === "number" ? input.precipMm : 0
    const periodHours =
      periodHoursBetween(input.periodStart, input.periodEnd) ??
      (typeof input.windowHours === "number" ? input.windowHours : null)
    const meta = {
      station: input.station || "Safdarjung",
      periodHours,
    }
    return replayLine ? replayLine(mm, meta) : `HISTORICAL REPLAY · ${meta.station.toUpperCase()} · ${Math.round(mm)} MM`
  }
  if (input.scenarioActive || input.rainMode === "slider") {
    const mm = typeof input.precipMm === "number" ? input.precipMm : 0
    return scenarioLine(mm)
  }
  return `${sourceStatus} · ${rainAvailabilityLabel(input)}`
}
