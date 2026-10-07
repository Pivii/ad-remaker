# ADR-002 - Split provider Skills into a local policy layer and pinned vendor Skills

## Status

Accepted on October 7, 2026 (maintainer decisions recorded during triage of issue #4).

## Context

The six `*-usage` Skills (Brandsearch, TrendTrack, Higgsfield, Kie.ai, Pika, fal.ai) were Hermes adaptations of vendor-written Skills. The adaptation removed most tool-specific detail, such as Higgsfield's REST, upload, and error flows, and repeated the same agent rules in all six files: cost approval, no silent retry, download outputs, and treat claims as historical.

The result was duplicated policy plus a weaker copy of vendor documentation that drifts as vendors change their CLIs, APIs, and Skills. Several vendors now publish official Skills, and Hermes can install them with `hermes skills install` and re-scan them with `hermes skills audit`.

## Decision

Skills are split into two layers.

Agent layer, in this repository:

- `winning-ad-remake-workflow` keeps its role as the central business Skill.
- `provider-policy` holds the shared provider rules, written once.
- `providers` is the routing directory: per vendor, the official Skill or docs source, the pinned ref, the license, the route order (MCP, CLI, REST), and the date the source was checked. Its pin table is the single source of truth for pins.

Vendor layer, installed from official sources by reference, never copied into this repository:

- Vendor Skills are pinned to a commit, not tracked at latest. None of the vendor repositories had a release tag when checked. Updating a pin is a deliberate change followed by `hermes skills audit`.
- `scripts/install_provider_skills.sh` installs only the vendors a user names, at their pinned commit. Free-mode users install nothing.
- Vendors without an official Skill (TrendTrack, Brandsearch) keep a thin entry in `providers`. A vendor whose Skills cannot be pinned (Kie.ai) is listed without a pin and the script refuses it.

The six `*-usage` Skills are removed. Each `references/upstream.md` moves verbatim to `docs/provenance/<vendor>.md`.

## Consequences

- The shared rules exist in one Skill, and vendor-specific guidance comes from the vendor's own maintained Skill.
- Pins are installed from commit-pinned `raw.githubusercontent.com` SKILL.md URLs, because Hermes v0.20.2 resolves `owner/repo/path` identifiers against the default branch and has no ref syntax.
- External Skills run with the agent's permissions. Every install or pin change must be followed by `hermes skills audit`, and `provider-policy` takes precedence over any vendor Skill.
- `hermes profile update` replaces the profile's `skills/` directory, so vendor Skills must be reinstalled after each profile update. On the same update, existing installs lose the removed `*-usage` Skills.
- The vendor layer is only as available as each vendor's source. Kie.ai's Skills cannot be pinned or installed by Hermes v0.20.2, and the fal.ai Skills repository declares no license. Both are recorded in `providers`.
- The provenance rule changes: `references/upstream.md` stays only with `winning-ad-remake-workflow`; provider source texts live in `docs/provenance/`.
