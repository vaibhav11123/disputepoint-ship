# V2 Wireframes — grayscale gate (F10)

**Protocol (NN/g 5-second + first-click):** Show each frame ≤5s. Ask: What is this for? First-click task: “Find the disputed incident that needs a human.”

**Release gate:** Do not treat hi-fi UI as done until **≥2/2** blind testers identify (1) disputed incident (2) human-review need (3) next action.

Catalog ids on every frame: F10-01, F10-02, F10-03.

## Frame 1 — Command `[F1]`

```
DISPUTEPOINT · DISTRICT OPERATIONS · NEW DELHI · RAINFALL SCENARIO
ACTIVE  HIGH  DISPUTED  AWAITING YOU

| # | Location        | Pri | State                 | Agency    |
| 1 | Purana Quila…   | H   | RESPONSIBILITY DISPUTED | MCD↔PWD |
| 2 | …               |     |                       |           |

[ MAP ~45% muted Delhi pins ]
```

## Frame 2 — Incident `[F2]`

```
PURANA QUILA  ·  HIGH  ·  RESPONSIBILITY DISPUTED
MCD ↔ PWD  ·  NO AUTO-ASSIGNMENT
Effect: competing claims — exclusive responsibility not established
[ ESCALATE FOR HUMAN REVIEW ]
Event rail: RECEIVED → … → DISPUTED
```

## Frame 3 — Evidence `[F3]`

```
CASE EVIDENCE
CLAIM MCD → SOURCE → EXTRACT → POINT → Supports MCD · NOT exclusive
CLAIM PWD → … → Supports PWD · NOT exclusive
WHAT WOULD RESOLVE THIS? □ jurisdiction □ drain □ maintenance □ agency □ field
```

## Frame 4 — Coordination `[F5]`

```
HUMAN REVIEW REQUIRED
Reason: Competing claims + no exclusive responsibility
Route: District EOC → IC → Agency → Engineering
NEXT ACTION: Confirm operational responsibility
[ COPY BRIEF ]  Official channels ▸
```

## Frame 5 — Audit `[F4]`

```
HUMAN DECISION
Incident DP-…  ASSIGN TO MCD  Actor: INCIDENT COMMANDER
Reason: …  Evidence: n  Audit: AUD-…
Timeline: …
```

## Frame 6 — Demo `[F6]`

```
(no ops chrome)
RAIN → QUEUE REORDER → MAP → PURANA → WE DON’T GUESS → EVIDENCE → HUMAN → AUDIT
```

## Gate record

| Tester | Date | Disputed? | Human review? | Next action? | Pass |
|--------|------|-----------|---------------|--------------|------|
| _TBD_ | | | | | |
| _TBD_ | | | | | |
