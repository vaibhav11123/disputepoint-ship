import { copy } from "../lib/copy"
import { osmBrowseUrl } from "../lib/placeCoords"
import { AgencyBlock } from "./StateChip"

export function PlaceStrip({
  name,
  lat,
  lon,
  agenciesClaimed,
  coordSource,
}: {
  name: string
  lat: number | null
  lon: number | null
  agenciesClaimed: string[]
  coordSource?: "fixture" | "climax_fallback" | null
}) {
  const hasCoords = typeof lat === "number" && typeof lon === "number"

  return (
    <aside className="place-strip place-caption-bar" data-testid="place-strip" aria-label={copy.place.aria}>
      <div className="place-caption-main">
        <p className="place-strip-name">{name}</p>
        {hasCoords ? (
          <p className="mono place-coords" data-testid="place-coords">
            {lat.toFixed(5)}, {lon.toFixed(5)}
            {coordSource === "climax_fallback" ? (
              <span className="muted"> · {copy.map.scenarioLocation}</span>
            ) : null}
          </p>
        ) : (
          <p className="muted">{copy.place.unverified}</p>
        )}
      </div>
      <div className="place-caption-meta">
        {agenciesClaimed.length > 0 ? (
          <span className="claimed-row">
            <AgencyBlock agency={null} claimed={agenciesClaimed} />
          </span>
        ) : null}
        {hasCoords ? (
          <a className="place-osm" href={osmBrowseUrl(lat, lon)} target="_blank" rel="noreferrer">
            {copy.place.osm}
          </a>
        ) : null}
      </div>
      <p className="muted place-caption">{copy.place.caption}</p>
      <p className="muted place-caption">{copy.place.jurisdictionNote}</p>
    </aside>
  )
}
