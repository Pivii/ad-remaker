---
name: providers
description: Use when choosing, installing, or routing to an external provider (Brandsearch, TrendTrack, Higgsfield, Kie.ai, Pika, fal.ai, Meta Ads). Lists each vendor's official Skill or documentation source, pinned ref, license, route order, and the date the source was checked.
---

# Providers

This is a routing directory, not usage documentation. How to use a vendor comes from its official Skill or documentation, listed below. The shared rules for every provider call are in `provider-policy`, and they win over any vendor Skill.

Every source, license, and route below was checked on the date in the table. Treat it as a dated snapshot: re-check before relying on it, and never treat an entry as proof that a vendor is connected.

## Pin table

This table is the single source of truth for vendor Skill pins. `scripts/install_provider_skills.sh` reads it, and `scripts/validate_distribution.py` checks its shape. Keep one row per vendor and no `|` inside cells. `Pinned ref` is a full 40-character commit SHA, or `none` when there is no vendor Skill that can be pinned.

<!-- provider-pins:begin -->
| Vendor | Repository | Skill path | Pinned ref | License | Checked |
|---|---|---|---|---|---|
| higgsfield | higgsfield-ai/skills | higgsfield-generate | f83af0bc1d937c8119099a11f8ebbf5e6fb99819 | MIT | 2026-10-07 |
| pika | Pika-Labs/Pika-Plugins | skills/ugc-ads | f27b3ba28a7be7c5f3a74d8fdd54b770f5d8157b | Apache-2.0 | 2026-10-07 |
| fal | fal-ai-community/skills | skills/genmedia | 9ca850412943251fc9a466c4c29fdaf7a303a3d8 | none declared | 2026-10-07 |
| kie-ai | none | none | none | unknown | 2026-10-07 |
| trendtrack | none | none | none | not applicable | 2026-10-07 |
| brandsearch | none | none | none | not applicable | 2026-10-07 |
| meta-ads | none | none | none | not applicable | pending |
<!-- provider-pins:end -->

None of the vendor repositories had a release tag on 2026-10-07, so every pin is a commit on the default branch.

## Installing vendor Skills

Install only the vendors you pay for. A user in free mode installs nothing.

```bash
scripts/install_provider_skills.sh higgsfield fal          # into the ad-remaker profile
scripts/install_provider_skills.sh --dry-run pika          # print the commands only
```

The script installs each vendor Skill from its commit-pinned URL, `https://raw.githubusercontent.com/<repository>/<pinned ref>/<skill path>/SKILL.md`, with `hermes -p ad-remaker skills install <url> --yes`, then runs `hermes -p ad-remaker skills audit`. It exits non-zero, before installing anything, if a vendor is unknown or has no pin.

A commit URL is used because Hermes v0.20.2 resolves `owner/repo/path` identifiers against the default branch and has no ref syntax, while its URL source fetches `SKILL.md` and the support files it references from the same pinned location.

`hermes profile update` replaces the profile's whole `skills/` directory, which is where vendor Skills are installed. Run the install script again after each profile update.

## Updating a pin

Updating is a deliberate change, never automatic:

1. Read the vendor's diff between the current pin and the new commit, and re-check the license.
2. Change `Pinned ref`, `License`, and `Checked` in the table, and bump `version` in `distribution.yaml`.
3. Reinstall with the script, which runs `hermes skills audit`. External Skills run with the agent's permissions, so review the audit before using the Skill.

## Vendors

Route order lists the routes a vendor offers, in the order to try them. Use a route only when it is connected and authenticated, as `provider-policy` requires.

### Higgsfield

- Official Skill: [`higgsfield-ai/skills`](https://github.com/higgsfield-ai/skills), Skill `higgsfield-generate`, release 0.13.0 at the pinned commit. The repository also holds seven other Skills; install them only by adding a deliberate pin.
- License: MIT, from the repository `LICENSE`.
- Route order: MCP, then CLI (`@higgsfield/cli` on npm, which `higgsfield-generate` wraps), then REST (`https://api.higgsfield.ai`).

### Pika

- Official Skill: [`Pika-Labs/Pika-Plugins`](https://github.com/Pika-Labs/Pika-Plugins), Skill `ugc-ads`. Its Skills assume a Pika MCP server registered as `pika`.
- Not used: [`Pika-Labs/Pika-Skills`](https://github.com/Pika-Labs/Pika-Skills). Its README states the repository is deprecated and its Skills no longer work because the Pika Developer API was discontinued.
- License: Apache-2.0, from the repository `LICENSE`.
- Route order: MCP only. No CLI found, and the former Developer API (REST) is discontinued.

### fal.ai

- Official Skill: [`fal-ai-community/skills`](https://github.com/fal-ai-community/skills), Skill `genmedia`, which drives the `genmedia` CLI ([`fal-ai-community/genmedia-cli`](https://github.com/fal-ai-community/genmedia-cli), MIT).
- License: none declared. The repository has no root `LICENSE` and GitHub reports no license; only `skills/fal-redesign/` carries an MIT `LICENSE`. The Skill is installed by reference from fal's public repository and never copied into this one.
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

- Reserved for issue #5, which adds a local `meta-ads-usage` Skill and fills in this entry. Until then, the paused-campaign rules in `winning-ad-remake-workflow` apply.
