#!/usr/bin/env python3
"""Write a first-three-second frame sheet (first-3s-sheet.jpg) and its index (first-3s-sheet.csv).

Samples four frames per second over the first three seconds: one row per second, four tiles per row.
"""

from __future__ import annotations

import sys

from _media import build_sheet, parse_args, probe_duration, report, require

FRAMES_PER_SECOND = 4
SECONDS = 3
TILE_WIDTH = 320


def main() -> int:
    source, output_dir = parse_args(sys.argv, __doc__)
    tools = require("ffmpeg", "ffprobe")
    duration = probe_duration(tools["ffprobe"], source)
    step = 1 / FRAMES_PER_SECOND
    times = [round(i * step, 3) for i in range(FRAMES_PER_SECOND * SECONDS) if i * step < duration]
    output_dir.mkdir(parents=True, exist_ok=True)
    report(build_sheet(tools, source, output_dir, "first-3s-sheet", times, FRAMES_PER_SECOND, TILE_WIDTH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
