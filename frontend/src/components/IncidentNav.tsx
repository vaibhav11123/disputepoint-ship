import { motion } from "motion/react"
import { navigate, type AppRoute } from "../lib/router"
import { Button } from "./ui/button"
import { Tabs, TabsList, TabsTrigger } from "./ui/tabs"

const TABS = [
  { value: "incident", label: "Incident" },
  { value: "evidence", label: "Evidence" },
  { value: "coordination", label: "Coordination" },
  { value: "audit", label: "Audit" },
] as const

type TabValue = (typeof TABS)[number]["value"]

function tabFromRoute(route: AppRoute): TabValue {
  if (route.name === "evidence" || route.name === "coordination" || route.name === "audit") return route.name
  return "incident"
}

export function IncidentNav({
  id,
  route,
  title,
}: {
  id: string
  route: AppRoute
  title?: string
}) {
  const value = tabFromRoute(route)

  return (
    <motion.div
      className="incident-nav"
      initial={{ opacity: 0, y: -4 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.18 }}
      data-testid="incident-nav"
    >
      <div className="incident-nav-bar">
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => navigate({ name: "command" })}
          data-testid="back-command"
        >
          ← Command
        </Button>
        {title ? <h2 className="incident-title">{title}</h2> : null}
      </div>
      <Tabs
        value={value}
        onValueChange={(next) => {
          const name = next as TabValue
          if (name === "incident") navigate({ name: "incident", id })
          else navigate({ name, id })
        }}
      >
        <TabsList aria-label="Incident sections">
          {TABS.map((tab) => (
            <TabsTrigger key={tab.value} value={tab.value}>
              {tab.label}
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>
    </motion.div>
  )
}
