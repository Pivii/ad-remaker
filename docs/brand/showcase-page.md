# Showcase page: design handoff

Status: first design recorded as validated on October 8, 2026. Implementation handoff revised on the same date; local copy adaptations require maintainer review before publication.
Design source: Claude Design canvas, private to the maintainer: https://claude.ai/artifact/7RKMDg6kWBckmwiCLg9PBf

This file is the build spec for a one-page site that presents the agent, its two install paths, and a separate third-party Rerun template. It reuses the logo identity described in [logo-brief.md](logo-brief.md).

Provenance: visual tokens, typography, section order, and motion were transcribed from the design linked above. The private canvas was not independently checked during this revision. The copy table, current installation instructions, third-party scope notes, and layout adjustments for those changes are locally authored adaptations based on `SOUL.md`, `README.md`, and the dated vendor source. They are not claimed to be approved canvas text.

## Goal

Present Ad Remaker in one scroll. Keep the no-code Rerun template first in the install section, with its third-party status and workflow differences visible. The Hermes profile and Claude Code plugin follow because they need a terminal. Both exist today in this private repository; public access and an open-source license are not yet available.

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
| Lime | `#C6F432` | Nav install button, Rerun button, code text, hover outlines. Always with ink text, never white |
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

1. **Header and hero, ink background.** Nav: wordmark left; "How it works", "Guardrails" and a lime "Install" pill right. Hero, two columns: eyebrow pill `Hermes · Claude Code · A separate Rerun template`, H1 "Turn ad references into your own creative.", lead paragraph from the copy table, primary button "Explore the install options" (accent, anchor `#install`) and ghost button "See the workflow" (anchor `#how`). Right column: the logo mark drawn large (max 480 px square), built from the logo brief geometry so it can animate.
2. **Stack legend, paper.** Four columns, one per card color: Research (purple), Generation (orange), Runtime (lime), The finished ad (accent). A 20 px swatch plus a title and the description from the copy table.
3. **How it works, `#how`.** H2 "From an ad reference to your own, in six steps." Six cards (min 300 px), with titles and descriptions from the copy table. Step 04 is the only ink card, with the chip "04 · YOU APPROVE".
4. **Guardrails, `#rules`, ink background.** H2 "It works for you. It never spends for you." Four cards with a lime stroke icon, titled "Never an exact copy", "No invented claims", "Approval before any spend", and "Nothing goes live alone", with descriptions from the copy table. Display the scope note directly below the heading: these rules apply to Ad Remaker's Hermes profile and Claude Code plugin, not automatically to the third-party template.
5. **Install, `#install`.** H2 "Run it where you already work." Three cards (min 320 px), in this order:
   - **Rerun template**, ink card, chips "No code" and "Third-party template". Body and three lime checks from the copy table. Keep the workflow-difference notice visible next to the lime button "View the Rerun template". Do not label it "Recommended" or present it as an installation of this distribution.
   - **Hermes profile**, chip "Public access pending", body from the copy table, code block `hermes profile install /path/to/ad-remaker --yes`.
   - **Claude Code plugin**, chip "Public access pending", body from the copy table, code block with the two commands in the installation section below.
6. **Footer.** Wordmark and the line "Analyze the mechanics. Rebuild for your product. You approve every spend."

Install cards share one structure (chip row, title, body that grows, bottom element). Use a shared bottom row with a minimum height of 60 px and enough room for the two-line plugin command. Align the cards at the bottom; do not clip or shrink code to preserve a fixed height.

## Copy for implementation

The following locally authored text completes the handoff. Use it literally when implementing; maintainer review remains required before publication. Headings, labels, and button text are specified in Layout above.

| Element | Text |
|---|---|
| Hero lead | Find competitor ads with public performance signals, break down their creative mechanics, and adapt them to your real product. You approve paid generation and any publication. |
| Research description | Find credible references and separate public signals from proven results. |
| Generation description | Turn an approved adaptation into creatives with the tools you connect. |
| Runtime description | Run the Ad Remaker agent in Hermes or Claude Code. |
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
| Guardrails scope note | These safeguards govern Ad Remaker in Hermes and Claude Code. The separate Rerun template has its own workflow; review its differences below. |
| Never an exact copy description | Rebuild the creative mechanics for your product. Remove the competitor's identifiable content. |
| No invented claims description | Use evidence for product claims, testimonials, and results. Report what remains unknown. |
| Approval before any spend description | Approve the exact paid batch before generation. Campaign spend needs separate approval. |
| Nothing goes live alone description | Publication, activation, and scheduling each require explicit approval. |
| Rerun body | A separate no-code template published by Rerun. Review its workflow and provider requirements before using it. |
| Rerun check 1 | Template listed as free, with about five minutes of setup. Connected service costs are separate and must be checked. |
| Rerun check 2 | The vendor describes competitor-ad discovery every Monday. |
| Rerun check 3 | With Meta Ads connected, approved creatives are delivered as paused drafts; otherwise, as an import pack. |
| Rerun workflow-difference notice | Rerun describes recreating approved blueprints "one to one". Ad Remaker forbids exact copies. This template is not an installation of Ad Remaker and does not inherit its safeguards. |
| Hermes body | Install the profile from a local clone of this private repository. Repository access is required; public access is pending. Configure your model and enable only the providers you use. |
| Claude Code body | Install the existing plugin through this repository's marketplace. Repository access is required; public access is pending. Sign in only to the providers you use. |

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

These commands follow the current [README](../../README.md). Public availability is a separate decision from implementation; do not defer the plugin command until a future shipment.

## Links

| Target | URL |
|---|---|
| Rerun template, with the maintainer's affiliate code | `https://rerun.build/templates/recreate-competitor-ads-meta?via=aRLmG4` |

Vendor source: [Rerun template page](https://rerun.build/templates/recreate-competitor-ads-meta), checked on October 8, 2026. Its page lists the template as free, estimates five minutes of setup, describes Monday discovery and paused Meta drafts, and explicitly offers an import pack when Meta Ads is not connected. These are dated vendor claims, not evidence of a working connection or an end-to-end test. Recheck them before publication. Template pricing does not establish the cost of connected services.

External links open in a new tab with `rel="noopener"`. Disclose the affiliate link wherever the site's legal pages require it.

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
| Install cards | Lift 6 px with a hard 8 px offset shadow (ink, or lime on the Rerun card); the code block gets a lime inner outline |

## Open items

- Public access and licensing: the repository is private and its current license is Proprietary. Update access labels and installation guidance only after those decisions change; do not promise an open-source release.
- Copy review: the implementation text above is a local adaptation, not recovered approved canvas text. Review it before publication.
- Rerun recommendation: retain the visible third-party distinction and workflow-difference notice. Only recommend it as a compatible Ad Remaker path after its workflow is verified to preserve the no-exact-copy rule. Never weaken `SOUL.md` to resolve this mismatch.
- The accent blue follows open decision 1 of the logo brief. Keep it in a single variable.
- A motion design video based on the card stack is planned. Its brief will live in this folder.
