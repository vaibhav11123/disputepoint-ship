import { useEffect, useState, type ComponentType } from "react"
import { getPoint, listPoints, QUEUE_REFRESH, SELECT_POINT, type PointDetail, type PointRow } from "./api/client"
import { AdvisoryBanner } from "./components/AdvisoryBanner"
import { PointCard } from "./components/PointCard"
import { QueueTable } from "./components/QueueTable"
import { TopBar } from "./components/TopBar"

type PaletteProps = { onSelect: (id: string) => void }
type EvalProps = Record<string, never>

const paletteMods = import.meta.glob("./components/CommandPalette.tsx", { eager: true }) as Record<string, { CommandPalette?: ComponentType<PaletteProps> }>
const evalMods = import.meta.glob("./components/EvalLink.tsx", { eager: true }) as Record<string, { EvalLink?: ComponentType<EvalProps> }>
const CommandPalette = Object.values(paletteMods)[0]?.CommandPalette
const EvalLink = Object.values(evalMods)[0]?.EvalLink

export function App() {
  const [rows, setRows] = useState<PointRow[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [detail, setDetail] = useState<PointDetail | null>(null)
  const [hideSynthetic, setHideSynthetic] = useState(false)
  const [flashed, setFlashed] = useState<Set<string>>(new Set())
  const [pulse, setPulse] = useState(false)

  async function loadQueue(keepId?: string | null) {
    const listing = await listPoints()
    setRows(listing.items)
    setSelectedId((current) => keepId ?? current ?? listing.items[0]?.id ?? null)
    return listing.items
  }

  useEffect(() => {
    let cancelled = false
    loadQueue()
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Queue failed to load.")
      })
    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    if (!selectedId) return
    let cancelled = false
    getPoint(selectedId)
      .then((point) => {
        if (!cancelled) setDetail(point)
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Point failed to load.")
      })
    return () => {
      cancelled = true
    }
  }, [selectedId, rows])

  useEffect(() => {
    function onRefresh() {
      const previous = new Map((rows ?? []).map((row) => [row.id, row.priority_rank]))
      loadQueue(selectedId)
        .then((items) => {
          const moved = new Set(items.filter((row) => previous.get(row.id) !== row.priority_rank).map((row) => row.id))
          setFlashed(moved)
          setPulse(true)
          window.setTimeout(() => {
            setFlashed(new Set())
            setPulse(false)
          }, 200)
        })
        .catch((err: unknown) => setError(err instanceof Error ? err.message : "Queue failed to load."))
    }
    function onSelect(event: Event) {
      const id = (event as CustomEvent<string>).detail
      if (id) setSelectedId(id)
    }
    window.addEventListener(QUEUE_REFRESH, onRefresh)
    window.addEventListener(SELECT_POINT, onSelect)
    return () => {
      window.removeEventListener(QUEUE_REFRESH, onRefresh)
      window.removeEventListener(SELECT_POINT, onSelect)
    }
  }, [rows, selectedId])

  const uncertain = detail ? detail.ownership_state !== "ASSIGNED" : true

  return (
    <div className="app">
      <a className="skip" href="#queue">Skip to queue</a>
      <TopBar hideSynthetic={hideSynthetic} onToggleSynthetic={() => setHideSynthetic((value) => !value)} pulse={pulse} />
      <div className="workspace">
        <section className="queue" id="queue" aria-label="Disputed points queue">
          {error ? <p className="error" role="alert">{error}</p> : null}
          {rows === null && !error ? <p>Loading disputed points.</p> : null}
          {rows ? (
            <QueueTable rows={rows} selectedId={selectedId} flashed={flashed} onSelect={setSelectedId} />
          ) : null}
        </section>
        <section className="card" aria-label="Point card">
          <AdvisoryBanner uncertain={uncertain} />
          {detail ? <PointCard point={detail} hideSynthetic={hideSynthetic} /> : <p className="muted">Select a point.</p>}
        </section>
      </div>
      <footer className="footer">
        {EvalLink ? <EvalLink /> : <span>Judges report lands with the eval package.</span>}
        {CommandPalette ? <CommandPalette onSelect={setSelectedId} /> : null}
      </footer>
    </div>
  )
}
