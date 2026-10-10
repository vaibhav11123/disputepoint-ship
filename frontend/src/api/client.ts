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
  source_date?: string | null
  title?: string | null
  publisher?: string | null
  establishes?: string | null
  does_not_establish?: string | null
  is_synthetic?: boolean
  agency?: string | null
}

export type SourceHealth = {
  source_id: string
  source_name: string
  access_status: string
  source_state: "LIVE" | "STALE" | "UNAVAILABLE" | "UNKNOWN" | "SCENARIO" | string
  observation_time?: string | null
  retrieved_at?: string | null
  last_attempt_at?: string | null
  last_success_at?: string | null
  units?: string | null
  freshness_limit_seconds?: number | null
  last_error_category?: string | null
  allowed_effects?: string[]
  value?: unknown
  location_or_station_id?: string | null
  retrieval_ok?: boolean | null
}

export type EvidenceCounts = {
  stored: number
  verified: number
  unavailable: number
  verification_failed: number
  not_reverified: number
  volunteer: number
}

export type HealthInfo = {
  ok: boolean
  rain_mode: string
  precip_mm?: number | null
  rain_retrieved_at?: string | null
  rain_observation_time?: string | null
  rain_source_state?: string | null
  rain_station?: string | null
  rain_period_start?: string | null
  rain_period_end?: string | null
  rain_window_hours?: number | null
  rain_priority_uses?: boolean | null
  scenario_active?: boolean
  replay_active?: boolean
  replay_id?: string | null
  replay_clock?: string | null
  replay_activated_point_ids?: string[]
  has_last_live?: boolean
  live_fetch?: boolean
  geo_fill?: string
  evidence_live_ok?: number
  evidence_live_fail?: number
  evidence_live_skipped?: number
  evidence_counts?: EvidenceCounts
  sources?: SourceHealth[]
}

export type ReplayStation = {
  station: string
  precip_mm: number
  period_start?: string
  period_end?: string
  affects_priority?: boolean
  source_url?: string
}

export type ReplayState = {
  replay_id: string
  label?: string
  disclaimer?: string
  mode: string
  clock: string | null
  precip_mm: number | null
  priority_station?: string
  priority_rule?: string
  stations: ReplayStation[]
  activated_point_ids: string[]
  milestones?: string[]
  gaps?: { points_without_day_evidence?: string[] }
  ownership_unchanged?: boolean
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
  incident_summary?: string
  claim_summaries?: Record<string, string>
}

export const QUEUE_REFRESH = "dp-queue-refresh"
export const SELECT_POINT = "dp-select-point"

/** Empty locally (Vite proxy). Ship It sets VITE_API_URL to the API Gateway origin. */
const API_BASE = String(import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "")

function apiUrl(path: string): string {
  if (!API_BASE) return path
  return `${API_BASE}${path.startsWith("/") ? path : `/${path}`}`
}

async function read<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(apiUrl(path), {
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
  return read<{
    source: string
    precip_mm: number | null
    is_synthetic?: boolean
    retrieved_at?: string
    display_unchanged?: boolean
    last_live_updated?: boolean
  }>("/rain/refresh", {
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
  return read<{ source: string; precip_mm: number; is_synthetic: boolean; last_live?: Record<string, unknown> }>(
    "/rain/scenario",
    {
      method: "POST",
      body: JSON.stringify({ precip_mm: precipMm }),
    },
  )
}

export function postClearScenario() {
  return read<{
    cleared?: boolean
    precip_mm?: number | null
    source?: string | null
    is_synthetic?: boolean
    last_live?: Record<string, unknown>
  }>("/rain/clear-scenario", {
    method: "POST",
    body: "{}",
  })
}

const REPLAY_ID = "delhi-2025-07-29"

export function getReplay(replayId = REPLAY_ID) {
  return read<ReplayState & { steps?: unknown[]; milestones: string[] }>(`/replays/${replayId}`)
}

export function seekReplay(body: { t?: string | null; step_index?: number | null }, replayId = REPLAY_ID) {
  return read<ReplayState>(`/replays/${replayId}/seek`, {
    method: "POST",
    body: JSON.stringify(body),
  })
}

export function exitReplay(replayId = REPLAY_ID) {
  return read<{ ok: boolean; mode: string }>(`/replays/${replayId}/exit`, {
    method: "POST",
    body: "{}",
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
