# Service matrix

This document tracks expected capabilities without conflating the presence of a Skill, MCP configuration, authentication, and verified operation.

## Possible states

- `awaiting source`: the source still needs to be provided.
- `pending audit`: the source is available but has not been validated.
- `configured`: the connection is declared without proof that it works.
- `verified`: a real, non-destructive call succeeded.
- `blocked`: a dependency or authentication issue prevents use.

## Current state

Last reviewed on October 7, 2026. Provider Skills follow the two-layer split in ADR-002: local Skills hold the agent rules (`provider-policy`) and the routing directory (`providers`); official vendor Skills are installed by reference at a pinned commit and are not part of the distribution. The vendor source texts of the removed `*-usage` Skills are kept in `docs/provenance/`.

| Service | Skill | MCP |
|---|---|---|
| Business workflow `winning-ad-remake-workflow` | present, pending audit | not applicable |
| Shared rules `provider-policy` | present, pending audit | not applicable |
| Routing directory `providers` | present, pending audit | not applicable |
| Brandsearch | no official Skill; thin entry in `providers` | not configured |
| TrendTrack | no official Skill; `providers` links the official agent guide | not configured |
| Higgsfield | official Skill `higgsfield-generate` pinned, not installed by the distribution | not configured |
| Kie.ai | official Skills exist but cannot be pinned or installed by Hermes v0.20.2 | not configured |
| Pika | official Skill `ugc-ads` (Pika-Plugins) pinned, not installed by the distribution | not configured |
| fal.ai | official Skill `genmedia` pinned, not installed by the distribution; repository declares no license | not configured |
| Meta Ads | absent; slot reserved in `providers` (#5) | not configured |

A pinned vendor Skill is installed only when a user runs `scripts/install_provider_skills.sh`. Pins, licenses, and check dates live in the pin table of `skills/providers/SKILL.md`.

No service is `configured` or `verified`. With no MCP configured, the agent can only use native tools and free public sources.

The statuses in the source report are historical and specific to the environment observed when it was written. They are not presented as the current state of this profile.

## Update rule

Before changing a service to `verified`, record:

1. the integration source and version;
2. the authentication method without storing the secret;
3. the tools actually discovered;
4. a dated, non-destructive test;
5. costs and limits verified against their source;
6. expected behavior after a timeout or ambiguous result.
