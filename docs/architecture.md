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

`mcp.json` remains empty until a connection has been supplied and verified. Secrets are never versioned. An installed Skill does not prove that an MCP is authenticated or operational.

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

The distribution owns `SOUL.md`, `config.yaml`, `mcp.json`, `skills/`, `cron/jobs.json`, and `distribution.yaml`. Secrets, memories, sessions, local assets, brand data, and work outputs remain specific to each installation.
