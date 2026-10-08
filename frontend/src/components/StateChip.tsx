export function StateChip({ state }: { state: string }) {
  const warn = state === "CONFLICT" || state === "UNKNOWN" || state === "UNCERTAIN"
  return <span className={warn ? "chip warn" : "chip ok"}>{state}</span>
}

export function AgencyBlock({ agency }: { agency: string | null }) {
  return <span>{agency ?? "—"}</span>
}
