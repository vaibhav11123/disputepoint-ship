/** Shared lifecycle contract — UI must not invent transitions beyond this table. */

export type ActorRole =
  | "EOC_OPERATOR"
  | "INCIDENT_COMMANDER"
  | "AGENCY_COORDINATOR"
  | "FIELD_ENGINEER"
  | "AUDITOR"
  | "SYSTEM"

export type LifecycleState =
  | "INCIDENT_RECEIVED"
  | "TRIAGED"
  | "RESPONSIBILITY_CLEAR"
  | "RESPONSIBILITY_DISPUTED"
  | "EVIDENCE_REVIEW"
  | "HUMAN_REVIEW"
  | "OFFICER_CONFIRMED"
  | "ASSIGNED"
  | "ACTION_PENDING"
  | "RESOLVED"
  | "AUDITED"

export const LIFECYCLE_TRANSITIONS: Record<string, Record<string, ActorRole[]>> = {
  INCIDENT_RECEIVED: { TRIAGED: ["EOC_OPERATOR", "INCIDENT_COMMANDER"] },
  TRIAGED: {
    RESPONSIBILITY_CLEAR: ["SYSTEM"],
    RESPONSIBILITY_DISPUTED: ["SYSTEM"],
  },
  RESPONSIBILITY_CLEAR: { ASSIGNED: ["SYSTEM"] },
  RESPONSIBILITY_DISPUTED: {
    EVIDENCE_REVIEW: ["EOC_OPERATOR", "INCIDENT_COMMANDER", "AGENCY_COORDINATOR"],
  },
  EVIDENCE_REVIEW: {
    HUMAN_REVIEW: ["EOC_OPERATOR", "INCIDENT_COMMANDER", "AGENCY_COORDINATOR"],
  },
  HUMAN_REVIEW: { OFFICER_CONFIRMED: ["INCIDENT_COMMANDER"] },
  OFFICER_CONFIRMED: { ASSIGNED: ["SYSTEM"] },
  ASSIGNED: {
    ACTION_PENDING: ["INCIDENT_COMMANDER", "AGENCY_COORDINATOR"],
    RESOLVED: ["INCIDENT_COMMANDER", "AGENCY_COORDINATOR"],
  },
  ACTION_PENDING: { RESOLVED: ["INCIDENT_COMMANDER", "AGENCY_COORDINATOR"] },
  RESOLVED: { AUDITED: ["SYSTEM", "AUDITOR"] },
}

/** ownership_state × lifecycle → agency rule */
export function agencyAllowed(
  ownership: string,
  lifecycle: LifecycleState,
  agency: string | null,
): boolean {
  if (ownership === "CONFLICT") {
    if (["RESPONSIBILITY_DISPUTED", "EVIDENCE_REVIEW", "HUMAN_REVIEW"].includes(lifecycle)) {
      return agency === null
    }
    if (["OFFICER_CONFIRMED", "ASSIGNED", "ACTION_PENDING", "RESOLVED", "AUDITED"].includes(lifecycle)) {
      return agency !== null
    }
  }
  if (ownership === "ASSIGNED") {
    if (["RESPONSIBILITY_DISPUTED", "EVIDENCE_REVIEW", "HUMAN_REVIEW"].includes(lifecycle)) return false
    return agency !== null
  }
  if (ownership === "UNKNOWN") {
    if (lifecycle === "RESPONSIBILITY_CLEAR") return false
    return agency === null
  }
  return true
}

export function canTransition(from: string, to: string, actor: ActorRole): boolean {
  const edges = LIFECYCLE_TRANSITIONS[from]
  if (!edges || !edges[to]) return false
  return edges[to].includes(actor)
}

/** Forbidden: CONFLICT path skipping human confirmation */
export function isForbiddenConflictAssign(fromLifecycle: string, toLifecycle: string): boolean {
  const dispute = ["RESPONSIBILITY_DISPUTED", "EVIDENCE_REVIEW", "HUMAN_REVIEW"]
  return dispute.includes(fromLifecycle) && toLifecycle === "ASSIGNED"
}

export function lifecycleFromOwnership(
  ownership: string,
  escalated: boolean,
  officerConfirmed: boolean,
): LifecycleState {
  if (officerConfirmed) return "OFFICER_CONFIRMED"
  if (escalated) return "HUMAN_REVIEW"
  if (ownership === "CONFLICT") return "RESPONSIBILITY_DISPUTED"
  if (ownership === "ASSIGNED") return "ASSIGNED"
  return "TRIAGED"
}

export type DecisionRecord = {
  actorRole: "INCIDENT_COMMANDER"
  agency: string
  reason: string
  evidenceIds: string[]
  timestamp: string
  previousOwnershipState: string
  previousLifecycleState: string
  decisionType: "OPERATIONAL_RESPONSIBILITY_CONFIRMATION"
  auditId: string
}

export const PURANA_QUILA = {
  id: "dp-purana-quila",
  lat: 28.60944,
  lon: 77.24417,
  label: "DEMO INCIDENT",
} as const

export const ESCALATE_REASONS = [
  "Competing agency claims",
  "Jurisdiction record missing",
  "Evidence does not establish exclusive responsibility",
  "Agency response overdue",
  "Field condition conflicts with jurisdiction record",
] as const

export const POSITRON_STYLE = "https://tiles.openfreemap.org/styles/positron"
export const POSITRON_FALLBACK = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"

export const DEMO_CHAPTERS = [
  { id: "delhi", center: [77.21, 28.61] as [number, number], zoom: 10, label: "Delhi district" },
  { id: "corridor", center: [77.24, 28.61] as [number, number], zoom: 12, label: "Drain corridor" },
  { id: "purana", center: [PURANA_QUILA.lon, PURANA_QUILA.lat] as [number, number], zoom: 14, label: "Purana Quila" },
] as const
