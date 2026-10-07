---
name: kie-ai-usage
description: Use when generating or editing media with Kie.ai, if its corresponding tools are available and authenticated.
---

# Kie.ai usage

Use Kie.ai only when its corresponding tools are available and authenticated.

1. Inspect the current model catalog and choose by capability; do not assume the upstream model list is current.
2. Upload local inputs through an available authenticated upload tool when the selected model requires public URLs.
3. State the model, units, and estimated cost and obtain explicit approval before generation.
4. Generate one variant first unless the user has approved a larger batch.
5. Wait for the asynchronous task to reach a terminal state using the available status tools.
6. Download outputs that must persist rather than relying on expiring URLs.
7. Do not silently retry failed or unsatisfactory generations; provide a new estimate and request approval first.
8. Treat model availability, pricing, and tool names in the upstream document as historical guidance until verified through current live tools.

See the verbatim [upstream source](references/upstream.md) for provenance and service-specific details.
