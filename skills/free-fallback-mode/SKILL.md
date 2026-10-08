---
name: free-fallback-mode
description: Use when no ad-intelligence, media-generation, or Meta Ads provider tool is available and authenticated, or the user has no paid account, to go from a competitor ad search to a complete remake pack with free public ad libraries and local tools only, while stating plainly what cannot be done without a provider.
---

# Free fallback mode

## Required rule loading

Before handling the task, read [the agent rules](references/agent-rules.md), generated from the canonical `SOUL.md`. Read the sibling `winning-ad-remake-workflow` and `provider-policy` Skills before applying this fallback. Read `meta-ads-usage` before preparing any Meta instructions. Resolve sibling Skills relative to this installed Skill directory, not the working project. If a required file is missing or unreadable, report it and stop the affected operation. Do not infer rule loading from installation or from this summary.

In Codex, explicit Skill invocation applies these operating instructions to the task; it does not create an isolated profile or globally inject a persona. The Codex package bundles no MCP servers. Hermes `config.yaml` flags apply only in Hermes; check the actual session tools in every runtime.


This Skill is the no-connection path of `winning-ad-remake-workflow`. It replaces each provider stage that has no available, authenticated tool. Every rule of the workflow, of `provider-policy`, and of `SOUL.md` still applies: evidence labels, no exact copy, supported claims only, zero competitor traces, and human approval before any cost or external action.

The result is a complete remake pack ready for a human or a tool chosen by the user. It is not a rendered ad.

## 1. Check capabilities before each stage

Run this check before research, analysis, generation, and campaign preparation, not only once per assignment.

