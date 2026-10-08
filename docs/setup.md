# First run and setup

Ad Remaker starts with a short choice: free public research and local analysis, connect services you already use, or choose each stage. You do not need a paid service. Choosing free is a finished setup: no login, provider installation or paid query. It supports scripts, storyboards and prompts, but does not render a new video from prompts. Local analysis still needs its installed dependencies, and public signals do not reveal private spend or ROAS.

## Start or edit setup

| Runtime | Explicit entrypoint |
|---|---|
| Claude Code | `/ad-remaker:setup` in an installed plugin session |
| Hermes | Ask the installed profile: `Use your setup Skill to configure Ad Remaker.` The runtime reads it with `skill_view` named `setup`; no invented slash namespace. |
| Codex CLI/Desktop | `$ad-remaker:setup` in an installed plugin session; available through Skill selection as `ad-remaker:setup` |

A relevant ad request through the workflow also checks setup before research. Automatic Skill selection is runtime/model dependent; if the introduction does not appear, invoke setup explicitly. This does not trigger on ordinary coding tasks or installation. You can say **free for everything**, **skip setup for now**, or **configure tools only**, **product only**, or **both**. Skipping does not save a permanent free choice. Answered stages are retained if setup is interrupted. Deferred video or delivery does not block research.

Example first task:

> Use Ad Remaker to analyze this product's competitor ads. Explain the research and video routes before starting; I have no paid services. Guide setup, save free for everything, then continue this request.

## Products and saved choices

Start from the product repository or provide a chosen private brief/product URL. The agent suggests facts from relevant non-secret docs, shows sources and asks for confirmation or missing data. Multiple plausible products require a choice; their briefs/competitors/approved claims remain separate. A brief inferred from docs is not evidence that claims are approved.

Tools are shared across that user's projects within one runtime environment, or within one installed Hermes profile. Product records are keyed by working directory and product ID. Task choices override product routes, which override user/profile routes. A saved free choice remains free even when a paid provider later becomes visible.

State is outside Git and plugin caches: `~/.config/ad-remaker/claude/` or `~/.config/ad-remaker/codex/` (honoring `XDG_CONFIG_HOME`), or `<installed-Hermes-profile>/ad-remaker-state/`. Updates preserve these paths. Credentials remain in runtime storage. Directory moves create a fresh workspace key; profile removal can remove profile-local state. See [ADR-006](decisions/ADR-006-guided-setup-state.md) and the [helper contract](../skills/setup/references/state.md) for schema, overrides, recovery and private paths. Invalid/incompatible files are reported and preserved; recovery never silently chooses free.

## Connect selected services

The wizard explains research (for example TrendTrack) and video generation (declared Higgsfield, Pika or fal.ai routes), qualifying documented REST-only or user-provided routes. No account is assumed. It inspects existing tools first and guides only what you choose. Meta delivery is optional and not required for competitor research.

1. Claude Code: open `/mcp`, select the existing chosen `plugin:ad-remaker:<server>`, authenticate in the browser and inspect status. Personal settings do not modify the plugin's `.mcp.json`.
2. Hermes: identify the active profile's config, review enabling only the selected server there, then use `hermes -p <profile> mcp login <server>`. Distribution defaults and other profiles stay unchanged.
3. Codex: the package has no MCP servers. Deliberately add only the selected server to user configuration using verified `codex mcp add <server> --url <official-endpoint>`, then `codex mcp login <server>`. Desktop uses its actual configuration home; CLI configuration is not proof of GUI OAuth.

Full client-specific instructions and official sources are in [the setup connection reference](../skills/setup/references/connections.md). No live OAuth was tested by this implementation. Selected, configured, authenticated and verified usable are separate states. A known zero-credit non-destructive check plus tool discovery is required for verified session use; otherwise operation remains unverified. Never paste secrets into chat or briefs.

Selecting a provider is **not spend approval**. Each metered operation still needs its exact cost/batch approval; publishing, activation, scheduling and ad spend require their separate approvals. Setup performs no provider queries, media generation or account writes. If a preferred service fails, its saved preference remains; the agent asks once for recovery or announces a previously authorized free fallback.
