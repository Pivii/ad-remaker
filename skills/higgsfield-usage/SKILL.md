---
name: higgsfield-usage
description: Use when generating or editing media with Higgsfield, if authenticated Higgsfield tools or API credentials are available.
---

# Higgsfield usage

Proceed only if authenticated Higgsfield tools are available or supported Higgsfield API credentials are already configured. Do not invent configuration or request credentials in chat.

1. Prefer available authenticated tools; inspect their current catalog and schemas before choosing a model.
2. If using the API, consult the current official model documentation for the endpoint and exact request schema. Never guess fields or construct status URLs.
3. Before submission, state the model, units, and estimated cost and obtain explicit approval.
4. Submit once. After an ambiguous timeout, do not repeat a generation request that lacks idempotency protection.
5. Poll the returned status URL with backoff until a terminal state. Use the returned cancel URL when cancellation is requested and supported.
6. Upload local inputs only with the service’s current upload flow, keeping Higgsfield credentials away from third-party upload hosts.
7. Download outputs that must outlive hosted retention.
8. Write prompts as shot descriptions and preserve character or seed continuity when the selected model supports it.
9. Treat model names, balances, retention periods, endpoints, error semantics, and tool availability in the upstream document as historical guidance until verified against current official documentation or live tool schemas.

See the verbatim [upstream source](references/upstream.md) for provenance and service-specific details.
