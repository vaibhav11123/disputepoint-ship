import { useEffect } from "react"
import { getHealth } from "../api/client"
import { useRain } from "../hooks/useRain"

const MODE_LABEL = { live: "Live", cache: "Cache", slider: "Slider" } as const

export function RainControl({ pulse }: { pulse: boolean }) {
  const rain = useRain()
  useEffect(() => {
    getHealth().then((health) => rain.setMode(health.rain_mode)).catch(() => undefined)
  }, [])
  const label = MODE_LABEL[rain.mode as keyof typeof MODE_LABEL] ?? "Cache"
  return (
    <form
      className={pulse ? "actions pulse" : "actions"}
      onSubmit={(event) => {
        event.preventDefault()
        void rain.apply(rain.precip)
      }}
    >
      <label className="field">
        Rain mm
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
      <span className="chip">{label}</span>
      {rain.mode === "slider" ? <span>Using scenario rain</span> : null}
      {rain.error ? <span className="error" role="alert">{rain.error}</span> : null}
    </form>
  )
}
