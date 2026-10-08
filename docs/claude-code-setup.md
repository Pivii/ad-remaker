# Claude Code setup

This page holds the Claude Code installation details that the root [README](../README.md) summarizes: installing the plugin, choosing which vendors it may connect to, the optional local FFmpeg tool, and vendor Skills. For how to use the agent once installed, see "Usage" in the README. First-run setup (`/ad-remaker:setup`), connecting a service you chose, and where choices are saved are in [the setup guide](setup.md).

## Install the plugin

The repository is its own one-plugin marketplace. Add it, then install the plugin:

```bash
claude plugin marketplace add Pivii/ad-remaker          # the private repository, with your GitHub access
# or, from a local clone: claude plugin marketplace add /path/to/ad-remaker
claude plugin install ad-remaker@ad-remaker
claude plugin details ad-remaker@ad-remaker             # 6 Skills, 1 agent, 5 MCP servers
```

To try it for one session without installing, run `claude --plugin-dir /path/to/ad-remaker`.

The plugin provides:

- the `ad-remaker` subagent, whose prompt is `SOUL.md` (invoke it as `@agent-ad-remaker:ad-remaker`, or start a session with `claude --agent ad-remaker:ad-remaker`);
- every Skill in `skills/`, namespaced as `ad-remaker:<skill>`;
- the vendor MCP servers declared in `.mcp.json`, the same ones as `config.yaml`.

## Use only the vendors you pay for

Claude Code has no `enabled: false` for a plugin's MCP servers: all five start when the plugin is enabled. Each one uses OAuth, so it stays unauthenticated and does nothing until you sign in with `claude mcp login plugin:ad-remaker:<name>` or from `/mcp`. Without a paid account, choose the free route in setup and sign in to nothing; the agent follows `free-fallback-mode`.

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

A URL pattern also blocks the same vendor's server when another plugin declares it; `{ "serverName": "plugin:ad-remaker:fal" }` blocks only this plugin's entry. `meta_ads` has no app ID in `.mcp.json`, unlike Hermes: Claude Code does not expand variables in an OAuth client ID. In a test on October 8, 2026, Claude Code built Meta's authorization URL with a client ID of its own; completing the sign-in was not tested. The servers and their sources are listed in [service-matrix.md](service-matrix.md).

## Optional free local FFmpeg tool

For analysis and finishing, Claude Code may use the community ffmpeg-skill separately from this plugin (ADR-004). It is optional: our local analysis scripts remain the distributed path. Do this in your working project, outside the Ad Remaker distribution, using the pinned commit from `skills/providers/SKILL.md`:

```bash
npx --yes skills add https://github.com/kajisho5/ffmpeg-skill/tree/008333aaf6722083392eb6bd8bd67b59884a2a26 --agent claude-code --skill ffmpeg-skill --yes
python3 .claude/skills/ffmpeg-skill/scripts/_contract.py doctor
```

This exact install was verified in a scratch Claude Code project on 2026-10-08: the root Skill, scripts, references, and templates were copied into `.claude/skills/ffmpeg-skill/` (with a canonical copy in `.agents/skills/ffmpeg-skill/`). It does not change the Ad Remaker plugin or install an MCP server. Review the pinned community source before installing; do not run the installer automatically during an ad task. Add `-g` only if you deliberately want it available in every project. A reinstall must use the full pinned URL again.

The scripts need Python 3.9 or later, `ffmpeg`, and `ffprobe`; each operation may require additional filters, encoders, fonts, or an already installed local transcription engine and cached model. `doctor` reports actual capabilities and may exit non-zero on a partially usable machine. On the test host, scenes and contact sheets worked with `--no-timecode`, while caption burning lacked the `subtitles` filter. Install dependencies or download models only with approval. Analysis and finishing routes, fallbacks, and output checks live in `free-fallback-mode` section 4. FFmpeg processing creates local files; it does not publish or generate a new ad from prompts.

Hermes cannot install this pin in v0.20.2; `scripts/install_provider_skills.sh ffmpeg-skill` refuses it. Do not copy it into a Hermes profile or use `npx ffmpeg-skill` there. Re-check on a Hermes upgrade as ADR-004 requires. Test details are in [tests/README.md](../tests/README.md).

## Vendor Skills

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
