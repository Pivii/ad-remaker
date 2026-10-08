#!/usr/bin/env python3
"""Regenerate the body of the Claude Code subagent from SOUL.md.

SOUL.md is the single source of the agent prompt (ADR-003). This script keeps
the frontmatter of agents/ad-remaker.md as written and replaces everything
after it with SOUL.md verbatim. `scripts/validate_distribution.py` fails when
the two differ. Run with `--check` to report without writing.
"""

from __future__ import annotations

import argparse
import sys

from validate_distribution import PLUGIN_AGENT, ROOT, SOUL_FILE, render_agent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="exit 1 if the subagent is out of date, without writing")
    args = parser.parse_args(argv)

    agent_path = ROOT / PLUGIN_AGENT
    current = agent_path.read_text(encoding="utf-8")
    expected = render_agent(current, (ROOT / SOUL_FILE).read_text(encoding="utf-8"))
    if expected is None:
        print(f"{PLUGIN_AGENT}: must begin with a closed YAML frontmatter block", file=sys.stderr)
        return 1
    if expected == current:
        print(f"{PLUGIN_AGENT} is in sync with {SOUL_FILE}.")
        return 0
    if args.check:
        print(f"{PLUGIN_AGENT} differs from {SOUL_FILE}; run python3 scripts/sync_claude_agent.py", file=sys.stderr)
        return 1
    agent_path.write_text(expected, encoding="utf-8")
    print(f"Updated {PLUGIN_AGENT} from {SOUL_FILE}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
