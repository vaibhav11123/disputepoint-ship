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
import { TopBar } from "./components/TopBar"
import { triageSummary } from "./components/TriageChip"
import {
  isJudgesMode,
  MAP_EXPAND_EVENT,
  pickColdOpenId,
  pickConflictFocusId,
  presentQueueForDemo,
  RAIN_STRIKE_EVENT,
} from "./lib/demoMode"
import { incidentIdFromRoute, navigate, useRoute } from "./lib/router"
import { AuditScreen } from "./screens/AuditScreen"
import { CommandScreen } from "./screens/CommandScreen"
import { CoordinationScreen } from "./screens/CoordinationScreen"
import { DemoScreen } from "./screens/DemoScreen"
import { EvidenceScreen } from "./screens/EvidenceScreen"
import { IncidentScreen } from "./screens/IncidentScreen"

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
  const route = useRoute()
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
  const flipRects = useRef<Map<string, DOMRect>>(new Map())

  const routePointId = incidentIdFromRoute(route)

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

  function openIncident(id: string) {
    setSelectedId(id)
    navigate({ name: "incident", id })
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
      } catch {
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
    if (routePointId) setSelectedId(routePointId)
  }, [routePointId])

  useEffect(() => {
    const id = routePointId ?? selectedId
    if (!id || route.name === "command" || route.name === "demo") {
      if (route.name === "command" || route.name === "demo") setDetail(null)
      return
    }
    let cancelled = false
    getPoint(id)
      .then((point) => {
        if (!cancelled) setDetail(point)
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Point failed to load.")
      })
    return () => {
      cancelled = true
    }
  }, [routePointId, selectedId, rows, detailTick, route.name])

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape" && route.name !== "command" && route.name !== "demo") {
        navigate({ name: "command" })
      }
    }
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [route.name])

  useEffect(() => {
    function captureFlip() {
      const map = new Map<string, DOMRect>()
      document.querySelectorAll<HTMLElement>("[data-point-id]").forEach((el) => {
        const id = el.dataset.pointId
        if (id) map.set(id, el.getBoundingClientRect())
      })
      flipRects.current = map
    }

    function playFlip() {
      const prev = flipRects.current
      if (prev.size === 0) return
      document.querySelectorAll<HTMLElement>("[data-point-id]").forEach((el) => {
        const id = el.dataset.pointId
        if (!id) return
        const first = prev.get(id)
        if (!first) return
        const last = el.getBoundingClientRect()
        const dy = first.top - last.top
        if (Math.abs(dy) < 1) return
        el.animate([{ transform: `translateY(${dy}px)` }, { transform: "translateY(0)" }], {
          duration: 320,
          easing: "cubic-bezier(0.2, 0.8, 0.2, 1)",
        })
      })
      flipRects.current = new Map()
    }

    function onRefresh(event: Event) {
      captureFlip()
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
          requestAnimationFrame(() => requestAnimationFrame(playFlip))
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
      if (id) openIncident(id)
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

  const summary = displayRows ? triageSummary(displayRows) : null
  const showOpsChrome = route.name !== "demo"

  return (
    <div className={judges ? "app judges" : "app demo"}>
      <a className="skip" href="#queue">
        Skip to queue
      </a>
      {showOpsChrome ? (
        <TopBar
          hideSynthetic={hideSynthetic}
          onToggleSynthetic={() => setHideSynthetic((value) => !value)}
          pulse={pulse}
          precipMm={precipMm}
          rainMode={precipMm > 5 ? "DEMO" : "IDLE"}
          counts={
            summary
              ? {
                  active: displayRows?.length ?? 0,
                  high: displayRows?.filter((r) => r.priority_rank <= 5).length ?? 0,
                  disputed: summary.disputed,
                  awaiting: summary.awaiting + summary.adjudicate,
                }
              : undefined
          }
        />
      ) : null}
      <div className={route.name === "command" ? "workspace command-only" : "workspace multipage"}>
        {route.name === "command" ? (
          <CommandScreen
            rows={displayRows}
            error={error}
            selectedId={selectedId}
            flashed={flashed}
            rainActive={rainActive}
            mapForceOpen={mapForceOpen}
            onSelect={openIncident}
          />
        ) : null}
        {route.name === "demo" ? (
          <DemoScreen
            rows={displayRows}
            selectedId={selectedId}
            rainActive={rainActive}
            onSelect={openIncident}
          />
        ) : null}
        {detail && route.name === "incident" ? (
          <IncidentScreen point={detail} route={route} hideSynthetic={hideSynthetic} judges={judges} />
        ) : null}
        {detail && route.name === "evidence" ? <EvidenceScreen point={detail} route={route} /> : null}
        {detail && route.name === "coordination" ? <CoordinationScreen point={detail} route={route} /> : null}
        {detail && route.name === "audit" ? <AuditScreen point={detail} route={route} /> : null}
        {routePointId && !detail && !error ? <p className="muted pad">Loading incident…</p> : null}
      </div>
      {showOpsChrome ? (
        <footer className="footer">
          <span>Rain source verified · Ownership decisions require human confirmation</span>
          <a className="muted" href="/demo">
            Demo
          </a>
          {judges && EvalLink ? <EvalLink /> : null}
          {judges && CommandPalette ? <CommandPalette onSelect={openIncident} /> : null}
          {!judges ? (
            <a className="muted judges-link" href="/command?judges=1">
              Judges inspection
            </a>
          ) : null}
        </footer>
      ) : null}
    </div>
  )
}
