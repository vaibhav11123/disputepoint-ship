import { useEffect, useRef, useState } from "react"
import { getHealth, postRainRefresh, postScenario, QUEUE_REFRESH } from "../api/client"

const POLL_MS = 15 * 60 * 1000

export function useRain() {
  const [precip, setPrecip] = useState(0)
  const [mode, setMode] = useState("cache")
  const [retrievedAt, setRetrievedAt] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const modeRef = useRef(mode)
  modeRef.current = mode

  async function refreshMode() {
    const health = await getHealth()
    setMode(health.rain_mode)
    if (typeof health.precip_mm === "number") setPrecip(health.precip_mm)
  }

  async function refreshLive() {
    setBusy(true)
    setError(null)
    try {
      const rain = await postRainRefresh()
      setPrecip(rain.precip_mm)
      setMode(rain.source === "open-meteo" ? "live" : rain.source === "scenario_slider" ? "slider" : "cache")
      setRetrievedAt(rain.retrieved_at ?? new Date().toISOString())
      window.dispatchEvent(new CustomEvent(QUEUE_REFRESH, { detail: { precip_mm: rain.precip_mm } }))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Live rain unavailable.")
      try {
        await refreshMode()
      } catch {
        /* keep prior mode */
      }
    } finally {
      setBusy(false)
    }
  }

  async function apply(mm: number) {
    setBusy(true)
    setError(null)
    try {
      const rain = await postScenario(mm)
      setPrecip(rain.precip_mm)
      setMode(rain.source === "scenario_slider" ? "slider" : rain.source === "open-meteo" ? "live" : "cache")
      setRetrievedAt(null)
      window.dispatchEvent(new CustomEvent(QUEUE_REFRESH, { detail: { precip_mm: rain.precip_mm } }))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Rain scenario failed.")
    } finally {
      setBusy(false)
    }
  }

  useEffect(() => {
    const id = window.setInterval(() => {
      if (document.visibilityState !== "visible") return
      if (modeRef.current === "slider") return
      void refreshLive()
    }, POLL_MS)
    return () => window.clearInterval(id)
  }, [])

  return {
    precip,
    setPrecip,
    mode,
    setMode,
    retrievedAt,
    busy,
    error,
    apply,
    refreshLive,
    refreshMode,
  }
}
