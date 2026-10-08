# Architecture

## Overview

```text
User
  -> ad-remaker Hermes profile
     -> SOUL.md: identity and global safeguards
     -> Skills: business procedures and usage rules
     -> native tools: web, browser, files, vision, terminal
     -> MCP: explicitly configured external services
     -> scripts: deterministic local processing
     -> local workspace: private brands, assets, memory, and sessions
  -> human approval before spending or external action
```

## Layers

### Profile

The profile isolates Ad Remaker's configuration, Skills, connections, memory, sessions, and scheduled jobs. It must not share its profile directory with another active agent.

### Identity

`SOUL.md` contains the mission and rules that apply to every assignment. It intentionally remains shorter than the business procedures.

### Skills

Skills define workflows, in two layers (ADR-002).

- Agent layer, distributed: the central business Skill orchestrates research, analysis, adaptation, approvals, production, quality control, and delivery. `provider-policy` holds the rules shared by every provider call, and `providers` routes each vendor to its official source.
- Vendor layer, installed per user: official vendor Skills, installed by reference at a pinned commit with `scripts/install_provider_skills.sh` and re-scanned with `hermes skills audit`. They are not copied into the distribution, and `provider-policy` takes precedence over them. A vendor whose Skill the Hermes skills guard blocks stays a thin entry in `providers`: the agent reads the pinned Skill as documentation, and the user installs the vendor CLI with approval.

A missing Skill must never be simulated. Source texts keep their provenance: the workflow's in `references/upstream.md`, the vendors' in `docs/provenance/`.

### MCP

Hermes reads MCP servers from the profile `config.yaml`, under `mcp_servers`. It does not read a root `mcp.json` in a profile, so the distribution does not ship one.

`config.yaml` declares one entry per vendor with a public official endpoint, each with `enabled: false`. Each user enables only the vendors they pay for. The sources and check dates are in `docs/service-matrix.md`.

Secrets are never versioned. Servers authenticate with OAuth, or with `${ENV_VAR}` placeholders that Hermes resolves from the installed profile's own `.env`. Every placeholder is declared in `distribution.yaml` `env_requires` with `required: false`. Hermes turns that list into a `.env.EXAMPLE` on install.

To enable a server in an installed profile:

1. In the installed profile's `config.yaml`, set `enabled: true` on that server.
2. If the server uses a placeholder, set the variable in the profile's `.env`. For example, `meta_ads` needs `META_APP_ID`: the ID of your own Meta app.
3. Run `hermes -p ad-remaker mcp login <name>` to complete OAuth, then `hermes -p ad-remaker mcp test <name>`.

`hermes profile update` preserves the installed `config.yaml` unless `--force-config` is passed. Servers declared in a later release therefore do not reach existing installs automatically. `--force-config` replaces the whole file, including any server the user enabled, so it resets those servers to disabled. To pick up a new server without that reset, copy its entry from this repository's `config.yaml` into the installed one.

An installed Skill does not prove that an MCP is authenticated or operational. A declared server is `configured` at most until it passes the update rule in `docs/service-matrix.md`.

### Scripts

Scripts make deterministic operations reproducible, such as frame extraction, contact sheets, media normalization, and pack validation. Scripts owned by a Skill live in that Skill's `scripts/` directory. Root repository scripts support development and distribution validation.

### Brand data

Brand-specific data is not part of the generic distribution. An installation may keep it under `local/brands/<brand>/`, which is ignored by Git and preserved across updates.

Suggested structure:

```text
local/brands/<brand>/
├── brand.md
├── products.md
├── claims.md
├── audiences.md
├── competitors.md
└── assets/
```

### Claude Code plugin

The repository root is also a Claude Code plugin (ADR-003). It reuses `skills/` unchanged and adds four files:

- `.claude-plugin/plugin.json`: the manifest. Its `version` equals `distribution.yaml`.
- `.claude-plugin/marketplace.json`: a one-plugin marketplace pointing at the repository root, so the plugin installs with `claude plugin install ad-remaker@ad-remaker`.
- `agents/ad-remaker.md`: the `ad-remaker` subagent. Its body is `SOUL.md`, written by `scripts/sync_claude_agent.py`.
- `.mcp.json`: the same vendor servers as `config.yaml` `mcp_servers`, under the same names and URLs.

Claude Code starts a plugin's MCP servers whenever the plugin is enabled; there is no per-server `enabled: false`. Every declared server uses OAuth and stays unauthenticated until the user signs in. Users turn off the vendors they do not pay for in `/mcp` or with `deniedMcpServers` (see `README.md`). `scripts/validate_distribution.py` fails when the subagent body differs from `SOUL.md`, when the two MCP declarations differ, or when the plugin version differs from `distribution.yaml`.

### Codex CLI and Desktop plugin

Codex reuses the same canonical `skills/` tree (ADR-005). `.codex-plugin/plugin.json` has the same identity/version as the profile and an explicit empty MCP mapping, overriding Claude's declarations on the tested CLI. It does not load the Claude subagent as a global persona. Every Skill first loads its generated `references/agent-rules.md` plus applicable sibling policies; `scripts/sync_skill_rules.py` and validation keep the rules identical to `SOUL.md`.

Local installation consumes the tracked-file allowlisted export from `scripts/export_codex_package.py`, never a live development clone. Private Git installation consumes a clean Git snapshot. Brand data, sessions, outputs and credentials belong outside the package/cache. Contributor context is not operating context; start tasks from the user's working project.

Vendor MCP servers and vendor Skills are optional per user and not bundled into Codex. The plugin starts no vendor servers; existing user tools can still be present. Users explicitly add/disable/remove the desired server in Codex configuration and authenticate separately. No Codex OAuth/Meta client-ID behavior or live provider capability is verified by parsing its configuration. FFmpeg remains Claude-only under ADR-004. CLI and Desktop are required targets. Headless checks of the Desktop-bundled backend are distinct from actual Plugins Directory/composer verification; the latter remains required before issue #22 is complete. Exact commands, tested versions, and remaining surface checks are in `README.md` and `tests/README.md`.

### Scheduled jobs

The distribution currently provides no scheduled jobs. Any future routine must be shipped paused and must never trigger spending, publication, or campaign activation on its own.

## File ownership

The distribution owns `SOUL.md`, `config.yaml`, `skills/`, `cron/jobs.json`, and `distribution.yaml`. The plugin files (`.claude-plugin/`, `.codex-plugin/`, `agents/`, `.mcp.json`) are derived from them and checked by the validator. `config.yaml` is copied on install but preserved on `hermes profile update` unless `--force-config` is passed. Secrets, memories, sessions, local assets, brand data, and work outputs remain specific to each installation.

## Guided setup and private state

The sixth shared Skill, `setup`, offers first-use routes before research and retains the original task. Its deterministic helper persists non-secret choices separately from canonical-project-keyed product context outside distributed files and Git. Canonical rules require this check; explicit invocation remains available when implicit Skill selection is absent. The service-readiness reference is generated from the service matrix for Skills-only installs. See [ADR-006](decisions/ADR-006-guided-setup-state.md) and [setup](setup.md). Connections, operation approvals and existing vendor ownership remain separate.
