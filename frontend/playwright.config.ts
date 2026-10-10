import { defineConfig, devices } from "@playwright/test"

const fresh = Boolean(process.env.CI || process.env.DP_E2E_FRESH)

export default defineConfig({
  testDir: "../tests/e2e",
  fullyParallel: false,
  workers: 1,
  use: { baseURL: "http://127.0.0.1:5173", ...devices["Desktop Chrome"] },
  webServer: [
    {
      command: "rm -f runs/disputepoint.sqlite && PYTHONPATH=. .venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000",
      cwd: "..",
      port: 8000,
      reuseExistingServer: !fresh,
      timeout: 30000,
    },
    {
      command: "npm run dev --prefix frontend",
      cwd: "..",
      port: 5173,
      reuseExistingServer: !fresh,
      timeout: 30000,
    },
  ],
})
