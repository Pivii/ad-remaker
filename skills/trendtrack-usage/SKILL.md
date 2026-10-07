---
name: trendtrack-usage
description: Use when researching ecommerce stores, ads, or campaigns with TrendTrack, if its tools are available and authenticated.
---

# TrendTrack usage

Use TrendTrack only when its corresponding tools are available and authenticated.

1. Check current usage or credit balance before a broad query.
2. Start with a small result limit and narrow filters; widen only after validating the query.
3. Use the current store, Meta, or TikTok search path appropriate to the request, as exposed by the live tools.
4. For recent top-ad analysis, prefer current reach or scaling-window fields over first-seen date when those fields are available.
5. Distinguish numeric ad identifiers from UUID-based resource identifiers when the live schema does.
6. Before any write, confirm the target and scope. Never invoke a destructive operation or confirmation flag without explicit user authorization; prefer non-destructive move behavior when available.
7. Treat monthly allowances, credit costs, field names, platform coverage, and destructive-action semantics in the upstream document as historical guidance until verified through current tool schemas and responses.

See the verbatim [upstream source](references/upstream.md) for provenance and service-specific details.
