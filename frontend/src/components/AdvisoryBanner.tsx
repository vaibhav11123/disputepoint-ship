export function AdvisoryBanner({ uncertain }: { uncertain: boolean }) {
  return (
    <div className="banner" role="note">
      <strong>Advisory only — not an official agency assignment.</strong>
      {uncertain ? <span>Ownership uncertain — escalate to coordination cell.</span> : null}
    </div>
  )
}
