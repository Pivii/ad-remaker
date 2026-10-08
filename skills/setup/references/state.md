# Private state contract (schema 1)

Use the installed Skill's `scripts/setup_state.py`, not a recreated script. It uses only Python standard library and makes no network calls. Identify runtime (`claude`, `codex`, `hermes`) and working project explicitly. Never infer runtime from the product repository. The CLI must be accessible; if it cannot run, report persistence as unavailable rather than pretend choices were saved.

## Locations and ownership

- Claude Code: `${XDG_CONFIG_HOME:-~/.config}/ad-remaker/claude/`.
- Codex CLI/Desktop: `${XDG_CONFIG_HOME:-~/.config}/ad-remaker/codex/`.
- Hermes: `<active-installed-profile-home>/ad-remaker-state/`. Identify this home with `hermes -p <selected-profile> config path`; use its parent as `--profile-home`. Do not assume shell `HERMES_HOME` refers to that profile. The helper also accepts an explicitly set active `HERMES_HOME`.

Within each root, `setup.json` holds user/profile choices; `projects/<sha256-canonical-project-path>.json` holds that workspace's products and pending task. Files are private (0600 on POSIX, directories created 0700), outside product Git trees and plugin caches. No Git exclusion edits are needed: these paths are never in a product repository by default. Explicit `--state-dir` selects another private root, useful for tests, chosen by the user rather than inferred from project content. Never point it inside source/cache or a tracked project. Hermes runtime roots are isolated; runtimes do not share credentials or preference roots automatically.

Moving a project path creates a new workspace key. A user can deliberately copy its private project record to the new key after confirming ownership; do not automatically match names across projects. An existing external brand brief is imported only after the user selects and validates it. Settings survive plugin cache replacement and Hermes profile updates because they are outside `skills/` and the managed distribution files. Profile removal or deleting the private root removes them.

## Commands

Replace `HELPER`, `RUNTIME`, `PRIVATE_ROOT` and `PROJECT` with actual paths; quote paths and JSON. Normally omit `--state-dir` to use the paths above. Hermes uses `--profile-home` instead.

```bash
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT status
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT choose --free
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT complete
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT choose --research trendtrack --generation deferred --delivery free --fallback ask
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT task --task 'Original non-secret ad request'
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT product --product product-a --brief '{"name":"Product A","audience":"Confirmed audience","competitors":["Confirmed competitor"],"approved_claims":[],"sources":["README.md, confirmed by user"]}'
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT resolve --product product-a --task-routes '{"research":"free"}'
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT connection --provider trendtrack --status configured
python3 HELPER --runtime RUNTIME --state-dir PRIVATE_ROOT --project PROJECT task --task ''
```

`choose` saves answered stages, preserving others and completion status. `complete` requires all three answered; `deferred` is an explicit valid answer. `product --overrides '{"generation":"pika"}'` replaces only that product's route overrides; omit it to preserve existing overrides, or pass `{}` to clear them. Tools-only edits do not touch product data. `resolve --task-routes` changes only the current resolution, never persistent settings. `status` does not create directories. Partial choices remain incomplete until `complete`. No command resets state or deletes credentials.

## Schema and recovery

`setup.json` has exactly `schema_version: 1`, `complete: bool`, `routes: {research, generation, delivery}`, `fallback: ask|free`, and `connections: {provider: {status, checked_at}}`. Routes can be free, deferred, or a supported provider for that stage. Connection metadata is historical; every resolution returns `connection_check_required: true`. Verification does not bypass policy.

Project records have `schema_version: 1`, `products: {id: {brief, routes}}` and `pending_task: string`. Brief fields are restricted to name, URL, audience, markets, competitors, approved claims, asset paths and sources. Credentials/arbitrary configuration fields and obvious token patterns are rejected, but the user and agent must still avoid including any private credential in free text.

Schema 1 is the first version, so no legacy preference migration can be assumed. An absent file prompts setup once, including for existing installs. Compatible files load unchanged across updates. Invalid JSON, incompatible versions, malformed fields or symlink paths fail before overwriting the original. Explain the error; offer a fresh private state directory or a reviewed migration preserving a backup. Do not silently reset, assign free or downgrade unknown schemas. Writes use private temporary files, atomic replacement and a per-root lock; no provider/account operation is available in this helper.
