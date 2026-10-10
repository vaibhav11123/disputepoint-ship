import { useEffect, useRef, useState } from "react"
import Map, { Marker, NavigationControl, type MapRef } from "react-map-gl/maplibre"
import "maplibre-gl/dist/maplibre-gl.css"
import { copy } from "../lib/copy"
import { POSITRON_FALLBACK, POSITRON_STYLE } from "../lib/lifecycle"

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

export function PointFocusMap({
  lat,
  lon,
  name,
  height = 320,
  zoom = 15.5,
}: {
  lat: number | null
  lon: number | null
  name: string
  height?: number
  zoom?: number
}) {
  const [styleUrl, setStyleUrl] = useState(POSITRON_STYLE)
  const mapRef = useRef<MapRef>(null)
  const reduced = typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches
  const ready = typeof lat === "number" && typeof lon === "number"

  useEffect(() => {
    if (!ready) return
    const map = mapRef.current
    if (!map) return
    slowFlyTo(map, [lon, lat], zoom, reduced)
  }, [lat, lon, zoom, reduced, ready])

  if (!ready) {
    return (
      <div className="point-focus-map empty" data-testid="point-focus-map">
        <p className="muted">{copy.place.mapEmpty}</p>
      </div>
    )
  }

  return (
    <div className="point-focus-map" data-testid="point-focus-map" aria-label={copy.place.mapFocus(name)}>
      <div className="point-focus-frame" style={{ height }}>
        <Map
          ref={mapRef}
          initialViewState={{ longitude: lon, latitude: lat, zoom }}
          mapStyle={styleUrl}
          style={{ width: "100%", height: "100%" }}
          onError={() => {
            if (styleUrl !== POSITRON_FALLBACK) setStyleUrl(POSITRON_FALLBACK)
          }}
        >
          <NavigationControl position="top-right" showCompass={false} />
          <Marker longitude={lon} latitude={lat} anchor="bottom">
            <button type="button" className="map-pin selected" aria-label={name} title={name} />
          </Marker>
        </Map>
      </div>
      <p className="muted maphud-credit">{copy.place.credit}</p>
    </div>
  )
}
