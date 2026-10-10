import { copy } from "./copy"

const FETCH_FAIL = new Set(["fetch_failed", "fetch_forbidden", "fetch_rate_limited"])

/** Types that are not volunteer community reports — chip from type/status, not channel. */
const NON_VOLUNTEER_TYPES = new Set([
  "PRESS_REPORT",
  "COURT_ORDER",
  "GOV_ORDER",
  "AGENCY_CLAIM",
  "OFFICIAL_NOTICE",
])

function isSkipped(status: string | null | undefined): boolean {
  if (!status) return false
  return status.startsWith("skipped") || status === "skipped"
}

function isVolunteerCommunity(item: {
  type?: string | null
  channel?: string | null
}): boolean {
  if (item.channel !== "VOLUNTEER_REPORTED") return false
  const t = item.type ?? ""
  if (t && NON_VOLUNTEER_TYPES.has(t)) return false
  return true
}

/** Chip label from provenance / live_status — skipped must never look verified. */
export function evidenceChip(item: {
  type?: string | null
  channel?: string | null
  live_status?: string | null
  live_verified?: boolean
}): string {
  if (isVolunteerCommunity(item)) return copy.evidence.community
  const status = item.live_status
  if (isSkipped(status)) return copy.evidence.verificationSkipped
  if (status === "ok" && item.live_verified !== false) return copy.evidence.verified
  if (status === "quote_miss") return copy.evidence.verificationFailed
  if (status && FETCH_FAIL.has(status)) return copy.evidence.unavailable
  if (status == null || status === "") {
    if (item.type === "PRESS_REPORT") return copy.evidence.pressReport
    return copy.evidence.notReverified
  }
  return copy.evidence.stored
}

export function evidenceChipTone(item: {
  type?: string | null
  channel?: string | null
  live_status?: string | null
  live_verified?: boolean
}): "ok" | "warn" | "" {
  if (isVolunteerCommunity(item)) return "warn"
  const status = item.live_status
  if (isSkipped(status)) return "warn"
  if (status === "ok" && item.live_verified !== false) return "ok"
  if (status === "quote_miss" || (status && FETCH_FAIL.has(status))) return "warn"
  return ""
}
