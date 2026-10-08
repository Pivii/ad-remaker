#!/usr/bin/env python3
"""Write a full frame sheet (frame-sheet.jpg) and its timestamp index (frame-sheet.csv) for a local video.

Samples one frame per second, or evenly spaced frames capped at 120 for longer videos,
tiled left to right and top to bottom in rows of six.
"""

from __future__ import annotations

import sys

from _media import build_sheet, parse_args, probe_duration, report, require

MAX_FRAMES = 120
COLUMNS = 6
TILE_WIDTH = 240


def main() -> int:
    source, output_dir = parse_args(sys.argv, __doc__)
    tools = require("ffmpeg", "ffprobe")
    duration = probe_duration(tools["ffprobe"], source)
    interval = max(1.0, duration / MAX_FRAMES)
    times: list[float] = []
    moment = 0.0
    while moment < duration and len(times) < MAX_FRAMES:
        times.append(round(moment, 3))
        moment += interval
    output_dir.mkdir(parents=True, exist_ok=True)
    report(build_sheet(tools, source, output_dir, "frame-sheet", times, COLUMNS, TILE_WIDTH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
