# Ad Remaker skills

This repository contains eight integrated Hermes Skills:

- `winning-ad-remake-workflow` — end-to-end evidence, generation approval, quality control, and paused Meta workflow.
- `free-fallback-mode`: no-connection path from free public ad libraries and local analysis scripts to a complete remake pack, without rendering.
- `brandsearch-usage` — conditional Brandsearch research workflow.
- `trendtrack-usage` — conditional TrendTrack ecommerce and ad-intelligence workflow.
- `higgsfield-usage` — conditional Higgsfield media-generation workflow.
- `kie-ai-usage` — conditional Kie.ai media-generation workflow.
- `pika-usage` — conditional Pika generation and editing workflow.
- `fal-usage` — conditional fal.ai generation workflow.

## Provenance policy

Each skill keeps the supplied source document verbatim at `references/upstream.md` and links to it from `SKILL.md`. The operational `SKILL.md` is an English Hermes adaptation: it removes installation-state wording, makes service behavior conditional on current tool availability and authentication, and treats upstream service counts, connections, schemas, pricing, and capabilities as historical guidance until verified.

`free-fallback-mode` is the exception: it is locally authored from section 7.2 of the historical report, has no upstream Skill text, and owns deterministic local analysis scripts in its `scripts/` directory.

No credentials or MCP configuration are included. Paid generation requires explicit approval under the workflow’s cost controls.
