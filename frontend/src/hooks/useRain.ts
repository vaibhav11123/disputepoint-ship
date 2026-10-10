import { useEffect, useRef, useState } from "react"
import { getHealth, postClearScenario, postRainRefresh, postScenario, QUEUE_REFRESH } from "../api/client"
import { copy } from "../lib/copy"

const POLL_MS = 15 * 60 * 1000

export function useRain() {
  const [precip, setPrecip] = useState(0)
  const [mode, setMode] = useState("cache")
  const [sourceState, setSourceState] = useState<string | null>(null)
  const [scenarioActive, setScenarioActive] = useState(false)
  const [retrievedAt, setRetrievedAt] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const modeRef = useRef(mode)
  modeRef.current = mode

  function applyHealth(health: Awaited<ReturnType<typeof getHealth>>) {
    setMode(health.rain_mode)
    setSourceState(health.rain_source_state ?? null)
    setScenarioActive(Boolean(health.scenario_active))
    if (health.precip_mm == null) setPrecip(0)
    else if (typeof health.precip_mm === "number") setPrecip(health.precip_mm)
    setRetrievedAt(health.rain_retrieved_at ?? health.rain_observation_time ?? null)
  }

  async function refreshMode() {
    const health = await getHealth()
    applyHealth(health)
  }

  async function refreshLive() {
    setBusy(true)
    setError(null)
    try {
      const rain = await postRainRefresh()
      if (rain.source === "historical_replay" || rain.display_unchanged) {
        // Stash updated under historical display — re-sync health, do not flip to LIVE.
        await refreshMode()
        window.dispatchEvent(
          new CustomEvent(QUEUE_REFRESH, {
            detail: { precip_mm: typeof rain.precip_mm === "number" ? rain.precip_mm : undefined },
          }),
        )
        return
      }
      setPrecip(rain.precip_mm)
      setMode(rain.source === "open-meteo" ? "live" : rain.source === "scenario_slider" ? "slider" : "cache")
      setScenarioActive(false)
      setSourceState("LIVE")
      setRetrievedAt(rain.retrieved_at ?? new Date().toISOString())
      window.dispatchEvent(new CustomEvent(QUEUE_REFRESH, { detail: { precip_mm: rain.precip_mm } }))
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.rain.liveFail)
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
      setMode("slider")
      setScenarioActive(true)
      setSourceState("SCENARIO")
      setRetrievedAt(null)
      window.dispatchEvent(new CustomEvent(QUEUE_REFRESH, { detail: { precip_mm: rain.precip_mm } }))
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.rain.scenarioFail)
    } finally {
      setBusy(false)
    }
  }

  async function clearScenario() {
    setBusy(true)
    setError(null)
    try {
      const rain = await postClearScenario()
      const mm = typeof rain.precip_mm === "number" ? rain.precip_mm : null
      if (mm != null) setPrecip(mm)
      await refreshMode()
      window.dispatchEvent(
        new CustomEvent(QUEUE_REFRESH, { detail: { precip_mm: mm ?? undefined } }),
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.rain.clearFail)
    } finally {
      setBusy(false)
    }
  }

  useEffect(() => {
    const id = window.setInterval(() => {
      if (document.visibilityState !== "visible") return
      if (modeRef.current === "slider" || modeRef.current === "replay") return
      void refreshLive()
    }, POLL_MS)
    return () => window.clearInterval(id)
  }, [])

  return {
    precip,
    setPrecip,
    mode,
    setMode,
    sourceState,
    scenarioActive,
    retrievedAt,
    busy,
    error,
    apply,
    clearScenario,
    refreshLive,
    refreshMode,
  }
}
