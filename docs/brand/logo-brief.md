# Logo brief: Ad Remaker

Status: concept selected, refinement pending (October 7, 2026).
Refinement tool: Claude Design.

## The product in one sentence

Ad Remaker is an agent that finds competitor ads with public performance signals, breaks down their creative mechanics, and rebuilds them for a brand's real product. It never copies an ad exactly.

The logo should read as advertising first, and as a remake of existing creative second.

## Selected direction: concept C, "tool stack"

![Concept C sketch](logo-concept-c-sketch.svg)

A stack of offset ad cards, each in a different color. The front card is the finished ad: solid, with a play symbol. The cards behind it are the inputs: the source ads and the tools that analyze and regenerate them.

What the mark should say:

- Layers: the agent deconstructs an ad into its parts.
- Many colors: several tools work together (research, generation, delivery).
- One front card: the output is a single, finished, new ad.

Other directions explored and set aside are in [logo-exploration-round-2.png](logo-exploration-round-2.png): A (Sponsored badge), B (9:16 story), D (promo sticker). Concept B's story cues (progress bars at the top, CTA pill at the bottom) can be reused on the front card if they improve the "ad" reading.

## Color direction

Each back card evokes one tool in the stack. The front card uses a blue close to Meta, because Meta is where the final campaign lands.

| Card | Sketch color | Intended reference | Status |
|---|---|---|---|
| Front | `#0866FF` | Meta (campaign destination) | To verify against the official brand guide |
| Back 1 | `#FF7A1A` | Generation tools (Higgsfield, Kie.ai, Pika, fal.ai) | Placeholder |
| Back 2 | `#FF4FA3` | Generation tools | Placeholder |
| Back 3 | `#8B5CF6` | Research tools (Brandsearch, TrendTrack) | Placeholder |
| Back 4 | `#C6F432` | Hermes (agent runtime) | Placeholder |

The sketch colors were chosen by eye. Check each tool's official brand colors before finalizing, and replace or drop a color if it does not match.

## Constraints

- Evoke the tools' colors only. Do not reuse any third-party logo shape, glyph, or wordmark. Ad Remaker has no rights to those marks, and the tool list will change over time.
- The mark must still work if one tool is removed from the stack. Do not tie a card to a specific vendor in any visible way.
- Must stay readable at 32 px and recognizable at 16 px. Reduce the number of back cards for small sizes if needed (for example, 2 back cards at 16 px).
- Must work on a light and a dark background.
- Wordmark is lowercase `ad remaker`, heavy geometric sans serif. Not final, open to change.

## Known issues with the sketch

1. Five cards look busy at small sizes.
2. The back cards are all the same size, so the depth reads as flat. Try perspective, scale, or decreasing opacity.
3. The play triangle is generic. Try something more specific to ads (CTA pill, story progress bars, a small "Ad" label).
4. The colors have no hierarchy. The front card should clearly dominate.

## Deliverables

- [ ] Icon (mark only), SVG, light and dark versions
- [ ] Small-size icon variant for 16 px and 32 px
- [ ] Horizontal lockup: icon + `ad remaker` wordmark
- [ ] Final palette with verified hex values
- [ ] PNG exports at 512 px and 1024 px for the profile and the README

Store final files in `docs/brand/` and update this brief's status line.
