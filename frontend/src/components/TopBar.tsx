import type { ComponentType } from "react"
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
  rainMode = "DEMO",
}: {
  hideSynthetic: boolean
  onToggleSynthetic: () => void
  pulse: boolean
  counts?: { active: number; high: number; disputed: number; awaiting: number }
  actorRole?: string
  precipMm?: number
  rainMode?: string
}) {
  return (
    <header className="topbar">
      <div className="brand-block">
        <h1>DisputePoint</h1>
        <span className="muted brand-sub">DISTRICT OPERATIONS · NEW DELHI DISTRICT</span>
        <span className="chip" data-testid="role-chip" title="Session actor">
          {actorRole.replace(/_/g, " ")}
        </span>
      </div>
      {counts ? (
        <div className="counts-strip" data-testid="counts-strip">
          <span>ACTIVE {counts.active}</span>
          <span>HIGH {counts.high}</span>
          <span>DISPUTED {counts.disputed}</span>
          <span className="chip warn">AWAITING YOU {counts.awaiting}</span>
        </div>
      ) : null}
      <LiveSources />
      <div className="slot">
        <span className="mono rain-scenario-label" data-testid="rain-scenario-label">
          {precipMm > 5 ? `RAINFALL SCENARIO · ${Math.round(precipMm)} mm` : `RAIN STATUS · ${rainMode}`}
        </span>
        {RainControl ? <RainControl pulse={pulse} /> : <span className="muted">Rain control loads with the rain package.</span>}
        <button type="button" aria-pressed={hideSynthetic} onClick={onToggleSynthetic}>
          {hideSynthetic ? "Synthetic hidden" : "Hide synthetic"}
        </button>
        <span className="mono muted" aria-label="Local time IST">
          {clockIst()} IST
        </span>
      </div>
    </header>
  )
}
