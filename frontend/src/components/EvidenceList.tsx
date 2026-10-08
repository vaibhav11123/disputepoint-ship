import type { EvidenceItem } from "../api/client"

export function EvidenceList({ items }: { items: EvidenceItem[] }) {
  if (items.length === 0) return <p className="muted">No evidence rows on this point.</p>
  return (
    <dl>
      {items.map((item) => (
        <div key={item.id}>
          <dt>{item.type}</dt>
          <dd>
            <q>{item.quote}</q>{" "}
            <a href={item.url} target="_blank" rel="noreferrer">source</a>
          </dd>
        </div>
      ))}
    </dl>
  )
}
