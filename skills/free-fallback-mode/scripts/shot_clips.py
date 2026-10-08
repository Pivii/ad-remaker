#!/usr/bin/env python3
"""Write one silent clip per detected shot (shots/shot-NNN.mp4) plus the cut list they follow (cut-list.csv).

Shots are detected with PySceneDetect, then cut and re-encoded with ffmpeg without audio
or source metadata so that every clip starts exactly on its cut. Odd frame sizes are cropped
by at most one pixel to the even size the encoders require.

On a re-run, clips left by an earlier run (shot-NNN.mp4 in shots/) are deleted first, so the
folder always matches the new cut list. Other files in shots/ are never touched.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from _media import detect_shots, parse_args, report, require, run, write_cut_list

OWN_CLIP = re.compile(r"^shot-\d{3,}\.mp4(\.part)?$")
EVEN_CROP = "crop=trunc(iw/2)*2:trunc(ih/2)*2:0:0"


def video_encoder(ffmpeg: str) -> list[str]:
    encoders = run([ffmpeg, "-hide_banner", "-encoders"]).stdout
    if " libx264 " in encoders:
        return ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"]
    return ["-c:v", "mpeg4", "-q:v", "3", "-pix_fmt", "yuv420p"]


def remove_own_clips(clips_dir: Path) -> None:
    for path in clips_dir.iterdir():
        if path.is_file() and OWN_CLIP.match(path.name):
            path.unlink()


def main() -> int:
    source, output_dir = parse_args(sys.argv, __doc__)
    tools = require("ffmpeg", "ffprobe", "scenedetect")
    shots = detect_shots(tools, source)
    clips_dir = output_dir / "shots"
    clips_dir.mkdir(parents=True, exist_ok=True)
    remove_own_clips(clips_dir)
    encoder = video_encoder(tools["ffmpeg"])
    written: list[Path] = []
    try:
        for index, (start, end) in enumerate(shots, start=1):
            clip = clips_dir / f"shot-{index:03d}.mp4"
            partial = clip.with_name(clip.name + ".part")
            run([
                tools["ffmpeg"], "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                "-ss", f"{start:.3f}", "-i", str(source), "-t", f"{end - start:.3f}",
                "-an", "-sn", "-dn", "-map_metadata", "-1", "-vf", EVEN_CROP, *encoder,
                "-f", "mp4", str(partial),
            ])
            partial.replace(clip)
            written.append(clip)
    except SystemExit:
        remove_own_clips(clips_dir)
        raise
    report([write_cut_list(shots, output_dir), *written])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
