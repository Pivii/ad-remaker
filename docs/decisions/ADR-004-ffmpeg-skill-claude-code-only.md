# ADR-004 - Keep ffmpeg-skill optional and Claude Code only

## Status

Accepted on October 8, 2026 (issue #13).

## Context

The community repository [`kajisho5/ffmpeg-skill`](https://github.com/kajisho5/ffmpeg-skill/tree/008333aaf6722083392eb6bd8bd67b59884a2a26) ships a root-level Skill, 42 Python scripts driving local FFmpeg, delivery templates, and a Claude Code plugin manifest. Version 2.5.1 at commit `008333aaf6722083392eb6bd8bd67b59884a2a26` declares MIT in `LICENSE`. These are dated observations checked on 2026-10-08, not evidence that it is installed on a user's machine.

The maintainer's scratch-profile triage in issue #13 found that Hermes v0.20.2 cannot install it:

- The pinned raw `SKILL.md` URL fails with "Could not fetch ... from any source". `UrlSource.fetch` tries every support path returned by `_referenced_support_paths`: `references/devices.md`, `references/gotchas.md`, `references/scripts.md`, and the literal `scripts/*.py`. The wildcard path returns 404 and aborts the bundle; even without that failure, it would not fetch all 42 scripts.
- The GitHub source requires an `owner/repo/path` sub-path. `kajisho5/ffmpeg-skill` has its Skill at the repository root and is not found.
- The skills guard never ran. Its verdict is unknown; this is a fetch limitation, not an observed safety verdict. The triage scratch profile was deleted afterwards.

Our local scripts from issue #1 already provide the guaranteed distributed analysis path. Issue #6 makes the same operating Skills available in Claude Code, where the pinned upstream Skill can be installed separately.

## Decision

Recommend ffmpeg-skill only as an optional free local tool in Claude Code. Keep its source, full commit, license, root path, Hermes `Install` value `no`, and check date in the existing pin table. No upstream Skill, scripts, templates, or MCP configuration are copied into this distribution, and neither runtime depends on it.

The root `README.md` documents the verified pinned project install. Route to its actual installed scripts only when their required dependencies are available: analysis (`scenes.py`, `look.py`, `cut.py --segments`, `caption.py --transcribe`) and finishing (`fit.py` 9:16, `caption.py`, `redact.py` for a known blur region, `render.py --template reels` or `tiktok`, `check.py`). Read the installed source and `--help`; do not invent flags or assume optional Whisper engines or cached models exist. Our local analysis scripts and existing transcription path remain the fallback. Missing finishing capability is reported; a remake pack without a render stays a pack.

Local processing uses no paid provider credits. All approval rules for paid generation, publication, activation, scheduling, and ad spend stay unchanged. Dependency or model installation still needs the user's approval under the operating Skills. Blurring a region does not establish zero competitor traces; the workflow still inspects the result and fails on any identifiable trace.

Never copy ffmpeg-skill into Hermes or run its `npx ffmpeg-skill` installer on a Hermes profile: that would bypass the guard rather than solve the source limitation.

## Consequences

- Provenance remains distinct: ffmpeg-skill is a community tool referenced at a pin; our Skills and scripts are locally authored adaptations. It is not an official FFmpeg integration.
- FFmpeg builds differ. A successful install does not establish filter, font, encoder, or transcription availability. Follow per-tool errors and `doctor` capability results; a global `ok: false` does not imply every script is unusable.
- Scratch verification on 2026-10-08 installed the pin in Claude Code and exercised scenes and contact sheets on synthetic media. The host FFmpeg 8.1 lacked `drawtext` and `subtitles`; `doctor` exited 1 and caption burning was not validated. See `tests/README.md` for the exact evidence and limits.
- Re-check support after every Hermes upgrade, and before proposing any Hermes install: inspect the new URL installer's glob/bundle handling and GitHub root-source support, then install the same pinned source in a scratch profile. Confirm that every required support file arrives and that the skills guard actually runs, record its verdict, run `hermes skills audit`, and smoke-test the installed scripts. Keep `Install: no` until those checks pass and a new decision explicitly enables Hermes. Never bypass an adverse guard verdict.
