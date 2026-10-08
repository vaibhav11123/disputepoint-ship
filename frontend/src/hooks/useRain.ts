import { useState } from "react"
import { getHealth, postScenario, QUEUE_REFRESH } from "../api/client"

export function useRain() {
  const [precip, setPrecip] = useState(0)
  const [mode, setMode] = useState("cache")
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function refreshMode() {
    const health = await getHealth()
    setMode(health.rain_mode)
  }

  async function apply(mm: number) {
    setBusy(true)
    setError(null)
    try {
      const rain = await postScenario(mm)
      setMode(rain.source === "scenario_slider" ? "slider" : rain.source === "open-meteo" ? "live" : "cache")
      window.dispatchEvent(new Event(QUEUE_REFRESH))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Rain scenario failed.")
    } finally {
      setBusy(false)
    }
  }

  return { precip, setPrecip, mode, setMode, busy, error, apply, refreshMode }
}
