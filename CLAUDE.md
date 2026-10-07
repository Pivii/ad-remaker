@AGENTS.md

# Working on this repository

This repository is the source of the Ad Remaker agent, packaged as a Hermes profile distribution. You are editing the agent, not acting as it. Read `SOUL.md` and the Skills to understand the agent's behavior, but do not adopt its persona while working here.

## What the agent does

Ad Remaker finds competitor ads that show public performance signals, deconstructs their creative mechanics, and adapts them to a given brand's real product. It never copies an ad exactly, never invents claims, and never spends money or publishes anything without explicit human approval.

## Where things live

| Path | Role | Format owner |
|---|---|---|
| `distribution.yaml` | Profile manifest (name, version, Hermes version) | Hermes |
| `SOUL.md` | Agent identity and non-negotiable rules | Hermes |
| `config.yaml` | Credential-free Hermes defaults | Hermes |
| `mcp.json` | Declared MCP servers, empty until one is verified | Hermes |
| `cron/jobs.json` | Distributed scheduled jobs, currently none | Hermes |
| `skills/<name>/SKILL.md` | Operational Skill (YAML frontmatter `name` + `description`) | Agent Skills standard |
| `skills/<name>/references/upstream.md` | Source Skill text as supplied, kept for provenance | Do not edit |
| `docs/ad-remaker-complete-operating-report.md` | Translated historical report, dated October 7, 2026 | Source material, do not rewrite |
| `docs/service-matrix.md` | Integration readiness per service | Update when a status changes |
| `scripts/validate_distribution.py` | Structural and safety validator | Keep in sync with required files |

## Skills

- `winning-ad-remake-workflow` is the central business Skill. It orchestrates research, analysis, cost approval, generation, QC, delivery, and the paused Meta campaign gate.
- The six `*-usage` Skills (Brandsearch, TrendTrack, Higgsfield, Kie.ai, Pika, fal.ai) describe how to use one provider safely. Each is conditional: it applies only when that provider's tools are available and authenticated.
- When editing a Skill, change `SKILL.md` only. Keep `references/upstream.md` verbatim and keep the link to it at the bottom of `SKILL.md`.
- Treat model names, prices, tool counts, and connection states from upstream files and the report as historical until verified.

## Rules when changing the distribution

- Never commit secrets, tokens, `.env` files, brand data, customer data, generated media, memories, or sessions. Installation-specific brand data belongs in `local/brands/<brand>/`, which is gitignored.
- Do not add an MCP server to `mcp.json` or mark a service `verified` in `docs/service-matrix.md` without the evidence listed in that file's update rule.
- Any new cron job must ship paused and must never trigger spending, publication, or campaign activation.
- If you add a required file, add it to `REQUIRED_FILES` in `scripts/validate_distribution.py`.
- Bump `version` in `distribution.yaml` for every release.

## Validate

```bash
python3 scripts/validate_distribution.py
```

PyYAML is optional; the validator falls back to a minimal parser without it. For release testing, also install the profile locally with `hermes profile install` and confirm it loads.

## Agent skills

### Issue tracker

Issues live in GitHub Issues on `Pivii/ad-remaker`, managed with the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `CONTEXT.md` plus ADRs in `docs/decisions/`. See `docs/agents/domain.md`.
