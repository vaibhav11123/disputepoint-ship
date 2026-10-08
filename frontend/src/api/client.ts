export type PointRow = {
  id: string
  name: string
  lat: number | null
  lon: number | null
  agencies_claimed: string[]
  ownership_confidence: number
  ownership_state: "ASSIGNED" | "CONFLICT" | "UNKNOWN" | string
  responsible_agency: string | null
  priority_score: number
  priority_rank: number
  rain_delta?: number | null
  status: string
  uncertainty_band?: string
  readiness?: { state?: string; is_synthetic?: boolean }
  recommended_action?: string
}

export type EvidenceItem = {
  id: string
  type: string
  quote: string
  url: string
  channel?: "VOLUNTEER_REPORTED" | "OFFICIAL" | string | null
  live_verified?: boolean
  live_status?: string
  retrieved_at?: string
}

export type HealthInfo = {
  ok: boolean
  rain_mode: string
  precip_mm?: number
  rain_retrieved_at?: string | null
  live_fetch?: boolean
  geo_fill?: string
  evidence_live_ok?: number
  evidence_live_fail?: number
  evidence_live_skipped?: number
}

export type AuditRow = {
  action: string
  reviewer: string
  timestamp: string
  previous_recommendation?: string | null
  final_decision?: Record<string, unknown>
}

export type PointDetail = PointRow & {
  components?: Record<string, number>
  explanation?: string[]
  counterfactuals?: { factor: string; delta_pct: number; copy: string }[]
  evidence?: EvidenceItem[]
  provenance?: {
    source: string
    retrieved_at: string
    is_synthetic: boolean
    is_derived: boolean
  }
  audit?: AuditRow[]
  advisory?: boolean
  recommended_agency?: string | null
  human_selected_agency?: string | null
  override_reason?: string
  escalate_reason?: string
  escalated?: boolean
  officer_confirmed?: boolean
  lifecycle_state?: string
  decision_record?: Record<string, unknown>
  geo_source?: string
  geo_licence?: string
}

export const QUEUE_REFRESH = "dp-queue-refresh"
export const SELECT_POINT = "dp-select-point"

async function read<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: { "content-type": "application/json", ...(init?.headers ?? {}) },
    ...init,
  })
  const body = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = (body as { detail?: { code?: string; message?: string }; code?: string; message?: string }).detail
    const code = detail?.code ?? (body as { code?: string }).code ?? "DP-ERROR"
    const message = detail?.message ?? (body as { message?: string }).message ?? response.statusText
    throw new Error(`${code}: ${message}`)
  }
  return body as T
}

export function listPoints() {
  return read<{ items: PointRow[] }>("/points")
}

export function getPoint(id: string) {
  return read<PointDetail>(`/points/${id}`)
}

export function getHealth() {
  return read<HealthInfo>("/health")
}

export function postRainRefresh() {
  return read<{ source: string; precip_mm: number; is_synthetic: boolean; retrieved_at?: string }>("/rain/refresh", {
    method: "POST",
    body: "{}",
  })
}

export function postEvidenceRefresh() {
  return read<{
    ok: boolean
    evidence_live_ok: number
    evidence_live_fail: number
    evidence_live_skipped: number
  }>("/evidence/refresh", {
    method: "POST",
    body: "{}",
  })
}

export function postScenario(precipMm: number) {
  return read<{ source: string; precip_mm: number; is_synthetic: boolean }>("/rain/scenario", {
    method: "POST",
    body: JSON.stringify({ precip_mm: precipMm }),
  })
}

export function postAck(id: string, reviewer: string) {
  return read<{ status: string }>(`/points/${id}/ack`, {
    method: "POST",
    body: JSON.stringify({ reviewer }),
  })
}

export function postOverride(id: string, agency: string, reason: string, reviewer: string) {
  return read<AuditRow>(`/points/${id}/override`, {
    method: "POST",
    body: JSON.stringify({ agency, reason, reviewer }),
  })
}

export function postEscalate(id: string, reason: string, reviewer: string, actorRole = "EOC_OPERATOR") {
  return read<AuditRow>(`/points/${id}/escalate`, {
    method: "POST",
    body: JSON.stringify({ reason, reviewer, actor_role: actorRole }),
  })
}

export function postConfirm(
  id: string,
  agency: string,
  reason: string,
  reviewer: string,
  evidenceIds: string[],
  actorRole = "INCIDENT_COMMANDER",
) {
  return read<{ action: string; decision: Record<string, unknown> }>(`/points/${id}/confirm`, {
    method: "POST",
    body: JSON.stringify({
      agency,
      reason,
      reviewer,
      evidence_ids: evidenceIds,
      actor_role: actorRole,
    }),
  })
}
