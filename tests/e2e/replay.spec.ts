import { expect, test } from "@playwright/test"

test("historical replay advances on /demo without inventing Purana day event", async ({ page }) => {
  await page.goto("/demo")
  await expect(page.getByTestId("historical-replay")).toBeVisible()
  await expect(page.getByText(/HISTORICAL REPLAY/i).first()).toBeVisible()
  await page.getByTestId("replay-advance").click()
  await expect(page.getByTestId("replay-state")).toBeVisible({ timeout: 10000 })
  await expect(page.getByTestId("replay-gaps")).toContainText(/without 29 Jul evidence/i)
  // Period-honest label — not MM / 6H
  await expect(page.getByTestId("replay-state")).not.toContainText(/MM\s*\/\s*6H/i)
  // Purana corpus case remains reachable via explicit demo CTA; not via replay fabrication
  await page.getByRole("button", { name: /PURANA QUILA/i }).click()
  await expect(page).toHaveURL(/\/incident\/dp-purana-quila/)
})

test("R5: selecting map point during replay stays on /demo", async ({ page }) => {
  await page.goto("/demo")
  await page.getByTestId("replay-advance").click()
  await expect(page.getByTestId("replay-state")).toBeVisible({ timeout: 10000 })
  // Advance until at least one activation (may take a few steps)
  for (let i = 0; i < 6; i++) {
    const undocumented = page.getByTestId("replay-undocumented")
    if (await undocumented.isVisible().catch(() => false)) break
    const advance = page.getByTestId("replay-advance")
    if (await advance.isDisabled()) break
    await advance.click()
    await page.waitForTimeout(200)
  }
  await expect(page).toHaveURL(/\/demo/)
  // Click map canvas area if markers exist — highlight only
  const map = page.locator(".maplibregl-map").first()
  if (await map.isVisible().catch(() => false)) {
    await map.click({ position: { x: 120, y: 120 } }).catch(() => undefined)
  }
  await expect(page).toHaveURL(/\/demo/)
})

test("exit replay then command has no historical rain mode", async ({ page }) => {
  await page.goto("/demo")
  await page.getByTestId("replay-advance").click()
  await expect(page.getByTestId("replay-state")).toBeVisible({ timeout: 10000 })
  await page.getByTestId("replay-exit").click()
  await page.goto("/command")
  const footer = page.getByTestId("footer-rain-status")
  await expect(footer).toBeVisible({ timeout: 10000 })
  await expect(footer).not.toContainText(/HISTORICAL REPLAY/i)
})
