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
  return read<{ ok: boolean; rain_mode: string }>("/health")
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

export function postEscalate(id: string, reason: string, reviewer: string) {
  return read<AuditRow>(`/points/${id}/escalate`, {
    method: "POST",
    body: JSON.stringify({ reason, reviewer }),
  })
}
