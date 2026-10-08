import { useEffect, useMemo, useRef, useState } from "react"
import Map, { Marker, NavigationControl, type MapRef } from "react-map-gl/maplibre"
import "maplibre-gl/dist/maplibre-gl.css"
import type { PointRow } from "../api/client"
import { MAP_EXPAND_EVENT } from "../lib/demoMode"

const DELHI = { longitude: 77.21, latitude: 28.61, zoom: 11 }
const OSM_STYLE = {
  version: 8 as const,
  sources: {
    osm: {
      type: "raster" as const,
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "© OpenStreetMap contributors",
    },
  },
  layers: [{ id: "osm", type: "raster" as const, source: "osm" }],
}

function hasCoords(row: PointRow) {
  return typeof row.lat === "number" && typeof row.lon === "number"
}

export function MapHUD({
  rows,
  selectedId,
  onSelect,
  defaultOpen = false,
  rainActive = false,
  forceOpen = false,
}: {
  rows: PointRow[]
  selectedId: string | null
  onSelect: (id: string) => void
  defaultOpen?: boolean
  rainActive?: boolean
  forceOpen?: boolean
}) {
  const mapped = useMemo(() => rows.filter(hasCoords), [rows])
  const [open, setOpen] = useState(defaultOpen)
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
    if (!open || !selectedId) return
    const point = mapped.find((row) => row.id === selectedId)
    if (!point || point.lat == null || point.lon == null) return
    const map = mapRef.current
    if (!map) return
    const center = { center: [point.lon, point.lat] as [number, number], zoom: 13 }
    if (reduced) map.jumpTo(center)
    else map.flyTo({ ...center, duration: 700 })
  }, [selectedId, open, mapped, reduced])

  if (mapped.length === 0) return null

  return (
    <div className={rainActive ? "maphud rain-active" : "maphud"} data-testid="map-hud">
      <button type="button" className="maphud-toggle" aria-expanded={open} onClick={() => setOpen((value) => !value)}>
        {open ? "Hide map" : "Show map"} ({mapped.length} geocoded)
      </button>
      {open ? (
        <div className="maphud-frame" aria-label="OpenStreetMap context">
          {rainActive ? <div className="rain-veil" aria-hidden="true" /> : null}
          <Map ref={mapRef} initialViewState={DELHI} mapStyle={OSM_STYLE} style={{ width: "100%", height: 220 }} attributionControl>
            <NavigationControl position="top-right" showCompass={false} />
            {mapped.map((row) => (
              <Marker
                key={row.id}
                longitude={row.lon as number}
                latitude={row.lat as number}
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
            ))}
          </Map>
          <p className="muted maphud-credit">© OpenStreetMap contributors · ODbL</p>
        </div>
      ) : null}
    </div>
  )
}
