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
}: {
  hideSynthetic: boolean
  onToggleSynthetic: () => void
  pulse: boolean
}) {
  return (
    <header className="topbar">
      <div className="brand-block">
        <h1>DisputePoint</h1>
        <span className="muted brand-sub">WATERLOGGING COORDINATION</span>
      </div>
      <LiveSources />
      <div className="slot">
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
