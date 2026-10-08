---
name: meta-ads-usage
description: Read before any Meta ad action or command (go live, activate, create, edit, read back, budget, or schedule a Meta campaign, ad set, or ad on Facebook or Instagram, or give the user a Meta command or Ads Manager step to run), through Meta's ads MCP server or the Ads CLI, including the Meta campaign step of winning-ad-remake-workflow. Holds the paused-by-default, read-back, and separate-approval rules for Meta.
---

# Meta Ads usage

## Required rule loading

Before handling the task, read [the agent rules](references/agent-rules.md), generated from the canonical `SOUL.md`. Read the sibling `provider-policy` and `providers` Skills before any Meta command, instructions, or account action. Resolve sibling Skills relative to this installed Skill directory, not the working project. If a required file is missing or unreadable, report it and stop the affected operation. Do not infer rule loading from installation or from this summary.

In Codex, explicit Skill invocation applies these operating instructions to the task; it does not create an isolated profile or globally inject a persona. The Codex package bundles no MCP servers. Hermes `config.yaml` flags apply only in Hermes; check the actual session tools in every runtime.


Meta publishes no official agent Skill (checked on 2026-10-08), so this local Skill links Meta's own documentation and holds the rules for Meta campaign objects. `provider-policy` applies to every Meta call; this Skill adds the Meta-specific rules. Use `providers` for the route order.

Every source, tool name, and command below was checked against Meta's documentation on 2026-10-08. Treat it as a dated snapshot: inspect the live tool list or `--help` output before relying on it.

## 1. What Meta's tools reach

- The campaign, ad set, ad, creative, catalog, and reporting tools of the MCP server and the Ads CLI act only on the ad accounts, Pages, and catalogs the authenticated user or system user has been granted. They do not reach other advertisers' accounts.
- The MCP server also has `ads_library_search`, which searches the public Meta Ad Library. It reads only. Its coverage and limits compared with the Ad Library API are unverified.
- Competitor research belongs to the research stage of `winning-ad-remake-workflow`, where `providers` lists `ads_library_search` and the free Ad Library website as routes. Never use a Meta campaign step to look up competitor ads.

## 2. Routes

Use a route only when it is connected and authenticated, as `provider-policy` requires.

### MCP server

- Docs: [overview](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-overview), [get started](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started), [ad creation and management tools](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-tools-ad-creation-and-management). Endpoint: `https://mcp.facebook.com/ads`.
- This profile declares it in `config.yaml` as `meta_ads`, disabled, with OAuth and `${META_APP_ID}` as the client ID. Only the user enables it.
- Authentication paths documented by Meta:
  - Own Meta app: create or reuse an app at <https://developers.facebook.com/apps>, add the **Create & manage ads with ads MCP server** use case, and set the redirect URL for the MCP client in the app's Facebook Login for Business settings. OAuth then opens the Facebook Login for Business dialog. The app ID is the OAuth client ID.
  - No app: Meta states that owning a Meta app is not a prerequisite and points to [How to set up Meta ads AI connectors](https://www.facebook.com/business/help/1456422242197840). Whether the profile's `meta_ads` entry works without `META_APP_ID` is untested.
  - Meta also documents a user access token sent as `Authorization: Bearer`. This profile does not declare it.
- Documented tools for this Skill: `ads_create_campaign`, `ads_create_ad_set`, and `ads_create_ad` (each creates the object paused), `ads_update_entity` (edits an existing object), `ads_activate_entity` (paused to active, starts spending), `ads_get_ad_entities` (retrieves campaigns, ad sets, and ads), and `ads_account_get_activity_logs`.
- Ads MCP server rules: since July 16, 2026, anyone with full control of a business portfolio can limit what AI agents may do on an ad account, from budget changes to catalog updates ([announcement](https://www.facebook.com/business/news/meta-ads-ai-connectors)). Suggest them to the user as an optional server-side guard. They do not replace the rules below, and they are not verified in this profile.

### Ads CLI

- Docs: [overview](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview), [get started](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started), [command reference](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/command-reference).
- Install with the command recorded in `providers`, only with the user's approval under `provider-policy`. Requires Python 3.12 or later.
- Authentication: a Meta system user access token in `ACCESS_TOKEN` and the ad account in `AD_ACCOUNT_ID`, set by the user in the environment or a `.env` file. Never ask for the token in chat. Check with `meta auth status`.
- Commands are `meta [global options] ads <resource> <action>`. Global options such as `--output json` go before `ads`.
- Never pass `--force` or `--no-input` to a write or delete command.
- Dry run: `--execution-options validate_only` validates `campaign create` and `campaign update` without applying them, so nothing is created or spent. It appears in the `--help` of `meta-ads` 1.2.0 (checked on 2026-10-08), not in Meta's web docs, and not on `adset create` or `ad create`.

## 3. Create paused

1. Before the first write, confirm the ad account, Page, objects, names, and budget with the user, as `provider-policy` requires for account writes.
2. Create every campaign, ad set, and ad paused:
   - MCP: the create tools create paused objects. Do not pass a field that would make them active.
   - CLI: `--status` defaults to `PAUSED`, but always pass it explicitly, for example `meta ads campaign create --name "NAME" --objective OBJECTIVE --status PAUSED`, and the same for `adset create` and `ad create`. Never pass `--status ACTIVE` to a create command.
3. A budget set on a paused object spends nothing until activation, but it must be part of what the user confirmed in step 1. CLI budgets are in cents (`--daily-budget 5000` is 50.00 in the account currency).
4. Do not set start or end times unless the user approved that schedule under section 5.

## 4. Read back after every create or edit

1. After every create and every edit, read the object back: `ads_get_ad_entities` on the MCP, or `meta --output json ads campaign get <CAMPAIGN_ID>` (`adset get <AD_SET_ID>`, `ad get <AD_ID>`) on the CLI. Meta documents an `effective_status` column for the CLI `list` commands, not the fields of `get`; use `list` when `get` does not show the status.
2. Confirm that the object's status is `PAUSED`, and report the effective status when it is shown.
3. If the read fails, the status is missing, or the value is anything other than `PAUSED`, stop. Make no further write, report the status as **unknown** (or the value read), and wait for the user.
4. After an ambiguous timeout on a create, read back before anything else; never create the object again blindly.

## 5. Activation, scheduling, and spend

Activation, scheduling, and any budget change on an object that is not confirmed paused each need their own explicit approval. Approval of the remake, of the campaign preparation, or of an earlier budget does not cover them.

1. Ask first. Show the exact objects (names and IDs), the action, the budget and currency, and any start and end time, and wait for an explicit yes for that action.
2. Only after that approval:
   - activate with `ads_activate_entity`, or `meta ads campaign update <CAMPAIGN_ID> --status ACTIVE` (`adset update`, `ad update`);
   - change a budget with `ads_update_entity`, or `update` with `--daily-budget` or `--lifetime-budget`;
   - schedule with the start or end time the user approved.
3. Read the object back and report its status and budget.
4. If approvals are turned off or the session runs in yolo mode, never activate, schedule, or change a live budget. Stop and give the user the exact command or Ads Manager step instead.
