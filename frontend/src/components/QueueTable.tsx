import type { PointRow } from "../api/client"
import { AgencyBlock, StateChip } from "./StateChip"
import { TriageChip } from "./TriageChip"

function rankLabel(rank: number) {
  return `[${String(rank).padStart(2, "0")}]`
}

export function QueueTable({
  rows,
  selectedId,
  flashed,
  onSelect,
}: {
  rows: PointRow[]
  selectedId: string | null
  flashed: Set<string>
  onSelect: (id: string) => void
}) {
  if (rows.length === 0) {
    return <p>No disputed points loaded. Check fixtures.</p>
  }
  return (
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Name</th>
          <th>Triage</th>
          <th>State</th>
          <th>Agency</th>
          <th>Priority</th>
          <th>RainΔ</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr
            key={row.id}
            tabIndex={0}
            role="button"
            aria-label={`Select ${row.name}`}
            aria-selected={row.id === selectedId}
            className={[flashed.has(row.id) ? "flash" : "", row.id === selectedId ? "selected-row" : "", "queue-row"]
              .filter(Boolean)
              .join(" ")}
            data-point-id={row.id}
            onClick={() => onSelect(row.id)}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault()
                onSelect(row.id)
              }
            }}
          >
            <td className="rank">{rankLabel(row.priority_rank)}</td>
            <td title={row.name}>{row.name}</td>
            <td>
              <TriageChip state={row.ownership_state} />
            </td>
            <td>
              <StateChip state={row.ownership_state} compact />
            </td>
            <td>
              <AgencyBlock agency={row.responsible_agency} claimed={row.agencies_claimed} />
            </td>
            <td className="mono">{row.priority_score.toFixed(2)}</td>
            <td className="mono">{row.rain_delta == null ? "—" : row.rain_delta > 0 ? `+${row.rain_delta}` : String(row.rain_delta)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
