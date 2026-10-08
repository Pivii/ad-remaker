---
name: free-fallback-mode
description: Use when no ad-intelligence, media-generation, or Meta Ads provider tool is available and authenticated, or the user has no paid account, to go from a competitor ad search to a complete remake pack with free public ad libraries and local tools only, while stating plainly what cannot be done without a provider.
---

# Free fallback mode

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
