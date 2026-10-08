# DisputePoint — root Makefile
# Phase 7 Agent A owns real install/test/run. Stubs fail clearly until apps exist.
# See docs/PHASE6.md and docs/build/GAPS.md.

.PHONY: install test run deploy help

help:
	@echo "Targets: install test run deploy"
	@echo "Phase 7 app code not started — see docs/PHASE6.md Agent A / docs/build/GAPS.md GAP-BOOT-*"

install:
	@if [ -d backend ] && [ -f backend/pyproject.toml -o -f backend/requirements.txt ]; then \
		echo "TODO: install backend deps"; \
	else \
		echo "make install: Phase 7 backend not present yet (docs/build/GAPS.md GAP-BOOT-01)"; \
		exit 1; \
	fi
	@if [ -d frontend ] && [ -f frontend/package.json ]; then \
		echo "TODO: npm/pnpm install frontend"; \
	else \
		echo "make install: Phase 7 frontend not present yet"; \
		exit 1; \
	fi

test:
	@if [ -d backend ]; then echo "TODO: pytest"; else echo "make test: no backend yet"; exit 1; fi

run:
	@echo "make run: start API + UI when Phase 7 exists (fixtures under data/fixtures/)"
	@exit 1

deploy:
	@echo "make deploy: prefer Ship It; see infra/README.md (SAM Build It day-1 recon gate)"
	@exit 1
