import { useEffect, useMemo, useState } from "react"
import { listPoints, SELECT_POINT, type PointRow } from "../api/client"

export function CommandPalette({ onSelect }: { onSelect: (id: string) => void }) {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState("")
  const [rows, setRows] = useState<PointRow[]>([])

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault()
        setOpen(true)
        listPoints().then((listing) => setRows(listing.items)).catch(() => setRows([]))
      }
      if (event.key === "Escape") setOpen(false)
    }
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [])

  const matches = useMemo(() => {
    const needle = query.trim().toLowerCase()
    return rows.filter((row) => needle.length === 0 || row.name.toLowerCase().includes(needle)).slice(0, 8)
  }, [query, rows])

  function choose(id: string) {
    onSelect(id)
    window.dispatchEvent(new CustomEvent(SELECT_POINT, { detail: id }))
    setOpen(false)
    setQuery("")
  }

  if (!open) return null
  return (
    <div className="palette" role="dialog" aria-label="Jump to point">
      <form
        onSubmit={(event) => {
          event.preventDefault()
          if (matches[0]) choose(matches[0].id)
        }}
      >
        <label className="field">
          Point
          <input autoFocus aria-label="Point search" value={query} onChange={(event) => setQuery(event.target.value)} />
        </label>
        <ul>
          {matches.map((row) => (
            <li key={row.id}>
              <button type="button" onClick={() => choose(row.id)}>{row.name}</button>
            </li>
          ))}
        </ul>
      </form>
    </div>
  )
}
