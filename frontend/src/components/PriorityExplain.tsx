import type { PointDetail } from "../api/client"

const LABELS: Record<string, string> = {
  zero_R: "Why now",
  resolve_U: "Why this agency",
  zero_Q: "Why this location",
  zero_G: "Readiness gap",
}

export function PriorityExplain({ point }: { point: PointDetail }) {
  const components = point.components ?? {}
  return (
    <details className="why-rank">
      <summary>Why this rank</summary>
      <div className="bars" aria-label="Priority components">
        {["R", "S", "C", "Q", "U", "G"].map((key) => {
          const value = components[key] ?? 0
          return (
            <div className="bar" key={key}>
              <span>{key}</span>
              <span className="track"><span className="fill" style={{ width: `${Math.round(value * 100)}%` }} /></span>
              <span>{value.toFixed(2)}</span>
            </div>
          )
        })}
      </div>
      <div className="chips">
        {(point.counterfactuals ?? []).map((row) => (
          <button type="button" key={row.factor} title={row.copy}>
            {LABELS[row.factor] ?? row.factor} {row.delta_pct > 0 ? "+" : ""}{row.delta_pct}%
          </button>
        ))}
      </div>
      {(point.explanation ?? []).some((line) => line.includes("coordination_uncertainty")) ? (
        <p className="muted">U is coordination uncertainty, not physical severity.</p>
      ) : null}
    </details>
  )
}
