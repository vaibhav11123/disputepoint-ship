import { expect, test, type Page } from "@playwright/test"
import fs from "node:fs"
import path from "node:path"

const OUT = path.resolve(__dirname, "../../runs/visual-qa/latest")
const VIEWPORT = { width: 1440, height: 900 }
const PURANA = "dp-purana-quila"

async function shot(page: Page, name: string) {
  fs.mkdirSync(OUT, { recursive: true })
  await page.screenshot({ path: path.join(OUT, name), fullPage: false })
}

async function openPoint(page: Page, id: string) {
  await page.locator(`tr[data-point-id="${id}"]`).click()
  await expect(page).toHaveURL(new RegExp(`/incident/${id}`))
}

function writePassTemplate(autoOk: boolean) {
  fs.mkdirSync(OUT, { recursive: true })
  const a = autoOk ? "x" : " "
  const body = `# Visual Hackathon Gate — PASS checklist

Auto capture: **${autoOk ? "PASS" : "FAIL"}** (\`make visual-qa\`)
Generated: ${new Date().toISOString()}

## Automated (this run)

- [${a}] V0-cold.png — Command queue|map; District incident command; map open
- [${a}] V1-rain-before / during / after — Configure → scenario 42 mm
- [${a}] V2-conflict.png — Purana assessment; AUTO-ASSIGNMENT BLOCKED; agency —
- [${a}] V3-evidence.png — Evidence ledger / VIEW SOURCE path
- [${a}] V4-escalate-before / after — Escalate → AWAITING DECISION / clock
- [${a}] V5-human.png — OFFICER CONFIRMED / human-verified seal
- [${a}] V6-replay.png — Incident Replay scrub (if present)
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
    await page.goto("/command")
    await expect(page.locator("table tbody tr")).toHaveCount(35)
    await expect(page.getByTestId("command-hero")).toContainText(/District incident command/i)
    await expect(page.getByTestId("command-map-hero")).toBeVisible()
    await expect(page.getByTestId("command-queue")).toBeVisible()
    await expect(page.locator(".maplibregl-map")).toBeVisible({ timeout: 15000 })
    await expect(page.getByText("θ")).toHaveCount(0)
    await page.waitForTimeout(1500)
    await shot(page, "V0-cold.png")

    await shot(page, "V1-rain-before.png")
    await page.getByTestId("scenario-strip").getByText("Configure").click()
    await page.getByTestId("rain-strike").click()
    await expect(page.getByTestId("rain-mm")).toContainText(/42/, { timeout: 10000 })
    await expect(page.getByTestId("rain-mm")).toContainText(/RAINFALL SCENARIO/)
    await shot(page, "V1-rain-during.png")
    await page.waitForTimeout(600)
    await shot(page, "V1-rain-after.png")

    await openPoint(page, PURANA)
    await expect(page.getByTestId("ownership-conflict")).toBeVisible({ timeout: 10000 })
    await expect(page.getByTestId("no-auto-assign")).toContainText(/AUTO.*ASSIGNMENT BLOCKED/)
    await expect(page.getByTestId("agency-null")).toContainText("—")
    await expect(page.locator(".claim-grid")).toBeVisible()
    await expect(page.getByTestId("conflict-effect")).toContainText(/Incident Commander review|exclusive|responsibility/i)
    await shot(page, "V2-conflict.png")

    await page.getByRole("tab", { name: "Evidence" }).click()
    await expect(page.getByTestId("evidence-screen")).toBeVisible({ timeout: 10000 })
    await expect(page.getByTestId("evidence-ledger")).toBeVisible()
    const viewSource = page.getByRole("button", { name: /VIEW SOURCE/i }).first()
    if (await viewSource.count()) await viewSource.click()
    await expect(page.getByText(/CLAIM|SOURCE/i).first()).toBeVisible()
    await shot(page, "V3-evidence.png")

    await page.getByRole("tab", { name: "Incident" }).click()
    await shot(page, "V4-escalate-before.png")
    const alreadyHuman = (await page.getByTestId("human-verified").count()) > 0
    if (!alreadyHuman) {
      await page.getByLabel("Escalate reason").selectOption({ index: 1 })
      await page.getByTestId("escalate-human-review").click()
      await expect(page).toHaveURL(/\/audit/, { timeout: 15000 })
      await expect(page.getByTestId("accountability-clock")).toBeVisible()
      await expect(page.getByTestId("owner-pending").or(page.getByText(/AWAITING DECISION/i))).toBeVisible()
      await shot(page, "V4-escalate-after.png")

      await page.getByRole("tab", { name: "Incident" }).click()
      await page.getByLabel("Confirm agency").selectOption({ index: 1 })
      await page.getByLabel("Confirm reason").fill("Jurisdiction and field evidence reviewed")
      const evidenceBox = page.locator(".evidence-check input[type=checkbox]").first()
      if (await evidenceBox.count()) await evidenceBox.check()
      await page.getByTestId("confirm-decision").click()
      await expect(page).toHaveURL(/\/audit/, { timeout: 15000 })
    } else {
      await shot(page, "V4-escalate-after.png")
    }
    await expect(page.getByTestId("human-verified")).toBeVisible()
    await expect(page.getByTestId("human-verified")).toContainText(/OFFICER CONFIRMED|HUMAN DECISION/)
    await shot(page, "V5-human.png")

    const replay = page.getByTestId("incident-replay")
    if (await replay.count()) {
      await expect(replay).toBeVisible()
      const scrub = replay.locator('input[type="range"]')
      if (await scrub.count()) await scrub.fill("2")
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
