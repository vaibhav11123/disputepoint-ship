export function ReadinessBlock({
  readiness,
  hideSynthetic,
}: {
  readiness?: { state?: string; is_synthetic?: boolean }
  hideSynthetic: boolean
}) {
  const synthetic = Boolean(readiness?.is_synthetic) && !hideSynthetic
  return (
    <p>
      <span className="muted">Readiness {readiness?.state ?? "UNKNOWN"}. </span>
      {readiness?.is_synthetic ? <span>Readiness: synthetic fixture (not live SCADA).</span> : null}{" "}
      {synthetic ? <span className="chip synthetic">SYNTHETIC</span> : null}
    </p>
  )
}
