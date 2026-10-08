# Showcase page: design handoff

Status: first design validated on October 8, 2026. Ready to build.
Design source: Claude Design canvas, private to the maintainer: https://claude.ai/artifact/7RKMDg6kWBckmwiCLg9PBf

This file is the build spec for a one-page site that presents the agent and its install paths. It reuses the logo identity described in [logo-brief.md](logo-brief.md). Every value below comes from the validated design.

## Goal

Present Ad Remaker in one scroll, and send non-technical visitors to the Rerun template first. The open source paths (Hermes profile, Claude Code plugin) come second, because they need a terminal.

## Tokens

| Token | Value | Use |
|---|---|---|
| Ink | `#121212` | Dark sections, text on light, code blocks |
| Paper | `#FFFFFF` | Page background |
| Soft surface | `#F4F4F2` | Workflow step cards |
| Line | `#E6E6E6` | Section dividers |
| Line on ink | `#333333` | Guardrail card borders |
| Text muted | `#555555` on paper, `#BDBDBD` or `#D4D4D4` on ink | Body copy |
| Accent | `#0866FF` | Front card, primary button, "Recommended" chip. Exposed as one variable, see open decision 1 in the logo brief |
| Lime | `#C6F432` | Nav install button, Rerun button, code text, hover outlines. Always with ink text, never white |
| Orange | `#FF7A1A` | Step 05 chip, "In progress" chip. Ink text |
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

1. **Header and hero, ink background.** Nav: wordmark left; "How it works", "Guardrails" and a lime "Install" pill right. Hero, two columns: eyebrow pill `On Rerun · Hermes · Claude Code`, H1 "Remake the ads that already win.", lead paragraph, primary button "Start free on Rerun" (accent, opens the Rerun link) and ghost button "See the workflow" (anchor `#how`). Right column: the logo mark drawn large (max 480 px square), built from the logo brief geometry so it can animate.
2. **Stack legend, paper.** Four columns, one per card color: Research (purple), Generation (orange), Runtime (lime), The finished ad (accent). A 20 px swatch plus a title and one line.
3. **How it works, `#how`.** H2 "From a proven ad to your own, in six steps." Six cards (min 300 px): select the reference, take it apart, design a clean remake, approve the cost, generate and inspect, deliver with the campaign paused. Step 04 is the only ink card, with the chip "04 · YOU APPROVE".
4. **Guardrails, `#rules`, ink background.** H2 "It works for you. It never spends for you." Four cards with a lime stroke icon: never an exact copy, no invented claims, approval before any spend, nothing goes live alone.
5. **Install, `#install`.** H2 "Run it where you already work." Three cards (min 320 px), in this order:
   - **Rerun template**, ink card, chips "No code" and "Recommended". Three lime checks: free with about 5 minutes of setup, new competitor ads every Monday, drafts land paused in Meta Ads Manager. Lime button "Use the template, free".
   - **Hermes profile**, chip "Open source soon", code block `hermes profile install [REPO URL]`.
   - **Claude Code plugin**, chip "In progress", code block `[PLUGIN INSTALL COMMAND]`.
6. **Footer.** Wordmark and the line "Analyze the mechanics. Rebuild for your product. You approve every spend."

Install cards share one structure (chip row, title, body that grows, bottom element). The bottom element is 60 px high in all three cards (the Rerun button and both code blocks), so they stay aligned in height whatever the body length.

## Links

| Target | URL |
|---|---|
| Rerun template, with the maintainer's affiliate code | `https://rerun.build/templates/recreate-competitor-ads-meta?via=aRLmG4` |

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

- `[REPO URL]`: fill when the repository goes public.
- `[PLUGIN INSTALL COMMAND]`: fill when the Claude Code plugin ships.
- Copy mismatch: the Rerun template page says it recreates ads "one to one". This page and `SOUL.md` say the agent never copies an ad exactly. Align one of the two before launch.
- The accent blue follows open decision 1 of the logo brief. Keep it in a single variable.
- A motion design video based on the card stack is planned. Its brief will live in this folder.
