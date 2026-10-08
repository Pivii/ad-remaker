# Contributing to Ad Remaker

Thank you for helping. Ad Remaker is MIT-licensed, and outside contributions are welcome. Useful help includes:

- new free research sources, such as public ad libraries the agent does not list yet;
- provider integrations, following the provider rules below;
- improvements to the Skills in `skills/`, especially fixes for behavior you saw in a real run;
- documentation, including translations of the example prompts in the README;
- bug reports from real runs: what you asked, what the agent did, and on which runtime and version.

If you are unsure whether an idea fits, open an issue first.

## Where to read first

- [`docs/architecture.md`](docs/architecture.md): how the profile, the Skills, the MCP servers, and the scripts fit together.
- [`docs/decisions/`](docs/decisions/): the architecture decisions (ADRs) and why they were made.
- [`SOUL.md`](SOUL.md) and [`skills/README.md`](skills/README.md): the agent's rules and what each Skill does.
- `CONTEXT.md`, the domain glossary, once it exists at the repository root. It is created when the first terms are settled.

Coding agents working on this repository also follow [`AGENTS.md`](AGENTS.md) and [`CLAUDE.md`](CLAUDE.md). This guide says the same things for people.

## Set up and run the checks

```bash
git clone https://github.com/Pivii/ad-remaker.git
cd ad-remaker
python3 scripts/validate_distribution.py
python3 tests/check_mcp_fixtures.py
```

The validator checks required files, manifests, MCP declarations, secrets, and Skill structure. The fixture check makes sure the validator rejects every invalid MCP example in `tests/fixtures/mcp/`. Both run offline in a few seconds. PyYAML is optional.

Before you open a pull request, run the smoke test and paste its output in the pull request:

```bash
tests/smoke.sh --chat
```

It runs the two checks above, installs your checkout into a throwaway Hermes profile named `ar-smoke-*` that it always deletes, and runs a few headless chat scenarios. What it costs: stage 3 calls only the chat model (by default `gpt-6.1-sol` through the `openai-codex` provider, which uses your ChatGPT subscription allowance; authenticate first with `hermes auth add openai-codex`). It never calls an ad or media provider and never touches your own `ad-remaker` profile. Without Hermes installed, stages 2 and 3 print `SKIPPED`. Stages, options, and the other models you can select are described in [`tests/README.md`](tests/README.md).

## Try your change on each runtime

Start each runtime from a scratch folder outside the repository, so the contributor instructions in `AGENTS.md` and `CLAUDE.md` are not loaded as if they were the agent's own.

- **Claude Code**: `claude --plugin-dir /path/to/your/clone` loads your checkout for one session without installing it. `claude plugin validate /path/to/your/clone/.claude-plugin/plugin.json` checks the manifest; one warning about the root `CLAUDE.md` is expected.
- **Hermes**: install into a throwaway profile, never over your real one, then delete it:

  ```bash
  hermes profile install /path/to/your/clone --name ad-remaker-dev --yes
  hermes -p ad-remaker-dev skills list
  hermes -p ad-remaker-dev model
  hermes -p ad-remaker-dev
  hermes profile delete -y ad-remaker-dev
  ```

- **Codex**: `python3 tests/check_codex.py` installs a clean export into a throwaway Codex home, checks the five Skills and the empty MCP mapping, and removes everything, with no model call. To try it by hand, follow the local export steps in [`docs/codex-setup.md`](docs/codex-setup.md); never install a live development clone.

Never sign in to a vendor, run a paid generation, or touch a real ad account while testing a contribution.

## Repository rules

- **Nothing private in Git.** No secrets, tokens, `.env` files, brand or customer data, generated media, memories, or sessions. Brand data for your own use goes in `local/brands/<brand>/`, which is ignored by Git.
- **Language and style.** Write repository documentation in clear English. Do not use the em dash character in prose. Keep exact product names, commands, and quoted source text as they are.
- **Source texts stay verbatim.** Never edit `docs/provenance/` or `skills/winning-ad-remake-workflow/references/upstream.md`. When you change the workflow, edit its `SKILL.md` only.
- **`SOUL.md` has generated copies.** After editing it, run `python3 scripts/sync_claude_agent.py` and `python3 scripts/sync_skill_rules.py`, and commit the regenerated `agents/ad-remaker.md` and `skills/*/references/agent-rules.md` with it. Never edit those copies by hand.
- **Versions move together.** `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` equals `version` in `distribution.yaml`. Bump all three for every release.
- **MCP servers are declared twice.** Add a server to `config.yaml` under `mcp_servers` with `enabled: false`, and to `.mcp.json` under the same name and URL. Use OAuth or `${ENV_VAR}` placeholders declared in `distribution.yaml` `env_requires`, and record its official source and check date in `docs/service-matrix.md`.
- **Vendor pins are deliberate.** To change a vendor Skill pin in `skills/providers/SKILL.md`: read the vendor's diff, check the license again, update `Pinned ref`, `License`, and `Checked` in the pin table, bump the version, and run `hermes skills audit` after reinstalling. Never copy or patch a vendor Skill into `skills/`.
- **New required files.** If you add a file the distribution needs, add it to `REQUIRED_FILES` in `scripts/validate_distribution.py`.
- **Dated facts stay dated.** Model names, prices, tool counts, and connection states from the historical report or vendor pages are snapshots. Do not present them as current, and do not describe a capability the Skills do not have.

