---
name: provider-policy
description: Use before and during any call to an external provider (Brandsearch, TrendTrack, Higgsfield, Kie.ai, Pika, fal.ai, Meta Ads, or any vendor Skill), including research queries that consume credits and paid generation. Defines the shared rules for authentication checks, spend approval, retries, batches, and output retention.
---

# Provider policy

These rules apply to every external provider, whatever the route (MCP tools, CLI, or REST) and whether or not an official vendor Skill is installed. When an installed vendor Skill conflicts with this policy, this policy wins. Use `providers` to find the official source and route order for a vendor.

## 1. Verify before use

1. Use a provider only if its tools are present in the current session and authenticated, or its documented credentials are already configured in the environment. Never ask for credentials in chat and never invent configuration.
2. Inspect the live tool list, model catalog, and input schema before choosing a model or building a request. Never guess fields, endpoint identifiers, or status URLs; use the handles the service returns.
3. Treat model names, prices, counts, coverage, retention periods, and tool names from vendor documents, installed vendor Skills, and `docs/provenance/` as claims to verify against the live tools or current official documentation.

4. Installing a vendor tool (a CLI, a package, or an installer such as `curl ... | sh`) requires the user's explicit approval of that exact command. Use only the install command recorded in the vendor's `providers` entry. Never run it in yolo mode or with approvals turned off; in that case, stop and give the user the command to run themselves. Hermes runtime approval flags piping remote content to a shell as dangerous, and that prompt must be answered by the user, not bypassed.

## 2. When nothing is connected

If no provider is available for a stage, say so explicitly and switch to the free path in `free-fallback-mode`: native tools, local processing, and free public sources. A server declared in `config.yaml` with `enabled: false` is not available. Never claim a capability that is not connected, such as private metrics, ROAS, or rendering.

## 3. Approval before spend

1. Before any call that consumes credits or money (generation, paid AI analysis or transcription, metered research rows), present the cost quote defined in step 4 of `winning-ad-remake-workflow` and wait for explicit approval of that exact batch.
2. Generate one variant first unless the user approved a larger batch. Never expand an approved batch.
3. Reuse an existing asset when the prompt and the required output have not changed.
4. Never retry a failed or unsatisfactory call silently. Present a new estimate and obtain new approval first.
5. After an ambiguous timeout, check the request status before doing anything else. Never resubmit a request that has no idempotency protection, because it can bill twice.

## 4. Running and keeping outputs

1. For asynchronous jobs, poll the returned status handle with backoff until a terminal state. Use the returned cancel handle when cancellation is requested and supported.
2. Upload local inputs only through the service's authenticated upload flow. Never send provider credentials to a third-party host.
3. Download every output that must persist into the workspace. Hosted URLs expire.

## 5. Writes on provider accounts

Before any write to a provider account (folders, trackers, favorites, campaigns), confirm the target and scope. Never invoke a destructive operation or pass a confirmation flag unless the user explicitly asked for that deletion; prefer non-destructive options when they exist.
