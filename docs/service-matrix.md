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
| Brandsearch | present, pending audit | not declared: a hosted MCP exists, but its endpoint is not public |
| TrendTrack | present, pending audit | configured, disabled by default |
| Higgsfield | present, pending audit | configured, disabled by default |
| Kie.ai | present, pending audit | not declared: no official MCP server |
| Pika | present, pending audit | configured, disabled by default |
| fal.ai | present, pending audit | configured, disabled by default |
| Meta Ads | absent | configured, disabled by default |

No service is `verified`. `configured` means only that the server is declared in `config.yaml` `mcp_servers` with `enabled: false`; no live connection has been tested. Until a user enables and authenticates a server, the agent can only use native tools and free public sources.

## Declared MCP servers

Each server is declared in `config.yaml` under the name shown, with `enabled: false`. Endpoints and authentication methods were checked against the vendor's official documentation on October 7, 2026. They are dated snapshots: check again before relying on them.

| Service | Name | Endpoint | Authentication | Official source | Checked |
|---|---|---|---|---|---|
| TrendTrack | `trendtrack` | `https://api.trendtrack.io/v1/mcp` | OAuth 2.1 with PKCE (an API key is also offered) | https://docs.trendtrack.io/connect/manus | 2026-10-07 |
| Higgsfield | `higgsfield` | `https://mcp.higgsfield.ai/mcp` | OAuth, no API key; generation spends plan credits | https://higgsfield.ai/creator-hub/help-center/mcp-cli/what-is-higgsfield-mcp | 2026-10-07 |
| Pika | `pika` | `https://mcp.pika.me/api/mcp` | OAuth (a `dk_` developer key is also offered) | https://github.com/Pika-Labs/Pika-Plugins | 2026-10-07 |
| fal.ai | `fal` | `https://mcp.fal.ai/mcp-relay` | OAuth | https://fal.ai/docs/documentation/setting-up/mcp/other-clients | 2026-10-07 |
| Meta Ads | `meta_ads` | `https://mcp.facebook.com/ads` | OAuth through the user's own Meta app; its app ID is the OAuth client ID (`META_APP_ID`) | https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started | 2026-10-07 |

Before declaring a new server, record its official source and check date in this table, ship it with `enabled: false`, and keep secrets out of `config.yaml`. `scripts/validate_distribution.py` enforces the last two.

The statuses in the source report are historical and specific to the environment observed when it was written. They are not presented as the current state of this profile.

## Update rule

Before changing a service to `verified`, record:

1. the integration source and version;
2. the authentication method without storing the secret;
3. the tools actually discovered;
4. a dated, non-destructive test;
5. costs and limits verified against their source;
6. expected behavior after a timeout or ambiguous result.