## Safety rules you must not weaken

These rules protect the people who run the agent. A pull request that loosens them will not be merged.

- No paid generation without a cost estimate and explicit approval of that exact batch.
- No publication, activation, scheduling, or spend without a separate, explicit human approval.
- Meta campaign objects are created paused and read back after every write.
- Any new scheduled job ships paused and never triggers spending, publication, or campaign activation.

## Issues and pull requests

- Issues live in [GitHub Issues](https://github.com/Pivii/ad-remaker/issues). Use the bug report or feature request template.
- The maintainer triages with these labels: `needs-triage` (new, not yet reviewed), `needs-info` (waiting for details from the reporter), `ready-for-agent` (specified well enough for a coding agent), `ready-for-human` (needs a person), and `wontfix`.
- Name your branch after its type and issue, for example `feat/24-usage-contributing` or `fix/<issue>-<short-name>`.
- Use a short conventional title for the pull request, such as `docs: ...`, `feat: ...`, or `fix: ...`, and reference the issue (`Closes #N`).
- The pull request description must include the output of `tests/smoke.sh --chat`. The template lists the other checks.

## Repository structure

- `distribution.yaml`: profile-distribution manifest.
- `SOUL.md`: stable identity and non-negotiable safeguards.
- `config.yaml`: credential-free Hermes defaults, including the official vendor MCP servers under `mcp_servers`. Every server ships disabled; see `docs/architecture.md` to enable one.
- `cron/jobs.json`: distributed scheduled jobs. It is currently empty.
- `.claude-plugin/`: Claude Code plugin manifest (`plugin.json`, version kept equal to `distribution.yaml`) and the one-plugin marketplace (`marketplace.json`).
- `.codex-plugin/plugin.json`: Codex Skills manifest, explicitly no bundled MCP servers.
- `agents/ad-remaker.md`: Claude Code subagent. Its body is generated from `SOUL.md` by `scripts/sync_claude_agent.py`.
- `.mcp.json`: the vendor MCP servers for Claude Code, the same set as `config.yaml`.
- `skills/`: the business workflow, the shared provider policy, the Meta rules, the free fallback mode, and the `providers` routing directory with its vendor pin table.
- `docs/claude-code-setup.md` and `docs/codex-setup.md`: installation details per runtime.
- `docs/ad-remaker-complete-operating-report.md`: complete historical source report, translated into English.
- `docs/architecture.md`: distribution layering and ownership boundaries.
- `docs/service-matrix.md`: integration readiness states without unsupported availability claims.
- `docs/provenance/`: verbatim vendor source texts kept for provenance.
- `docs/decisions/`: architecture decisions.
- `docs/brand/`: logo files, the logo brief with its usage rules, and the showcase page design handoff.
- `scripts/validate_distribution.py`: local structural and safety validator, for all three runtime packages.
- `scripts/sync_claude_agent.py`: regenerates the subagent body from `SOUL.md`.
- `scripts/sync_skill_rules.py`: generates each Skill-local rule reference from `SOUL.md`.
- `scripts/export_codex_package.py`: exports a clean local Codex marketplace.
- `scripts/install_provider_skills.sh`: installs pinned official vendor Skills into the profile, then runs `hermes skills audit`.
- `tests/`: the smoke test, Codex checks, acceptance guidance, and redistributable fixtures.

## Source material

The repository was initialized from the operating report provided on October 7, 2026: the [Ad Remaker report](https://sucqmcejnrnvcdnrwhld.supabase.co/storage/v1/object/public/published/3695/ad-remaker-fonctionnement/ad-remaker-fonctionnement-complet.md?v=1791399468681), kept in English in `docs/ad-remaker-complete-operating-report.md`. That report documents the target architecture, business workflow, safeguards, proposed integrations, and their status at the time of observation. Historical availability statements in the report are not evidence of current tool or MCP availability.

Provider rules live in the local `provider-policy` Skill. Official vendor Skills are not bundled: each user installs only the vendors they pay for, at a pinned commit (see `docs/decisions/ADR-002-provider-skill-layers.md`).

## License

This repository is licensed under the [MIT License](LICENSE). External vendor source material retained for provenance and separately installed vendor Skills keep their own terms; the MIT license does not relicense them.
