# Tests

Tests must verify the distribution before each stable release.

## Current checks

- required files are present;
- `distribution.yaml`, `config.yaml`, `mcp.json`, and `cron/jobs.json` have valid syntax and expected shapes;
- secret files and local runtime state are absent;
- added Skills have valid frontmatter and structure;
- the removed `*-usage` Skills are absent and their source texts exist in `docs/provenance/`;
- the pin table in `skills/providers/SKILL.md` is well formed: known vendors, a 40-character commit or `none` per row, an `Install` value (`hermes` only with a pin), a license note, and a check date;
- the English-facing operating report exists and the old French-facing path does not.

Run:

```bash
python3 scripts/validate_distribution.py
```

Check the provider install script without installing anything:

```bash
bash -n scripts/install_provider_skills.sh
scripts/install_provider_skills.sh --dry-run pika                   # prints the pinned commands, exit 0
scripts/install_provider_skills.sh --dry-run higgsfield fal kie-ai  # not installable with Hermes, exit 3
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
| 2026-10-08 | v0.20.2 | 0.2.0 | Scratch profile. 3 local Skills listed; upgrading from 0.1.0 removes the six `*-usage` Skills. Pika `ugc-ads` installs at its pin, scan SAFE, but the 0.2.0 script's post-install check failed on SIGPIPE (fixed). Higgsfield fails to fetch at its pinned URL (SKILL.md links a directory) and the GitHub form is blocked by the skills guard (`curl_pipe_shell`, `allowed_tools_field`); fal.ai `genmedia` is blocked (`curl_pipe_shell` twice); `--force` does not override. `hermes skills install` exits 0 on fetch failure. `hermes profile update` wipes hub-installed vendor Skills. |
| 2026-10-08 | v0.20.2 | 0.2.0 (after fix) | Scratch profile `ad-remaker-scratch`, deleted afterwards. 3 local Skills listed. `install_provider_skills.sh --profile ad-remaker-scratch pika`: scan SAFE, audit SAFE, `ugc-ads` listed as a `url` community Skill, exit 0. `higgsfield` and `fal` refused with exit 3 before calling Hermes. |
