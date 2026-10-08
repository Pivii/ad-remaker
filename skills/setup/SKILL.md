---
name: setup
description: Guide first-use Ad Remaker configuration, save free or connected research/video routes, and confirm separate product briefs. Use on the first relevant ad task, to resume interrupted onboarding, or to edit tools/product setup. Ordinary coding tasks do not need onboarding.
---

# Ad Remaker setup

## Required rule loading

Before handling the task, read [the agent rules](references/agent-rules.md), generated from canonical `SOUL.md`, and sibling `provider-policy` and `providers` Skills with their rule references. Resolve sibling Skills from this installed directory, never from the product repository. Read `meta-ads-usage` before any Meta guidance. Missing rules block the affected operation.

Loading this Skill as a policy dependency does not recursively execute the wizard: check state once per relevant task. Setup runs on a relevant user task, never during installation. Keep the original request through the questionnaire and resume it when the applicable setup is complete. Do not start research before offering first-use choices. Tools-only setup does not require a product brief.

## 1. Load choices before asking

Run the bundled stdlib helper [scripts/setup_state.py](scripts/setup_state.py) with the identified runtime and working project. Read [state.md](references/state.md) for paths, commands, schema, editing and recovery. `status` is read-only and absent state is incomplete, never an implicit free choice. In Hermes identify the active installed profile home first; do not use the distribution's config or another profile.

If completed compatible settings exist, resolve current-task choice over product override over user/profile route. Respect an explicit saved free route even if a provider is now visible. Recheck tool availability when its stage runs; stored connection history is dated evidence only. Proceed without the onboarding questionnaire. Explicit setup can edit **tools**, **product**, or **both** without resetting unrelated answers or credentials.

For incomplete settings, preserve the original task in the private project's `pending_task` when the user accepts setup; save each answered stage promptly and resume partial answers. Never persist credentials or a request containing secrets. Keep the original task in session context when persistence is unavailable and explain that setup will not survive a new session. Never claim it was saved. If the user says **skip setup for now**, retain incomplete state, do not save new route choices, and continue with available permitted tools and explicit limits for this task only.

## 2. Offer a short guided choice

Adapt this introduction to the user's language:

> Ad Remaker can use public ad libraries and local analysis tools, or connected services for ad research and video creation. You do not need a paid service to start. Use the free path, connect services you already use, or configure each stage?

Ask at most three questions in one batch. A clear **free for everything** answer calls `choose --free`, followed by `complete`; it needs no vendor choice, login, installation or provider call. Explain that free means public research and script/storyboard/prompts, **no new video rendered from prompts**, and local analysis requires installed dependencies. Public signals do not prove spend or ROAS. Continue the original task, asking only for missing product facts. Do not promote paid tools on subsequent free tasks.

For stage choices, offer:

| Stage | Options | Guidance |
|---|---|---|
| Research | Public libraries; existing supported service; later | TrendTrack is a declared research route. Brandsearch is usable only through a user-provided working connection, no public endpoint here. |
| Video creation | Script/storyboard/prompts; existing generator; later | Higgsfield, Pika and fal.ai have declared MCP routes. Kie.ai is a documented REST route, no bundled MCP or pinned installable Skill. |
| Delivery | Files/manual import; later | Default to manual files only after the user accepts this default; offer Meta only when requested or relevant. |

Use `providers` and [service-readiness.md](references/service-readiness.md), then current official docs and actual tools for selected services. These are supported declared routes, not verified accounts. Do not list invented prices, capabilities or endpoints. An analysis request can finish setup with generation/delivery explicitly deferred; unrelated stages never block research.

Save provider preference on selection, independent of authentication. Ask once whether an unavailable preferred route should use free automatically with a notice or ask each time; save `fallback: free` only on explicit consent, otherwise `ask`. Selecting a provider authorizes no spending or external account writes.

## 3. Guide only selected connections

Inspect actual runtime tools/status first. Reuse a working connection, and let the user still choose free. Read [connections.md](references/connections.md) for client-specific steps before guidance. Only a documented, non-destructive check known to consume no credits plus tool discovery can establish **verified usable in this session**. If none is known, keep **configured/unverified** and explain that setup can finish with this limitation. No generation, research query, tracker/folder/campaign creation, spend, publishing, scheduling or activation during setup. No login flow for the free path.

Record **selected**, **configured**, **verified** or **blocked**, with a date. Cancellation/failure stays pending: report the actual blocker and offer reconnect, later, or an explicit free alternative. Never silently change the saved provider preference. Do not install a CLI, package, Skill or model without the existing exact-command approval. Never ask for keys, passwords or tokens in chat or briefs.

## 4. Confirm product context separately

For a relevant ad task, inspect only relevant non-secret product docs the user has made available (for example README or product brief). Do not recursively scan credentials, customer records or unrelated files. Present inferred facts with their source; ask only for missing/ambiguous items and confirmation. Inferred claims are not approved claims.

One clear product does not require re-entry. If several products are plausible, ask which one; maintain distinct IDs/briefs/competitors. With no repository context, offer an existing private brief, a product URL, or a short basic brief. Read only a user-selected external brief. Store confirmed name/URL/audience/markets/competitors/approved claims/assets/sources with `product`; never promote an unconfirmed claim into `approved_claims`. `status` lists existing products for this workspace, and `resolve --product ID` selects one. Do not automatically reuse another project's product. Product setup or editing does not overwrite tool choices; tools setup does not overwrite briefs.

## 5. Finish and continue

Call `complete` only after every stage has an explicit free, deferred or provider choice. Pending connections may remain unverified; completion means preferences answered, not connected. Summarize the selected routes and actual session status briefly, then continue the retained request. Clear `pending_task` only once it has resumed. In routine use, a short line is enough: "Product A; public research; video creation deferred."

If a preferred route fails later, keep it saved and report recovery for that stage. Apply an explicitly permitted free fallback with a notice, otherwise ask once for this task's alternative. Re-read `provider-policy` for each operation's cost approval; setup never supplies that approval.
