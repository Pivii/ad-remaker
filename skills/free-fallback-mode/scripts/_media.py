"""Shared helpers for the free-fallback-mode analysis scripts.

Every script takes a local input video and an output directory, writes files
only, and never accesses the network or downloads anything.
"""

from __future__ import annotations

import csv
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXIT_PROCESSING = 1
EXIT_USAGE = 2
EXIT_MISSING_DEPENDENCY = 3

INSTALL_HINTS = {
    "ffmpeg": "Install ffmpeg (https://ffmpeg.org/download.html), for example `brew install ffmpeg` or `apt install ffmpeg`.",
    "ffprobe": "ffprobe ships with ffmpeg. Install ffmpeg (https://ffmpeg.org/download.html).",
    "scenedetect": "Install PySceneDetect (https://www.scenedetect.com), for example `pipx install 'scenedetect[opencv-headless]'`.",
}

CUT_LIST_FIELDS = (
    "shot",
    "start_seconds",
    "end_seconds",
    "duration_seconds",
    "start_timecode",
    "end_timecode",
)


def die(message: str, code: int) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_args(argv: list[str], description: str) -> tuple[Path, Path]:
    script = Path(argv[0]).name
    if len(argv) != 3 or argv[1] in {"-h", "--help"}:
        print(f"usage: {script} <input-video> <output-dir>\n\n{description}", file=sys.stderr)
        raise SystemExit(0 if len(argv) == 2 and argv[1] in {"-h", "--help"} else EXIT_USAGE)
    source = Path(argv[1])
    if "://" in argv[1]:
        die(f"input must be a local file, not a URL: {argv[1]}. This script never downloads anything.", EXIT_USAGE)
    if not source.is_file():
        die(f"input video not found: {source}", EXIT_USAGE)
    output_dir = Path(argv[2])
    if output_dir.exists() and not output_dir.is_dir():
        die(f"output path exists and is not a directory: {output_dir}", EXIT_USAGE)
    return source.resolve(), output_dir


def require(*tools: str) -> dict[str, str]:
    """Return resolved paths for the tools, or exit with a readable message."""
    found: dict[str, str] = {}
    missing: list[str] = []
    for tool in tools:
        path = shutil.which(tool)
        if path is None:
            missing.append(tool)
        else:
            found[tool] = path
    if missing:
        lines = [f"required tool not found on PATH: {', '.join(missing)}."]
        lines.extend(f"  {tool}: {INSTALL_HINTS[tool]}" for tool in missing)
        lines.append("Nothing was written. This script never installs or downloads dependencies.")
        die("\n".join(lines), EXIT_MISSING_DEPENDENCY)
    return found


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        tail = "\n".join(detail[-10:]) if detail else "no output"
        die(f"{Path(command[0]).name} failed (exit {result.returncode}):\n{tail}", EXIT_PROCESSING)
    return result


def probe_duration(ffprobe: str, source: Path) -> float:
    result = run([
        ffprobe, "-v", "error", "-select_streams", "v:0",
        "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(source),
    ])
    try:
        duration = float(result.stdout.strip().splitlines()[0])
    except (IndexError, ValueError):
        die(f"cannot read the duration of {source}; is it a video file?", EXIT_PROCESSING)
    if not math.isfinite(duration) or duration <= 0:
        die(f"input has no usable duration: {source}", EXIT_PROCESSING)
    return duration


def timecode(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def detect_shots(tools: dict[str, str], source: Path) -> list[tuple[float, float]]:
    """Detect shots with PySceneDetect's content detector at its default threshold."""
    duration = probe_duration(tools["ffprobe"], source)
    with tempfile.TemporaryDirectory(prefix="ad-remaker-cuts-") as scratch:
        run([
            tools["scenedetect"], "--quiet", "-i", str(source), "-o", scratch,
            "detect-content", "list-scenes", "--quiet", "--skip-cuts", "--filename", "scenes.csv",
        ])
        scenes_csv = Path(scratch) / "scenes.csv"
        if not scenes_csv.is_file():
            die("PySceneDetect produced no scene list", EXIT_PROCESSING)
        with scenes_csv.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    shots: list[tuple[float, float]] = []
    for row in rows:
        try:
            shots.append((float(row["Start Time (seconds)"]), float(row["End Time (seconds)"])))
        except (KeyError, ValueError):
            die("unexpected PySceneDetect CSV format; expected 'Start Time (seconds)' and 'End Time (seconds)' columns", EXIT_PROCESSING)
    if not shots:
        shots = [(0.0, duration)]
    return shots


def write_cut_list(shots: list[tuple[float, float]], output_dir: Path) -> Path:
    path = output_dir / "cut-list.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(CUT_LIST_FIELDS)
        for index, (start, end) in enumerate(shots, start=1):
            writer.writerow([
                index, f"{start:.3f}", f"{end:.3f}", f"{end - start:.3f}", timecode(start), timecode(end),
            ])
    return path


def build_sheet(
    tools: dict[str, str],
    source: Path,
    output_dir: Path,
    name: str,
    times: list[float],
    columns: int,
    tile_width: int,
) -> list[Path]:
    """Extract one frame per timestamp and tile them row by row into <name>.jpg plus <name>.csv."""
    with tempfile.TemporaryDirectory(prefix="ad-remaker-frames-") as scratch:
        frames: list[Path] = []
        for index, moment in enumerate(times, start=1):
            frame = Path(scratch) / f"frame_{index:04d}.png"
            run([
                tools["ffmpeg"], "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                "-ss", f"{moment:.3f}", "-i", str(source), "-frames:v", "1",
                "-vf", f"scale={tile_width}:-2", str(frame),
            ])
            if not frame.is_file():
                break
            frames.append(frame)
        if not frames:
            die(f"no frame could be extracted from {source}", EXIT_PROCESSING)
        columns = min(columns, len(frames))
        rows = math.ceil(len(frames) / columns)
        sheet = output_dir / f"{name}.jpg"
        run([
            tools["ffmpeg"], "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
            "-framerate", "1", "-start_number", "1", "-i", str(Path(scratch) / "frame_%04d.png"),
            "-vf", f"tile={columns}x{rows}:padding=4:margin=4", "-frames:v", "1", "-q:v", "3", str(sheet),
        ])
    index_path = output_dir / f"{name}.csv"
    with index_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("tile", "row", "column", "time_seconds", "timecode"))
        for position, moment in enumerate(times[: len(frames)]):
            writer.writerow([
                position + 1, position // columns + 1, position % columns + 1, f"{moment:.3f}", timecode(moment),
            ])
    return [sheet, index_path]


def report(paths: list[Path]) -> None:
    for path in paths:
        print(path)
