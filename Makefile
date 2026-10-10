# DisputePoint — toolchain (WP-00).
# install / test / run satisfy NFR-009. deploy stays a later gate.

.PHONY: install test run deploy help visual-qa

VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn

help:
	@echo "Targets: install test run deploy visual-qa"
	@echo "API defaults to 127.0.0.1:8000; UI defaults to 127.0.0.1:5173"

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	npm install

test:
	@test -x $(PY) || (echo "make test: run make install first"; exit 1)
	@if [ ! -d tests ]; then \
		echo "pytest: no tests/ yet (expected until WP-01)"; \
		exit 0; \
	fi; \
	$(PY) -m pytest -q tests; status=$$?; \
	if [ $$status -eq 5 ]; then \
		echo "pytest: no tests collected (expected until WP-01)"; \
		exit 0; \
	fi; \
	exit $$status

run:
	@test -x $(UVICORN) || (echo "make run: run make install first"; exit 1)
	@if [ -f backend/app/main.py ]; then APP=backend.app.main:app; else APP='backend.app:create_app --factory'; fi; \
	DP_LIVE_FETCH=1 $(UVICORN) $$APP --host 127.0.0.1 --port 8000 & api_pid=$$!; \
	npm run dev --prefix frontend & ui_pid=$$!; \
	trap 'kill $$api_pid $$ui_pid 2>/dev/null; wait $$api_pid $$ui_pid 2>/dev/null' INT TERM EXIT; \
	wait $$api_pid $$ui_pid

deploy:
	@echo "make deploy: prefer Ship It; see infra/README.md (SAM Build It day-1 recon gate)"
	@exit 1

visual-qa:
	@mkdir -p runs/visual-qa/latest
	CI=1 DP_E2E_FRESH=1 npx playwright test -c frontend/playwright.config.ts tests/e2e/visual-hackathon.spec.ts
	@echo "Screenshots + PASS.md → runs/visual-qa/latest/ (human mute/AWS/Earth still required)"
