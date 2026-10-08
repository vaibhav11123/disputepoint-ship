# DisputePoint AWS path

Phase 6 §16A. This file is the eligibility path. It is not a completed deploy.

## Chosen path for this tree

**B Build It**, until a human account passes G-AWS.

| Service | Product role |
|---------|----------------|
| API Gateway | HTTPS front for the decision routes |
| Lambda | Same FastAPI app as `backend.app.main:app` |
| DynamoDB | Point and audit state (`PointsTable`) |
| S3 | Evidence objects, public access blocked |
| EventBridge | Hourly rain poll, rule created **DISABLED** |

Bedrock stays off. No extra services.

Local demo stays `make run`: API `127.0.0.1:8000`, UI `127.0.0.1:5173`.

## What a human still does at G-AWS

1. `aws login` on the Free Tier account.
2. Install SAM.
3. `sam build -t infra/template.yaml` then `sam deploy` only after the account is confirmed.
4. Smoke `GET /health` on the output `ApiUrl`.
5. Put that URL on screen for the video (W9). Do not invent a URL here.

`make deploy` still exits 1 until that smoke exists.
