<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/brand/logo-lockup-horizontal-dark.svg">
    <img src="docs/brand/logo-lockup-horizontal.svg" alt="Ad Remaker" width="400">
  </picture>
</p>

# Ad Remaker

Inspired by the Recreate competitor ads agent from [Rerun](https://rerun.build/templates/recreate-competitor-ads-meta?via=aRLmG4). If you want the same agent without installing or configuring anything, use Rerun directly.

This is an independent, unofficial adaptation. According to the maintainer, the marketing team (Théo) authorized an open-source release on October 8, 2026, provided attribution is included. These are affiliate links: the maintainer may earn a commission.

Independent agent project specialized in analyzing and adapting effective advertising concepts. The same files install as a Hermes profile or as a Claude Code plugin (see `docs/decisions/ADR-003-claude-code-plugin.md`).

## Status

The repository was initialized from the operating report provided on October 7, 2026. That report documents the target architecture, business workflow, safeguards, proposed integrations, and their status at the time of observation. Historical availability statements in the report are not evidence of current tool or MCP availability.

Provider rules live in the local `provider-policy` Skill. Official vendor Skills are not bundled: each user installs only the vendors they pay for, at a pinned commit, with `scripts/install_provider_skills.sh` in Hermes, or with the commands under "Vendor Skills in Claude Code" (see `docs/decisions/ADR-002-provider-skill-layers.md`).

## Which version should you choose?

Rerun is the simple option if you want to get started without a terminal. The plugin and profile let you use your existing environment.

| Criterion | [Rerun](https://rerun.build?via=aRLmG4) | Claude Code plugin | Hermes profile |
|---|---|---|---|
| Intended users | Non-technical users who want a ready-to-use agent | People who already use Claude Code | People who run Hermes |
| Setup time | A few seconds to add the agent; about 5 min for configuration, according to the template page | A few minutes if Claude Code is already configured, plus connections to the services you use (estimate) | A few minutes if Hermes is already configured, plus model selection and connections to the services you use (estimate) |
| Hosting | Hosted and managed by the service | On the machine where you run Claude Code | On the machine or server where you run Hermes |
| Cost | Free trial to get started, then a paid subscription; model and service costs depend on usage | Free plugin (MIT); Claude Code access, models, and external services depend on your plans | Free profile (MIT); models, optional hosting, and external services depend on your plans |
| External tools needed | Higgsfield or Kie AI (or another generator) for generation; TrendTrack is optional for research; Meta Ads is optional for drafts | TrendTrack is optional; Higgsfield or Kie AI (or another connected generator) for generation; Meta Ads is optional; local analysis mode works without a generator | TrendTrack is optional; Higgsfield or Kie AI (or another connected generator) for generation; Meta Ads is optional; local analysis mode works without a generator |

Information checked on October 8, 2026: [template](https://rerun.build/templates/recreate-competitor-ads-meta?via=aRLmG4) and [service plans](https://rerun.build/pricing?via=aRLmG4). The free trial requires a payment card. Adding the template does not connect your external accounts. Research can use public ad libraries when TrendTrack is unavailable; delivery provides files for manual import when Meta Ads is unavailable. Plans and requirements may change.

## Install

### Hermes

```bash
hermes profile install /path/to/ad-remaker --yes
hermes -p ad-remaker skills list
```

Then set a model with `hermes -p ad-remaker model`. Vendor MCP servers ship disabled in `config.yaml`; `docs/architecture.md` explains how to enable the ones you pay for. Vendor Skills are optional: `scripts/install_provider_skills.sh pika`.

### Claude Code

The repository is its own one-plugin marketplace. Add it, then install the plugin:

```bash
claude plugin marketplace add Pivii/ad-remaker          # the private repository, with your GitHub access
# or, from a local clone: claude plugin marketplace add /path/to/ad-remaker
claude plugin install ad-remaker@ad-remaker
claude plugin details ad-remaker@ad-remaker             # 5 Skills, 1 agent, 5 MCP servers
```

To try it for one session without installing, run `claude --plugin-dir /path/to/ad-remaker`.

The plugin provides:

- the `ad-remaker` subagent, whose prompt is `SOUL.md` (invoke it as `@agent-ad-remaker:ad-remaker`, or start a session with `claude --agent ad-remaker:ad-remaker`);
- every Skill in `skills/`, namespaced as `ad-remaker:<skill>`;
- the vendor MCP servers declared in `.mcp.json`, the same ones as `config.yaml`.

#### Use only the vendors you pay for

Claude Code has no `enabled: false` for a plugin's MCP servers: all five start when the plugin is enabled. Each one uses OAuth, so it stays unauthenticated and does nothing until you sign in with `claude mcp login plugin:ad-remaker:<name>` or from `/mcp`. Without a paid account, sign in to nothing: the agent follows `free-fallback-mode`.

To stop Claude Code from connecting to a vendor you do not pay for, either turn the server off in `/mcp` (per project), or block it everywhere with `deniedMcpServers` in your own `~/.claude/settings.json`, one entry per vendor:

```json
{
  "deniedMcpServers": [
    { "serverUrl": "https://api.trendtrack.io/*" },
    { "serverUrl": "https://mcp.higgsfield.ai/*" },
    { "serverUrl": "https://mcp.fal.ai/*" }
  ]
}
```

A URL pattern also blocks the same vendor's server when another plugin declares it; `{ "serverName": "plugin:ad-remaker:fal" }` blocks only this plugin's entry. `meta_ads` has no app ID in `.mcp.json`, unlike Hermes: Claude Code does not expand variables in an OAuth client ID. In a test on October 8, 2026, Claude Code built Meta's authorization URL with a client ID of its own; completing the sign-in was not tested. The servers and their sources are listed in `docs/service-matrix.md`.

#### Optional free local FFmpeg tool in Claude Code

For analysis and finishing, Claude Code may use the community ffmpeg-skill separately from this plugin (ADR-004). It is optional: our local analysis scripts remain the distributed path. Do this in your working project, outside the Ad Remaker distribution, using the pinned commit from `skills/providers/SKILL.md`:

```bash
npx --yes skills add https://github.com/kajisho5/ffmpeg-skill/tree/008333aaf6722083392eb6bd8bd67b59884a2a26 --agent claude-code --skill ffmpeg-skill --yes
python3 .claude/skills/ffmpeg-skill/scripts/_contract.py doctor
```

This exact install was verified in a scratch Claude Code project on 2026-10-08: the root Skill, scripts, references, and templates were copied into `.claude/skills/ffmpeg-skill/` (with a canonical copy in `.agents/skills/ffmpeg-skill/`). It does not change the Ad Remaker plugin or install an MCP server. Review the pinned community source before installing; do not run the installer automatically during an ad task. Add `-g` only if you deliberately want it available in every project. A reinstall must use the full pinned URL again.

The scripts need Python 3.9 or later, `ffmpeg`, and `ffprobe`; each operation may require additional filters, encoders, fonts, or an already installed local transcription engine and cached model. `doctor` reports actual capabilities and may exit non-zero on a partially usable machine. On the test host, scenes and contact sheets worked with `--no-timecode`, while caption burning lacked the `subtitles` filter. Install dependencies or download models only with approval. Analysis and finishing routes, fallbacks, and output checks live in `free-fallback-mode` section 4. FFmpeg processing creates local files; it does not publish or generate a new ad from prompts.

Hermes cannot install this pin in v0.20.2; `scripts/install_provider_skills.sh ffmpeg-skill` refuses it. Do not copy it into a Hermes profile or use `npx ffmpeg-skill` there. Re-check on a Hermes upgrade as ADR-004 requires. Test details are in `tests/README.md`.

#### Vendor Skills in Claude Code

Vendor Skills are optional and installed by reference, at the commit pinned in the pin table of `skills/providers/SKILL.md`. Never install one at its latest commit. For ffmpeg-skill use the exact root-Skill command above. For paid vendor Skills replace `<repository>`, `<pinned ref>`, and `<skill path>` with the values of the vendor's row; rows whose `Pinned ref` is `none` (Kie.ai, TrendTrack, Brandsearch, Meta Ads) have nothing to install.

```bash
npx skills add https://github.com/<repository>/tree/<pinned ref>/<skill path> --agent claude-code
```

This installs into the current project's `.claude/skills/` and records the commit in `skills-lock.json`; add `-g` to install for every project.

Pika and Higgsfield also publish a Claude Code plugin marketplace in the same repository, which installs all of their Skills at once. `claude plugin marketplace add owner/repo#ref` accepts a branch or tag but not a commit, so add the marketplace from a clone checked out at the pinned commit:

```bash
git clone https://github.com/Pika-Labs/Pika-Plugins.git ~/vendor/Pika-Plugins
git -C ~/vendor/Pika-Plugins checkout --detach <pinned ref>
claude plugin marketplace add ~/vendor/Pika-Plugins && claude plugin install pika@pika-plugins
# Higgsfield: clone https://github.com/higgsfield-ai/skills.git the same way, then
# claude plugin marketplace add <clone> && claude plugin install higgsfield@higgsfield
```

Keep the clone: Claude Code loads a marketplace added from a local path in place. To move to a new pin, check out the new commit after updating the pin table.

Pika's plugin declares its own `pika` MCP server with the same URL as this plugin's; with both plugins installed, Claude Code 2.1.288 listed only one `pika` server. Higgsfield's and fal.ai's Skills tell the agent to install their CLI with `curl ... | sh`. The Hermes skills guard blocks them (ADR-002); Claude Code has no such guard, so `provider-policy` applies: the user approves that exact command, or runs it themselves.

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
- `.claude-plugin/`: Claude Code plugin manifest (`plugin.json`, version kept equal to `distribution.yaml`) and the one-plugin marketplace (`marketplace.json`).
- `agents/ad-remaker.md`: Claude Code subagent. Its body is generated from `SOUL.md` by `scripts/sync_claude_agent.py`.
- `.mcp.json`: the vendor MCP servers for Claude Code, the same set as `config.yaml`.
- `skills/`: the business workflow, the shared provider policy, and the `providers` routing directory with its vendor pin table.
- `docs/ad-remaker-complete-operating-report.md`: complete historical source report, translated into English.
- `docs/architecture.md`: distribution layering and ownership boundaries.
- `docs/service-matrix.md`: integration readiness states without unsupported availability claims.
- `docs/provenance/`: verbatim vendor source texts kept for provenance.
- `docs/decisions/`: architecture decisions.
- `docs/brand/`: logo files, the logo brief with its usage rules, and the showcase page design handoff.
- `scripts/validate_distribution.py`: local structural and safety validator, for both runtimes.
- `scripts/sync_claude_agent.py`: regenerates the subagent body from `SOUL.md`.
- `scripts/install_provider_skills.sh`: installs pinned official vendor Skills into the profile, then runs `hermes skills audit`.
- `tests/`: acceptance guidance and redistributable fixtures.

## Validation

Run from any directory:

```bash
python3 /path/to/ad-remaker/scripts/validate_distribution.py
```

## License

[MIT](LICENSE), copyright 2026 Pivi Solutions. External vendor source material retained for provenance and separately installed vendor Skills remain subject to their own terms; this license does not relicense them.

## Report source

[Ad Remaker report](https://sucqmcejnrnvcdnrwhld.supabase.co/storage/v1/object/public/published/3695/ad-remaker-fonctionnement/ad-remaker-fonctionnement-complet.md?v=1791399468681)
