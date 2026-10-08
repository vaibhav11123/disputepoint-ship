import type { PointRow } from "../api/client"
import { MapHUD } from "../components/MapHUD"
import { QueueTable } from "../components/QueueTable"
import { triageSummary } from "../components/TriageChip"

export function CommandScreen({
  rows,
  error,
  selectedId,
  flashed,
  rainActive,
  mapForceOpen,
  onSelect,
}: {
  rows: PointRow[] | null
  error: string | null
  selectedId: string | null
  flashed: Set<string>
  rainActive: boolean
  mapForceOpen: boolean
  onSelect: (id: string) => void
}) {
  const summary = rows ? triageSummary(rows) : null

  return (
    <section className="command-screen" id="queue" aria-label="Disputed points queue">
      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}
      {rows === null && !error ? <p>Loading disputed points.</p> : null}
      {summary ? (
        <p className="triage-strip" data-testid="triage-summary">
          {summary.act} act · {summary.adjudicate} adjudicate · {summary.awaiting} awaiting you · {summary.research}{" "}
          research
        </p>
      ) : null}
      {rows ? (
        <div className="command-layout">
          <QueueTable rows={rows} selectedId={selectedId} flashed={flashed} onSelect={onSelect} />
          <div className="command-map-hero" data-testid="command-map-hero">
            <MapHUD
              rows={rows}
              selectedId={selectedId}
              onSelect={onSelect}
              defaultOpen
              rainActive={rainActive}
              forceOpen={mapForceOpen}
            />
          </div>
        </div>
      ) : null}
    </section>
  )
}
