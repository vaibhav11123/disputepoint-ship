import type { ComponentType } from "react"

type RainProps = { pulse: boolean }

const rainMods = import.meta.glob("./RainControl.tsx", { eager: true }) as Record<string, { RainControl?: ComponentType<RainProps> }>
const RainControl = Object.values(rainMods)[0]?.RainControl

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
      <h1>DisputePoint</h1>
      <div className="slot">
        {RainControl ? <RainControl pulse={pulse} /> : <span className="muted">Rain control loads with the rain package.</span>}
        <button type="button" aria-pressed={hideSynthetic} onClick={onToggleSynthetic}>
          {hideSynthetic ? "Synthetic hidden" : "Hide synthetic"}
        </button>
      </div>
    </header>
  )
}
