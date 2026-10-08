# AWS demo beat (W9) — on camera 2:00–2:30

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
UI (S3 / CloudFront)
        │
        ▼
   API Gateway
        │
        ▼
     Lambda  ──► DynamoDB (points / audit)
        │
        ├──► S3 (fixtures / static)
        └──► EventBridge (rain schedule)
                │
                ▼
            CloudWatch logs
```

## Operator pointers

- [AWS_OPERATOR.md](../operations/AWS_OPERATOR.md)
- [DEPLOYMENT.md](../operations/DEPLOYMENT.md)
- [DEMO_REHEARSAL.md](DEMO_REHEARSAL.md) dual path

## Checklist

- [ ] Path chosen (Ship It / Build It)
- [ ] Diagram on disk for screen share
- [ ] One live request visible
- [ ] No secrets on screen
