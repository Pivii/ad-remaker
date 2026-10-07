# Service matrix

This document tracks expected capabilities without conflating the presence of a Skill, MCP configuration, authentication, and verified operation.

## Possible states

- `awaiting source`: the source still needs to be provided.
- `pending audit`: the source is available but has not been validated.
- `configured`: the connection is declared without proof that it works.
- `verified`: a real, non-destructive call succeeded.
- `blocked`: a dependency or authentication issue prevents use.

## Initial state

- Business workflow `winning-ad-remake-workflow`: awaiting source.
- Brandsearch: Skill awaiting source, MCP not configured.
- TrendTrack: Skill awaiting source, MCP not configured.
- Higgsfield: Skill awaiting source, MCP not configured.
- Kie.ai: Skill awaiting source, MCP not configured.
- Pika: Skill awaiting source, MCP not configured.
- fal.ai: Skill awaiting source, MCP not configured.
- Meta Ads: no integrated Skill or connection.

The statuses in the source report are historical and specific to the environment observed when it was written. They are not presented as the current state of this profile.

## Update rule

Before changing a service to `verified`, record:

1. the integration source and version;
2. the authentication method without storing the secret;
3. the tools actually discovered;
4. a dated, non-destructive test;
5. costs and limits verified against their source;
6. expected behavior after a timeout or ambiguous result.
