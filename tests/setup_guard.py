#!/usr/bin/env python3
"""Allow only parsed bundled-helper argument vectors confined to scratch roots."""
import importlib.util
import contextlib
import io
from pathlib import Path
import re
import shlex


def helper_command(command, config):
    if not isinstance(command, str) or re.search(r'[;&|><`\n]|\$[({]', command):
        return []
    try:
        words = shlex.split(command)
        if len(words) < 3 or words[0] not in {'python3', config['python']} or words[1] != config['helper']:
            return []
        spec = importlib.util.spec_from_file_location('guarded_setup_state', config['helper'])
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with contextlib.redirect_stderr(io.StringIO()):
            args = module.parser().parse_args(words[2:])
        if args.state_dir != config['state_dir'] or args.project not in config['projects'] or args.runtime != config['runtime'] or args.profile_home:
            return []
        # Connection history is synthetic metadata only; helper has no network,
        # config, login, account or arbitrary file-write action.
        module.state_root(args.runtime, args.state_dir)
        return words
    except (ValueError, OSError, SystemExit):
        return []


def permitted_read(event, config):
    name = event.get('tool_name'); inputs = event.get('tool_input') or {}
    if name == 'Read' and inputs.get('file_path') in config['files']:
        return [inputs['file_path']]
    if name == 'Skill' and inputs.get('skill') in config.get('skills', []):
        return ['skill:' + inputs['skill']]
    if name == 'Bash':
        try:
            words = shlex.split(inputs.get('command', ''))
        except ValueError:
            return []
        if len(words) > 1 and words[0] in {'cat', '/bin/cat'} and all(p in config['files'] for p in words[1:]):
            return words[1:]
    return []


def main():
    import json
    import sys
    config = json.loads(Path(sys.argv[1]).read_text())
    event = json.load(sys.stdin)
    reads = permitted_read(event, config)
    setup = helper_command((event.get('tool_input') or {}).get('command'), config['setup']) if event.get('tool_name') == 'Bash' else []
    allowed = bool(reads or setup)
    with Path(config['log']).open('a') as log:
        log.write(json.dumps({'tool': event.get('tool_name'), 'reads': reads, 'setup': setup, 'blocked': not allowed, 'input': event.get('tool_input')}) + '\n')
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'allow' if allowed else 'deny', 'permissionDecisionReason': 'Isolated test: exact instruction reads and scratch-confined helper only.'}}))


if __name__ == '__main__':
    main()
