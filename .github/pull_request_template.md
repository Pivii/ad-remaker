<!-- Closes #<issue> -->

**What changed and why**

**Checks**

- [ ] `python3 scripts/validate_distribution.py` passes
- [ ] `python3 tests/check_mcp_fixtures.py` passes
- [ ] `tests/smoke.sh --chat` passes; output pasted below
- [ ] No secrets, `.env` files, brand or customer data, generated media, memories, or sessions
- [ ] No em dash in prose; `docs/provenance/` and `references/upstream.md` untouched
- [ ] After a `SOUL.md` change: `scripts/sync_claude_agent.py` and `scripts/sync_skill_rules.py` run, generated files committed
- [ ] For a release: `version` bumped equally in `distribution.yaml`, `.claude-plugin/plugin.json`, and `.codex-plugin/plugin.json`
- [ ] Approval before paid generation, publication, activation, scheduling, and spend is unchanged

**Smoke test output**

```text

```
