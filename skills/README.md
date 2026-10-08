# Ad Remaker skills

Skills are split into two layers, as recorded in `docs/decisions/ADR-002-provider-skill-layers.md`.

## Agent layer (this repository)

- `winning-ad-remake-workflow`: end-to-end evidence, generation approval, quality control, and paused Meta workflow.
- `provider-policy`: the shared rules for every provider call (authentication check, approval before spend, no silent retry or batch expansion, output retention, and the free path when nothing is connected).
- `providers`: routing directory with each vendor's official source, pinned ref, license, route order, and check date.
- `free-fallback-mode`: no-connection path from free public ad libraries and local analysis scripts to a complete remake pack, without rendering.

## Vendor layer (installed by reference)

Official vendor Skills are not copied into this repository. Each user installs only the vendors they pay for, at the commit pinned in `providers`:

```bash
scripts/install_provider_skills.sh pika
```

The script runs `hermes skills audit` after installing. On 2026-10-08 only Pika is installable. Higgsfield and fal.ai are thin entries: the Hermes v0.20.2 skills guard blocks their Skills, so `providers` points to the pinned vendor Skill as a source to read and to the vendor's own CLI install command, which needs the user's approval under `provider-policy`. Free-mode users install nothing. Run it again after `hermes profile update`, which replaces the profile's `skills/` directory.

## Provenance policy

`winning-ad-remake-workflow` keeps its supplied source document verbatim at `references/upstream.md` and links to it from `SKILL.md`. Its operational `SKILL.md` is an English Hermes adaptation that treats upstream service counts, connections, schemas, pricing, and capabilities as historical guidance until verified.

`free-fallback-mode` is locally authored from section 7.2 of the historical report, has no upstream Skill text, and owns deterministic local analysis scripts in its `scripts/` directory.

The vendor source texts of the removed `*-usage` Skills are kept verbatim in `docs/provenance/`. They are not loaded by the agent and must not be edited.

No credentials are included. The official vendor MCP servers are declared, disabled, in the profile `config.yaml`. Paid calls require explicit approval under `provider-policy`.
