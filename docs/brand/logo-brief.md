# Logo brief: Ad Remaker

Status: concept C refined and drawn, files delivered, three decisions open (October 7, 2026).
Refinement tool: Claude Design.

## The product in one sentence

Ad Remaker is an agent that finds competitor ads with public performance signals, breaks down their creative mechanics, and rebuilds them for a brand's real product. It never copies an ad exactly.

The logo should read as advertising first, and as a remake of existing creative second.

## Selected direction: concept C, "tool stack"

![Concept C sketch](logo-concept-c-sketch.svg)

A stack of offset ad cards, each in a different color. The front card is the finished ad: solid, with its own content. The cards behind it are the inputs: the source ads and the tools that analyze and regenerate them.

What the mark should say:

- Layers: the agent deconstructs an ad into its parts.
- Many colors: several tools work together (research, generation, delivery).
- One front card: the output is a single, finished, new ad.

Other directions explored and set aside are in [logo-exploration-round-2.png](logo-exploration-round-2.png): A (Sponsored badge), B (9:16 story), D (promo sticker). Concept B's story cues are now used on the front card.

## Refinement round 3

The four known issues of the sketch are addressed as follows.

| Sketch issue | Resolution |
|---|---|
| Five cards look busy at small sizes | Reduced to three cards behind one front card. The pink card was dropped because it carried the same meaning as the orange one. |
| Depth reads flat | Strict size ladder. Card heights 76, 66, 56, 46 and a 13 unit step to the left per card. No shadow, no perspective, no opacity change. |
| The play triangle is generic | Replaced by concept B's ad cues: three story progress bars with the first one active, and a CTA pill at the bottom of the front card. |
| No hierarchy | The front card is the widest (56 against 46), the only one with content, and the only saturated blue. |

The card order also changed. In the sketch the lime card is the farthest back, so its visible edge sits directly on the background and drops to about 1.4:1 contrast on a light surface. Lime is now the card immediately behind the front card, where its edge is framed by the orange card and the blue card. Order from back to front is purple, orange, lime, blue.

## Geometry

All files are drawn on a 120 by 120 grid. The mark occupies 95 by 76, optically centered.

| Card | x | y | width | height | radius | Fill |
|---|---|---|---|---|---|---|
| 4, research | 13 | 37 | 46 | 46 | 9 | `#8B5CF6` |
| 3, generation | 26 | 32 | 46 | 56 | 10 | `#FF7A1A` |
| 2, runtime | 39 | 27 | 46 | 66 | 11 | `#C6F432` |
| 1, the finished ad | 52 | 22 | 56 | 76 | 13 | `#0866FF` |

Front card content, white: three bars at y 30, each 12.5 by 3.5, radius 1.75, at x 58, 73.5 and 89, the second and third at 45 percent opacity; one CTA pill at x 58, y 80, 44 by 11, radius 5.5.

Clear space is 13 grid units on every side, the same value as the step between two cards.

## Size tiers

| Tier | Use | Content |
|---|---|---|
| Full | 48 px and up | Three cards behind, story bars and CTA pill |
| Compact | 24 to 32 px | Two cards behind, CTA pill only |
| Micro | 16 px | Two cards behind, 16 unit steps, no content on the front card |

Detail is dropped before cards are, because the card ladder is the recognizable part. The purple card is the first one removed.

## Color direction

Each back card evokes one tool family in the stack. The front card uses a blue close to Meta, because Meta is where the final campaign lands.

| Card | Hex | Intended reference | Status |
|---|---|---|---|
| Front | `#0866FF` | Meta (campaign destination) | Not verified against the official brand guide |
| Card 2 | `#C6F432` | Hermes (agent runtime) | Placeholder |
| Card 3 | `#FF7A1A` | Generation tools | Placeholder |
| Card 4 | `#8B5CF6` | Research tools | Placeholder |
| Ink | `#121212` | Wordmark and app tile | Local to this brief |

Parked: `#FF4FA3`, the second generation card of the sketch. It can come back if the stack ever needs a fifth card.

The sketch colors were chosen by eye. Check each tool's official brand colors before finalizing, and replace or drop a color if it does not match.

## Wordmark

Lowercase `ad remaker`, Poppins 700, letter spacing -3 percent. The glyphs are converted to outlines in the delivered SVG files, so the lockups carry no font dependency. Poppins is licensed under the SIL Open Font License.

## Constraints

- Evoke the tools' colors only. Do not reuse any third-party logo shape, glyph, or wordmark. Ad Remaker has no rights to those marks, and the tool list will change over time.
- The mark must still work if one tool is removed from the stack. Do not tie a card to a specific vendor in any visible way.
- Must stay readable at 32 px and recognizable at 16 px.
- Must work on a light and a dark background. The same mark is used on both, so there is no separate dark version of the icon.
- Never place the mark on a blue close to the front card's own blue.
- Depth comes from the size ladder alone. Removing a card is allowed, reordering the cards is not.

## Open decisions

1. The front card blue. Building the identity on a blue this close to Meta's couples the brand to one platform, while the constraint above says the tool list will change. A proprietary blue would keep the paid campaign reading without the dependency. Current files ship `#0866FF` as specified in this brief.
2. The card order. The reorder described in Refinement round 3 is a legibility fix. If the lime card must stay farthest back for meaning, it has to be darkened instead.
3. The typeface. This brief asks for a heavy geometric sans, which Poppins is. The round 2 exploration image shows a grotesque with a two storey `a`, which is a different family. Poppins is shipped.

## Deliverables

- [x] Icon (mark only), SVG, works on light and dark
- [x] Small-size icon variants for 16 px and 32 px
- [x] Horizontal lockup: icon + `ad remaker` wordmark, light and dark
- [x] PNG exports at 512 px and 1024 px for the profile and the README
- [ ] Final palette with verified hex values (blocked by open decision 1 and by the tool color checks)

## Files

| File | Use |
|---|---|
| `logo-mark.svg` | Full mark, 48 px and up |
| `logo-mark-compact.svg` | Compact mark, 24 to 32 px |
| `logo-mark-micro.svg` | Micro mark, 16 px |
| `logo-tile-dark.svg` | App tile, ink background, radius 28 of 120 |
| `logo-lockup-horizontal.svg` | Horizontal lockup, ink wordmark, for light backgrounds |
| `logo-lockup-horizontal-dark.svg` | Horizontal lockup, white wordmark, for dark backgrounds |
| `logo-mark-512.png`, `logo-mark-1024.png` | Raster exports, transparent background |
| `logo-tile-dark-512.png` | Raster export for profile pictures that need a filled square |

The front card color appears in every SVG file. To test another blue across the set, replace `#0866FF` in `docs/brand/*.svg` and re-export the PNG files.
