#!/usr/bin/env python3
"""Test-only PreToolUse guard: exact installed instruction reads, deny all else."""
from __future__ import annotations
import json
from pathlib import Path
import shlex
import sys
from setup_guard import helper_command


def permitted(event: dict, files: set[str]) -> list[str]:
    if event.get('tool_name') != 'Bash':
        return []
    inputs = event.get('tool_input')
    if not isinstance(inputs, dict) or not isinstance(inputs.get('command'), str):
        return []
    try:
        words = shlex.split(inputs['command'])
    except ValueError:
        return []
    if len(words) < 2 or words[0] not in {'cat', '/bin/cat'}:
        return []
    if not all(word in files for word in words[1:]):
        return []
    return words[1:]


def main() -> int:
    config = json.loads(Path(sys.argv[1]).read_text())
    event = json.load(sys.stdin)
    reads = permitted(event, set(config['files']))
    setup = helper_command(event.get('tool_input', {}).get('command'), config['setup']) if event.get('tool_name') == 'Bash' and config.get('setup') else []
    with Path(config['log']).open('a') as log:
        log.write(json.dumps({'tool': event.get('tool_name'), 'reads': reads,
                              'setup': setup, 'blocked': not bool(reads or setup), 'input': event.get('tool_input')}) + '\n')
    output = {'hookEventName': 'PreToolUse', 'permissionDecision': 'allow' if reads or setup else 'deny'}
    if not (reads or setup):
        output['permissionDecisionReason'] = ('Test-only guard: no shell/vendor side effects. '
            'Only cat with exact absolute installed Skill/rule paths is permitted.')
    print(json.dumps({'hookSpecificOutput': output}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
