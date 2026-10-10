import type { PointDetail } from "../api/client"
import { copy } from "../lib/copy"

export function ProvenanceFooter({ point }: { point: PointDetail }) {
  const provenance = point.provenance
  if (!provenance) return null
  const hasOsm = Boolean(point.lat != null && point.lon != null && (point.geo_licence || point.geo_source === "nominatim"))
  return (
    <div data-testid="provenance">
      <p className="muted">
        {provenance.source} · {provenance.retrieved_at} · synthetic {String(provenance.is_synthetic)} · derived{" "}
        {String(provenance.is_derived)}
      </p>
      {point.lat != null && point.lon != null ? (
        <p className="mono muted">
          {point.lat.toFixed(5)}, {point.lon.toFixed(5)}
        </p>
      ) : null}
      {hasOsm ? <p className="muted">{copy.provenance.osmData}</p> : null}
    </div>
  )
}
