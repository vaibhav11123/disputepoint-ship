import { copy } from "../lib/copy"

export function AdvisoryBanner({ uncertain }: { uncertain: boolean }) {
  return (
    <div className="banner" role="note">
      <strong>{copy.advisory.status}</strong>
      {uncertain ? (
        <span>
          {copy.advisory.unresolved} {copy.advisory.escalate}
        </span>
      ) : null}
    </div>
  )
}
