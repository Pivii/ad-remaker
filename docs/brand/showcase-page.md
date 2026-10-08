# Showcase page: design handoff

Status: first design recorded as validated on October 8, 2026. Implementation handoff revised on the same date; local copy adaptations require maintainer review before publication.
Design source: Claude Design canvas, private to the maintainer: https://claude.ai/artifact/7RKMDg6kWBckmwiCLg9PBf

This file is the build spec for a one-page site that presents the agent, its three install paths, example prompts, and a hosted alternative. It reuses the logo identity described in [logo-brief.md](logo-brief.md).

Provenance: visual tokens, typography, section order, and motion were transcribed from the design linked above. The private canvas was not independently checked during this revision. The copy table, current installation instructions, third-party scope notes, and layout adjustments for those changes are locally authored adaptations based on `SOUL.md`, `README.md`, and the dated vendor source. They are not claimed to be approved canvas text.

## Goal

Present Ad Remaker in one scroll. Place the attribution immediately below the hero title and the comparison before the local installation commands. The hosted option is the simple path for people who do not use a terminal. This independent distribution provides a Claude Code plugin, a Codex plugin, and a Hermes profile under MIT. After installation, the page shows how to start the agent and three example prompts, then invites contributions. The repository remains private pending maintainer approval.

## Tokens

| Token | Value | Use |
|---|---|---|
| Ink | `#121212` | Dark sections, text on light, code blocks |
| Paper | `#FFFFFF` | Page background |
| Soft surface | `#F4F4F2` | Workflow step cards |
| Line | `#E6E6E6` | Section dividers |
| Line on ink | `#333333` | Guardrail card borders |
| Text muted | `#555555` on paper, `#BDBDBD` or `#D4D4D4` on ink | Body copy |
| Accent | `#0866FF` | Front card and primary button. Exposed as one variable, see open decision 1 in the logo brief |
| Lime | `#C6F432` | Nav install button, hosted-option button, code text, hover outlines. Always with ink text, never white |
| Orange | `#FF7A1A` | Step 05 chip. Ink text |
| Purple | `#8B5CF6` | Steps 01 and 02 chips. White text only at 14 px bold or larger |

Radii: buttons and chips 999 px, step cards 24 px, install cards 28 px, guardrail cards 20 px, code blocks 14 px.

## Typography

| Role | Family | Settings |
|---|---|---|
| Display and headings | Poppins | 700, letter spacing -0.03em to -0.035em. H1 `clamp(44px, 6vw, 76px)`, line height 1.02. H2 `clamp(34px, 4.4vw, 52px)`, line height 1.08. Card titles 600 at 22 px, install titles 700 at 30 px |
| Body | DM Sans | 400 to 700. Hero lead 20 px, body 16 to 18 px, line height 1.55 to 1.6 |
| Labels and code | JetBrains Mono | 400 to 500, 13 to 15 px. Eyebrow labels uppercase, letter spacing 0.04em |

The wordmark in the nav and footer is lowercase `ad remaker`, Poppins 700, -0.03em, matching the logo. Use the SVG lockups from this folder in production instead of live text if possible.

## Layout

Content width 1200 px max, 24 px side gutter. Every row wraps to one column on a phone. Card grids use `repeat(auto-fit, minmax(<min>, 1fr))`.

