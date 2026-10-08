# Service matrix

This document tracks expected capabilities without conflating the presence of a Skill, MCP configuration, authentication, and verified operation.

## Possible states

- `awaiting source`: the source still needs to be provided.
- `pending audit`: the source is available but has not been validated.
- `configured`: the connection is declared without proof that it works.
- `verified`: a real, non-destructive call succeeded.
- `blocked`: a dependency or authentication issue prevents use.

## Current state

Last reviewed on October 8, 2026. Provider Skills follow the two-layer split in ADR-002: local Skills hold the agent rules (`provider-policy`) and the routing directory (`providers`); installable official vendor Skills are installed by reference at a pinned commit and are not part of the distribution. The vendor source texts of the removed `*-usage` Skills are kept in `docs/provenance/`.

| Service | Skill | MCP |
|---|---|---|
| Business workflow `winning-ad-remake-workflow` | present, pending audit | not applicable |
| Shared rules `provider-policy` | present, pending audit | not applicable |
| Routing directory `providers` | present, pending audit | not applicable |
| Free fallback `free-fallback-mode` (local scripts, no provider) | present, pending audit | not applicable |
| Brandsearch | no official Skill; thin entry in `providers` | not declared: a hosted MCP exists, but its endpoint is not public |
| TrendTrack | no official Skill; `providers` links the official agent guide | configured, disabled by default |
| Higgsfield | thin entry; official Skill `higgsfield-generate` pinned as a source to read, blocked by the Hermes v0.20.2 skills guard | configured, disabled by default |
| Kie.ai | official Skills exist but cannot be pinned or installed by Hermes v0.20.2 | not declared: no official MCP server |
| Pika | official Skill `ugc-ads` (Pika-Plugins) pinned and installable with the script; install verified in a scratch profile on 2026-10-08 | configured, disabled by default |
| fal.ai | thin entry; official Skill `genmedia` pinned as a source to read, blocked by the Hermes v0.20.2 skills guard; repository declares no license (accepted) | configured, disabled by default |
| Meta Ads | absent; slot reserved in `providers` (#5) | configured, disabled by default |

A pinned vendor Skill is installed only when a user runs `scripts/install_provider_skills.sh`, and only for rows whose `Install` is `hermes`. An installed Skill is not a connection, and neither is a declared MCP server: see the next paragraph. Pins, licenses, and check dates live in the pin table of `skills/providers/SKILL.md`.

No service is `verified`. `configured` means only that the server is declared in `config.yaml` `mcp_servers` with `enabled: false`; no live connection has been tested. Until a user enables and authenticates a server, the agent can only use native tools and free public sources, following `free-fallback-mode`. Its local analysis scripts need `ffmpeg` and PySceneDetect installed on the host; the distribution does not install them.

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
