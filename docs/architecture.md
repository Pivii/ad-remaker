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
