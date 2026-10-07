# Tests

Tests must verify the distribution before each stable release.

## Current checks

- required files are present;
- `distribution.yaml`, `config.yaml`, `mcp.json`, and `cron/jobs.json` have valid syntax and expected shapes;
- secret files and local runtime state are absent;
- added Skills have valid frontmatter and structure;
- the English-facing operating report exists and the old French-facing path does not;
- local installation with `hermes profile install` succeeds when release testing is performed.

Run:

```bash
python3 scripts/validate_distribution.py
```

Future business acceptance tests must use redistributable fixtures without sensitive data or competitor assets redistributed without authorization.
