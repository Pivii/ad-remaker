# Tests

Tests must verify the distribution before each stable release.

## Current checks

- required files are present;
- `distribution.yaml`, `config.yaml`, `mcp.json`, and `cron/jobs.json` have valid syntax and expected shapes;
- secret files and local runtime state are absent;
- added Skills have valid frontmatter and structure;
- the removed `*-usage` Skills are absent and their source texts exist in `docs/provenance/`;
- the pin table in `skills/providers/SKILL.md` is well formed: known vendors, a 40-character commit or `none` per row, a license note, and a check date;
- the English-facing operating report exists and the old French-facing path does not.

Run:

```bash
python3 scripts/validate_distribution.py
```

Check the provider install script without installing anything:

```bash
bash -n scripts/install_provider_skills.sh
scripts/install_provider_skills.sh --dry-run higgsfield pika fal   # prints the pinned commands, exit 0
scripts/install_provider_skills.sh --dry-run kie-ai                 # no pin, exit 3
scripts/install_provider_skills.sh --dry-run acme                   # unknown vendor, exit 2
```

Future business acceptance tests must use redistributable fixtures without sensitive data or competitor assets redistributed without authorization.

## Release install check

Before each stable release, install the distribution into a local Hermes profile and confirm it loads:

```bash
hermes profile install /path/to/ad-remaker --yes            # first install
hermes profile install /path/to/ad-remaker --force --yes    # reinstall, user data preserved
hermes profile show ad-remaker                              # SOUL.md exists, Skills count matches skills/
hermes -p ad-remaker skills list                            # every Skill is listed and enabled
hermes -p ad-remaker mcp list                               # matches the declared MCP servers
```

The installed profile has no model configured. Set one before chatting, for example with `hermes -p ad-remaker model`.

### Install log

| Date | Hermes | Version installed | Result |
|---|---|---|---|
| 2026-10-07 | v0.20.2 | 0.1.0 | Installed. SOUL.md loaded, 7 Skills listed and enabled, no MCP servers, no model configured. Not tested in chat. |
