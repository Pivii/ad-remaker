#!/usr/bin/env python3
"""Export a clean skills-only Codex marketplace from tracked working-tree files."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def export(destination: Path) -> None:
    destination = destination.resolve()
    if destination.exists() or destination == ROOT or ROOT in destination.parents:
        raise ValueError('Destination must be a new directory outside the source repository.')
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    selected = [p for p in tracked if p.startswith('skills/') or p in {
        'LICENSE', '.claude-plugin/marketplace.json', '.codex-plugin/plugin.json'}]
    if '.codex-plugin/plugin.json' not in selected:
        raise ValueError('Codex manifest is not tracked; stage release files before export.')
    # An allowlist excludes contributor context, Claude MCP declarations and all
    # runtime state, even if an ignored worktree or private workspace exists.
    for relative in selected:
        source = ROOT / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f'Export requires an ordinary tracked file: {relative}')
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    manifest = json.loads((destination / '.codex-plugin/plugin.json').read_text())
    if manifest.get('mcpServers') != {}:
        raise ValueError('Codex package must have an explicit empty MCP mapping.')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    export(args.destination)
    print(f'Clean Codex marketplace exported to {args.destination.resolve()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
