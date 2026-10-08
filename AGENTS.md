# Project instructions

This public repository defines an installable Ad Remaker profile distribution for Hermes.

## Current scope

- Keep the translated historical report under `docs/` as source material.
- Do not invent missing Skills, MCP configurations, credentials, prices, service capabilities, or connection status.
- Treat every connection and tool status in the report as a dated snapshot, not current truth.
- Require explicit approval before paid generation, publication, campaign activation, scheduling, or ad spend.
- Preserve clear provenance among source material, imported Skills, and locally authored adaptations.
- Keep secrets, memory, sessions, customer data, brand data, generated outputs, and other runtime state outside the distribution.
- Run `python3 scripts/validate_distribution.py` before declaring distribution changes complete.

## Repository language

Use clear English for all repository-facing product, operating, test, and contributor documentation. Preserve exact product names, identifiers, commands, filenames, and quoted source material when accuracy requires it. Do not use em dash characters in authored prose.
