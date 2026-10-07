# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Layout

Single-context repo:

```
/
├── CONTEXT.md              ← domain glossary (created lazily)
├── SOUL.md                 ← agent identity and non-negotiable rules
├── docs/decisions/         ← ADRs, named ADR-NNN-<slug>.md
│   └── ADR-001-profile-distribution.md
└── skills/<name>/SKILL.md
```

ADRs live in `docs/decisions/`, not `docs/adr/`. Follow the format in `docs/decisions/README.md` and number new decisions `ADR-NNN`.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root.
- **`docs/decisions/`**: read ADRs that touch the area you're about to work in.

If `CONTEXT.md` doesn't exist, **proceed silently**. Don't flag its absence; don't suggest creating it upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates it lazily when terms or decisions actually get resolved.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal. Either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-001 (profile distribution), but worth reopening because…_
