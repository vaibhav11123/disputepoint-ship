import { expect, test, type Page } from "@playwright/test"
import fs from "node:fs"
import path from "node:path"

const OUT = path.resolve(__dirname, "../../runs/visual-qa/latest")
const VIEWPORT = { width: 1440, height: 900 }

async function shot(page: Page, name: string) {
  fs.mkdirSync(OUT, { recursive: true })
  await page.screenshot({ path: path.join(OUT, name), fullPage: false })
}

function writePassTemplate(autoOk: boolean) {
  fs.mkdirSync(OUT, { recursive: true })
  const a = autoOk ? "x" : " "
  const body = `# Visual Hackathon Gate — PASS checklist

Auto capture: **${autoOk ? "PASS" : "FAIL"}** (\`make visual-qa\`)
Generated: ${new Date().toISOString()}

## Automated (this run)

- [${a}] V0-cold.png — ACT/ASSIGNED top; CONFLICT mid-list; map collapsed
- [${a}] V1-rain-before / during / after — reorder + map expand
- [${a}] V2-conflict.png — NO AUTO-ASSIGN · Agency —
- [${a}] V3-evidence.png — CLAIM→SOURCE→QUOTE→DECISION EFFECT
- [${a}] V4-escalate-before / after — CASE · ESCALATED · PENDING HUMAN
- [${a}] V5-human.png — HUMAN VERIFIED seal
- [${a}] V6-replay.png — Incident Replay scrub
- [${a}] V7-aws.png — architecture page (services we use)

## Human-only (required before calling video hackathon-ready)

- [ ] Mute video test: stranger answers WHERE → WHAT CHANGED → WHO DISAGREES → WHY → WHAT NEXT
- [ ] Thumbnail test (pause at aha frame readable at 20%)
- [ ] 10s stranger script without audio
- [ ] Earth Studio cut (Mode C) if used — see EARTH_STUDIO_SHOT.md
- [ ] AWS frame on camera (Ship It or SAM) — see AWS_DEMO_BEAT.md
- [ ] YouTube ≤3:00 signed-out watch

Do **not** mark G-VIDEO until human rows are checked.

Visual sentence: Rain changes priority. The point becomes disputed. Evidence explains why. The system refuses to guess. A human takes ownership.
`
  fs.writeFileSync(path.join(OUT, "PASS.md"), body, "utf8")
}

test.describe.configure({ mode: "serial" })

test("visual hackathon capture V0–V7", async ({ page }) => {
  let autoOk = false
  try {
    await page.setViewportSize(VIEWPORT)
    await page.goto("/")
    await expect(page.locator("table tbody tr")).toHaveCount(35)
    await page.waitForTimeout(5000)

    const firstState = page.locator("table tbody tr").first().locator("td").nth(3)
    await expect(firstState).toContainText("ASSIGNED")
    await expect(page.getByRole("button", { name: /Show map/ })).toBeVisible()
    await expect(page.locator(".maplibregl-map")).toHaveCount(0)
    await expect(page.getByText("θ")).toHaveCount(0)
    await shot(page, "V0-cold.png")

    await shot(page, "V1-rain-before.png")
    await page.getByTestId("rain-strike").click()
    await expect(page.getByText(/Using scenario rain/)).toBeVisible()
    await expect(page.locator(".maplibregl-map")).toBeVisible({ timeout: 8000 })
    await shot(page, "V1-rain-during.png")
    await expect(page.getByTestId("ownership-conflict")).toBeVisible({ timeout: 8000 })
    await expect(page.getByTestId("no-auto-assign")).toContainText("NO AUTO-ASSIGN")
    await expect(page.getByTestId("agency-null")).toContainText("—")
    await page.waitForTimeout(800)
    await shot(page, "V1-rain-after.png")

    await shot(page, "V2-conflict.png")
    await expect(page.getByTestId("conflict-effect")).toContainText("does not establish exclusive responsibility")

    await page.getByRole("button", { name: "Trace" }).first().click()
    await expect(page.getByTestId("evidence-trace")).toContainText("CLAIM → SOURCE → QUOTE → DECISION EFFECT")
    await shot(page, "V3-evidence.png")

    await shot(page, "V4-escalate-before.png")
    const alreadyHuman = (await page.getByTestId("human-verified").count()) > 0
    if (!alreadyHuman) {
      await page.getByRole("button", { name: "ESCALATE" }).click()
      await expect(page.getByTestId("accountability-clock")).toBeVisible()
      await expect(page.getByTestId("owner-pending")).toContainText("PENDING HUMAN")
      await expect(page.getByTestId("accountability-clock")).toContainText("ESCALATED")
      await expect(page.getByTestId("accountability-clock")).toContainText("CASE")
      await shot(page, "V4-escalate-after.png")

      await page.getByLabel("Override reason").fill("DM cell assigns PWD for this window")
      await page.getByRole("button", { name: "OVERRIDE" }).click()
    } else {
      await page.getByRole("button", { name: "ESCALATE" }).click()
      await expect(page.getByTestId("accountability-clock")).toBeVisible()
      await expect(page.getByTestId("accountability-clock")).toContainText("ESCALATED")
      await expect(page.getByTestId("accountability-clock")).toContainText("CASE")
      await shot(page, "V4-escalate-after.png")
    }
    await expect(page.getByTestId("human-verified")).toBeVisible()
    await expect(page.getByTestId("human-verified")).toContainText("HUMAN VERIFIED")
    await shot(page, "V5-human.png")

    await expect(page.getByTestId("incident-replay")).toBeVisible()
    const scrub = page.getByTestId("incident-replay").locator('input[type="range"]')
    if (await scrub.count()) {
      await scrub.fill("2")
    }
    await shot(page, "V6-replay.png")

    await page.goto("/aws-arch.html")
    await expect(page.getByTestId("aws-arch-diagram")).toBeVisible()
    await shot(page, "V7-aws.png")

    autoOk = true
  } finally {
    writePassTemplate(autoOk)
  }
  expect(autoOk).toBe(true)
})
