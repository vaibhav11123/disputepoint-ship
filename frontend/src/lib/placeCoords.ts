import { PURANA_QUILA } from "./lifecycle"

/** Resolve display coords — Purana climax fallback only; never invent other pins. */
export function resolvePlaceCoords(point: {
  id: string
  lat: number | null
  lon: number | null
}): { lat: number; lon: number; source: "fixture" | "climax_fallback" } | null {
  if (typeof point.lat === "number" && typeof point.lon === "number") {
    return { lat: point.lat, lon: point.lon, source: "fixture" }
  }
  if (point.id === PURANA_QUILA.id) {
    return { lat: PURANA_QUILA.lat, lon: PURANA_QUILA.lon, source: "climax_fallback" }
  }
  return null
}

export function osmBrowseUrl(lat: number, lon: number) {
  return `https://www.openstreetmap.org/?mlat=${lat}&mlon=${lon}#map=17/${lat}/${lon}`
}
