import { useEffect, useState, useSyncExternalStore } from "react"

/** Cold open: normalize `/` to `/command` before first paint. */
if (typeof window !== "undefined") {
  const path = window.location.pathname
  if (path === "/" || path === "") {
    window.history.replaceState(null, "", `/command${window.location.search || ""}`)
  }
}

export type AppRoute =
  | { name: "command" }
  | { name: "incident"; id: string }
  | { name: "evidence"; id: string }
  | { name: "coordination"; id: string }
  | { name: "audit"; id: string }
  | { name: "demo" }

function searchKeep(): string {
  return window.location.search || ""
}

export function parsePath(pathname: string): AppRoute {
  const path = pathname.replace(/\/+$/, "") || "/"
  if (path === "/" || path === "/command") return { name: "command" }
  if (path === "/demo") return { name: "demo" }
  const m = path.match(/^\/incident\/([^/]+)(?:\/(evidence|coordination|audit))?$/)
  if (m) {
    const id = decodeURIComponent(m[1])
    if (m[2] === "evidence") return { name: "evidence", id }
    if (m[2] === "coordination") return { name: "coordination", id }
    if (m[2] === "audit") return { name: "audit", id }
    return { name: "incident", id }
  }
  return { name: "command" }
}

export function pathFor(route: AppRoute): string {
  switch (route.name) {
    case "command":
      return "/command"
    case "demo":
      return "/demo"
    case "incident":
      return `/incident/${encodeURIComponent(route.id)}`
    case "evidence":
      return `/incident/${encodeURIComponent(route.id)}/evidence`
    case "coordination":
      return `/incident/${encodeURIComponent(route.id)}/coordination`
    case "audit":
      return `/incident/${encodeURIComponent(route.id)}/audit`
  }
}

export function navigate(route: AppRoute, replace = false) {
  const url = pathFor(route) + searchKeep()
  if (replace) window.history.replaceState(null, "", url)
  else window.history.pushState(null, "", url)
  window.dispatchEvent(new PopStateEvent("popstate"))
}

function subscribe(onStoreChange: () => void) {
  window.addEventListener("popstate", onStoreChange)
  return () => window.removeEventListener("popstate", onStoreChange)
}

function getSnapshot(): string {
  return window.location.pathname
}

export function useRoute(): AppRoute {
  const pathname = useSyncExternalStore(subscribe, getSnapshot, () => "/command")
  const [route, setRoute] = useState(() => parsePath(pathname))

  useEffect(() => {
    setRoute(parsePath(pathname))
    if (pathname === "/" || pathname === "") {
      navigate({ name: "command" }, true)
    } else if (parsePath(pathname).name === "command" && pathname !== "/command" && pathname !== "/") {
      // unknown → command
      if (!pathname.startsWith("/incident") && pathname !== "/demo" && pathname !== "/command") {
        navigate({ name: "command" }, true)
      }
    }
  }, [pathname])

  return route
}

export function incidentIdFromRoute(route: AppRoute): string | null {
  if (route.name === "command" || route.name === "demo") return null
  return route.id
}
