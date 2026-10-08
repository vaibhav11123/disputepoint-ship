import { motion } from "motion/react"
import type { PointRow } from "../api/client"
import { MapHUD } from "../components/MapHUD"
import { navigate } from "../lib/router"
import { Button } from "../components/ui/button"

export function DemoScreen({
  rows,
  selectedId,
  rainActive,
  onSelect,
}: {
  rows: PointRow[] | null
  selectedId: string | null
  rainActive: boolean
  onSelect: (id: string) => void
}) {
  return (
    <section className="demo-screen" aria-label="Demo signature" data-testid="demo-screen">
      <motion.div
        className="demo-chapters"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.35 }}
      >
        <h1 className="demo-brand">DisputePoint</h1>
        <p className="demo-line">Signature interaction — rain reorder → disputed point → human confirm.</p>
        <div className="demo-actions">
          <Button type="button" onClick={() => navigate({ name: "command" })}>
            Enter command
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate({ name: "incident", id: "dp-purana-quila" })}
          >
            Open Purana climax
          </Button>
        </div>
      </motion.div>
      {rows ? (
        <div className="demo-map">
          <MapHUD
            rows={rows}
            selectedId={selectedId ?? "dp-purana-quila"}
            onSelect={onSelect}
            defaultOpen
            rainActive={rainActive}
            forceOpen
          />
        </div>
      ) : null}
    </section>
  )
}
