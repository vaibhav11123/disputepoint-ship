import { useState } from "react"
import { motion } from "motion/react"
import type { PointRow } from "../api/client"
import { HistoricalReplay } from "../components/HistoricalReplay"
import { MapHUD } from "../components/MapHUD"
import { Button } from "../components/ui/button"
import { copy } from "../lib/copy"
import { navigate } from "../lib/router"

export function DemoScreen({
  rows,
  selectedId,
  rainActive,
  onSelect,
  onHighlight,
  undocumentedCount = 0,
}: {
  rows: PointRow[] | null
  selectedId: string | null
  rainActive: boolean
  onSelect: (id: string) => void
  /** While historical replay is active: local highlight only (no navigation). */
  onHighlight?: (id: string) => void
  undocumentedCount?: number
}) {
  const [activated, setActivated] = useState<string[]>([])
  const [localHighlight, setLocalHighlight] = useState<string | null>(null)
  const replayLive = activated.length > 0 || rainActive
  const highlightId =
    localHighlight ?? activated[0] ?? selectedId ?? "dp-purana-quila"

  function pick(id: string) {
    if (replayLive && onHighlight) {
      setLocalHighlight(id)
      onHighlight(id)
      return
    }
    onSelect(id)
  }

  return (
    <section className="demo-screen" aria-label={copy.demo.region} data-testid="demo-screen">
      <motion.div
        className="demo-chapters"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.35 }}
      >
        <h1 className="demo-brand">{copy.brand.name}</h1>
        <p className="dp-label">{copy.demo.region}</p>
        <p className="demo-line">{copy.demo.headline}</p>
        <p className="muted">{copy.demo.sub}</p>
        <div className="demo-actions">
          <Button type="button" onClick={() => navigate({ name: "command" })}>
            {copy.demo.start}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate({ name: "incident", id: "dp-purana-quila" })}
          >
            {copy.demo.purana}
          </Button>
        </div>
        <p className="dp-label" style={{ marginTop: 16 }}>
          {copy.demo.historicalDay}
        </p>
        <HistoricalReplay
          onActivated={(ids) => {
            setActivated(ids)
            setLocalHighlight(ids[0] ?? null)
            if (ids[0] && onHighlight) onHighlight(ids[0])
          }}
        />
        {undocumentedCount > 0 ? (
          <p className="muted mono" data-testid="replay-undocumented">
            {copy.historicalReplay.undocumented(undocumentedCount)}
          </p>
        ) : null}
      </motion.div>
      {rows ? (
        <div className="demo-map">
          <MapHUD
            rows={rows}
            selectedId={highlightId}
            onSelect={pick}
            defaultOpen
            rainActive={rainActive || activated.length > 0}
            forceOpen
          />
        </div>
      ) : null}
    </section>
  )
}