1. **Header and hero, ink background.** Nav: wordmark left; "How it works", "Guardrails", "Try it" and a lime "Install" pill right. Hero, two columns: eyebrow pill `Hermes · Claude Code · Codex`, H1 "Turn ad references into your own creative.", attribution from the section below directly under the H1, lead paragraph from the copy table, primary button "Explore the install options" (accent, anchor `#install`) and ghost button "See the workflow" (anchor `#how`). Right column: the logo mark drawn large (max 480 px square), built from the logo brief geometry so it can animate.
2. **Stack legend, paper.** Four columns, one per card color: Research (purple), Generation (orange), Runtime (lime), The finished ad (accent). A 20 px swatch plus a title and the description from the copy table.
3. **How it works, `#how`.** H2 "From an ad reference to your own, in six steps." Six cards (min 300 px), with titles and descriptions from the copy table. Step 04 is the only ink card, with the chip "04 · YOU APPROVE".
4. **Guardrails, `#rules`, ink background.** H2 "It works for you. It never spends for you." Four cards with a lime stroke icon, titled "Never an exact copy", "No invented claims", "Approval before any spend", and "Nothing goes live alone", with descriptions from the copy table. Display the scope note directly below the heading: these rules apply to Ad Remaker's Hermes profile, Claude Code plugin, and Codex plugin.
5. **Choose a version, `#install`.** H2 "Which version should you choose?". Render the comparison below with four option columns and one row-label column. Preserve the option order: hosted service, Claude Code plugin, Codex plugin, Hermes profile. On phones, allow horizontal table scrolling with visible row labels, or render equivalent labeled cards. Place the hosted-service link and its affiliate disclosure inside this comparison. Follow it with three local installation cards (min 320 px):
   - **Claude Code plugin**, chip "Public access pending", body from the copy table, code block with the two commands in the installation section below.
   - **Codex plugin**, chip "Public access pending", body from the copy table, code block with the two Codex commands in the installation section below.
   - **Hermes profile**, chip "Public access pending", body from the copy table, code block `hermes profile install /path/to/ad-remaker --yes`.
6. **Try it, `#try`.** H2 "Try it with three prompts." Below it, a platform switcher with three tabs in this order: Claude Code, Codex, Hermes. Render it as an accessible tab list (`role="tablist"`, arrow keys move between tabs); tab buttons use the 999 px radius, the active tab is ink with white text, inactive tabs are paper with a line border. Each tab shows the start line from "Usage prompts for implementation" below in a code block, then three prompt cards (min 300 px, soft surface, 24 px radius): a JetBrains Mono label `01`, `02`, `03`, the prompt title, the prompt in a code block, and the "what to expect" line. In the Codex tab, prefix each prompt with `$ad-remaker:winning-ad-remake-workflow ` exactly as shown below. Close the section with the sentence "Approval questions before any spend or publication are expected behavior." and a text link "More examples in the README" to the repository README.
7. **Contribute, `#contribute`, ink background.** H2 "Help build it." Body from the copy table, then two buttons: lime "Read the contributing guide" linking to `CONTRIBUTING.md` on GitHub (`https://github.com/Pivii/ad-remaker/blob/main/CONTRIBUTING.md`) and ghost "Browse open issues" linking to `https://github.com/Pivii/ad-remaker/issues`.
8. **Footer.** Wordmark and the line "Analyze the mechanics. Rebuild for your product. You approve every spend."

Install cards share one structure (chip row, title, body that grows, bottom element). Use a shared bottom row with a minimum height of 60 px and enough room for the two-line plugin command. Align the cards at the bottom; do not clip or shrink code to preserve a fixed height.

## Copy for implementation

The following locally authored text completes the handoff. Use it literally when implementing; maintainer review remains required before publication. Headings, labels, and button text are specified in Layout above.

