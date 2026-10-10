/**
 * MapLibre GL JS v6 + Vite: worker must be registered once before any Map mounts.
 * Without this, tiles stay blank with "Worker failed to load".
 * @see https://maplibre.org/maplibre-gl-js/docs/guides/v5-to-v6-migration-guide/
 */
import { setWorkerUrl } from "maplibre-gl"
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url"

setWorkerUrl(workerUrl)
