import type { PointRow } from "../api/client"
import { MapHUD } from "../components/MapHUD"
import { QueueTable } from "../components/QueueTable"
import { Button } from "../components/ui/button"
import { copy } from "../lib/copy"
import { pickConflictFocusId } from "../lib/demoMode"

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
  const awaitingRows =
    rows?.filter((r) => r.ownership_state === "CONFLICT" || Boolean((r as PointRow & { escalated?: boolean }).escalated)) ??
    []
  const firstDisputed = (rows && pickConflictFocusId(rows)) || awaitingRows[0]?.id || null
  const selected = rows?.find((r) => r.id === selectedId) ?? null

  return (
    <section className="command-screen" id="queue" aria-label={copy.command.region}>
      <header className="command-hero" data-testid="command-hero">
        <h2 className="dp-page-title">{copy.command.hero}</h2>
        <p className="muted">{copy.command.heroSub}</p>
      </header>
      {error ? (
        <p className="error" role="alert">
          {error.includes("Retry") ? error : copy.command.queueFailRetry}
        </p>
      ) : null}
      {rows === null && !error ? <p>{copy.command.loading}</p> : null}
      {awaitingRows.length > 0 && firstDisputed ? (
        <div className="awaiting-next-strip" data-testid="awaiting-next-strip">
          <span className="dp-status-label">{copy.command.awaitingStrip(awaitingRows.length)}</span>
          <Button type="button" size="sm" variant="outline" onClick={() => onSelect(firstDisputed)}>
            {copy.command.viewDisputes}
          </Button>
        </div>
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
              forceOpen={mapForceOpen || true}
              fillHeight
            />
            {selected ? (
              <div className="map-selected-summary" data-testid="map-selected-summary">
                <strong>{selected.name}</strong>
                <span className="muted">
                  {selected.ownership_state === "CONFLICT"
                    ? copy.state.responsibilityDisputed
                    : selected.responsible_agency ?? "Unresolved"}
                </span>
                <Button type="button" size="sm" variant="default" onClick={() => onSelect(selected.id)}>
                  Open
                </Button>
              </div>
            ) : null}
          </div>
        </div>
      ) : null}
    </section>
  )
}