1. List the tools actually present in this session. An installed Skill, a declared MCP server, a past session, or the historical report does not prove that a tool is available. A provider counts as available only as `provider-policy` section 1 defines it, and only if a read-only call (for example an account, status, or listing call) succeeds without spending anything. An MCP server declared in the profile `config.yaml` with `enabled: false` is not available: this distribution declares every vendor server that way, and enabling and authenticating one is the user's decision, never the agent's.
2. Check the local tools:

   ```bash
   for tool in ffmpeg ffprobe scenedetect yt-dlp whisper whisper-cli; do
     printf '%s: ' "$tool"; command -v "$tool" || echo missing
   done
   python3 -c "import faster_whisper" 2>/dev/null && echo "faster-whisper: present" || echo "faster-whisper: missing"
   ```

   Check the native web search and browser tools the same way, with one harmless query or page load. A fresh profile may have no web search backend (it needs the user's own search API key) or may miss browser dependencies. If neither works, say so and ask the user for library URLs, files, or screenshots; never report research that could not be run.
3. Tell the user which stages run on a provider, which run on this free path, and which local tools are missing, for example:

   | Stage | Route | Note |
   |---|---|---|
   | Research | free path | No ad-intelligence tool available |
   | Analysis | free path | `scenedetect` missing: cut list and shot clips are **unknown** |
   | Generation | free path | No engine available: prompts only, no rendering |
   | Campaign | free path | No Meta tool available: manual launch pack |

4. When a local tool is missing, name it, give its install hint, mark the artifacts that depend on it **unknown**, and continue with the rest. Do not install software, download models, or create accounts without the user's explicit approval; for vendor tools, `provider-policy` section 1 applies.

Stages can mix. If a generation engine is available but no research tool is, run research here and generation under `provider-policy`, using that vendor's entry in `providers` and the workflow's cost approval step.

## 2. Research with free public ad libraries

Search the libraries that match the user's market and channels. Entry points as of 2026-10-07; confirm each one in the browser before relying on it:

| Library | Entry point |
|---|---|
| Meta Ad Library | `https://www.facebook.com/ads/library/` |
| TikTok Creative Center | `https://ads.tiktok.com/business/creativecenter/` |
| TikTok Commercial Content Library | `https://library.tiktok.com/` |
| Google Ads Transparency Center | `https://adstransparency.google.com/` |
| LinkedIn Ad Library | `https://www.linkedin.com/ad-library/` |
| Microsoft Ads Ad Library | `https://adlibrary.ads.microsoft.com/` |

Use the library websites through whichever browser or web search tool passed the check in section 1. The Meta Ad Library API is gated and, as observed on 2026-10-07, limited to ads delivered in the EU or UK and to political or social-issue ads, so it does not replace the website for other commercial research.

For each candidate, record the URL, advertiser, capture date, first-seen or start date, active status, platforms and placements, number of visible variants, format, and any engagement shown publicly. Apply the label rules of the workflow: **fact** for what the page shows, **estimate** for inferences such as run length from a start date, **opinion** for creative judgment, **unknown** for the rest. Any figure a library displays is a public signal: quote it with its source and capture date, never as spend, conversion, or profitability.

Spend, revenue, conversion rate, and ROAS are always **unknown** on this path. A long run is a signal worth studying, not proof of profitability. Then score and reject candidates exactly as in step 1 of the workflow, and present a short reasoned shortlist before going further.

## 3. Retrieve the creative

Use the first option that works:

1. a file the user supplies;
2. a public video URL downloaded with `yt-dlp`, only when the platform's terms allow it and the user agrees:

   ```bash
   yt-dlp --no-playlist -o "<work-dir>/reference.%(ext)s" "<public-url>"
   ```

3. screenshots and notes taken from the library preview.

Never bypass a login, paywall, or protection. `yt-dlp` may not support a given library page; if it fails, report the error and fall back to the next option. Keep the reference in a working directory of the installation, never inside the distribution repository, and record its URL and capture date. Library media can be temporary, so retrieve it once and keep the local copy until the workflow's clean-up step.

## 4. Analyze locally

### Optional Claude Code route: ffmpeg-skill

Use this route only in Claude Code when the community ffmpeg-skill is already installed at the `providers` pin. Hermes always uses our scripts below (ADR-004). Resolve the actual installed `<ffmpeg-skill-dir>` from the session's Skill location; a repository link, pin-table row, or historical test is not an installation. For a project install, check that `skills-lock.json` records the full pinned `ref` for `ffmpeg-skill`; a copied directory alone does not establish its revision. Read its `SKILL.md`, confirm the script exists, and run that script's `--help` before forming a command. Do not install it automatically: the documented pinned project install is in the root `README.md`.

Check Python 3.9 or later, `ffmpeg`, and `ffprobe`, then the filters and encoders required by the requested operation. Probe inputs with the installed `probe.py`; use `--dry-run --json` before an encode. If a dependency is missing or a script fails, report the actual error and use the fallback below for the affected analysis artifact. Run `python3 <ffmpeg-skill-dir>/scripts/_contract.py doctor --json` after a capability failure or when checking the machine on request. Read per-tool `usable` and `missing`: global `ok: false` can still permit scenes or contact sheets. Never treat an installed Skill as proof of working filters or transcription.

Keep every input, output, sidecar, and intermediate in `<work-dir>` outside the distribution. Use new output paths and preserve originals. These analysis commands use flags checked at the pin; replace the example segment range with measured timestamps:

```bash
FFMPEG_SCRIPTS="<ffmpeg-skill-dir>/scripts"
python3 "$FFMPEG_SCRIPTS/probe.py" "<work-dir>/reference.mp4" --json
python3 "$FFMPEG_SCRIPTS/scenes.py" "<work-dir>/reference.mp4" --json > "<work-dir>/analysis/scenes.json"
python3 "$FFMPEG_SCRIPTS/look.py" "<work-dir>/reference.mp4" --tiles 4x3 -o "<work-dir>/analysis/overview.png" --json
python3 "$FFMPEG_SCRIPTS/cut.py" "<work-dir>/reference.mp4" --segments 0-2 --accurate -o "<work-dir>/analysis/segment.mp4" --json
```

Create the analysis directory first. `scenes.json` is a measured scene report, not our `cut-list.csv` schema. A 4x3 contact sheet is an overview, not a substitute for the full per-second or first-three-second sheets. Use our scripts below for those required artifacts, the standard cut-list CSV, and silent per-shot clips. Read and visually inspect the generated PNG; link it with the timestamps. If `drawtext` is absent, `look.py --no-timecode` and `scenes.py --sheet <path> --no-timecode` can still work, but they have no burnt-in timestamps: record the actual sample times, or use our CSV-backed sheets. Never invent timestamp labels.

For `caption.py --transcribe`, first verify a local supported engine (whisper.cpp, faster-whisper, or openai-whisper) and its model are already installed and cached. Read the pinned engine-selection code before use: `--model` accepts the engine's model name or path, and a name can trigger a download. Check every engine it can fall back to, not just the first installed one; if you cannot establish that the entire attempted route uses only existing models, skip automatic transcription. Do not download a model without approval. For example, only with a verified local engine/model:

```bash
python3 "$FFMPEG_SCRIPTS/caption.py" "<work-dir>/reference.mp4" --transcribe --model "<installed-model-name-or-path>" --language "<language>" --mode mux --write-srt "<work-dir>/analysis/transcript.srt" -o "<work-dir>/analysis/transcribed.mp4" --json
```

`--mode mux` writes a separate video with a toggleable subtitle stream, not burnt-in pixels. Confirm the required mux encoder and read the SRT; label transcription **estimate** until checked. Without the engine, model, or required capability, use the existing transcription path below or mark spoken words **unknown**. No paid transcription is started as a fallback.

### Distributed analysis path

The scripts in this Skill's `scripts/` directory are deterministic. Each takes a local video and an output directory, writes files only, never accesses the network, and exits non-zero with a readable message when a dependency is missing.

| Script | Needs | Writes |
|---|---|---|
| `cut_list.py` | ffprobe, PySceneDetect | `cut-list.csv`: shot, start, end, duration in seconds and timecodes |
| `frame_sheet.py` | ffmpeg, ffprobe | `frame-sheet.jpg` (one frame per second, capped at 120, six per row) and `frame-sheet.csv` (tile to timestamp) |
| `first_three_seconds_sheet.py` | ffmpeg, ffprobe | `first-3s-sheet.jpg` (four frames per second, one row per second) and `first-3s-sheet.csv` |
| `shot_clips.py` | ffmpeg, ffprobe, PySceneDetect | `shots/shot-NNN.mp4` (silent, metadata stripped, one per shot) and `cut-list.csv` |

```bash
SCRIPTS="<this-skill-dir>/scripts"
python3 "$SCRIPTS/cut_list.py" "<work-dir>/reference.mp4" "<work-dir>/analysis"
python3 "$SCRIPTS/frame_sheet.py" "<work-dir>/reference.mp4" "<work-dir>/analysis"
python3 "$SCRIPTS/first_three_seconds_sheet.py" "<work-dir>/reference.mp4" "<work-dir>/analysis"
python3 "$SCRIPTS/shot_clips.py" "<work-dir>/reference.mp4" "<work-dir>/analysis"
```

The sheets carry no burned-in labels; read each tile's timestamp from the matching CSV. Re-running a script into the same directory replaces its own outputs: `shot_clips.py` first deletes earlier `shot-NNN.mp4` files in `shots/` and leaves any other file there untouched. Clips of odd-sized videos are cropped by at most one pixel to an even size. Exit code 3 means a dependency is missing, 2 means bad input, 1 means processing failed.

Transcribe with whichever Whisper-family tool is already installed:

```bash
# openai-whisper (downloads model weights on first use: ask first)
whisper "<work-dir>/reference.mp4" --model small --output_format srt --output_dir "<work-dir>/analysis"

# whisper.cpp (needs a model file the user already has, and 16 kHz mono audio)
ffmpeg -i "<work-dir>/reference.mp4" -ar 16000 -ac 1 -c:a pcm_s16le "<work-dir>/analysis/audio.wav"
whisper-cli -m "<model.bin>" -l <language> -f "<work-dir>/analysis/audio.wav" -osrt -of "<work-dir>/analysis/transcript"
```

Set `<language>` to the ad's spoken language code (for example `en`); use `auto` only when it is unknown, since detection can fail on short clips. Label the transcript an **estimate** of the spoken words until checked against the audio or the captions. `faster-whisper` is a Python library without its own command; use it only if it is already installed. If no transcriber is available, read on-screen text from the frame sheets, ask the user for captions, and mark the spoken transcript **unknown**.

Then write, linked to the artifacts above: literal notes for every shot in the cut list, the hook in the first three seconds, pacing (shot count, average and shortest shot length from the cut list), text timing, voice notes, and music notes. Voice character, music genre, and tempo are **unknown** unless the transcript, the user, or an available tool establishes them. For a still image, map the composition with percentage-based x/y zones instead.

### Finishing an existing remake in Claude Code

The same installed-script and per-operation gates apply when the user supplies an existing remake or an approved generation batch returns one. This edits existing media; it does not generate a new ad from prompts or turn the free pack into a claimed render. Paid generation and all external actions still follow `provider-policy` and the workflow's approvals.

Use `fit.py` for 9:16, `caption.py` for supplied/verified text, `redact.py` to blur an explicitly identified region, and `render.py` for a destination export. Check the real frame before choosing a region or crop. For example, choose one destination, an actual existing SRT, and measured pixel coordinates rather than running these as an unplanned batch:

```bash
python3 "$FFMPEG_SCRIPTS/fit.py" "<work-dir>/remake.mp4" --aspect 9:16 --fit pad -o "<work-dir>/vertical.mp4" --json
python3 "$FFMPEG_SCRIPTS/caption.py" "<work-dir>/vertical.mp4" --srt "<work-dir>/approved.srt" -o "<work-dir>/captioned.mp4" --json
python3 "$FFMPEG_SCRIPTS/redact.py" "<work-dir>/remake.mp4" --x <x> --y <y> --width <width> --height <height> --mode blur -o "<work-dir>/redacted.mp4" --json
python3 "$FFMPEG_SCRIPTS/render.py" --template reels "<work-dir>/clean-remake.mp4" -o "<work-dir>/final-reels.mp4" --json
python3 "$FFMPEG_SCRIPTS/check.py" "<work-dir>/final-reels.mp4" --platform reels --json
```

For TikTok use `--template tiktok` and `--platform tiktok`. Fit before captions; if the edit needs three or more steps, use the installed `render.py` project format after reading its help/reference. A delivery-only request needs a single template, not every recipe above. The render template encodes local files and performs technical checks; it never uploads or publishes. Caption burning needs a working `subtitles` filter and fonts, while template stages depend on the actual requested inputs. If a finishing tool is unavailable, report the missing output and deliver the pack or existing intermediate with that limitation; our local analysis scripts remain available and are not a promise of equivalent finishing.

Require exit 0, an existing nonempty output, and a probe matching the requested duration, dimensions, frame rate, and audio. Review `check.py` warnings and failures, then run `look.py` and inspect pixels after every picture change. A technical pass does not approve the ad. Blurring a known leftover competitor mark is allowed only if the final no longer contains any identifiable trace; if the region, packaging, person, voice, music, caption, watermark, or metadata still identifies the competitor, the workflow's QC fails and the material must be replaced or removed. Keep both score thresholds and final human approval.

## 5. Design the remake pack

Apply step 3 of the workflow: keep the hook type, sequence, framing, pacing, transitions, text timing, and format; replace every competitor product, brand element, person, voice, music track, caption, watermark, and metadata trace; use only claims supported by the user's brand files or sources; select two to four real product photos. Write each deliverable as a separate file in `<work-dir>/pack/` and link every file.

1. **Storyboard** (`storyboard.md`): one row per source shot with source time, duration, framing and camera, action, on-screen text and its timing, transition, and the remake content for that shot, including which product photo it uses.
2. **Script** (`script.md`): timed voice-over lines, on-screen text, and subtitles. Each claim cites its supporting source; anything unsupported is removed, not softened.
3. **Paste-ready prompts** (`prompts.md`): per shot, one image prompt and one video prompt (subject, action, camera, lighting, duration, aspect ratio) plus constraints (no logos, no text unless specified, the product as in the referenced photo). Write them tool-agnostic and state that they have not been run.
4. **Two casting options** (`casting.md`): option A and option B, clearly different people (age range, appearance, setting, wardrobe, delivery). Neither may resemble the competitor's talent or any real person without consent.
5. **Editing, music, and voice brief** (`brief.md`): edit rhythm from the cut list, transitions, text and subtitle style, format and length; music mood, structure, and a target tempo labelled **estimate**, licensed or royalty-free only, never the source track; voice tone, pace, and direction; sound effects list.
6. **QC checklist** (`qc-checklist.md`): the workflow's step 5 checks to apply once a render exists: shot-by-shot comparison, structural faithfulness at least 8/10, production quality at least 7/10, product appearance, claim check, and a competitor-trace list (name, logo, packaging, product, person, voice, music, watermark, caption, metadata). Leave the scores empty: no render exists yet.
7. **Manual Meta launch pack** (`meta-launch-pack.md`): campaign name `competitor · angle · format · date`, objective (**opinion**), default budget `20/day` in local currency unless the user sets one, audience and placements, primary text, headline, description, call to action, destination URL, creative specs, ad names, and a checklist the user follows in Meta Ads Manager: create every object paused, review it, and activate it only by their own decision.

Close by offering explicit decisions such as **Choose person A**, **Choose person B**, **Request changes**, and **Stop**.

## 6. What this mode does not do

- It does not access private data, spend, revenue, conversion, or ROAS for any ad.
- It does not render images, video, voice, music, or sound effects. Prompts and briefs are not outputs.
- It does not consume any service's credits.
- It does not create, edit, or activate any Meta object; the user launches the campaign manually.
- It does not score a render that does not exist, and does not sync with external accounts.

Say this plainly in the final message, next to the list of delivered files.

## 7. Rendering outside this mode

- **Local generation.** ComfyUI, Wan, and LTX-Video can run on the user's own machine, depending on GPU and memory. This Skill does not install, configure, or run them; the user may paste the prompts there.
- **Pika free credits.** On 2026-10-07, Pika's free account credits were the only free hosted tier found. This is a dated observation, not verified for the current session. Using it requires a Pika account and the `pika` MCP server enabled and authenticated by the user, which takes the generation stage out of this mode: follow `provider-policy` and the Pika entry in `providers`, since the batch still consumes the account's credits.
- **A native image or video tool** offered by the session is an engine too: confirm it is present, state its cost or mark it **unknown**, and get approval before a batch.

## 8. Completion

This mode is complete when the shortlist is labelled, every analysis artifact is linked or marked **unknown** with the reason, all seven pack files are linked, the limits in section 6 are stated, and no external object has been created.

Source: locally authored from section 7.2 of `docs/ad-remaker-complete-operating-report.md` in the distribution repository, a dated historical report. There is no upstream Skill text.
