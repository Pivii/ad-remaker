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

Skills define workflows. The central business Skill must orchestrate research, analysis, adaptation, approvals, production, quality control, and delivery. Service Skills explain the safe use of a specific integration.

A missing Skill must never be simulated. Source files supplied later must retain their provenance, be audited, and be adapted only when necessary.

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

### Scheduled jobs

The distribution currently provides no scheduled jobs. Any future routine must be shipped paused and must never trigger spending, publication, or campaign activation on its own.

## File ownership

The distribution owns `SOUL.md`, `config.yaml`, `skills/`, `cron/jobs.json`, and `distribution.yaml`. `config.yaml` is copied on install but preserved on `hermes profile update` unless `--force-config` is passed. Secrets, memories, sessions, local assets, brand data, and work outputs remain specific to each installation.
