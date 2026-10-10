import type { EvidenceItem } from "../api/client"

export function EvidenceList({ items }: { items: EvidenceItem[] }) {
  if (items.length === 0) return <p className="muted">No evidence rows on this point.</p>
  return (
    <dl>
      {items.map((item) => (
        <div key={item.id}>
          <dt>
            {item.type}{" "}
            {item.live_verified ? (
              <span className="chip ok">live verified</span>
            ) : (
              <span className="chip">fixture cache</span>
            )}
          </dt>
          <dd>
            {item.title ? <p className="dp-meta">{item.title}</p> : null}
            <q>{item.quote}</q>{" "}
            <a href={item.url} target="_blank" rel="noreferrer">source</a>
            {item.source_date ? <span className="muted"> · {item.source_date}</span> : null}
            {item.live_status && item.live_status !== "ok" ? (
              <span className="muted"> · {item.live_status}</span>
            ) : null}
          </dd>
        </div>
      ))}
    </dl>
  )
}
