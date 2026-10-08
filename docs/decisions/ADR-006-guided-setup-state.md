# ADR-006 - Guided first use with private preferences and product state

## Status

Accepted implementation decision for issue #25 on October 8, 2026.

## Context

An installed Skill or declared provider does not tell a newcomer which services are optional. An unconditional missing-provider fallback hides that choice. Conversation memory alone cannot preserve a free preference across sessions, distinguish products, or resume partial onboarding.

## Decision

Add a shared `setup` Skill and standard-library private-state helper. Advertising entrypoints load settings before research. First relevant use or explicit setup offers free, existing services or stage choices, in batches of at most three questions. Installation does not execute a model or authentication. Completed settings suppress onboarding; skip-for-now leaves setup incomplete. Preserve the original request and partial answers, then resume it. A free selection completes setup without connecting a service and produces research/analysis or a remake pack, not a new video rendered from prompts.

Schema 1 preferences live under `${XDG_CONFIG_HOME:-~/.config}/ad-remaker/<claude|codex>/setup.json`, or `<active-installed-Hermes-profile>/ad-remaker-state/setup.json`. Explicit private `--state-dir` supports user-selected storage and scratch tests. Within that runtime root, a canonical-project-path SHA-256 selects `projects/<hash>.json`; each product has its own confirmed brief and optional route overrides. This keeps all runtime data outside product Git and distributed/cache Skill directories without editing Git ignores. Hermes state remains profile-local, alongside installed runtime files rather than within managed `skills/`.

Persist only stage routes, completion, fallback choice, dated non-secret connection metadata, confirmed product context and a non-secret pending task. Credentials stay in client storage. A restrictive schema and obvious token rejection reduce accidental input; they cannot prove arbitrary free text contains no secret. Apply task choice over product override over user/profile preference. Explicit free always wins at its chosen scope. Stored verification is never current authentication; recheck actual tools and permitted zero-credit status before each affected stage.

The helper atomically writes private files under a per-root lock, rejects symlink state paths and refuses distribution/cache targets. Read-only status never creates state. Corrupt, unknown-version and malformed files are preserved and reported; no automatic destructive reset or guessed legacy migration. Recover with a fresh private root or a reviewed migration with backup. Schema 1 is the first contract, so existing installs receive the choices once rather than being opted into free. Settings survive plugin replacement and Hermes profile updates because those do not manage this private root. Directory moves deliberately create a new workspace key; automatic cross-product matching is excluded.

Provider selection is separate from connection and operation approval. Reuse actual working connections; guide only selected services with current client/vendor docs. Pending/cancelled auth stays pending. A declared route with no known cost-free check remains configured/unverified. Setup never performs research calls, generation or provider writes. Existing exact-operation approvals remain mandatory.

## Consequences

- Six shared Skills and their generated `SOUL.md` references serve Hermes, Claude Code and Codex. The setup service-readiness reference is generated from `docs/service-matrix.md` so a clean Skills-only Codex package retains the dated source without maintaining a second matrix.
- ADR-002 vendor ownership/pins and ADR-003 shared content remain intact. ADR-005 Codex still bundles no MCP; Claude declarations are unchanged; Hermes connection changes are reviewed in the active installed profile only.
- A wizard is an operating Skill, not a universal installation hook. Implicit selection depends on runtime/model discovery. Explicit invocation is documented and tested separately; ordinary coding requests do not need onboarding.
- Users can edit tools, product context or both independently. A provider failure cannot silently rewrite preference. Authorized free fallback is announced, otherwise ask for the affected task only.
- Test guards permit only exact installed instruction reads and validated helper argument vectors confined to scratch roots. All other execution and real providers remain blocked before dispatch. Headless checks do not prove Desktop GUI selection, OAuth success or live vendor operation.
