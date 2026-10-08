#!/usr/bin/env python3
"""Keep each installable Skill's agent rules derived from canonical SOUL.md."""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = (ROOT / 'SOUL.md').read_text(encoding='utf-8')
    stale = []
    targets = [(entry.parent / 'references/agent-rules.md', expected)
               for entry in sorted((ROOT / 'skills').glob('*/SKILL.md'))]
    if (ROOT / 'skills/setup/SKILL.md').exists():
        targets.append((ROOT / 'skills/setup/references/service-readiness.md',
                        (ROOT / 'docs/service-matrix.md').read_text(encoding='utf-8')))
    for target, expected in targets:
        if target.exists() and target.read_text(encoding='utf-8') == expected:
            continue
        stale.append(target.relative_to(ROOT).as_posix())
        if not args.check:
            target.parent.mkdir(exist_ok=True)
            target.write_text(expected, encoding='utf-8')
    if args.check and stale:
        print('Stale generated rules: ' + ', '.join(stale))
        return 1
    print('Skill agent rules in sync with SOUL.md.' if not stale else 'Generated rules: ' + ', '.join(stale))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
