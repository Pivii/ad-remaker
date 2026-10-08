#!/usr/bin/env python3
"""Check that the validator accepts valid MCP fixtures and rejects invalid ones.

Each file in tests/fixtures/mcp/ is passed to
`scripts/validate_distribution.py --config <fixture>`. Its first line declares
the expected outcome: `# expect: pass`, or `# expect: <text>` where <text> must
appear in the validator's error output. Fixtures named `valid-*` must pass and
`invalid-*` must fail. Each fixture runs with PyYAML when it is installed and
always with the stdlib fallback parser (`python3 -S`).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_distribution.py"
FIXTURES = ROOT / "tests" / "fixtures" / "mcp"


def parser_modes() -> list[tuple[str, list[str]]]:
    modes = [("stdlib fallback", [sys.executable, "-S"])]
    try:
        import yaml  # type: ignore  # noqa: F401
    except ImportError:
        return modes
    return [("PyYAML", [sys.executable])] + modes


def main() -> int:
    fixtures = sorted(FIXTURES.glob("*.yaml"))
    if not fixtures:
        print(f"no fixtures found in {FIXTURES}", file=sys.stderr)
        return 1

    failures = 0
    for fixture in fixtures:
        first_line = fixture.read_text(encoding="utf-8").splitlines()[0]
        if not first_line.startswith("# expect: "):
            print(f"FAIL {fixture.name}: first line must be '# expect: ...'")
            failures += 1
            continue
        expected = first_line[len("# expect: "):].strip()
        should_pass = expected == "pass"
        if should_pass != fixture.name.startswith("valid-"):
            print(f"FAIL {fixture.name}: name prefix and '# expect:' disagree")
            failures += 1
            continue

        for mode, command in parser_modes():
            result = subprocess.run(
                command + [str(VALIDATOR), "--config", str(fixture)],
                capture_output=True,
                text=True,
            )
            output = result.stdout + result.stderr
            if should_pass:
                ok = result.returncode == 0
            else:
                ok = result.returncode != 0 and expected in output
            print(f"{'ok  ' if ok else 'FAIL'} {fixture.name} ({mode}): exit {result.returncode}")
            if not ok or not should_pass:
                for line in output.strip().splitlines():
                    print(f"       {line}")
            failures += 0 if ok else 1

    print(f"{len(fixtures)} fixture(s), {failures} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
