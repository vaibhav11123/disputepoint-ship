import { useEffect, useMemo, useRef, useState, type ComponentType } from "react"
import {
  getHealth,
  getPoint,
  listPoints,
  postScenario,
  QUEUE_REFRESH,
  SELECT_POINT,
  type PointDetail,
  type PointRow,
} from "./api/client"
import { POINT_REFRESH } from "./components/ActionBlock"
import { AdvisoryBanner } from "./components/AdvisoryBanner"
import { MapHUD } from "./components/MapHUD"
import { PointCard } from "./components/PointCard"
import { QueueTable } from "./components/QueueTable"
import { triageSummary } from "./components/TriageChip"
import { TopBar } from "./components/TopBar"
import {
  isJudgesMode,
  MAP_EXPAND_EVENT,
  pickColdOpenId,
  pickConflictFocusId,
  presentQueueForDemo,
  RAIN_STRIKE_EVENT,
} from "./lib/demoMode"

type PaletteProps = { onSelect: (id: string) => void }
type EvalProps = Record<string, never>

const paletteMods = import.meta.glob("./components/CommandPalette.tsx", { eager: true }) as Record<
  string,
  { CommandPalette?: ComponentType<PaletteProps> }
>
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
  const [judges, setJudges] = useState(() => isJudgesMode())
  const [detailTick, setDetailTick] = useState(0)
  const [rainActive, setRainActive] = useState(false)
  const [precipMm, setPrecipMm] = useState(0)
  const [mapForceOpen, setMapForceOpen] = useState(false)
  const pendingStrikeFocus = useRef(false)

  async function loadQueue(keepId?: string | null, cold = false) {
    const listing = await listPoints()
    setRows(listing.items)
    setSelectedId((current) => {
      if (keepId) return keepId
      if (current) return current
      if (cold) return pickColdOpenId(listing.items)
      return listing.items[0]?.id ?? null
    })
    return listing.items
  }

  useEffect(() => {
    setJudges(isJudgesMode())
    let cancelled = false
    ;(async () => {
      try {
        const health = await getHealth()
        if (cancelled) return
        if (typeof health.precip_mm === "number" && health.precip_mm > 5) {
          await postScenario(0)
          if (!cancelled) setPrecipMm(0)
        } else if (typeof health.precip_mm === "number") {
          setPrecipMm(health.precip_mm)
        }
        if (cancelled) return
        await loadQueue(null, true)
      } catch (err: unknown) {
        if (cancelled) return
        try {
          await loadQueue(null, true)
        } catch (inner: unknown) {
          setError(inner instanceof Error ? inner.message : "Queue failed to load.")
        }
      }
    })()
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
  }, [selectedId, rows, detailTick])

  useEffect(() => {
    function onRefresh(event: Event) {
      const detailPrecip = (event as CustomEvent<{ precip_mm?: number }>).detail?.precip_mm
      if (typeof detailPrecip === "number") setPrecipMm(detailPrecip)
      const previous = new Map((rows ?? []).map((row) => [row.id, row.priority_rank]))
      const focusAfterStrike = pendingStrikeFocus.current
      pendingStrikeFocus.current = false
      loadQueue(focusAfterStrike ? null : selectedId)
        .then((items) => {
          const wet = typeof detailPrecip === "number" ? detailPrecip > 5 : precipMm > 5
          const presented = judges ? items : presentQueueForDemo(items, wet ? 42 : precipMm)
          const moved = new Set(
            presented.filter((row) => previous.get(row.id) !== row.priority_rank).map((row) => row.id),
          )
          setFlashed(moved)
          setPulse(true)
          setRainActive(wet || focusAfterStrike)
          if (focusAfterStrike) {
            const conflictId = pickConflictFocusId(presented)
            if (conflictId) setSelectedId(conflictId)
            setMapForceOpen(true)
            window.dispatchEvent(new Event(MAP_EXPAND_EVENT))
          }
          window.setTimeout(() => {
            setFlashed(new Set())
            setPulse(false)
          }, 450)
          window.setTimeout(() => setRainActive(false), 8000)
        })
        .catch((err: unknown) => setError(err instanceof Error ? err.message : "Queue failed to load."))
    }
    function onSelect(event: Event) {
      const id = (event as CustomEvent<string>).detail
      if (id) setSelectedId(id)
    }
    function onPointRefresh() {
      setDetailTick((n) => n + 1)
    }
    function onStrike() {
      pendingStrikeFocus.current = true
      setMapForceOpen(true)
      window.dispatchEvent(new Event(MAP_EXPAND_EVENT))
    }
    window.addEventListener(QUEUE_REFRESH, onRefresh)
    window.addEventListener(SELECT_POINT, onSelect)
    window.addEventListener(POINT_REFRESH, onPointRefresh)
    window.addEventListener(RAIN_STRIKE_EVENT, onStrike)
    return () => {
      window.removeEventListener(QUEUE_REFRESH, onRefresh)
      window.removeEventListener(SELECT_POINT, onSelect)
      window.removeEventListener(POINT_REFRESH, onPointRefresh)
      window.removeEventListener(RAIN_STRIKE_EVENT, onStrike)
    }
  }, [rows, selectedId, precipMm, judges])

  const displayRows = useMemo(() => {
    if (!rows) return null
    if (judges) return rows
    return presentQueueForDemo(rows, precipMm)
  }, [rows, precipMm, judges])

  const uncertain = detail ? detail.ownership_state !== "ASSIGNED" : true
  const summary = displayRows ? triageSummary(displayRows) : null

  return (
    <div className={judges ? "app judges" : "app demo"}>
      <a className="skip" href="#queue">
        Skip to queue
      </a>
      <TopBar hideSynthetic={hideSynthetic} onToggleSynthetic={() => setHideSynthetic((value) => !value)} pulse={pulse} />
      <div className="workspace">
        <section className="queue" id="queue" aria-label="Disputed points queue">
          {error ? (
            <p className="error" role="alert">
              {error}
            </p>
          ) : null}
          {rows === null && !error ? <p>Loading disputed points.</p> : null}
          {summary ? (
            <p className="triage-strip" data-testid="triage-summary">
              {summary.act} act · {summary.adjudicate} adjudicate · {summary.research} research
            </p>
          ) : null}
          {displayRows ? (
            <>
              <QueueTable rows={displayRows} selectedId={selectedId} flashed={flashed} onSelect={setSelectedId} />
              <MapHUD
                rows={displayRows}
                selectedId={selectedId}
                onSelect={setSelectedId}
                defaultOpen={false}
                rainActive={rainActive}
                forceOpen={mapForceOpen}
              />
            </>
          ) : null}
        </section>
        <section className="card" aria-label="Point card">
          <AdvisoryBanner uncertain={uncertain} />
          {detail ? <PointCard point={detail} hideSynthetic={hideSynthetic} judges={judges} /> : <p className="muted">Select a point.</p>}
        </section>
      </div>
      <footer className="footer">
        <span>Rain source verified · Ownership decisions require human confirmation</span>
        {judges && EvalLink ? <EvalLink /> : null}
        {judges && CommandPalette ? <CommandPalette onSelect={setSelectedId} /> : null}
        {!judges ? (
          <a className="muted judges-link" href="?judges=1">
            Judges inspection
          </a>
        ) : null}
      </footer>
    </div>
  )
}
