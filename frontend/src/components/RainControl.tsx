import { useEffect } from "react"
import { useRain } from "../hooks/useRain"
import { FollowStorm } from "./FollowStorm"
import { isJudgesMode, MAP_EXPAND_EVENT, RAIN_STRIKE_EVENT } from "../lib/demoMode"

const MODE_LABEL = { live: "Live", cache: "Cache", slider: "Slider" } as const
const STRIKE_MM = 42

export function RainControl({ pulse }: { pulse: boolean }) {
  const rain = useRain()
  const judges = isJudgesMode()
  useEffect(() => {
    rain.refreshMode().catch(() => undefined)
  }, [])
  const label = MODE_LABEL[rain.mode as keyof typeof MODE_LABEL] ?? "Cache"

  async function strike() {
    window.dispatchEvent(new Event(RAIN_STRIKE_EVENT))
    window.dispatchEvent(new Event(MAP_EXPAND_EVENT))
    await rain.apply(STRIKE_MM)
  }

  return (
    <form
      className={pulse ? "actions pulse rain-strip" : "actions rain-strip"}
      onSubmit={(event) => {
        event.preventDefault()
        void rain.apply(rain.precip > 0 ? rain.precip : STRIKE_MM)
      }}
    >
      <button
        type="button"
        className="primary-action rain-strike"
        data-testid="rain-strike"
        disabled={rain.busy}
        aria-busy={rain.busy}
        onClick={() => void strike()}
      >
        Rain Strike
      </button>
      <span className="mono" aria-live="polite" data-testid="rain-mm">
        {rain.mode === "slider" || rain.precip > 5
          ? `RAINFALL SCENARIO · ${rain.precip.toFixed(0)} mm`
          : `${rain.precip.toFixed(1)} mm`}
      </span>
      <span className="chip">{rain.mode === "slider" ? "DEMO" : label}</span>
      {rain.retrievedAt ? (
        <span className="muted mono" title={rain.retrievedAt}>
          {rain.retrievedAt.replace("T", " ").slice(0, 16)}Z
        </span>
      ) : null}
      {judges ? (
        <>
          <button type="button" disabled={rain.busy} aria-busy={rain.busy} onClick={() => void rain.refreshLive()}>
            Refresh live rain
          </button>
          <label className="field">
            Scenario mm
            <input
              aria-label="Scenario rain millimetres"
              type="number"
              min={0}
              step={1}
              value={rain.precip}
              onChange={(event) => rain.setPrecip(Number(event.target.value))}
            />
          </label>
          <button type="submit" disabled={rain.busy} aria-busy={rain.busy}>
            Apply rain
          </button>
        </>
      ) : (
        <label className="field visually-hidden">
          Scenario mm
          <input
            aria-label="Scenario rain millimetres"
            type="number"
            min={0}
            step={1}
            value={rain.precip}
            onChange={(event) => rain.setPrecip(Number(event.target.value))}
          />
        </label>
      )}
      {rain.mode === "slider" ? <span>Using scenario rain · DEMO</span> : null}
      <FollowStorm />
      {rain.error ? (
        <span className="error" role="alert">
          {rain.error}
        </span>
      ) : null}
    </form>
  )
}
