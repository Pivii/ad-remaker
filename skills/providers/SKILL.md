---
name: providers
description: Use when choosing, installing, or routing to an external provider (Brandsearch, TrendTrack, Higgsfield, Kie.ai, Pika, fal.ai, Meta Ads). Lists each vendor's official Skill or documentation source, pinned ref, license, route order, and the date the source was checked.
---

# Providers

This is a routing directory, not usage documentation. How to use a vendor comes from its official Skill or documentation, listed below. The shared rules for every provider call are in `provider-policy`, and they win over any vendor Skill.

Every source, license, and route below was checked on the date in the table. Treat it as a dated snapshot: re-check before relying on it, and never treat an entry as proof that a vendor is connected.

## Pin table

This table is the single source of truth for vendor Skill pins. `scripts/install_provider_skills.sh` reads it, and `scripts/validate_distribution.py` checks its shape. Keep one row per vendor and no `|` inside cells.

- `Pinned ref` is a full 40-character commit SHA, or `none` when there is no vendor source that can be pinned.
- `Install` is `hermes` when the script installs the pinned vendor Skill into the profile, or `no` when it refuses. A `no` row with a pin is a thin entry: the pinned commit is the source to read, not something to install.

<!-- provider-pins:begin -->
| Vendor | Repository | Skill path | Pinned ref | Install | License | Checked |
|---|---|---|---|---|---|---|
| higgsfield | higgsfield-ai/skills | higgsfield-generate | f83af0bc1d937c8119099a11f8ebbf5e6fb99819 | no | MIT | 2026-10-08 |
| pika | Pika-Labs/Pika-Plugins | skills/ugc-ads | f27b3ba28a7be7c5f3a74d8fdd54b770f5d8157b | hermes | Apache-2.0 | 2026-10-08 |
| fal | fal-ai-community/skills | skills/genmedia | 9ca850412943251fc9a466c4c29fdaf7a303a3d8 | no | none declared | 2026-10-08 |
| kie-ai | none | none | none | no | unknown | 2026-10-07 |
| trendtrack | none | none | none | no | not applicable | 2026-10-07 |
| brandsearch | none | none | none | no | not applicable | 2026-10-07 |
| meta-ads | none | none | none | no | not applicable | 2026-10-08 |
<!-- provider-pins:end -->

None of the vendor repositories had a release tag on 2026-10-07, so every pin is a commit on the default branch.

## Installing vendor Skills

Install only the vendors you pay for. A user in free mode installs nothing.

```bash
scripts/install_provider_skills.sh pika                    # into the ad-remaker profile
scripts/install_provider_skills.sh --dry-run pika          # print the commands only
```

The script installs each vendor Skill from its commit-pinned URL, `https://raw.githubusercontent.com/<repository>/<pinned ref>/<skill path>/SKILL.md`, with `hermes -p ad-remaker skills install <url> --yes`, then runs `hermes -p ad-remaker skills audit`. It exits non-zero, before installing anything, if a vendor is unknown or its `Install` value is not `hermes`. Only Pika is installable on 2026-10-08.

A commit URL is used because Hermes v0.20.2 resolves `owner/repo/path` identifiers against the default branch and has no ref syntax, while its URL source fetches `SKILL.md` and the support files it references from the same pinned location.

`hermes profile update` replaces the profile's whole `skills/` directory, which is where vendor Skills are installed. Run the install script again after each profile update.

## Updating a pin

Updating is a deliberate change, never automatic:

1. Read the vendor's diff between the current pin and the new commit, and re-check the license.
2. Change `Pinned ref`, `License`, and `Checked` in the table, and bump `version` in `distribution.yaml`.
3. Reinstall with the script, which runs `hermes skills audit`. External Skills run with the agent's permissions, so review the audit before using the Skill.

A thin entry with a pin (Higgsfield, fal.ai) can move back to `Install` `hermes` once the vendor Skill at the new commit passes the Hermes skills guard, for example after the vendor drops `curl | sh` from it. Check with `hermes skills inspect <pinned url>` and a scratch profile install first.

## Why Higgsfield and fal.ai are thin entries

On 2026-10-08, Hermes v0.20.2 could not install either vendor Skill at its pinned commit:

- Higgsfield: the pinned URL fails with "Could not fetch ... from any source", because `higgsfield-generate/SKILL.md` links `assets/audio`, which is a directory, and the URL source fails the whole bundle when a referenced support path is missing. The GitHub identifier form gets further, then the skills guard blocks it with `curl_pipe_shell` and `allowed_tools_field` findings.
- fal.ai: the skills guard blocks `genmedia` with two `curl_pipe_shell` findings, `SKILL.md` line 117 and `references/full-reference.md` line 10 (`curl https://genmedia.sh/install -fsS | bash`).

A dangerous verdict cannot be overridden: in Hermes v0.20.2, `should_allow_install` blocks it for community and trusted sources alike, `--force` does not apply, and there is no user-configurable trust list. This repository does not copy or patch vendor Skills to get around the guard (ADR-002). Instead, the agent reads the pinned vendor Skill as documentation, and the user installs the vendor CLI with the vendor's own command, under `provider-policy`.