| Element | Text |
|---|---|
| Hero lead | Find competitor ads with public performance signals, break down their creative mechanics, and adapt them to your real product. You approve paid generation and any publication. |
| Research description | Find credible references and separate public signals from proven results. |
| Generation description | Turn an approved adaptation into creatives with the tools you connect. |
| Runtime description | Run the Ad Remaker agent in Hermes, Claude Code, or Codex. |
| The finished ad description | Receive inspected files and a launch pack for your review. |
| Step 01 title | Select the reference |
| Step 01 description | Choose an ad from a verifiable source. Public activity alone does not prove profitability. |
| Step 02 title | Take it apart |
| Step 02 description | Analyze its hook, structure, pacing, visuals, and call to action. |
| Step 03 title | Design a clean remake |
| Step 03 description | Adapt the mechanics to your product, with supported claims and no identifiable competitor traces. |
| Step 04 title | Approve the cost |
| Step 04 description | Review the batch, price estimate, and retry allowance before paid generation begins. |
| Step 05 title | Generate and inspect |
| Step 05 description | Use available tools to produce the approved adaptation, then inspect the downloaded outputs. |
| Step 06 title | Deliver for review |
| Step 06 description | Receive a launch pack, or approved paused Meta drafts when the connection is available. Activation needs separate approval. |
| Guardrails scope note | These safeguards govern Ad Remaker in Hermes, Claude Code, and Codex. |
| Never an exact copy description | Rebuild the creative mechanics for your product. Remove the competitor's identifiable content. |
| No invented claims description | Use evidence for product claims, testimonials, and results. Report what remains unknown. |
| Approval before any spend description | Approve the exact paid batch before generation. Campaign spend needs separate approval. |
| Nothing goes live alone description | Publication, activation, and scheduling each require explicit approval. |
| Hermes body | Install the profile from a local clone of this private repository. Repository access is required; public access is pending. Configure your model and enable only the providers you use. |
| Claude Code body | Install the existing plugin through this repository's marketplace. Repository access is required; public access is pending. Sign in only to the providers you use. |
| Codex body | Install the plugin through this repository's marketplace in Codex CLI or Desktop. Repository access is required; public access is pending. It bundles no provider connections. |
| Contribute body | Ad Remaker is open source under MIT. Add a free research source, improve a Skill, fix the docs, or report what happened in a real run. |

## Current installation instructions

The Hermes command assumes an authorized local clone; replace `/path/to/ad-remaker` with its actual path:

```bash
hermes profile install /path/to/ad-remaker --yes
```

The Claude Code plugin already exists. Both commands are needed for a first installation, and access to the private GitHub repository is required:

```bash
claude plugin marketplace add Pivii/ad-remaker
claude plugin install ad-remaker@ad-remaker
```

The Codex plugin installs through the same marketplace, in Codex CLI or Desktop. Both commands are needed, with the same repository access:

```bash
codex plugin marketplace add Pivii/ad-remaker --ref main
codex plugin add ad-remaker@ad-remaker
```

These commands follow the current [README](../../README.md). Public availability is a separate decision from implementation; do not defer the plugin command until a future shipment.

## Usage prompts for implementation

The Try it section quotes the README's "Usage" section; do not write new prompts here. When the README prompts change, update this table in the same pull request.

| Tab | Start line |
|---|---|
| Claude Code | `claude --agent ad-remaker:ad-remaker` |
| Codex | `codex`, run from your own project folder; start each prompt with `$ad-remaker:winning-ad-remake-workflow` |
| Hermes | `hermes -p ad-remaker` |

| Card | Title | Prompt | What to expect |
|---|---|---|---|
| 01 | Free first run, no provider connected | `Find winning ads for <category> in the public ad libraries and give me a deconstruction of the best one.` | The agent reports which stages run on the free path and which tools are missing. |
| 02 | Full remake for your brand | `Here is my product page <url>. Find 3 competitor ads with real performance signals and propose a remake adapted to my product. Estimate costs before generating anything.` | Before any paid generation, the agent shows the batch with units, prices, retry margin, total, and currency, and waits for you to approve that exact batch. |
| 03 | Analyze an ad you already have | `Deconstruct this ad (<file or link>): hook, structure, offer, visual mechanics, and what I can reuse without copying.` | The agent asks before downloading a public video or installing a missing local tool such as `ffmpeg` or `scenedetect`. |

## Attribution and comparison for implementation

Render the following attribution literally below the hero title:

