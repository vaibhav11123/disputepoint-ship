import type { ReactNode } from "react"
import type { PointDetail } from "../api/client"
import { copy } from "../lib/copy"
import { resolvePlaceCoords } from "../lib/placeCoords"
import { PlaceStrip } from "./PlaceStrip"
import { PointFocusMap } from "./PointFocusMap"

export function IncidentWorkspace({
  point,
  children,
  mapHeight = 340,
  compactMap = false,
}: {
  point: PointDetail
  children: ReactNode
  mapHeight?: number
  /** Audit: shorter sticky map */
  compactMap?: boolean
}) {
  const coords = resolvePlaceCoords(point)
  const h = compactMap ? Math.min(mapHeight, 200) : mapHeight

  return (
    <div className={compactMap ? "incident-workspace compact" : "incident-workspace"} data-testid="incident-workspace">
      <div className="incident-workspace-main">{children}</div>
      <aside className="incident-workspace-map flush" aria-label={copy.place.mapAria}>
        <PointFocusMap
          lat={coords?.lat ?? null}
          lon={coords?.lon ?? null}
          name={point.name}
          height={h}
          zoom={compactMap ? 14 : 15.5}
        />
        <PlaceStrip
          name={point.name}
          lat={coords?.lat ?? null}
          lon={coords?.lon ?? null}
          agenciesClaimed={point.agencies_claimed}
          coordSource={coords?.source ?? null}
        />
      </aside>
    </div>
  )
}
