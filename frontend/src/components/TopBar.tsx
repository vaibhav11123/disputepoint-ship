import { useState, type ComponentType } from "react"
import { copy } from "../lib/copy"
import { isJudgesMode, isQuietDemoChrome } from "../lib/demoMode"
import { rainAvailabilityLabel, rainScenarioStripLine } from "../lib/rainStatus"
import { LiveSources } from "./LiveSources"

type RainProps = { pulse: boolean }

const rainMods = import.meta.glob("./RainControl.tsx", { eager: true }) as Record<string, { RainControl?: ComponentType<RainProps> }>
const RainControl = Object.values(rainMods)[0]?.RainControl

function clockIst() {
  try {
    return new Intl.DateTimeFormat("en-IN", {
      timeZone: "Asia/Kolkata",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    }).format(new Date())
  } catch {
    return "--:--"
  }
}

export function TopBar({
  hideSynthetic,
  onToggleSynthetic,
  pulse,
  counts,
  actorRole = "INCIDENT_COMMANDER",
  precipMm = 0,
  rainMode = "none",
  rainSourceState = null,
  scenarioActive = false,
  replayActive = false,
  rainStation = null,
  rainPeriodStart = null,
  rainPeriodEnd = null,
  rainPriorityUses = null,
  quietChrome,
}: {
  hideSynthetic: boolean
  onToggleSynthetic: () => void
  pulse: boolean
  counts?: { active: number; high: number; disputed: number; awaiting: number }
  actorRole?: string
  precipMm?: number
  rainMode?: string
  rainSourceState?: string | null
  scenarioActive?: boolean
  replayActive?: boolean
  rainStation?: string | null
  rainPeriodStart?: string | null
  rainPeriodEnd?: string | null
  rainPriorityUses?: boolean | null
  quietChrome?: boolean
}) {
  const quiet = quietChrome ?? isQuietDemoChrome()
  const judges = isJudgesMode()
  const [configureOpen, setConfigureOpen] = useState(false)

  const statusInput = {
    scenarioActive,
    replayActive,
    rainSourceState,
    rainMode,
    precipMm,
    station: rainStation,
    periodStart: rainPeriodStart,
    periodEnd: rainPeriodEnd,
    priorityUses: rainPriorityUses,
  }
  const scenarioLine = rainScenarioStripLine(
    statusInput,
    copy.rain.scenarioLine,
    copy.sources.sourceStatus,
    copy.rain.replayLine,
  )
  const dataState = rainAvailabilityLabel(statusInput)

  return (
    <div className="shell">
      <header className={quiet ? "topbar quiet-demo" : "topbar"}>
        <div className="brand-block">
          <div className="brand-row">
            <h1>{copy.brand.name}</h1>
            <span className="chip" data-testid="role-chip">
              {actorRole === "INCIDENT_COMMANDER" ? copy.topbar.role : actorRole.replace(/_/g, " ")}
            </span>
          </div>
        </div>
        <nav className="slot" aria-label="Primary">
          <span className="mono muted" style={{ color: "rgba(244,243,238,0.85)" }}>
            Command
          </span>
          <span className="mono muted" aria-label={copy.topbar.clockAria}>
            {clockIst()} IST
          </span>
        </nav>
      </header>

      {counts ? (
        <div className="metrics-strip" data-testid="counts-strip">
          <div className="metric">
            <span className="metric-num">{counts.active}</span>
            <span className="metric-label">{copy.topbar.active}</span>
          </div>
          <div className="metric">
            <span className="metric-num">{counts.high}</span>
            <span className="metric-label">{copy.topbar.highPriority}</span>
          </div>
          <div className="metric">
            <span className="metric-num">{counts.disputed}</span>
            <span className="metric-label">{copy.topbar.disputed}</span>
          </div>
          <div className="metric awaiting">
            <span className="metric-num">{counts.awaiting}</span>
            <span className="metric-label">Awaiting review</span>
          </div>
        </div>
      ) : null}

      <div className="scenario-strip" data-testid="scenario-strip">
        <span className="mono" data-testid="rain-scenario-label">
          {scenarioLine}
        </span>
        <span className="dp-meta" data-testid="rain-availability">
          {dataState}
        </span>
        <details
          open={configureOpen}
          onToggle={(e) => setConfigureOpen((e.target as HTMLDetailsElement).open)}
        >
          <summary>Configure</summary>
        </details>
      </div>

      {configureOpen ? (
        <div className="topbar-more" data-testid="topbar-more">
          <LiveSources compact={false} />
          {RainControl ? <RainControl pulse={pulse} /> : null}
          <button type="button" aria-pressed={hideSynthetic} onClick={onToggleSynthetic}>
            {hideSynthetic ? copy.topbar.scenarioHidden : copy.topbar.hideScenario}
          </button>
          {judges ? <span className="muted">Source controls</span> : null}
        </div>
      ) : null}
    </div>
  )
}
