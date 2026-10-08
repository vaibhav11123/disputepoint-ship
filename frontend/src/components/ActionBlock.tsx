import { useEffect, useMemo, useState } from "react"
import {
  postAck,
  postConfirm,
  postEscalate,
  postOverride,
  QUEUE_REFRESH,
  type PointDetail,
} from "../api/client"
import { ESCALATE_REASONS, type ActorRole } from "../lib/lifecycle"
import { navigate } from "../lib/router"

const AGENCIES = ["MCD", "PWD", "NDMC", "DJB", "PWD_FLOOD", "NHAI", "DMRC", "OTHER"]
export const POINT_REFRESH = "dp-point-refresh"

const CONFLICT_PRESET = "Competing agency claims; evidence does not establish exclusive responsibility"

export function ActionBlock({
  point,
  actorRole = "INCIDENT_COMMANDER",
}: {
  point: PointDetail
  actorRole?: ActorRole
}) {
  const [reviewer, setReviewer] = useState("cell-1")
  const [agency, setAgency] = useState("MCD")
  const [overrideReason, setOverrideReason] = useState("")
  const [escalateReason, setEscalateReason] = useState("")
  const [confirmReason, setConfirmReason] = useState("")
  const [selectedEvidence, setSelectedEvidence] = useState<string[]>([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const open = point.status === "OPEN"
  const ackEnabled = open && point.ownership_state === "ASSIGNED"
  const conflict = point.ownership_state === "CONFLICT"
  const isIc = actorRole === "INCIDENT_COMMANDER"
  const escalated = Boolean(point.escalated) || Boolean(point.escalate_reason) || (point.audit ?? []).some((a) => a.action === "ESCALATE")
  const evidenceIds = useMemo(() => (point.evidence ?? []).map((e) => e.id), [point.evidence])

  useEffect(() => {
    if (conflict && escalateReason.trim().length === 0) {
      setEscalateReason(CONFLICT_PRESET)
    }
  }, [point.id, conflict])

  useEffect(() => {
    if (evidenceIds.length && selectedEvidence.length === 0) {
      setSelectedEvidence(evidenceIds.slice(0, Math.min(2, evidenceIds.length)))
    }
  }, [point.id, evidenceIds])

  async function run(work: () => Promise<unknown>, after?: "audit") {
    setBusy(true)
    setError(null)
    try {
      await work()
      window.dispatchEvent(new Event(QUEUE_REFRESH))
      window.dispatchEvent(new CustomEvent(POINT_REFRESH, { detail: point.id }))
      if (after === "audit") navigate({ name: "audit", id: point.id })
    } catch (err) {
      setError(err instanceof Error ? err.message : "Action failed.")
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="actions hitl-block" aria-busy={busy} data-testid="hitl-actions">
      {conflict ? (
        <p className="muted hitl-hint">RESPONSIBILITY DISPUTED — escalate for human review; no auto-assign.</p>
      ) : null}
      <label className="field">
        Reviewer
        <input aria-label="Reviewer" value={reviewer} onChange={(event) => setReviewer(event.target.value)} />
      </label>
      <button type="button" disabled={!ackEnabled || busy || reviewer.length === 0} onClick={() => run(() => postAck(point.id, reviewer))}>
        ACK
      </button>
      <label className="field">
        Agency
        <select aria-label="Override agency" value={agency} onChange={(event) => setAgency(event.target.value)}>
          {AGENCIES.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </label>
      <label className="field">
        Override reason
        <input aria-label="Override reason" value={overrideReason} onChange={(event) => setOverrideReason(event.target.value)} />
      </label>
      <button
        type="button"
        disabled={!open || busy || !isIc || overrideReason.trim().length === 0 || reviewer.length === 0}
        title={isIc ? undefined : "Requires Incident Commander"}
        onClick={() => run(() => postOverride(point.id, agency, overrideReason.trim(), reviewer), "audit")}
      >
        OVERRIDE
      </button>
      <label className="field">
        Reason for human review
        <select
          aria-label="Escalate reason"
          value={escalateReason}
          onChange={(event) => setEscalateReason(event.target.value)}
        >
          <option value={CONFLICT_PRESET}>{CONFLICT_PRESET}</option>
          {ESCALATE_REASONS.map((reason) => (
            <option key={reason} value={reason}>
              {reason}
            </option>
          ))}
        </select>
      </label>
      <button
        type="button"
        className={conflict ? "primary-action" : undefined}
        data-testid="escalate-human-review"
        disabled={busy || escalateReason.trim().length === 0 || reviewer.length === 0}
        onClick={() => run(() => postEscalate(point.id, escalateReason.trim(), reviewer, actorRole), "audit")}
      >
        ESCALATE FOR HUMAN REVIEW
      </button>

      {(escalated || conflict) && !point.officer_confirmed ? (
        <section className="human-decision" data-testid="human-decision">
          <h3 className="section-h">HUMAN DECISION</h3>
          <p className="muted">Confirm operational responsibility (IC only).</p>
          <label className="field">
            Responsible agency
            <select aria-label="Confirm agency" value={agency} onChange={(event) => setAgency(event.target.value)} disabled={!isIc}>
              {AGENCIES.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </label>
          <label className="field">
            Reason
            <input
              aria-label="Confirm reason"
              value={confirmReason}
              disabled={!isIc}
              onChange={(event) => setConfirmReason(event.target.value)}
              placeholder="Jurisdiction record reviewed and confirmed"
            />
          </label>
          <fieldset className="evidence-check">
            <legend>Evidence reviewed</legend>
            {evidenceIds.length === 0 ? (
              <p className="muted">No evidence ids — confirm blocked.</p>
            ) : (
              evidenceIds.map((id) => (
                <label key={id} className="check">
                  <input
                    type="checkbox"
                    checked={selectedEvidence.includes(id)}
                    disabled={!isIc}
                    onChange={(event) => {
                      setSelectedEvidence((prev) =>
                        event.target.checked ? [...prev, id] : prev.filter((x) => x !== id),
                      )
                    }}
                  />
                  {id}
                </label>
              ))
            )}
          </fieldset>
          <button
            type="button"
            className="primary-action"
            data-testid="confirm-decision"
            disabled={
              busy ||
              !isIc ||
              confirmReason.trim().length === 0 ||
              selectedEvidence.length === 0 ||
              reviewer.length === 0
            }
            title={isIc ? undefined : "Requires Incident Commander"}
            onClick={() =>
              run(
                () => postConfirm(point.id, agency, confirmReason.trim(), reviewer, selectedEvidence, actorRole),
                "audit",
              )
            }
          >
            CONFIRM DECISION
          </button>
          {!isIc ? <p className="muted">Confirm disabled — requires Incident Commander.</p> : null}
        </section>
      ) : null}

      {point.officer_confirmed && point.decision_record ? (
        <p className="chip ok" data-testid="officer-confirmed-banner">
          OFFICER CONFIRMED · {String(point.decision_record.agency ?? point.responsible_agency)} ·{" "}
          {String(point.decision_record.auditId ?? "")}
        </p>
      ) : null}

      {error ? <p className="error" role="alert">{error}</p> : null}
    </div>
  )
}
