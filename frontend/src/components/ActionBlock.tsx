import { useEffect, useMemo, useState } from "react"
import {
  postConfirm,
  postEscalate,
  QUEUE_REFRESH,
  type PointDetail,
} from "../api/client"
import { copy } from "../lib/copy"
import { evidenceChip } from "../lib/evidenceStatus"
import { ESCALATE_REASONS, type ActorRole } from "../lib/lifecycle"
import { navigate } from "../lib/router"

const AGENCIES = ["MCD", "PWD", "NDMC", "DJB", "PWD_FLOOD", "NHAI", "DMRC", "OTHER"]
export const POINT_REFRESH = "dp-point-refresh"

function evidenceTitle(ev: { id: string; type: string; quote: string; live_status?: string; live_verified?: boolean }) {
  const type = ev.type?.replace(/_/g, " ") || "Evidence"
  const snippet = (ev.quote || "").trim()
  const short = snippet.length > 72 ? `${snippet.slice(0, 72)}…` : snippet
  return short ? `${type}: ${short}` : `${type} (${ev.id})`
}

function evidenceStatus(ev: {
  channel?: string | null
  live_verified?: boolean
  live_status?: string
}) {
  return evidenceChip(ev)
}

export function ActionBlock({
  point,
  actorRole = "INCIDENT_COMMANDER",
}: {
  point: PointDetail
  actorRole?: ActorRole
}) {
  const reviewer = copy.hitl.reviewerSilent
  const [agency, setAgency] = useState("")
  const [escalateReason, setEscalateReason] = useState("")
  const [confirmReason, setConfirmReason] = useState("")
  const [selectedEvidence, setSelectedEvidence] = useState<string[]>([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const conflict = point.ownership_state === "CONFLICT"
  const isIc = actorRole === "INCIDENT_COMMANDER"
  const escalated =
    Boolean(point.escalated) ||
    Boolean(point.escalate_reason) ||
    (point.audit ?? []).some((a) => a.action === "ESCALATE")
  const evidence = useMemo(() => point.evidence ?? [], [point.evidence])
  const evidenceIds = useMemo(() => evidence.map((e) => e.id), [evidence])

  useEffect(() => {
    if (conflict && escalateReason.trim().length === 0) {
      setEscalateReason(copy.hitl.conflictPreset)
    }
  }, [point.id, conflict, escalateReason])

  const missing: string[] = []
  if (!isIc) missing.push(copy.hitl.icOnly)
  if (!agency) missing.push(copy.hitl.agency)
  if (confirmReason.trim().length === 0) missing.push(copy.hitl.rationale)
  if (selectedEvidence.length === 0) missing.push(copy.hitl.evidenceReviewed)

  const canConfirm = missing.length === 0 && !busy

  async function run(work: () => Promise<unknown>, after?: "audit") {
    setBusy(true)
    setError(null)
    try {
      await work()
      window.dispatchEvent(new Event(QUEUE_REFRESH))
      window.dispatchEvent(new CustomEvent(POINT_REFRESH, { detail: point.id }))
      if (after === "audit") navigate({ name: "audit", id: point.id })
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.hitl.fail)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="actions-region hitl-block" aria-busy={busy} data-testid="hitl-actions">
      <h3 className="dp-section actions-region-title">{copy.hitl.title}</h3>

      <div className="actions-grid">
        <label className="field">
          <span className="dp-label">{copy.hitl.escalateReason}</span>
          <select
            aria-label={copy.hitl.escalateAria}
            value={escalateReason}
            onChange={(event) => setEscalateReason(event.target.value)}
          >
            <option value={copy.hitl.conflictPreset}>{copy.hitl.conflictPreset}</option>
            {ESCALATE_REASONS.map((reason) => (
              <option key={reason} value={reason}>
                {reason}
              </option>
            ))}
          </select>
        </label>
        <button
          type="button"
          className={conflict ? "primary-action escalate-cta" : undefined}
          data-testid="escalate-human-review"
          disabled={busy || escalateReason.trim().length === 0}
          onClick={() => run(() => postEscalate(point.id, escalateReason.trim(), reviewer, actorRole), "audit")}
        >
          {copy.hitl.escalate}
        </button>
      </div>

      {(escalated || conflict) && !point.officer_confirmed ? (
        <div className="human-decision" data-testid="human-decision">
          <h3 className="dp-section">{copy.hitl.decision}</h3>

          <div className="decision-step">
            <p className="dp-label">{copy.hitl.whyReview}</p>
            <p className="muted">{escalateReason || copy.hitl.conflictPreset}</p>
          </div>

          <div className="decision-step">
            <p className="dp-label">{copy.hitl.confirmLine}</p>
            <p className="muted">{copy.hitl.decisionSub}</p>
            <label className="field">
              <span className="dp-label">{copy.hitl.agency}</span>
              <select
                aria-label={copy.hitl.confirmAgencyAria}
                value={agency}
                onChange={(event) => setAgency(event.target.value)}
                disabled={!isIc}
              >
                <option value="">Select agency…</option>
                {AGENCIES.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </label>
            <label className="field">
              <span className="dp-label">{copy.hitl.rationale}</span>
              <input
                aria-label={copy.hitl.confirmReasonAria}
                value={confirmReason}
                disabled={!isIc}
                onChange={(event) => setConfirmReason(event.target.value)}
              />
            </label>
          </div>

          <fieldset className="evidence-check">
            <legend className="dp-label">{copy.hitl.evidenceReviewed}</legend>
            {evidenceIds.length === 0 ? (
              <p className="muted">{copy.hitl.noEvidence}</p>
            ) : (
              evidence.map((ev) => (
                <label key={ev.id} className="check">
                  <input
                    type="checkbox"
                    checked={selectedEvidence.includes(ev.id)}
                    disabled={!isIc}
                    onChange={(event) => {
                      setSelectedEvidence((prev) =>
                        event.target.checked ? [...prev, ev.id] : prev.filter((x) => x !== ev.id),
                      )
                    }}
                  />
                  <span>
                    <span className="evidence-title">{evidenceTitle(ev)}</span>
                    <span className="dp-meta"> · {evidenceStatus(ev)}</span>
                    <span className="visually-hidden">{ev.id}</span>
                  </span>
                </label>
              ))
            )}
          </fieldset>

          {!canConfirm && isIc ? (
            <p className="muted" data-testid="confirm-missing">
              {copy.hitl.missingRequirements} {missing.join(" · ")}
            </p>
          ) : null}

          <button
            type="button"
            className="primary-action escalate-cta"
            data-testid="confirm-decision"
            disabled={!canConfirm}
            title={isIc ? undefined : copy.hitl.disabledTitle}
            onClick={() =>
              run(
                () => postConfirm(point.id, agency, confirmReason.trim(), reviewer, selectedEvidence, actorRole),
                "audit",
              )
            }
          >
            {copy.hitl.confirm}
          </button>
          <p className="dp-meta">{copy.hitl.auditPromise}</p>
          {!isIc ? <p className="muted">{copy.hitl.disabled}</p> : null}
        </div>
      ) : null}

      {point.officer_confirmed && point.decision_record ? (
        <div data-testid="officer-confirmed-banner">
          <p className="chip ok">{copy.state.officerConfirmed}</p>
          <p className="muted">
            {copy.hitl.successAgency(
              String(point.decision_record.agency ?? point.responsible_agency),
              String(point.decision_record.auditId ?? ""),
            )}
          </p>
        </div>
      ) : null}

      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}
    </section>
  )
}
