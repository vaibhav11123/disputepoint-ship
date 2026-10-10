import type { PointRow } from "../api/client"
import { DEMO_CHAPTERS, PURANA_QUILA } from "./lifecycle"

/** Demo-default chrome vs judges inspection (`?judges=1`). */
export function isJudgesMode(): boolean {
  if (typeof window === "undefined") return false
  const q = new URLSearchParams(window.location.search)
  return q.get("judges") === "1" || q.has("judges")
}

/** Quieter topbar for camera (`?demo=1`) or default non-judges chrome. */
export function isQuietDemoChrome(): boolean {
  if (typeof window === "undefined") return true
  const q = new URLSearchParams(window.location.search)
  if (q.get("demo") === "1") return true
  if (isJudgesMode()) return false
  return true
}

/** Footer AWS honesty — never invent Ship It without VITE_AWS_MODE=ship. */
export function awsHonestyLabel(): string {
  const mode = (import.meta.env.VITE_AWS_MODE as string | undefined)?.toLowerCase()
  if (mode === "ship" || mode === "shipit") return "AWS · Ship It"
  if (mode === "sam" || mode === "build") return "AWS · Build It (SAM local)"
  return "AWS · local fixtures"
}

export function isDemoRoute(): boolean {
  if (typeof window === "undefined") return false
  return window.location.pathname === "/demo" || window.location.hash === "#demo"
}

/** Cold open: boring ops — first ASSIGNED (ACT), not RESEARCH/UNKNOWN. */
export function pickColdOpenId(items: { id: string; ownership_state: string }[]): string | null {
  const assigned = items.find((row) => row.ownership_state === "ASSIGNED")
  if (assigned) return assigned.id
  const conflict = items.find((row) => row.id === PURANA_QUILA.id || row.ownership_state === "CONFLICT")
  return conflict?.id ?? items[0]?.id ?? null
}

/** Prefer Purana Quila then any CONFLICT after Rain Strike. */
export function pickConflictFocusId(items: { id: string; ownership_state: string }[]): string | null {
  const preferred = items.find((row) => row.id === PURANA_QUILA.id && row.ownership_state === "CONFLICT")
  if (preferred) return preferred.id
  return items.find((row) => row.ownership_state === "CONFLICT")?.id ?? null
}

/**
 * Historical replay view: documented activations by clock t, in activation order.
 * Does not fabricate points; remainder count is for UI honesty.
 */
export function presentReplayQueue(
  items: PointRow[],
  activatedIds: string[],
): { active: PointRow[]; undocumentedCount: number } {
  const byId = new Map(items.map((row) => [row.id, row]))
  const active: PointRow[] = []
  for (const id of activatedIds) {
    const row = byId.get(id)
    if (row) active.push({ ...row, priority_rank: active.length + 1 })
  }
  return {
    active,
    undocumentedCount: Math.max(0, items.length - active.length),
  }
}

export function awaitingYouCount(items: { ownership_state: string; escalated?: boolean }[]): number {
  return items.filter((row) => row.ownership_state === "CONFLICT" || row.escalated).length
}

export { DEMO_CHAPTERS, PURANA_QUILA }

export const RAIN_STRIKE_EVENT = "dp-rain-strike"
export const MAP_EXPAND_EVENT = "dp-map-expand"
export const DEMO_CHAPTER_EVENT = "dp-demo-chapter"
