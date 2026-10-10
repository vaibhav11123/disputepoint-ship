import { useEffect, useState } from "react"
import { getHealth, postEvidenceRefresh, type HealthInfo, type SourceHealth } from "../api/client"
import { copy } from "../lib/copy"
import { isJudgesMode } from "../lib/demoMode"

/** Operator-facing strip only — gated IMD / NWDP / Google stay in /health, not UI. */
const OPERATOR_SOURCE_IDS = ["open-meteo-rain", "evidence-live"] as const

function findSource(health: HealthInfo, id: string): SourceHealth | undefined {
  return health.sources?.find((s) => s.source_id === id)
}

function rainLabel(health: HealthInfo): string {
  const state = health.rain_source_state || findSource(health, "open-meteo-rain")?.source_state
  const mm = health.precip_mm
  const mmPart = mm == null ? "—" : `${mm} mm`
  if (health.scenario_active || health.rain_mode === "slider" || state === "SCENARIO") {
    return `${copy.sources.rainfallScenario} · ${mmPart}`
  }
  if (state === "LIVE") return `${copy.sources.rainfallLive} · ${mmPart}`
  if (state === "STALE") return `${copy.sources.rainfallStale} · ${mmPart}`
  if (state === "UNAVAILABLE") return `${copy.sources.rainfallUnavailable} · ${mmPart}`
  return `${copy.sources.rainfallUnknown} · ${mmPart}`
}

function evidenceLabel(health: HealthInfo): string {
  const counts = health.evidence_counts
  if (counts) return copy.sources.evidenceCounts(counts)
  const src = findSource(health, "evidence-live")
  const state = src?.source_state
  if (state === "LIVE") return copy.sources.evidenceCurrent
  if (state === "STALE") return copy.sources.evidenceStale
  if (state === "UNAVAILABLE") return copy.sources.evidenceUnavailable
  return copy.sources.evidenceScenario
}

function fmtTime(value?: string | null): string {
  if (!value) return "—"
  return value.replace("T", " ").replace("Z", " UTC")
}

export function LiveSources({ compact = false }: { compact?: boolean }) {
  const [health, setHealth] = useState<HealthInfo | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [expanded, setExpanded] = useState(false)
  const judges = isJudgesMode()

  async function load() {
    try {
      setHealth(await getHealth())
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.sources.healthFail)
    }
  }

  useEffect(() => {
    void load()
    const id = window.setInterval(() => void load(), 60_000)
    return () => window.clearInterval(id)
  }, [])

  async function refreshEvidence() {
    setBusy(true)
    setError(null)
    try {
      await postEvidenceRefresh()
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.sources.evidenceFail)
    } finally {
      setBusy(false)
    }
  }

  if (!health) {
    return error ? (
      <span className="error" role="alert">
        {error}
      </span>
    ) : (
      <span className="muted live-sources">{copy.sources.sources}</span>
    )
  }

  const rain = findSource(health, "open-meteo-rain")
  const evidence = findSource(health, "evidence-live")
  const sourceCount = OPERATOR_SOURCE_IDS.length
  const rainLine = rainLabel(health)
  const evidenceLine = evidenceLabel(health)
  const observed = health.rain_observation_time || rain?.observation_time || health.rain_retrieved_at
  const retrieved = health.rain_retrieved_at || rain?.retrieved_at

  if (compact) {
    return (
      <div className="live-sources compact" data-testid="live-sources">
        <span className="chip">{copy.sources.dataStatus}</span>
        <span className={health.rain_source_state === "LIVE" ? "chip ok" : "chip"}>
          {health.rain_source_state || health.rain_mode}
        </span>
        {error ? (
          <span className="error" role="alert">
            {error}
          </span>
        ) : null}
      </div>
    )
  }

  return (
    <div className="live-sources" data-testid="live-sources">
      <button type="button" className="chip" onClick={() => setExpanded((v) => !v)} aria-expanded={expanded}>
        {copy.sources.dataStatusCount(sourceCount)}
      </button>
      <span className="muted" data-testid="source-health-summary">
        {rainLine}
        {observed ? ` · ${copy.sources.observed} ${fmtTime(observed)}` : ""}
        {retrieved ? ` · ${copy.sources.retrieved} ${fmtTime(retrieved)}` : ""}
        {health.scenario_active ? " · scenario active" : ""}
        {" · "}
        {evidenceLine}
      </span>
      {health.rain_source_state === "STALE" ? <span className="muted">{copy.sources.staleHint}</span> : null}
      {health.rain_source_state === "UNAVAILABLE" && !health.scenario_active ? (
        <span className="muted">{copy.sources.unavailableHint}</span>
      ) : null}
      {expanded || judges ? (
        <div className="source-health-detail mono muted" data-testid="source-health-detail">
          <div>
            {copy.sources.dataSources}: rainfall={rain?.source_state ?? "—"} value=
            {health.precip_mm == null ? "—" : health.precip_mm} retrieved={fmtTime(retrieved)} err=
            {rain?.last_error_category ?? "none"}
          </div>
          <div data-testid="evidence-counts-line">
            evidence={evidence?.source_state ?? "—"} · {evidenceLine}
          </div>
        </div>
      ) : null}
      {health.live_fetch ? (
        <button type="button" disabled={busy} aria-busy={busy} onClick={() => void refreshEvidence()}>
          {copy.sources.refreshEvidence}
        </button>
      ) : null}
      {error ? (
        <span className="error" role="alert">
          {error}
        </span>
      ) : null}
    </div>
  )
}
