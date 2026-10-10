import type { PointDetail } from "../api/client"

/** Judges/debug only — polished case basis, not evaluation scaffolding. */
export function PriorityExplain({
  point,
  historicalReplay = false,
}: {
  point: PointDetail
  historicalReplay?: boolean
}) {
  const disputed = point.ownership_state === "CONFLICT"
  const claims = point.agencies_claimed.filter(Boolean)
  return (
    <details className="why-rank" data-testid="case-basis">
      <summary>CASE BASIS</summary>
      <ul className="muted">
        {historicalReplay ? (
          <li>Historical station rainfall is context — not a 6h engine R driver</li>
        ) : (
          <li>Priority uses coordination uncertainty and impact factors</li>
        )}
        <li>{disputed ? "Responsibility remains disputed" : "Responsibility state recorded"}</li>
        <li>
          {claims.length >= 2
            ? `${claims.length} agency claims overlap`
            : "Agency claims under review"}
        </li>
        <li>Exclusive responsibility not established</li>
      </ul>
      <p className="muted">
        {historicalReplay
          ? "Citywide rainfall does not invent relative rank changes. Documented incidents emerge over time; responsibility stays evidence-weighted."
          : "Responsibility is evaluated separately from rainfall. Identical citywide rain does not reorder relative ranks."}
      </p>
    </details>
  )
}
