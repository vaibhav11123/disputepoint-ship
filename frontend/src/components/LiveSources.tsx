import { useEffect, useState } from "react"
import { getHealth, postEvidenceRefresh, type HealthInfo } from "../api/client"

export function LiveSources() {
  const [health, setHealth] = useState<HealthInfo | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function load() {
    try {
      setHealth(await getHealth())
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Health failed.")
    }
  }

  useEffect(() => {
    void load()
  }, [])

  async function refreshEvidence() {
    setBusy(true)
    setError(null)
    try {
      await postEvidenceRefresh()
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Evidence refresh failed.")
    } finally {
      setBusy(false)
    }
  }

  if (!health) {
    return error ? <span className="error" role="alert">{error}</span> : <span className="muted live-sources">Sources…</span>
  }

  const verified = health.evidence_live_ok ?? 0
  const failed = health.evidence_live_fail ?? 0
  const skipped = health.evidence_live_skipped ?? 0
  const total = verified + failed + skipped
  const rainBit = health.rain_mode === "live" ? "Open-Meteo" : health.rain_mode === "slider" ? "Slider rain" : "Rain cache"
  const geoBit = health.geo_fill === "nominatim" ? "Nominatim" : "Geo fixture"
  const evidenceBit = health.live_fetch
    ? `Evidence ${verified}/${total || "—"} live`
    : "Evidence fixture"
  return (
    <div className="live-sources" data-testid="live-sources">
      <span className={health.live_fetch ? "chip ok" : "chip"}>
        {health.live_fetch ? "Live fetch" : "Dry"}
      </span>
      <span className="muted">
        {rainBit} · {geoBit} · {evidenceBit} · OSM · Volunteer ≠ SCADA
      </span>
      {health.live_fetch ? (
        <button type="button" disabled={busy} aria-busy={busy} onClick={() => void refreshEvidence()}>
          Refresh evidence
        </button>
      ) : null}
      {error ? <span className="error" role="alert">{error}</span> : null}
    </div>
  )
}
