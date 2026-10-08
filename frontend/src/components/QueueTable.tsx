import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
} from "@tanstack/react-table"
import { useMemo } from "react"
import type { PointRow } from "../api/client"
import { AgencyBlock, StateChip } from "./StateChip"
import { TriageChip } from "./TriageChip"
import { Badge } from "./ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table"

function rankLabel(rank: number) {
  return `[${String(rank).padStart(2, "0")}]`
}

type QueueRow = PointRow & { escalated?: boolean; officer_confirmed?: boolean }

export function QueueTable({
  rows,
  selectedId,
  flashed,
  onSelect,
}: {
  rows: QueueRow[]
  selectedId: string | null
  flashed: Set<string>
  onSelect: (id: string) => void
}) {
  const columns = useMemo<ColumnDef<QueueRow>[]>(
    () => [
      {
        id: "rank",
        header: "Rank",
        cell: ({ row }) => <span className="rank">{rankLabel(row.original.priority_rank)}</span>,
      },
      {
        accessorKey: "name",
        header: "Name",
        cell: ({ row }) => <span title={row.original.name}>{row.original.name}</span>,
      },
      {
        id: "triage",
        header: "Triage",
        cell: ({ row }) => (
          <TriageChip state={row.original.ownership_state} escalated={Boolean(row.original.escalated)} />
        ),
      },
      {
        id: "state",
        header: "State",
        cell: ({ row }) => (
          <StateChip
            state={row.original.ownership_state}
            compact
            escalated={Boolean(row.original.escalated)}
            officerConfirmed={Boolean(row.original.officer_confirmed)}
          />
        ),
      },
      {
        id: "agency",
        header: "Agency",
        cell: ({ row }) => (
          <AgencyBlock agency={row.original.responsible_agency} claimed={row.original.agencies_claimed} />
        ),
      },
      {
        id: "priority",
        header: "Priority",
        cell: ({ row }) => <span className="mono">{row.original.priority_score.toFixed(2)}</span>,
      },
      {
        id: "rain",
        header: "RainΔ",
        cell: ({ row }) => {
          const d = row.original.rain_delta
          return (
            <span className="mono">{d == null ? "—" : d > 0 ? `+${d}` : String(d)}</span>
          )
        },
      },
    ],
    [],
  )

  const table = useReactTable({
    data: rows,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getRowId: (row) => row.id,
  })

  if (rows.length === 0) {
    return <p>No disputed points loaded. Check fixtures.</p>
  }

  const awaiting = rows.filter((r) => r.ownership_state === "CONFLICT" || r.escalated)

  return (
    <div className="queue-wrap">
      {awaiting.length > 0 ? (
        <div className="awaiting-region" data-testid="awaiting-you-region">
          <Badge variant="warn">AWAITING YOU</Badge>
          <span className="muted"> · {awaiting.length} need human review / disputed</span>
        </div>
      ) : null}
      <Table data-testid="command-queue">
        <TableHeader>
          {table.getHeaderGroups().map((hg) => (
            <TableRow key={hg.id}>
              {hg.headers.map((header) => (
                <TableHead key={header.id}>
                  {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows.map((row) => {
            const r = row.original
            return (
              <TableRow
                key={row.id}
                tabIndex={0}
                role="button"
                aria-label={`Open incident ${r.name}`}
                aria-selected={r.id === selectedId}
                className={[
                  flashed.has(r.id) ? "flash flip-target" : "flip-target",
                  r.id === selectedId ? "selected-row" : "",
                  r.ownership_state === "CONFLICT" || r.escalated ? "awaiting-row" : "",
                  "queue-row",
                ]
                  .filter(Boolean)
                  .join(" ")}
                data-point-id={r.id}
                onClick={() => onSelect(r.id)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault()
                    onSelect(r.id)
                  }
                }}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
                ))}
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </div>
  )
}
