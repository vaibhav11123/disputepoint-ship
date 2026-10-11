# AWS demo beat (W9) — on camera 2:10–2:35

**Rule:** Naming AWS only in the write-up is not enough ([WeMakeDevs rules](https://www.wemakedevs.org/aws/rules)).

## Preferred — Ship It

Show ≥10s:

1. Architecture diagram (below)
2. Live API Gateway URL **or** console request for rain / points
3. DynamoDB / S3 / CloudWatch breadcrumb if available

## Failover — Build It

1. Same diagram
2. `sam local invoke` (or documented SAM path) of the rain/re-rank handler
3. Say clearly: local SAM parity for eligibility

## Diagram (record this ASCII or redraw)

```text
UI (S3 website)
        │
        ▼
   API Gateway
        │
        ▼
     Lambda  ──► DynamoDB (points / audit stamps)
        │
        ├──► S3 (evidence + runtime snapshot)
        └──► EventBridge (rain + evidence schedules)
                │
                ▼
            CloudWatch logs
```

Do **not** say CloudFront is serving the live UI — Ship It is S3 website hosting.

**Spoken line (W9):** “Live on AWS — API Gateway, Lambda, DynamoDB, S3 website UI.” Show `/aws-arch.html` plus `GET /health` with `rain_source_state=LIVE` when true.

## Operator pointers

- [AWS_OPERATOR.md](../operations/AWS_OPERATOR.md)
- [DEPLOYMENT.md](../operations/DEPLOYMENT.md)
- [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md) dual path



## Live Ship It URLs (2026-10-10, stack `disputepoint`, `ap-south-1`)


| Surface           | URL                                                                                                                                                                                        |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| API Gateway       | [https://olnsv0shee.execute-api.ap-south-1.amazonaws.com](https://olnsv0shee.execute-api.ap-south-1.amazonaws.com)                                                                         |
| UI (S3 website)   | [http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com](http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com)                             |
| Architecture page | [http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html](http://disputepoint-uibucket-nuoadlgtpdko.s3-website.ap-south-1.amazonaws.com/aws-arch.html) |
| Health smoke      | `GET …/health` → `{"ok":true,…}`                                                                                                                                                           |
| Queue smoke       | `GET …/points` → Okhla CONFLICT / `responsible_agency: null`                                                                                                                               |


Redeploy: `make deploy` (profile `disputepoint`). Cleanup after video: `sam delete --stack-name disputepoint --region ap-south-1 --profile disputepoint`.

## Checklist

- [x] Path chosen (Ship It)
- [x] Diagram on disk for screen share (`frontend/public/aws-arch.html` + hosted copy)
- [x] One live request visible (API Gateway `/health` + `/points`)
- [ ] No secrets on screen