---
name: ship-it-deploy
description: Redeploy or smoke DisputePoint Ship It (ap-south-1).
edges:
  - target: context/setup.md
    condition: when running make deploy or aws login
  - target: context/stack.md
    condition: when checking AWS services used
last_updated: 2026-10-10
---

# Ship It deploy / smoke

## When

Redeploy after Lambda/API/UI changes, or warm the stack before G-VIDEO.

## Steps

1. `export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"`
2. `export AWS_PROFILE=disputepoint AWS_REGION=ap-south-1`
3. `aws sts get-caller-identity` — if expired, `aws login --profile disputepoint` (Chrome / `--remote` + paste code)
4. `make deploy` — stages `infra/package/`, SAM build/deploy, Vite build with `VITE_API_URL`, S3 sync, smokes `/health` + `/points`
5. Confirm `rain_source_state=LIVE` and UI origin CORS (not `*`)

## Pins

Operator URLs and cleanup: `docs/operations/AWS_OPERATOR.md` · demo beat: `docs/build/AWS_DEMO_BEAT.md`.

## Cleanup

After video: `sam delete --stack-name disputepoint --region ap-south-1 --profile disputepoint`
