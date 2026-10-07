#!/usr/bin/env python3
"""Write one silent clip per detected shot (shots/shot-NNN.mp4) plus the cut list they follow (cut-list.csv).

Shots are detected with PySceneDetect, then cut and re-encoded with ffmpeg without audio
or source metadata so that every clip starts exactly on its cut.
"""

from __future__ import annotations

import sys

from _media import detect_shots, parse_args, report, require, run, write_cut_list


def video_encoder(ffmpeg: str) -> list[str]:
    encoders = run([ffmpeg, "-hide_banner", "-encoders"]).stdout
    if " libx264 " in encoders:
        return ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"]
    return ["-c:v", "mpeg4", "-q:v", "3"]


def main() -> int:
    source, output_dir = parse_args(sys.argv, __doc__)
    tools = require("ffmpeg", "ffprobe", "scenedetect")
    shots = detect_shots(tools, source)
    clips_dir = output_dir / "shots"
    clips_dir.mkdir(parents=True, exist_ok=True)
    encoder = video_encoder(tools["ffmpeg"])
    written = [write_cut_list(shots, output_dir)]
    for index, (start, end) in enumerate(shots, start=1):
        clip = clips_dir / f"shot-{index:03d}.mp4"
        run([
            tools["ffmpeg"], "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
            "-ss", f"{start:.3f}", "-i", str(source), "-t", f"{end - start:.3f}",
            "-an", "-sn", "-dn", "-map_metadata", "-1", *encoder, str(clip),
        ])
        written.append(clip)
    report(written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