## Vendors

Route order lists the routes a vendor offers, in the order to try them. Use a route only when it is connected and authenticated, as `provider-policy` requires.

### Higgsfield

- Thin entry, not installed: see "Why Higgsfield and fal.ai are thin entries". The install script refuses `higgsfield`.
- Source to read: [`higgsfield-generate/SKILL.md` at the pinned commit](https://github.com/higgsfield-ai/skills/blob/f83af0bc1d937c8119099a11f8ebbf5e6fb99819/higgsfield-generate/SKILL.md) in [`higgsfield-ai/skills`](https://github.com/higgsfield-ai/skills), release 0.13.0. The repository holds seven other Skills.
- License: MIT, from the repository `LICENSE`.
- CLI install, from `higgsfield-generate/SKILL.md` and `INSTALL.md` at the pinned commit, run only with the user's approval: `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh`. The installer is fetched from the CLI repository's `main` branch, so it is not pinned.
- Route order: MCP, then CLI (`higgsfield`, published on npm as `@higgsfield/cli`), then REST (`https://api.higgsfield.ai`).

### Pika

- Official Skill: [`Pika-Labs/Pika-Plugins`](https://github.com/Pika-Labs/Pika-Plugins), Skill `ugc-ads`. Its Skills assume a Pika MCP server registered as `pika`.
- Installed with the script at the pinned commit in a scratch profile on 2026-10-08 (Hermes v0.20.2): scan verdict SAFE, `hermes skills audit` SAFE, listed as a `url` community Skill.
- Not used: [`Pika-Labs/Pika-Skills`](https://github.com/Pika-Labs/Pika-Skills). Its README states the repository is deprecated and its Skills no longer work because the Pika Developer API was discontinued.
- License: Apache-2.0, from the repository `LICENSE`.
- Route order: MCP only. No CLI found, and the former Developer API (REST) is discontinued.

### fal.ai

- Thin entry, not installed: see "Why Higgsfield and fal.ai are thin entries". The install script refuses `fal`.
- Source to read: [`skills/genmedia/SKILL.md` at the pinned commit](https://github.com/fal-ai-community/skills/blob/9ca850412943251fc9a466c4c29fdaf7a303a3d8/skills/genmedia/SKILL.md) in [`fal-ai-community/skills`](https://github.com/fal-ai-community/skills). It drives the `genmedia` CLI ([`fal-ai-community/genmedia-cli`](https://github.com/fal-ai-community/genmedia-cli), MIT).
- License: none declared for the Skills repository; only `skills/fal-redesign/` carries an MIT `LICENSE`. Accepted by the maintainer on 2026-10-08, because nothing from it is copied into this repository.
- CLI install, from `skills/genmedia/SKILL.md` at the pinned commit, run only with the user's approval: `curl https://genmedia.sh/install -fsS | bash` on Linux and macOS, then `genmedia setup --non-interactive --api-key "$FAL_KEY"`. The installer URL is not pinned.
- Route order: MCP, then CLI (`genmedia`, `FAL_KEY`), then REST.

### Kie.ai

- Official Skills: `npx skills add https://kie.ai`, served from `https://kie.ai/.well-known/agent-skills/index.json` as unversioned archives (`kie-models`, `kie-chat-agents`).
- Not pinned: the archives have no tag or commit to pin, and Hermes v0.20.2 does not resolve this source (`hermes skills inspect https://kie.ai` reports it cannot find it). The install script refuses `kie-ai`.
- License: unknown; none is published with the archives.
- Route order: REST (`KIE_API_KEY`). No official MCP server or CLI found.

### TrendTrack

- No official Skill. Official agent guide: <https://docs.trendtrack.io/docs/agent-guide.md>. Read it before calling the API; it requires a lookup call before other endpoints.
- License: not applicable, nothing is installed.
- Route order: MCP, then REST (`https://api.trendtrack.io/v1`, `TRENDTRACK_API_KEY`).

### Brandsearch

- No official Skill or public documentation found. Brandsearch has an MCP server and an API, but their endpoints are not public.
- License: not applicable, nothing is installed.
- Route order: MCP only, when the user has connected it.

### Meta Ads

- No official Skill (checked on 2026-10-08). The local `meta-ads-usage` Skill holds the Meta rules (paused by default, read-back, separate approval) and links Meta's documentation: [ads MCP server](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-overview) and [Ads CLI](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview).
- License: not applicable, nothing is installed from a Skill repository.
- CLI install, from Meta's Ads CLI get-started page on 2026-10-08, run only with the user's approval: `pip install meta-ads`, then `uv sync`. Python 3.12 or later.
- Route order for campaigns, ad sets, and ads: MCP (`https://mcp.facebook.com/ads`, declared as `meta_ads` in `config.yaml`), then CLI (`meta`, with `ACCESS_TOKEN` and `AD_ACCOUNT_ID`). Both reach only the user's own ad accounts.
- Route order for Ad Library research: the MCP tool `ads_library_search`, which reads the public Meta Ad Library, then the Ad Library website as the free path. The tool's limits compared with the Ad Library API are unverified.
