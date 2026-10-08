import { useState } from "react"
import { EvalDrawer } from "./EvalDrawer"

export function EvalLink() {
  const [open, setOpen] = useState(false)
  return (
    <>
      <button type="button" onClick={() => setOpen(true)}>Judges: baseline tournament</button>
      {open ? <EvalDrawer onClose={() => setOpen(false)} /> : null}
    </>
  )
}
