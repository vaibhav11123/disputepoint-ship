import type { PointRow } from "../api/client"

/** Demo-default chrome vs judges inspection (`?judges=1`). */
export function isJudgesMode(): boolean {
  if (typeof window === "undefined") return false
  const q = new URLSearchParams(window.location.search)
  return q.get("judges") === "1" || q.has("judges")
}

/** Cold open: boring ops — first ASSIGNED (ACT), not RESEARCH/UNKNOWN. */
export function pickColdOpenId(items: { id: string; ownership_state: string }[]): string | null {
  const assigned = items.find((row) => row.ownership_state === "ASSIGNED")
  if (assigned) return assigned.id
  const conflict = items.find((row) => row.id === "dp-purana-quila" || row.ownership_state === "CONFLICT")
  return conflict?.id ?? items[0]?.id ?? null
}

/** Prefer Purana Quila then any CONFLICT after Rain Strike. */
export function pickConflictFocusId(items: { id: string; ownership_state: string }[]): string | null {
  const preferred = items.find((row) => row.id === "dp-purana-quila" && row.ownership_state === "CONFLICT")
  if (preferred) return preferred.id
  return items.find((row) => row.ownership_state === "CONFLICT")?.id ?? null
}

/**
 * Dry demo presentation: ACT/ASSIGNED first, CONFLICT mid-list, RESEARCH last.
 * Wet (precip > 5): keep API priority order so Rain Strike visibly reorders.
 */
export function presentQueueForDemo(items: PointRow[], precipMm: number): PointRow[] {
  if (precipMm > 5) {
    return items.map((row, index) => ({ ...row, priority_rank: index + 1 }))
  }
  const assigned = items.filter((row) => row.ownership_state === "ASSIGNED")
  const conflict = items.filter((row) => row.ownership_state === "CONFLICT")
  const rest = items.filter((row) => row.ownership_state !== "ASSIGNED" && row.ownership_state !== "CONFLICT")
  const ordered = [...assigned, ...conflict, ...rest]
  return ordered.map((row, index) => ({ ...row, priority_rank: index + 1 }))
}

export const RAIN_STRIKE_EVENT = "dp-rain-strike"
export const MAP_EXPAND_EVENT = "dp-map-expand"
