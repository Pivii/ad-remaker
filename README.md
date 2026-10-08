<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/brand/logo-lockup-horizontal-dark.svg">
    <img src="docs/brand/logo-lockup-horizontal.svg" alt="Ad Remaker" width="400">
  </picture>
</p>

# Ad Remaker

Private working repository for an installable Hermes profile specialized in analyzing and adapting effective advertising concepts.

## Status

The repository was initialized from the operating report provided on October 7, 2026. That report documents the target architecture, business workflow, safeguards, proposed integrations, and their status at the time of observation. Historical availability statements in the report are not evidence of current tool or MCP availability.

Provider rules live in the local `provider-policy` Skill. Official vendor Skills are not bundled: each user installs only the vendors they pay for, at a pinned commit, with `scripts/install_provider_skills.sh` (see `docs/decisions/ADR-002-provider-skill-layers.md`).

## Established principles

- Analyze creative mechanics without copying an ad exactly.
- Separate observable facts, estimates, opinions, and unknowns.
- Do not generate paid content without a cost estimate and explicit approval.
- Do not publish, activate, schedule, or spend any budget without separate human approval.
- Remove every identifiable competitor trace from the final deliverable.
- Verify deliverables before reporting success.

## Repository structure

- `distribution.yaml`: profile-distribution manifest.
- `SOUL.md`: stable identity and non-negotiable safeguards.
- `config.yaml`: credential-free Hermes defaults, including the official vendor MCP servers under `mcp_servers`. Every server ships disabled; see `docs/architecture.md` to enable one.
- `cron/jobs.json`: distributed scheduled jobs. It is currently empty.
- `skills/`: the business workflow, the shared provider policy, and the `providers` routing directory with its vendor pin table.
- `docs/ad-remaker-complete-operating-report.md`: complete historical source report, translated into English.
- `docs/architecture.md`: distribution layering and ownership boundaries.
- `docs/service-matrix.md`: integration readiness states without unsupported availability claims.
- `docs/provenance/`: verbatim vendor source texts kept for provenance.
- `docs/decisions/`: architecture decisions.
- `docs/brand/`: logo files, the logo brief with its usage rules, and the showcase page design handoff.
- `scripts/validate_distribution.py`: local structural and safety validator.
- `scripts/install_provider_skills.sh`: installs pinned official vendor Skills into the profile, then runs `hermes skills audit`.
- `tests/`: acceptance guidance and redistributable fixtures.

## Validation

Run from any directory:

```bash
python3 /path/to/ad-remaker/scripts/validate_distribution.py
```

## Report source

[Ad Remaker report](https://sucqmcejnrnvcdnrwhld.supabase.co/storage/v1/object/public/published/3695/ad-remaker-fonctionnement/ad-remaker-fonctionnement-complet.md?v=1791399468681)
