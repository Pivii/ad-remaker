#!/usr/bin/env python3
"""Write a timestamped cut list (cut-list.csv) for a local video with PySceneDetect."""

from __future__ import annotations

import sys

from _media import detect_shots, parse_args, report, require, write_cut_list


def main() -> int:
    source, output_dir = parse_args(sys.argv, __doc__)
    tools = require("ffprobe", "scenedetect")
    shots = detect_shots(tools, source)
    output_dir.mkdir(parents=True, exist_ok=True)
    report([write_cut_list(shots, output_dir)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