Inspired by the Recreate competitor ads agent from [Rerun](https://rerun.build/templates/recreate-competitor-ads-meta?via=aRLmG4). If you want the same agent without installing or configuring anything, use Rerun directly.

This is an independent, unofficial adaptation. According to the maintainer, the marketing team (Théo) authorized an open-source release on October 8, 2026, provided attribution is included. These are affiliate links: the maintainer may earn a commission.

Render the same comparison as the README, including its dated source links and prerequisite note:

### Which version should you choose?

Rerun is the simple option if you want to get started without a terminal. The plugin and profile let you use your existing environment.

| Criterion | [Rerun](https://rerun.build?via=aRLmG4) | Claude Code plugin | Codex CLI and Desktop plugin | Hermes profile |
|---|---|---|---|---|
| Intended users | Non-technical users who want a ready-to-use agent | People who already use Claude Code | People who already use Codex CLI or Desktop | People who run Hermes |
| Setup time | A few seconds to add the agent; about 5 min for configuration, according to the template page | A few minutes if Claude Code is already configured, plus connections to the services you use (estimate) | A few minutes if Codex CLI is already configured; vendors are optional (estimate) | A few minutes if Hermes is already configured, plus model selection and connections to the services you use (estimate) |
| Hosting | Hosted and managed by the service | On the machine where you run Claude Code | On the machine where you run Codex | On the machine or server where you run Hermes |
| Cost | Free trial to get started, then a paid subscription; model and service costs depend on usage | Free plugin (MIT); Claude Code access, models, and external services depend on your plans | Free plugin (MIT); Codex model access and external services depend on your plans | Free profile (MIT); models, optional hosting, and external services depend on your plans |
| External tools needed | Higgsfield or Kie AI (or another generator) for generation; TrendTrack is optional for research; Meta Ads is optional for drafts | TrendTrack is optional; Higgsfield or Kie AI (or another connected generator) for generation; Meta Ads is optional; local analysis mode works without a generator | None for the text remake pack; local scripts need their declared dependencies; optional vendors are separately configured | TrendTrack is optional; Higgsfield or Kie AI (or another connected generator) for generation; Meta Ads is optional; local analysis mode works without a generator |

Information checked on October 8, 2026: [template](https://rerun.build/templates/recreate-competitor-ads-meta?via=aRLmG4) and [service plans](https://rerun.build/pricing?via=aRLmG4). The free trial requires a payment card. Adding the template does not connect your external accounts. Research can use public ad libraries when TrendTrack is unavailable; delivery provides files for manual import when Meta Ads is unavailable. Plans and requirements may change.

Use only this project's locally authored logo and visuals. Do not reuse the credited service's logo, screenshots, agent-board images, or other visuals. Do not describe this distribution as an official product. Keep the credited service's name inside the attribution and comparison only. Every link to that service must include `?via=aRLmG4`.

External links open in a new tab with `rel="noopener"`. Keep the affiliate disclosure visible beside the attribution and comparison.

## Hover and motion

All transitions use `cubic-bezier(.2, .8, .2, 1)`, 200 to 500 ms. Disable them under `prefers-reduced-motion: reduce`.

| Element | Hover |
|---|---|
| Hero logo stack | The four cards fan out to the left: purple `translateX(-22%) rotate(-7deg)`, orange `-12%, -4deg`, lime `-4%, -1.5deg`, front card `translate(4%, -3%) rotate(3deg)`. 500 ms |
| Primary button | Lifts 2 px with a soft accent shadow. Press scales to 0.97 |
| Lime buttons | Lift 2 px with a lime glow |
| Ghost button | Faint white fill, lighter border |
| Nav links | Lime underline grows from the left |
| Legend swatches | Scale 1.3 and rotate -8deg |
| Step cards | Lift 6 px, turn white, soft shadow; the number chip tilts -4deg and scales 1.06 |
| Guardrail cards | Border turns lime, background lightens slightly, lift 4 px, icon scales 1.15 |
| Install cards | Lift 6 px with a hard 8 px offset shadow (ink); the code block gets a lime inner outline |

## Open items

- Public access: the repository remains private. MIT is declared in `LICENSE` and both manifests. Change access labels only after the maintainer approves publication.
- Copy review: the implementation text above is a local adaptation, not recovered approved canvas text. Review it before publication.
- The accent blue follows open decision 1 of the logo brief. Keep it in a single variable.
- A motion design video based on the card stack is planned. Its brief will live in this folder.
- Repository links: the contributing guide and issues links work only for people with repository access until publication is approved.
- Codex Desktop: the install card covers CLI and Desktop. The Desktop Plugins Directory and Skill selection in its interface are not verified yet; see `docs/codex-setup.md`.
