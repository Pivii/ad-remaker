# ADR-003 - Ship the same content as a Claude Code plugin

## Status

Accepted on October 8, 2026 (issue #6).

## Context

Ad Remaker installs only as a Hermes profile (ADR-001). People without Hermes cannot use it. The Skills already follow the shared `SKILL.md` format in `skills/`, which is where a Claude Code plugin expects them, so the same repository can serve both runtimes without copying content.

Two parts do not carry over as is. Hermes reads the agent identity from `SOUL.md`, while Claude Code reads a subagent prompt from `agents/<name>.md`. Hermes reads MCP servers from `config.yaml` `mcp_servers`, each with `enabled: false`, while a Claude Code plugin reads `.mcp.json` and has no per-server `enabled` flag.

## Decision

The repository root is also a Claude Code plugin named `ad-remaker`:

- `.claude-plugin/plugin.json` is the manifest. Its `version` always equals `version` in `distribution.yaml`.
- `.claude-plugin/marketplace.json` lists this repository as a one-plugin marketplace, so `claude plugin marketplace add` and `claude plugin install` work from the private repository or a local clone. It is not a public marketplace.

  Update, October 8, 2026: the repository is now public, so the marketplace can be added without repository access. It is still not listed in any public plugin directory.
- `skills/` is loaded as is.
- `agents/ad-remaker.md` is the `ad-remaker` subagent. It is generated: its frontmatter is written by hand, and its body is `SOUL.md` verbatim. `scripts/sync_claude_agent.py` rewrites the body from `SOUL.md`, and `scripts/validate_distribution.py` fails when the body differs. `SOUL.md` stays the single source of the agent prompt; never edit the body of the subagent by hand.
- `.mcp.json` declares the same servers as `config.yaml` `mcp_servers`, under the same names and URLs, with no secrets. The validator fails when the two server sets or URLs differ.

## Consequences

- Both runtimes ship the same Skills and the same agent rules from one tree. A change to `SOUL.md` needs `python3 scripts/sync_claude_agent.py` in the same commit, or the validator fails. When two branches change `SOUL.md`, rerun the script after merging.
- A new MCP server must be declared in both `config.yaml` and `.mcp.json`.
- A Claude Code plugin's MCP servers start whenever the plugin is enabled. Every declared vendor server uses OAuth, so it stays unauthenticated, and unusable, until the user signs in. Users turn off the servers of vendors they do not pay for in `/mcp`, or block them with `deniedMcpServers` in their Claude Code settings (see `docs/claude-code-setup.md`). This replaces `enabled: false`, which only Hermes honors.
- In Claude Code 2.1.288, `${VAR}` and `${user_config.KEY}` are not expanded in a server's `oauth.clientId`: the literal text reached Meta's authorization URL. The `meta_ads` entry therefore has no `oauth` block. Without one, Claude Code obtained a client ID for `mcp.facebook.com/ads` by itself on 2026-10-08. Sign-in was not completed, so the server stays `configured` at most. Hermes still uses `META_APP_ID`.
- The subagent prompt is `SOUL.md` unchanged, including its first line, which calls the agent a Hermes agent. The Skills also mention Hermes-specific files such as `config.yaml`. Rewording either is a behavior change and out of scope here.
- Vendor Skills are installed by reference in Claude Code too, at the commit pinned in `skills/providers/SKILL.md` (ADR-002). The Hermes skills guard does not run in Claude Code, so `provider-policy` alone governs installing a vendor CLI.
- `claude plugin validate` warns that the root `CLAUDE.md` is not loaded as plugin context. That file is contributor guidance for this repository, not agent context, so the warning is expected.
