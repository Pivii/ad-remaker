# Ad Remaker

Private working repository for an installable Hermes profile specialized in analyzing and adapting effective advertising concepts.

## Status

The repository was initialized from the operating report provided on October 7, 2026. That report documents the target architecture, business workflow, safeguards, proposed integrations, and their status at the time of observation. Historical availability statements in the report are not evidence of current tool or MCP availability.

Provider Skills may be added and audited separately when their source files and provenance are available.

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
- `skills/`: business and provider operating procedures.
- `docs/ad-remaker-complete-operating-report.md`: complete historical source report, translated into English.
- `docs/architecture.md`: distribution layering and ownership boundaries.
- `docs/service-matrix.md`: integration readiness states without unsupported availability claims.
- `scripts/validate_distribution.py`: local structural and safety validator.
- `tests/`: acceptance guidance and redistributable fixtures.

## Validation

Run from any directory:

```bash
python3 /path/to/ad-remaker/scripts/validate_distribution.py
```

## Report source

[Ad Remaker report](https://sucqmcejnrnvcdnrwhld.supabase.co/storage/v1/object/public/published/3695/ad-remaker-fonctionnement/ad-remaker-fonctionnement-complet.md?v=1791399468681)
