import { useEffect } from "react"
import { useRain } from "../hooks/useRain"
import { FollowStorm } from "./FollowStorm"
import { copy } from "../lib/copy"
import { isJudgesMode, MAP_EXPAND_EVENT, RAIN_STRIKE_EVENT } from "../lib/demoMode"

const STRIKE_MM = 42

function productMode(mode: string, sourceState: string | null, scenarioActive: boolean): string {
  if (scenarioActive || mode === "slider" || sourceState === "SCENARIO") return copy.rain.scenario
  if (mode === "live" || sourceState === "LIVE") return copy.rain.live
  if (sourceState === "STALE") return copy.rain.lastObservation
  return copy.rain.unavailable
}

export function RainControl({ pulse }: { pulse: boolean }) {
  const rain = useRain()
  const judges = isJudgesMode()
  const onDemoRoute = typeof window !== "undefined" && window.location.pathname.startsWith("/demo")
  useEffect(() => {
    rain.refreshMode().catch(() => undefined)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- mount refresh only
  }, [])
  const modeChip = productMode(rain.mode, rain.sourceState, rain.scenarioActive)

  async function applyScenario() {
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
        onClick={() => void applyScenario()}
      >
        {copy.rain.apply}
      </button>
      <span className="mono" aria-live="polite" data-testid="rain-mm">
        {rain.scenarioActive || rain.mode === "slider"
          ? copy.rain.scenarioLine(rain.precip)
          : typeof rain.precip === "number"
            ? `${rain.precip.toFixed(1)} mm`
            : "— mm"}
      </span>
      <span className="chip" data-testid="rain-mode-chip">
        {modeChip}
      </span>
      {rain.retrievedAt ? (
        <span className="muted mono" title={rain.retrievedAt}>
          {rain.retrievedAt.replace("T", " ").slice(0, 16)}Z
        </span>
      ) : null}
      {judges ? (
        <>
          <button type="button" disabled={rain.busy} aria-busy={rain.busy} onClick={() => void rain.refreshLive()}>
            {copy.rain.refreshLive}
          </button>
          {rain.scenarioActive ? (
            <button
              type="button"
              data-testid="clear-scenario"
              disabled={rain.busy}
              aria-busy={rain.busy}
              onClick={() => void rain.clearScenario()}
            >
              {copy.rain.clearScenario}
            </button>
          ) : null}
          <label className="field">
            {copy.rain.label}
            <input
              aria-label={copy.rain.aria}
              type="number"
              min={0}
              step={1}
              value={rain.precip}
              onChange={(event) => rain.setPrecip(Number(event.target.value))}
            />
          </label>
          <button type="submit" disabled={rain.busy} aria-busy={rain.busy}>
            {copy.rain.apply}
          </button>
        </>
      ) : (
        <label className="field visually-hidden">
          {copy.rain.label}
          <input
            aria-label={copy.rain.aria}
            type="number"
            min={0}
            step={1}
            value={rain.precip}
            onChange={(event) => rain.setPrecip(Number(event.target.value))}
          />
        </label>
      )}
      {rain.scenarioActive ? (
        <span className="muted">
          {copy.rain.scenarioRainfall(rain.precip)} <span className="chip">{copy.rain.scenario}</span>
        </span>
      ) : null}
      {onDemoRoute ? <FollowStorm /> : null}
      {rain.error ? (
        <span className="error" role="alert">
          {rain.error}
        </span>
      ) : null}
    </form>
  )
}
