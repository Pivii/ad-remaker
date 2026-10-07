# Provider source provenance

These files are the vendor Skill texts supplied with the original report, kept verbatim for provenance. Each one was previously `skills/<vendor>-usage/references/upstream.md` and was moved here unchanged when the `*-usage` Skills were removed (see `docs/decisions/ADR-002-provider-skill-layers.md`).

| File | Former location |
|---|---|
| `brandsearch.md` | `skills/brandsearch-usage/references/upstream.md` |
| `fal.md` | `skills/fal-usage/references/upstream.md` |
| `higgsfield.md` | `skills/higgsfield-usage/references/upstream.md` |
| `kie-ai.md` | `skills/kie-ai-usage/references/upstream.md` |
| `pika.md` | `skills/pika-usage/references/upstream.md` |
| `trendtrack.md` | `skills/trendtrack-usage/references/upstream.md` |

Rules:

- Do not edit these files. They are source material, not operating instructions.
- The agent does not load them. Current vendor guidance comes from the official vendor Skills or docs listed in `skills/providers/SKILL.md`.
- Model names, prices, tool names, counts, and connection states in these files are a historical snapshot.
