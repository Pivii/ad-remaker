# Codex CLI and Desktop setup

This page holds the Codex installation details that the root [README](../README.md) summarizes. For how to use the agent once installed, see "Usage" in the README. First-run setup (`$ad-remaker:setup`), connecting a service you chose, and where choices are saved are in [the setup guide](setup.md). The packaging decision is [ADR-005](decisions/ADR-005-codex-skills-only.md).

## What is verified

Checked on October 8, 2026 (issue #22, PR #23):

- Codex CLI `0.160.0`: installation, discovery of the Skills (six since the `setup` Skill, issue #25), rule loading, guarded workflow and setup checks, update, and removal.
- Codex Desktop: the installed application is bundle `com.openai.codex`, version `26.930.61225` (build `13520`), with bundled runtime `0.160.1`. Headless checks of that bundled runtime passed installation, discovery of the six Skills, rule loading, and a guarded workflow check.
- Not verified: the Desktop Plugins Directory and Skill selection through the actual Desktop interface, the IDE extension, and cloud. Test details are in [tests/README.md](../tests/README.md).

This plugin adds six Skills, with no bundled MCP servers; local analysis works without vendor accounts. It uses your configured Codex model access. The plugin is free (MIT); model allowance and optional external services depend on your plans.

## Install

For an authenticated private Git installation:

```bash
codex plugin marketplace add Pivii/ad-remaker --ref main
codex plugin add ad-remaker@ad-remaker
codex plugin list --marketplace ad-remaker --json
```

For Desktop, the same marketplace registration is required so the plugin remains discoverable outside the package directory. The bundled Desktop backend accepts the existing compatibility catalog. After installation, restart or refresh the Desktop client, select the registered `ad-remaker` source in its Plugins Directory, and check that the six Skills appear in a new project outside this repository. This interface flow has not been verified yet. Users do not need to inspect the application version as an installation step.

The repository is public, so no Git authentication is needed to install. Never embed credentials in a repository URL. No vendor login is needed. Codex retains installer-created `.git` metadata in its private Git plugin cache on the tested client; the clean local export below has no Git metadata. Ignored worktrees, credentials and user runtime data are excluded in both tests. For a local checkout, export a clean package first; do not install a live development clone, because Codex can copy ignored files into its cache:

```bash
python3 /path/to/ad-remaker/scripts/export_codex_package.py /path/outside/repo/ad-remaker-codex
codex plugin marketplace add /path/outside/repo/ad-remaker-codex
codex plugin add ad-remaker@ad-remaker
```

The export destination must not exist. It includes every tracked Skill script/reference, including generated rules. Keep the exported marketplace directory for future installs. The script exports the tracked working-tree files, so release authors must validate and stage new files before exporting.

## Invoke the Skills

Start Codex from your own working project, outside the distribution checkout. Invoke the main workflow explicitly:

```text
$ad-remaker:winning-ad-remake-workflow Analyze this competitor ad for my product. No vendors are connected. Prepare the free remake pack and state missing inputs/capabilities.
```

The discovered selectors are `ad-remaker:winning-ad-remake-workflow`, `ad-remaker:free-fallback-mode`, `ad-remaker:provider-policy`, `ad-remaker:providers`, `ad-remaker:meta-ads-usage`, and `ad-remaker:setup`. Type `$` and select the Skill in the client. Each entrypoint first reads its generated agent rules and applicable sibling policies. Explicit invocation applies instructions to that task; it does not create a Hermes profile, a Claude subagent, or a global persona. Natural-language selection remains client/model-dependent.

## Update

To update a Git installation, refresh the tracked ref and reinstall:

```bash
codex plugin marketplace upgrade ad-remaker
codex plugin remove ad-remaker@ad-remaker
codex plugin add ad-remaker@ad-remaker
```

For a local marketplace, export the new validated version to a new directory, remove the plugin, remove the marketplace, add the new export path, and add the plugin again. `marketplace upgrade` does not support local paths. These commands update only this plugin/catalog; do not replace the user's config file or global instructions. Removal clears the plugin cache, so keep your working assets outside it.

## Uninstall

```bash
codex plugin remove ad-remaker@ad-remaker
codex plugin marketplace remove ad-remaker
```

## Optional vendors

Setup asks which services you want before the first research; [the setup guide](setup.md) describes connecting a chosen one. The details below explain how the Codex package itself behaves.

The explicit empty MCP mapping in `.codex-plugin/plugin.json` takes precedence over Claude's `.mcp.json` on the tested CLI. Hermes `enabled: false` is not a Codex setting. The installed package itself starts zero vendor servers. Other plugins/user configuration may still provide tools: check the actual session before each task.

To opt in, read `provider-policy` and the desired vendor's entry in `providers`, then add a disabled entry to your own Codex `config.toml`, preserving its other settings, for example:

```toml
[mcp_servers.pika]
enabled = false
url = "https://mcp.pika.me/api/mcp"
```

Inspect it with `codex mcp get pika --json`. This parses configuration without starting a provider. `codex mcp add --url` can automatically begin OAuth discovery/login on this client; use it only when deliberately connecting, not as a model-free parsing check.

Set `enabled = false` under `[mcp_servers.pika]` in your own Codex `config.toml` to stop it; set it true only when deliberately connecting. `codex mcp remove pika` removes it. The configuration parser is checked without a provider login or call. When you choose to authenticate, `codex mcp login pika` begins OAuth. OAuth, including Meta client-ID requirements, and real provider operation are unverified in Codex; consult the current official vendor docs before connecting. Do not reuse Claude's observed Meta client-ID behavior as evidence. See [service-matrix.md](service-matrix.md) for dated endpoint sources.

Vendor Skills are separately installed, never automatic. Use the existing source/pin/license table in `providers`, retain the complete vendor bundle, and review it before installing with a Codex-compatible client. No vendor Skill installation command is advertised as verified in Codex here. `scripts/install_provider_skills.sh` is Hermes-only. The optional community ffmpeg-skill remains Claude Code-only; Codex uses our distributed local analysis scripts and reports missing dependencies/finishing capabilities.
