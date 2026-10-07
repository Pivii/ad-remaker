# Service matrix

This document tracks expected capabilities without conflating the presence of a Skill, MCP configuration, authentication, and verified operation.

## Possible states

- `awaiting source`: the source still needs to be provided.
- `pending audit`: the source is available but has not been validated.
- `configured`: the connection is declared without proof that it works.
- `verified`: a real, non-destructive call succeeded.
- `blocked`: a dependency or authentication issue prevents use.

## Current state

Last reviewed on October 7, 2026. Each provider Skill is the Hermes adaptation of the supplied vendor source, kept in `references/upstream.md`.

| Service | Skill | MCP |
|---|---|---|
| Business workflow `winning-ad-remake-workflow` | present, pending audit | not applicable |
| Free fallback `free-fallback-mode` (local scripts, no provider) | present, pending audit | not applicable |
| Brandsearch | present, pending audit | not configured |
| TrendTrack | present, pending audit | not configured |
| Higgsfield | present, pending audit | not configured |
| Kie.ai | present, pending audit | not configured |
| Pika | present, pending audit | not configured |
| fal.ai | present, pending audit | not configured |
| Meta Ads | absent | not configured |

No service is `configured` or `verified`. With no MCP configured, the agent can only use native tools and free public sources, following `free-fallback-mode`. Its local analysis scripts need `ffmpeg` and PySceneDetect installed on the host; the distribution does not install them.

The statuses in the source report are historical and specific to the environment observed when it was written. They are not presented as the current state of this profile.

## Update rule

Before changing a service to `verified`, record:

1. the integration source and version;
2. the authentication method without storing the secret;
3. the tools actually discovered;
4. a dated, non-destructive test;
5. costs and limits verified against their source;
6. expected behavior after a timeout or ambiguous result.
