import { useEffect, useMemo, useRef, useState, type ComponentType } from "react"
import {
  getHealth,
  getPoint,
  listPoints,
  QUEUE_REFRESH,
  SELECT_POINT,
  type PointDetail,
  type PointRow,
} from "./api/client"
import { POINT_REFRESH } from "./components/ActionBlock"
import { TopBar } from "./components/TopBar"
import { triageSummary } from "./components/TriageChip"
import { copy } from "./lib/copy"
import {
  isJudgesMode,
  MAP_EXPAND_EVENT,
  pickColdOpenId,
  pickConflictFocusId,
  presentReplayQueue,
  RAIN_STRIKE_EVENT,
} from "./lib/demoMode"
import { periodHoursBetween, rainAvailabilityLabel } from "./lib/rainStatus"
import { incidentIdFromRoute, navigate, useRoute } from "./lib/router"
import { AuditScreen } from "./screens/AuditScreen"
import { CommandScreen } from "./screens/CommandScreen"
import { CoordinationScreen } from "./screens/CoordinationScreen"
import { DemoScreen } from "./screens/DemoScreen"
import { EvidenceScreen } from "./screens/EvidenceScreen"
import { IncidentScreen } from "./screens/IncidentScreen"

type PaletteProps = { onSelect: (id: string) => void }

const paletteMods = import.meta.glob("./components/CommandPalette.tsx", { eager: true }) as Record<
  string,
  { CommandPalette?: ComponentType<PaletteProps> }
>
const CommandPalette = Object.values(paletteMods)[0]?.CommandPalette

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
  const [rainMode, setRainMode] = useState("none")
  const [rainSourceState, setRainSourceState] = useState<string | null>(null)
  const [scenarioActive, setScenarioActive] = useState(false)
  const [replayActive, setReplayActive] = useState(false)
  const [rainStation, setRainStation] = useState<string | null>(null)
  const [rainPeriodStart, setRainPeriodStart] = useState<string | null>(null)
  const [rainPeriodEnd, setRainPeriodEnd] = useState<string | null>(null)
  const [rainPriorityUses, setRainPriorityUses] = useState<boolean | null>(null)
  const [replayActivatedIds, setReplayActivatedIds] = useState<string[]>([])
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

  async function syncHealth() {
    const health = await getHealth()
    setRainMode(health.rain_mode)
    setRainSourceState(health.rain_source_state ?? null)
    setScenarioActive(Boolean(health.scenario_active))
    const active = Boolean(health.replay_active)
    setReplayActive(active)
    setReplayActivatedIds(active ? listOrEmpty(health.replay_activated_point_ids) : [])
    setRainStation(health.rain_station ?? null)
    setRainPeriodStart(health.rain_period_start ?? null)
    setRainPeriodEnd(health.rain_period_end ?? null)
    setRainPriorityUses(
      typeof health.rain_priority_uses === "boolean" ? health.rain_priority_uses : null,
    )
    if (health.precip_mm == null) setPrecipMm(0)
    else if (typeof health.precip_mm === "number") setPrecipMm(health.precip_mm)
    return health
  }

  function listOrEmpty(ids: string[] | undefined): string[] {
    return Array.isArray(ids) ? ids : []
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
        await syncHealth()
        if (cancelled) return
        await loadQueue(null, true)
      } catch {
        if (cancelled) return
        try {
          await loadQueue(null, true)
        } catch (inner: unknown) {
          setError(inner instanceof Error ? inner.message : copy.chrome.queueFail)
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
        if (!cancelled) setError(err instanceof Error ? err.message : copy.chrome.pointFail)
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
      void syncHealth().catch(() => undefined)
      const previous = new Map((rows ?? []).map((row) => [row.id, row.priority_rank]))
      const focusAfterStrike = pendingStrikeFocus.current
      pendingStrikeFocus.current = false
      loadQueue(focusAfterStrike ? null : selectedId)
        .then((items) => {
          const demoMm = typeof detailPrecip === "number" ? detailPrecip : precipMm
          const wet = demoMm > 5
          // API priority_rank only — no demo re-sort that invents rain reorder.
          const moved = new Set(
            items.filter((row) => previous.get(row.id) !== row.priority_rank).map((row) => row.id),
          )
          setFlashed(moved)
          setPulse(true)
          setRainActive(wet || focusAfterStrike)
          if (focusAfterStrike) {
            const conflictId = pickConflictFocusId(items)
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
        .catch((err: unknown) => setError(err instanceof Error ? err.message : copy.chrome.queueFail))
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

  const replayView = useMemo(() => {
    if (!rows || !replayActive || route.name !== "demo") return null
    return presentReplayQueue(rows, replayActivatedIds)
  }, [rows, replayActive, route.name, replayActivatedIds])

  const displayRows = useMemo(() => {
    if (!rows) return null
    if (replayView) return replayView.active
    // Engine order only (fixtures curated for board mix). No demo rank rewrite.
    return rows
  }, [rows, replayView])

  const undocumentedReplayCount = replayView?.undocumentedCount ?? 0

  const summary = displayRows ? triageSummary(displayRows) : null
  const showOpsChrome = route.name !== "demo"
  const footerLabel = rainAvailabilityLabel({
    scenarioActive,
    replayActive,
    rainSourceState,
    rainMode,
    precipMm,
  })

  return (
    <div className={judges ? "app judges" : "app demo"}>
      <a className="skip" href="#queue">
        {copy.chrome.skip}
      </a>
      {showOpsChrome ? (
        <TopBar
          hideSynthetic={hideSynthetic}
          onToggleSynthetic={() => setHideSynthetic((value) => !value)}
          pulse={pulse}
          precipMm={precipMm}
          rainMode={rainMode}
          rainSourceState={rainSourceState}
          scenarioActive={scenarioActive}
          replayActive={replayActive}
          rainStation={rainStation}
          rainPeriodStart={rainPeriodStart}
          rainPeriodEnd={rainPeriodEnd}
          rainPriorityUses={rainPriorityUses}
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
            rainActive={rainActive || replayActive}
            onSelect={openIncident}
            onHighlight={(id) => setSelectedId(id)}
            undocumentedCount={undocumentedReplayCount}
          />
        ) : null}
        {detail && route.name === "incident" ? (
          <IncidentScreen point={detail} route={route} hideSynthetic={hideSynthetic} judges={judges} />
        ) : null}
        {detail && route.name === "evidence" ? <EvidenceScreen point={detail} route={route} /> : null}
        {detail && route.name === "coordination" ? <CoordinationScreen point={detail} route={route} /> : null}
        {detail && route.name === "audit" ? <AuditScreen point={detail} route={route} /> : null}
        {routePointId && !detail && !error ? <p className="muted pad">{copy.chrome.loadingIncident}</p> : null}
      </div>
      {showOpsChrome ? (
        <footer className="footer">
          <span className="muted" data-testid="footer-rain-status">
            {replayActive
              ? copy.rain.replayLine(precipMm, {
                  station: rainStation || "Safdarjung",
                  periodHours: periodHoursBetween(rainPeriodStart, rainPeriodEnd),
                })
              : scenarioActive
                ? copy.rain.scenarioLine(precipMm)
                : footerLabel}
          </span>
          <a className="muted" href="/demo">
            {copy.chrome.footerDemo}
          </a>
          {judges ? (
            <a className="muted" href="/aws-arch.html">
              {copy.chrome.footerArchitecture}
            </a>
          ) : null}
          {judges && CommandPalette ? <CommandPalette onSelect={openIncident} /> : null}
        </footer>
      ) : null}
    </div>
  )
}
