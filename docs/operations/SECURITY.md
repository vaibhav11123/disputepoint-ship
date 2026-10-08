# Security (MVP / hackathon)

Condensed from [HLD.md](../HLD.md) §6 and Phase 6 NFRs. Scoped to a **single-tenant public-read demo** — not a production multi-tenant control plane.

## Posture

| Topic | MVP choice |
|-------|------------|
| Auth | None (Cognito out). Document the risk. |
| Tenancy | Single demo officer persona |
| Secrets | Env / SSM only; never commit `.env` (NFR-004) |
| CORS | Localhost + deployed origin only |
| Bedrock | Off — fixtures-only evidence |

## OWASP API Top 10 2023 — yellow map

Source: [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-toc/).

| Risk | DisputePoint MVP response |
|------|---------------------------|
| API1 BOLA | Point ids are fixture-scoped; no cross-tenant IDs. Still validate `id` pattern `^dp-[a-z0-9-]+$`. |
| API2 Broken auth | N/A auth — mitigate by short-lived demo URL + no PII secrets in API. |
| API3 Property auth | Return public fields only; do not expose raw secrets or internal keys. |
| API4 Resource consumption | Tiny fixture set (~12–15 points); rain poll ≥5–15 min; no per-keystroke LLM. |
| API5 Function auth | HITL mutations are demo-open; accept risk; no admin backdoor routes. |
| API6 Sensitive flows | OVERRIDE/ACK are advisory; no payment/scalping flows. |
| API7 SSRF | Do not proxy arbitrary URLs from client; Open-Meteo URL is locked in LLD. |
| API8 Misconfig | CORS allowlist; no debug endpoints in deploy; OpenAPI is inventory (API9). |
| API9 Inventory | Frozen [openapi.yaml](../openapi.yaml) — nine routes only. |
| API10 Unsafe consumption | Validate Open-Meteo JSON; timeout + cache/slider fallback; never trust rain blindly. |

## Explicit non-goals

- Full OAuth / Cognito
- WAF / bot management (optional later)
- Encrypting fixture JSON at rest beyond platform defaults

## References

- [OWASP API Security Project](https://owasp.org/www-project-api-security/)
- [HLD.md](../HLD.md) §6
