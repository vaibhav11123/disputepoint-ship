import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
} from "@tanstack/react-table"
import { useMemo } from "react"
import type { PointRow } from "../api/client"
import { copy } from "../lib/copy"
import { AgencyBlock } from "./StateChip"
import { nextActionLabel, TriageChip } from "./TriageChip"
import { Badge } from "./ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table"

function rankLabel(rank: number) {
  return String(rank).padStart(2, "0")
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
        accessorKey: "name",
        header: copy.queue.incident,
        cell: ({ row }) => (
          <span title={row.original.name}>
            <span className="rank mono dp-meta">{rankLabel(row.original.priority_rank)} </span>
            {row.original.name}
          </span>
        ),
      },
      {
        id: "status",
        header: copy.queue.status,
        cell: ({ row }) => (
          <TriageChip
            state={row.original.ownership_state}
            escalated={Boolean(row.original.escalated)}
            officerConfirmed={Boolean(row.original.officer_confirmed)}
          />
        ),
      },
      {
        id: "responsibility",
        header: copy.queue.responsibility,
        cell: ({ row }) => (
          <AgencyBlock agency={row.original.responsible_agency} claimed={row.original.agencies_claimed} />
        ),
      },
      {
        id: "priority",
        header: copy.queue.priority,
        cell: ({ row }) => <span className="mono dp-meta">{row.original.priority_score.toFixed(2)}</span>,
      },
      {
        id: "next",
        header: copy.queue.nextAction,
        cell: ({ row }) => (
          <span className="muted dp-meta">
            {nextActionLabel(
              row.original.ownership_state,
              Boolean(row.original.escalated),
              Boolean(row.original.officer_confirmed),
            )}
          </span>
        ),
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
    return <p>{copy.command.empty}</p>
  }

  const awaiting = rows.filter(
    (r) =>
      !r.officer_confirmed &&
      r.ownership_state !== "ASSIGNED" &&
      (r.ownership_state === "CONFLICT" || r.escalated),
  )

  return (
    <div className="queue-wrap">
      {awaiting.length > 0 ? (
        <div className="awaiting-region visually-hidden" data-testid="awaiting-you-region" aria-hidden="true">
          <Badge variant="warn">{copy.command.awaitingStrip(awaiting.length)}</Badge>
          <span className="muted"> {copy.queue.awaitingRegion(awaiting.length)}</span>
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
                aria-label={copy.queue.openIncident(r.name)}
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
