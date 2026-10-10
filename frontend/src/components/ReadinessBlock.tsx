import { copy } from "../lib/copy"

export function ReadinessBlock({
  readiness,
  hideSynthetic,
}: {
  readiness?: { state?: string; is_synthetic?: boolean }
  hideSynthetic: boolean
}) {
  const synthetic = Boolean(readiness?.is_synthetic) && !hideSynthetic
  return (
    <p title={readiness?.is_synthetic ? copy.readiness.tooltip : undefined}>
      <span className="muted">{copy.readiness.caseStatus(readiness?.state ?? "UNKNOWN")}. </span>
      {readiness?.is_synthetic ? <span>{copy.readiness.scenarioData}</span> : null}{" "}
      {synthetic ? <span className="chip synthetic">{copy.readiness.chip}</span> : null}
    </p>
  )
}
