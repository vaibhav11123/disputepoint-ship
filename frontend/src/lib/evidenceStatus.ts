import { copy } from "./copy"

const FETCH_FAIL = new Set(["fetch_failed", "fetch_forbidden", "fetch_rate_limited"])

function isSkipped(status: string | null | undefined): boolean {
  if (!status) return false
  return status.startsWith("skipped") || status === "skipped"
}

/** Chip label from provenance / live_status — skipped must never look verified. */
export function evidenceChip(item: {
  channel?: string | null
  live_status?: string | null
  live_verified?: boolean
}): string {
  if (item.channel === "VOLUNTEER_REPORTED") return copy.evidence.community
  const status = item.live_status
  if (isSkipped(status)) return copy.evidence.verificationSkipped
  if (status === "ok" && item.live_verified !== false) return copy.evidence.verified
  if (status === "quote_miss") return copy.evidence.verificationFailed
  if (status && FETCH_FAIL.has(status)) return copy.evidence.unavailable
  if (status == null || status === "") return copy.evidence.notReverified
  return copy.evidence.stored
}

export function evidenceChipTone(item: {
  channel?: string | null
  live_status?: string | null
  live_verified?: boolean
}): "ok" | "warn" | "" {
  if (item.channel === "VOLUNTEER_REPORTED") return "warn"
  const status = item.live_status
  if (isSkipped(status)) return "warn"
  if (status === "ok" && item.live_verified !== false) return "ok"
  if (status === "quote_miss" || (status && FETCH_FAIL.has(status))) return "warn"
  return ""
}
