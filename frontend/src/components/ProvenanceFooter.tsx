import type { PointDetail } from "../api/client"

export function ProvenanceFooter({ point }: { point: PointDetail }) {
  const provenance = point.provenance
  if (!provenance) return null
  return (
    <p className="muted" data-testid="provenance">
      {provenance.source} · {provenance.retrieved_at} · synthetic {String(provenance.is_synthetic)} · derived{" "}
      {String(provenance.is_derived)}
    </p>
  )
}
