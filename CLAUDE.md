@AGENTS.md

# Working on this repository

This repository is the source of the Ad Remaker agent, packaged as a Hermes profile distribution and, from the same files, as a Claude Code plugin (ADR-003). You are editing the agent, not acting as it. Read `SOUL.md` and the Skills to understand the agent's behavior, but do not adopt its persona while working here.

## What the agent does

Ad Remaker finds competitor ads that show public performance signals, deconstructs their creative mechanics, and adapts them to a given brand's real product. It never copies an ad exactly, never invents claims, and never spends money or publishes anything without explicit human approval.

## Where things live

| Path | Role | Format owner |
|---|---|---|
| `distribution.yaml` | Profile manifest (name, version, Hermes version) | Hermes |
| `SOUL.md` | Agent identity and non-negotiable rules | Hermes |
| `config.yaml` | Credential-free Hermes defaults and the declared MCP servers (`mcp_servers`, all `enabled: false`) | Hermes |
| `cron/jobs.json` | Distributed scheduled jobs, currently none | Hermes |
| `.claude-plugin/plugin.json` | Claude Code plugin manifest; `version` equals `distribution.yaml` | Claude Code |
| `.claude-plugin/marketplace.json` | One-plugin marketplace serving this repository, not public | Claude Code |
| `agents/ad-remaker.md` | Claude Code subagent: hand-written frontmatter, body generated from `SOUL.md` | Generated, do not edit the body |
| `.mcp.json` | Claude Code MCP servers, same names and URLs as `config.yaml` `mcp_servers` | Claude Code |
| `skills/<name>/SKILL.md` | Operational Skill (YAML frontmatter `name` + `description`) | Agent Skills standard |
| `skills/winning-ad-remake-workflow/references/upstream.md` | Source workflow text as supplied, kept for provenance | Do not edit |
| `skills/providers/SKILL.md` | Vendor routing directory and the pin table (single source of truth for vendor Skill pins) | This repo |
| `docs/provenance/<vendor>.md` | Vendor source texts from the removed `*-usage` Skills, kept verbatim | Do not edit |
| `docs/decisions/` | Architecture decisions (ADR-001 profile distribution, ADR-002 provider Skill layers, ADR-003 Claude Code plugin) | This repo |
| `docs/ad-remaker-complete-operating-report.md` | Translated historical report, dated October 7, 2026 | Source material, do not rewrite |
| `docs/service-matrix.md` | Integration readiness per service | Update when a status changes |
| `scripts/validate_distribution.py` | Structural and safety validator | Keep in sync with required files |
| `scripts/sync_claude_agent.py` | Rewrites the body of `agents/ad-remaker.md` from `SOUL.md` | This repo |
| `scripts/install_provider_skills.sh` | Installs the vendor Skills a user names, at their pinned commit, then runs `hermes skills audit` | Reads the pin table in `skills/providers/SKILL.md` |

## Skills

Skills are split into two layers (ADR-002).

- Agent layer, in this repo:
  - `winning-ad-remake-workflow` is the central business Skill. It orchestrates research, analysis, cost approval, generation, QC, delivery, and the Meta campaign step.
  - `meta-ads-usage` covers Meta's ads MCP server and Ads CLI, and holds the Meta rules (paused by default, read-back, separate approval for activation, scheduling, and spend). Write a Meta campaign rule here and nowhere else. Meta publishes no official Skill.
  - `provider-policy` holds the rules shared by every provider call (auth check, approval before spend, no silent retry or batch expansion, download outputs, free path when nothing is connected). Write a shared provider rule here and nowhere else.
  - `providers` is the routing directory: per vendor, the official source, pinned ref, license, route order, and check date.
- Vendor layer, not in this repo: official vendor Skills installed by reference with `scripts/install_provider_skills.sh`, only for pin table rows with `Install` `hermes` (Pika on 2026-10-08). Vendors whose Skills the Hermes skills guard blocks (Higgsfield, fal.ai) are thin entries with `Install` `no`. Never copy or patch a vendor Skill into `skills/` to get around the guard.
- Changing a vendor pin is deliberate: read the vendor diff, re-check the license, update `Pinned ref`, `License`, and `Checked` in the pin table, bump the version, and run `hermes skills audit` after reinstalling.
- When editing `winning-ad-remake-workflow`, change `SKILL.md` only. Keep `references/upstream.md` verbatim and keep the link to it at the bottom of `SKILL.md`. Never edit `docs/provenance/`.
- Treat model names, prices, tool counts, and connection states from upstream files, provenance files, and the report as historical until verified.

## Rules when changing the distribution

- Never commit secrets, tokens, `.env` files, brand data, customer data, generated media, memories, or sessions. Installation-specific brand data belongs in `local/brands/<brand>/`, which is gitignored.
- MCP servers are declared in `config.yaml` under `mcp_servers`; Hermes does not read a profile `mcp.json`. Every declared server ships with `enabled: false`, uses OAuth or `${ENV_VAR}` placeholders declared in `distribution.yaml` `env_requires` (`required: false`), and has its official source URL and check date in `docs/service-matrix.md`. Never mark a service `verified` without the evidence listed in that file's update rule.
- `hermes profile update` preserves an installed `config.yaml` unless `--force-config` is passed, so servers declared later do not reach existing installs automatically.
- Any new cron job must ship paused and must never trigger spending, publication, or campaign activation.
- If you add a required file, add it to `REQUIRED_FILES` in `scripts/validate_distribution.py`.
- After any change to `SOUL.md`, run `python3 scripts/sync_claude_agent.py` and commit `agents/ad-remaker.md` with it. Never edit the subagent body by hand.
- Declare an MCP server in both `config.yaml` (`enabled: false`) and `.mcp.json`, under the same name and URL.
- Keep `version` in `.claude-plugin/plugin.json` equal to `version` in `distribution.yaml`.
- Bump `version` in `distribution.yaml` for every release.

## Validate

```bash
python3 scripts/validate_distribution.py
python3 tests/check_mcp_fixtures.py   # the validator must reject every invalid MCP fixture
```

PyYAML is optional; the validator falls back to a minimal parser without it. For release testing, also install the profile locally with `hermes profile install` and confirm it loads.

## Agent skills

### Issue tracker

Issues live in GitHub Issues on `Pivii/ad-remaker`, managed with the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `CONTEXT.md` plus ADRs in `docs/decisions/`. See `docs/agents/domain.md`.
