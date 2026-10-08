import { expect, test, type Page } from "@playwright/test"

async function openPoint(page: Page, id: string) {
  await page.locator(`tr[data-point-id="${id}"]`).click()
}

test("E2E-01 cold queue is home", async ({ page }) => {
  await page.goto("/")
  await expect(page.getByRole("region", { name: "Disputed points queue" })).toBeVisible()
  await expect(page.locator("table tbody tr")).toHaveCount(14)
  await expect(page.locator("canvas, .maplibregl-map")).toHaveCount(0)
  await expect(page.getByText("Loading disputed points.")).toHaveCount(0)
  await page.locator("table tbody tr").first().click()
  await expect(page.getByText("Advisory only — not an official agency assignment.")).toBeVisible()
  await page.locator("table tbody tr").first().focus()
  await expect(page.locator("table tbody tr").first()).toBeFocused()
})

test("E2E-02 scenario rain stays on the slider path", async ({ page }) => {
  await page.goto("/")
  await expect(page.locator("table tbody tr")).toHaveCount(14)
  const before = await page.locator("table tbody tr").first().locator("td").nth(4).innerText()
  await page.getByLabel("Scenario rain millimetres").fill("40")
  await page.getByRole("button", { name: "Apply rain" }).click()
  await expect(page.getByText("Using scenario rain")).toBeVisible()
  await expect(page.getByText("Slider")).toBeVisible()
  await expect(page.locator("table tbody tr")).toHaveCount(14)
  await expect(page.locator("table tbody tr").first().locator("td").nth(4)).not.toHaveText(before)
})

test("E2E-03 null agency and escalate copy", async ({ page }) => {
  await page.goto("/")
  await openPoint(page, "dp-purana-quila")
  const card = page.getByRole("region", { name: "Point card" })
  await expect(card.getByText("UNKNOWN", { exact: true })).toBeVisible()
  await expect(card.getByText("—", { exact: true })).toBeVisible()
  await expect(card.getByText("Claimed: NDMC, PWD, MCD, IFC")).toBeVisible()
  await expect(card.getByText("Ownership uncertain — escalate to coordination cell.").first()).toBeVisible()
})

test("E2E-04 override and escalate write the audit panel", async ({ page }) => {
  await page.goto("/")
  await openPoint(page, "dp-purana-quila")
  await expect(page.getByRole("button", { name: "ACK" })).toBeDisabled()
  await page.getByLabel("Override reason").fill("cell assigns PWD for this window")
  await page.getByRole("button", { name: "OVERRIDE" }).click()
  await expect(page.getByTestId("decision-audit")).toContainText("OVERRIDE")
  await expect(page.getByTestId("decision-audit")).toContainText("PWD")
  await page.getByLabel("Escalate reason").fill("two agencies still claimed")
  await page.getByRole("button", { name: "ESCALATE" }).click()
  await expect(page.getByTestId("decision-audit")).toContainText("ESCALATE")
})

test("E2E-05 synthetic badge is not live SCADA", async ({ page }) => {
  await page.goto("/")
  await page.locator("table tbody tr").first().click()
  await expect(page.getByText("SYNTHETIC", { exact: true })).toBeVisible()
  await expect(page.getByText("Readiness: synthetic fixture (not live SCADA).")).toBeVisible()
  await page.getByRole("button", { name: "Hide synthetic" }).click()
  await expect(page.getByText("SYNTHETIC", { exact: true })).toHaveCount(0)
  await expect(page.getByText("Readiness: synthetic fixture (not live SCADA).")).toBeVisible()
})

test("E2E-06 Purana Quila spine", async ({ page }) => {
  await page.goto("/")
  await expect(page.locator("table tbody tr")).toHaveCount(14)
  await openPoint(page, "dp-purana-quila")
  await expect(page.getByRole("region", { name: "Point card" }).getByText("—", { exact: true })).toBeVisible()
  await expect(page.locator("q").first()).toBeVisible()
  await page.getByLabel("Scenario rain millimetres").fill("40")
  await page.getByRole("button", { name: "Apply rain" }).click()
  await expect(page.getByText("Using scenario rain")).toBeVisible()
  await page.getByLabel("Escalate reason").fill("coordination cell takes the window")
  await page.getByRole("button", { name: "ESCALATE" }).click()
  await expect(page.getByTestId("decision-audit")).toContainText("ESCALATE")
  await expect(page.getByTestId("provenance")).toContainText("data/fixtures/points.json")
})

test("E2E-08 command palette selects a point", async ({ page }) => {
  await page.goto("/")
  await expect(page.locator("table tbody tr")).toHaveCount(14)
  await page.keyboard.press("Meta+k")
  await page.getByLabel("Point search").fill("Purana")
  await page.getByRole("dialog", { name: "Jump to point" }).getByRole("button", { name: "Purana Quila Rd storm drain (India Gate→Yamuna)" }).click()
  await expect(page.getByRole("heading", { name: /Purana Quila/ })).toBeVisible()
  await expect(page.getByText("Billing")).toHaveCount(0)
  await expect(page.getByText("Settings")).toHaveCount(0)
})

test("E2E-09 eval drawer leaves metrics blank", async ({ page }) => {
  await page.goto("/")
  await page.getByRole("button", { name: "Judges: baseline tournament" }).click()
  const drawer = page.getByRole("dialog", { name: "Baseline tournament" })
  await expect(drawer).toContainText("tests/eval/baseline_tournament.md")
  await expect(drawer).toContainText("TBD")
  await expect(drawer).not.toContainText(/0\.\d+/)
})
