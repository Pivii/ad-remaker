# Architecture decisions

This directory contains durable decisions that change Ad Remaker's structure or behavior.

Recommended format for each decision:

```markdown
# ADR-NNN - Title

## Status
Proposed, accepted, superseded, or abandoned.

## Context
Why the decision is necessary.

## Decision
What was selected.

## Consequences
Benefits, costs, limits, and any migration work.
```

Accepted decisions:

- `ADR-001-profile-distribution.md`: distribute Ad Remaker as a Hermes profile.
- `ADR-002-provider-skill-layers.md`: keep provider policy local and install pinned official vendor Skills.
- `ADR-003-claude-code-plugin.md`: ship the same content as a Claude Code plugin, with `SOUL.md` as the single source of the subagent prompt.
