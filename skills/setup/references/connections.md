# Selected-service connection guidance

Client commands checked headlessly on October 8, 2026: Claude Code 2.1.288, Hermes 0.20.2 and Codex CLI 0.160.0. Recheck the selected client's help and the provider's current official docs before configuration. These are connection procedures, not verified live provider integrations. The bundled service-readiness reference is generated from `docs/service-matrix.md`; provider routes/pins remain in sibling `providers`.

First inspect discovered tools and reported auth status without a provider operation. A previously working connection needs no new login. Tool discovery/auth alone establishes configured/authenticated at most; do not manufacture a cost-free test. If the current docs expose no known zero-credit non-destructive check, keep operation unverified. Never run paid research, media generation or account writes to test setup.

## Claude Code

1. Ask the user to open `/mcp`, select the existing `plugin:ad-remaker:<server>` entry and authenticate in the browser when they choose a service. Names declared here: trendtrack, higgsfield, pika, fal, meta_ads. Login requires the user's browser interaction; the agent must not fill credentials or claim it completed on their behalf.
2. Reinspect reported status and discovered tools; explain a failed or cancelled login and keep the chosen preference pending. Offer retry, deferred configuration or explicit free fallback.
3. Do not alter distributed `.mcp.json` or store personal settings in the plugin cache. Plugin entries have no Hermes `enabled: false` semantics. Unwanted services can be disabled through `/mcp` or denied in user settings, as the existing README documents.

Source: [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp#authenticate-with-remote-mcp-servers).

## Hermes

1. Identify the profile the user launched and its actual configuration path with `hermes -p <profile> config path`. Read only relevant server configuration, without exposing secrets. Show the exact proposed change `mcp_servers.<chosen-server>.enabled: true` for that installed profile and obtain approval before applying it. Never modify the source distribution, defaults or another profile.
2. A reviewed command uses `hermes -p <profile> config set mcp_servers.<chosen-server>.enabled true`. The user then runs `hermes -p <profile> mcp login <chosen-server>` and completes browser authentication. Keep credentials in Hermes storage. Meta additionally requires the user's own app/client configuration; no Meta setup during ordinary competitor research.
3. Inspect `hermes -p <profile> mcp list` and discovered tools in a fresh session. `hermes -p <profile> mcp test <chosen-server>` is a client connection test, not proof of a billable operation or a blanket instruction to invoke vendor tools. Verify its behavior before suggesting it; do not call an unknown vendor health/tool endpoint. Report configured/unverified unless the zero-cost verification contract is known.

Source: [Hermes MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp/). Local command help confirms config set, mcp login/list/test on the tested version. Runtime approval remains in force for configuration changes and installations.

## Codex CLI and Desktop

The package bundles **no MCP servers** (ADR-005). Users deliberately configure selected providers in their own Codex configuration. Shared CLI/Desktop configuration depends on the actual client configuration home; do not assume different homes share login.

1. Inspect the selected client's `codex mcp list`/`codex mcp get <server>` and actual session tools, without exposing credential files. If already configured and working, reuse it. Do not add duplicate entries.
2. For a declared OAuth endpoint, verify it in current official vendor docs. Show the exact user-owned addition before execution. Example for a selected TrendTrack route: `codex mcp add trendtrack --url https://api.trendtrack.io/v1/mcp`. The user approves deliberate configuration and runs `codex mcp login trendtrack` to complete browser authentication. The CLI supports these commands on 0.160.0; this is not evidence that each vendor's OAuth works.
3. Inspect session tool discovery after restarting or refreshing the client. Failed/cancelled auth stays pending, with no saved free replacement. Desktop GUI connection/selection interactions and live vendor OAuth are unverified here; use explicit setup invocation when automatic selection is absent.

Source: [official Codex MCP guide](https://learn.chatgpt.com/docs/extend/mcp?surface=cli). Endpoint sources are in the generated service-readiness reference. For Kie.ai REST or a user-provided Brandsearch connection, use the provider's documented user-owned route; never invent an MCP entry. No API key, token or password belongs in chat or a product brief.
