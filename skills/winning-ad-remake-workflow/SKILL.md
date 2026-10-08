---
name: winning-ad-remake-workflow
description: Use when researching a winning ad and producing a brand-safe remake with cost approval, evidence labeling, strict QC, and a gated Meta campaign step.
---

# Winning-ad remake workflow

## Required rule loading

Before handling the task, read [the agent rules](references/agent-rules.md), generated from the canonical `SOUL.md`. Read the sibling `provider-policy` and `providers` Skills now. Before any Meta stage, read `meta-ads-usage`; for an unavailable provider stage, read `free-fallback-mode`. Resolve sibling Skills relative to this installed Skill directory, not the working project. If a required file is missing or unreadable, report it and stop the affected operation. Do not infer rule loading from installation or from this summary.

In Codex, explicit Skill invocation applies these operating instructions to the task; it does not create an isolated profile or globally inject a persona. The Codex package bundles no MCP servers. Hermes `config.yaml` flags apply only in Hermes; check the actual session tools in every runtime.


Every call to an external provider follows `provider-policy`. Use `providers` to find a vendor's official source and route order. Before each stage below, check which providers are actually connected; a server declared in `config.yaml` with `enabled: false` is not connected. When a stage has none, run it with the `free-fallback-mode` Skill and tell the user which stages use that free path.

## 1. Select and classify the reference

1. Find the reference through a connected ad-intelligence provider or a relevant public ad library (listed in `free-fallback-mode`). Never publish or promote the competitor ad.
2. Score run length, active status, variants, placements, engagement, repeated creative patterns, and product-audience fit.
3. Label every material statement as **fact**, **estimate**, **opinion**, or **unknown**:
   - **fact**: directly supported by linked evidence;
   - **estimate**: inferred numeric value or range;
   - **opinion**: subjective creative judgment;
   - **unknown**: not established by available evidence.
4. Reject prior copies, weak fits, insufficient evidence, and concepts likely to look unconvincingly AI-generated.

## 2. Analyze the source

When the required inspection or transcription tools are available, produce and link an exact timestamped cut list, full frame sheet, first-three-second frame sheet, per-shot silent clips, literal shot notes, transcript, pacing notes, voice notes, and music notes. For stills, map composition with percentage-based x/y zones. Mark unavailable evidence as **unknown** rather than inventing it. The scripts of `free-fallback-mode` produce the cut list, both frame sheets, and the silent clips locally in any mode. In Claude Code only, when the pinned ffmpeg-skill is actually installed and the operation's dependencies are available, use its analysis route in `free-fallback-mode` section 4 (`scenes.py`, `look.py`, `cut.py --segments`, optional `caption.py --transcribe`). Otherwise use our distributed scripts and existing transcription path. Do not treat overview sheets or a different scene-report format as the required artifacts; link all evidence and mark gaps **unknown**.

## 3. Design a clean remake

Preserve the hook, sequence, framing, pacing, transitions, text timing, and format, while replacing every competitor product, brand element, person, voice, music track, caption, watermark, and metadata trace. Use only supported claims, two to four real product photos, and two clearly different casting options. Never fabricate reviews, testimonials, scarcity, endorsements, results, or capabilities.

Choose models only from a connected generation provider, as `provider-policy` requires. Treat model recommendations in the upstream document as historical preferences, not guaranteed current availability. When no generation provider is connected, stop at the remake pack described in `free-fallback-mode`; never claim or simulate a render.

## 4. Obtain approval before cost

Before every paid generation batch, show:
- exact units;
- per-unit price;
- subtotal;
- 20% retry margin;
- estimated total cost and currency;
- available balance when the service exposes it.

Label uncertain pricing as **estimate** and unavailable pricing or balance as **unknown**. Approval, batch limits, and retries follow `provider-policy`.

## 5. Generate and inspect

Preserve the real product’s appearance from supplied photos. Reject distorted packaging, unreadable labels, implausible anatomy or motion, identity leakage, or generally unconvincing output.

For an existing remake in Claude Code, the optional installed ffmpeg-skill may finish it locally with `fit.py` 9:16, `caption.py`, `redact.py` for a measured blur region, `render.py --template reels` or `tiktok`, and `check.py`, following the gates and checks in `free-fallback-mode` section 4. Never install it automatically or assume its filters, fonts, or transcription models exist. Our analysis scripts remain the fallback; if finishing is unavailable, report the gap and deliver the pack or existing intermediate. Local encoding does not authorize paid generation or publication.

Compare source and remake shot by shot. Record brief reasons for both scores and require:
- structural faithfulness of at least 8/10;
- production quality of at least 7/10;
- zero competitor traces.

Fail immediately if any competitor name, logo, packaging, product, person, voice, music, watermark, caption, metadata, or other trace remains. A paid revision is a new batch under `provider-policy`.

## 6. Deliver and gate campaign creation

Link every created file, including analysis artifacts, prompts, selected source photos, intermediate renders, finals, and comparison sheets. Offer explicit decisions such as **Approve batch**, **Choose person A**, **Choose person B**, **Request changes**, **Approve final**, and **Stop**.

After final approval, prepare a Meta campaign only if authenticated Meta tools are available, following `meta-ads-usage`; otherwise deliver the manual Meta launch pack described in `free-fallback-mode`. Use a default budget of `20/day` in local currency and name it `competitor · angle · format · date`, unless the user specifies otherwise.

Delete locally stored competitor creative files only after the user approves the final remake and confirms the reference is no longer needed. Keep analysis artifacts and user/product assets unless separately requested.

Work is complete only when all requested files are linked, the final passes both score thresholds with zero competitor traces, paid actions have matching approvals, every created Meta object has passed the read-back in `meta-ads-usage`, and confirmed competitor source files have been deleted. When generation ran on the free path, the pack is complete under section 8 of `free-fallback-mode`, and the score thresholds apply once a render exists.

See the verbatim [upstream source](references/upstream.md) for provenance and the original workflow.
