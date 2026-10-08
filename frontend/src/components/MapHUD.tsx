import { useEffect, useMemo, useRef, useState } from "react"
import Map, { Marker, NavigationControl, type MapRef } from "react-map-gl/maplibre"
import "maplibre-gl/dist/maplibre-gl.css"
import type { PointRow } from "../api/client"
import { MAP_EXPAND_EVENT } from "../lib/demoMode"
import { DEMO_CHAPTERS, POSITRON_FALLBACK, POSITRON_STYLE, PURANA_QUILA } from "../lib/lifecycle"

const DELHI = { longitude: 77.21, latitude: 28.61, zoom: 11 }

function hasCoords(row: PointRow) {
  return typeof row.lat === "number" && typeof row.lon === "number"
}

function slowFlyTo(
  map: { flyTo: (o: Record<string, unknown>) => void; jumpTo: (o: Record<string, unknown>) => void },
  center: [number, number],
  zoom: number,
  reduced: boolean,
) {
  const base = { center, zoom, essential: true as const }
  if (reduced) {
    map.jumpTo(base)
    return
  }
  map.flyTo({ ...base, speed: 0.2, curve: 1, duration: 900 })
}

export function MapHUD({
  rows,
  selectedId,
  onSelect,
  defaultOpen = false,
  rainActive = false,
  forceOpen = false,
  chapterIndex = null,
}: {
  rows: PointRow[]
  selectedId: string | null
  onSelect: (id: string) => void
  defaultOpen?: boolean
  rainActive?: boolean
  forceOpen?: boolean
  /** Demo Signature Interaction chapter index into DEMO_CHAPTERS */
  chapterIndex?: number | null
}) {
  const mapped = useMemo(() => rows.filter(hasCoords), [rows])
  const [open, setOpen] = useState(defaultOpen)
  const [styleUrl, setStyleUrl] = useState(POSITRON_STYLE)
  const mapRef = useRef<MapRef>(null)
  const reduced = typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches

  useEffect(() => {
    if (forceOpen) setOpen(true)
  }, [forceOpen])

  useEffect(() => {
    function onExpand() {
      setOpen(true)
    }
    window.addEventListener(MAP_EXPAND_EVENT, onExpand)
    return () => window.removeEventListener(MAP_EXPAND_EVENT, onExpand)
  }, [])

  useEffect(() => {
    if (!open) return
    const map = mapRef.current
    if (!map) return
    if (chapterIndex != null && DEMO_CHAPTERS[chapterIndex]) {
      const ch = DEMO_CHAPTERS[chapterIndex]
      slowFlyTo(map, ch.center, ch.zoom, reduced)
      return
    }
    if (!selectedId) return
    const point = mapped.find((row) => row.id === selectedId)
    let lon = point?.lon
    let lat = point?.lat
    if (selectedId === PURANA_QUILA.id && (lon == null || lat == null)) {
      lon = PURANA_QUILA.lon
      lat = PURANA_QUILA.lat
    }
    if (lon == null || lat == null) return
    slowFlyTo(map, [lon, lat], 13, reduced)
  }, [selectedId, open, mapped, reduced, chapterIndex])

  if (mapped.length === 0) return null

  return (
    <div className={rainActive ? "maphud rain-active" : "maphud"} data-testid="map-hud">
      <button type="button" className="maphud-toggle" aria-expanded={open} onClick={() => setOpen((value) => !value)}>
        {open ? "Hide map" : "Show map"} ({mapped.length} geocoded)
      </button>
      {open ? (
        <div className="maphud-frame" aria-label="District map context">
          {rainActive ? <div className="rain-veil" aria-hidden="true" /> : null}
          <Map
            ref={mapRef}
            initialViewState={DELHI}
            mapStyle={styleUrl}
            style={{ width: "100%", height: 280 }}
            attributionControl
            onError={() => {
              if (styleUrl !== POSITRON_FALLBACK) setStyleUrl(POSITRON_FALLBACK)
            }}
          >
            <NavigationControl position="top-right" showCompass={false} />
            {mapped.map((row) => {
              const lon = row.id === PURANA_QUILA.id ? (row.lon ?? PURANA_QUILA.lon) : (row.lon as number)
              const lat = row.id === PURANA_QUILA.id ? (row.lat ?? PURANA_QUILA.lat) : (row.lat as number)
              return (
                <Marker
                  key={row.id}
                  longitude={lon}
                  latitude={lat}
                  anchor="bottom"
                  onClick={(event) => {
                    event.originalEvent.stopPropagation()
                    onSelect(row.id)
                  }}
                >
                  <button
                    type="button"
                    className={row.id === selectedId ? "map-pin selected" : "map-pin"}
                    aria-label={`Select ${row.name}`}
                    title={row.name}
                  />
                </Marker>
              )
            })}
          </Map>
          <p className="muted maphud-credit">
            Positron basemap · © OpenStreetMap / OpenFreeMap · DEMO climax {PURANA_QUILA.lat}, {PURANA_QUILA.lon}
          </p>
        </div>
      ) : null}
    </div>
  )
}
