---
name: winning-ad-remake-workflow
description: Use when researching a winning ad and producing a brand-safe remake with cost approval, evidence labeling, strict QC, and paused Meta safeguards.
---

# Winning-ad remake workflow

## 1. Select and classify the reference

1. Find the reference through an available authenticated ad-intelligence tool or a relevant public ad library. Never publish or promote the competitor ad.
2. Score run length, active status, variants, placements, engagement, repeated creative patterns, and product-audience fit.
3. Label every material statement as **fact**, **estimate**, **opinion**, or **unknown**:
   - **fact**: directly supported by linked evidence;
   - **estimate**: inferred numeric value or range;
   - **opinion**: subjective creative judgment;
   - **unknown**: not established by available evidence.
4. Reject prior copies, weak fits, insufficient evidence, and concepts likely to look unconvincingly AI-generated.

## 2. Analyze the source

When the required inspection or transcription tools are available, produce and link an exact timestamped cut list, full frame sheet, first-three-second frame sheet, per-shot silent clips, literal shot notes, transcript, pacing notes, voice notes, and music notes. For stills, map composition with percentage-based x/y zones. Mark unavailable evidence as **unknown** rather than inventing it.

## 3. Design a clean remake

Preserve the hook, sequence, framing, pacing, transitions, text timing, and format, while replacing every competitor product, brand element, person, voice, music track, caption, watermark, and metadata trace. Use only supported claims, two to four real product photos, and two clearly different casting options. Never fabricate reviews, testimonials, scarcity, endorsements, results, or capabilities.

Choose models only from the currently available authenticated generation tools and current schemas. Treat model recommendations in the upstream document as historical preferences, not guaranteed current availability.

## 4. Obtain approval before cost

Before every paid generation batch, show:
- exact units;
- per-unit price;
- subtotal;
- 20% retry margin;
- estimated total cost and currency;
- available balance when the service exposes it.

Label uncertain pricing as **estimate** and unavailable pricing or balance as **unknown**. Wait for explicit approval before calling any paid generation tool. Generate only the approved batch. Never spend retries silently; provide a new estimate and obtain new approval.

## 5. Generate and inspect

Preserve the real product’s appearance from supplied photos. Reject distorted packaging, unreadable labels, implausible anatomy or motion, identity leakage, or generally unconvincing output.

Compare source and remake shot by shot. Record brief reasons for both scores and require:
- structural faithfulness of at least 8/10;
- production quality of at least 7/10;
- zero competitor traces.

Fail immediately if any competitor name, logo, packaging, product, person, voice, music, watermark, caption, metadata, or other trace remains. Any paid revision requires another approved batch.

## 6. Deliver and gate campaign creation

Link every created file, including analysis artifacts, prompts, selected source photos, intermediate renders, finals, and comparison sheets. Offer explicit decisions such as **Approve batch**, **Choose person A**, **Choose person B**, **Request changes**, **Approve final**, and **Stop**.

After final approval, prepare a Meta campaign only if authenticated Meta tools are available. Use a default budget of `20/day` in local currency and name it `competitor · angle · format · date`, unless the user specifies otherwise. Explicitly set every campaign, ad set, and ad to paused. Read back each object with an available Meta status tool and verify it remains paused after creation or edits. Never publish, activate, schedule spend, or spend money without separate explicit approval. If paused status cannot be verified, stop and report it as **unknown**.

Delete locally stored competitor creative files only after the user approves the final remake and confirms the reference is no longer needed. Keep analysis artifacts and user/product assets unless separately requested.

Work is complete only when all requested files are linked, the final passes both score thresholds with zero competitor traces, paid actions have matching approvals, every created Meta object has been re-checked as paused, and confirmed competitor source files have been deleted.

See the verbatim [upstream source](references/upstream.md) for provenance and the original workflow.
