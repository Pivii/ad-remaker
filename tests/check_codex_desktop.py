#!/usr/bin/env python3
"""Check the installed Desktop app's bundled runtime, without opening its GUI.

This does not validate Plugins Directory clicks or composer interaction.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile

from check_codex import PLUGIN, ROOT, Server, binary, command, config_fingerprint, export


def app_metadata(app: Path) -> tuple[dict, Path]:
    info = plistlib.loads((app / 'Contents/Info.plist').read_bytes())
    if info.get('CFBundleIdentifier') != 'com.openai.codex':
        raise ValueError('Expected the official Codex Desktop bundle com.openai.codex.')
    embedded = app / 'Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex'
    if not embedded.is_file():
        raise ValueError('Installed Desktop bundle has no inspectable embedded runtime at the expected path.')
    # Read only application source, never application/user runtime databases.
    source = (app / 'Contents/Resources/app.asar').read_bytes()
    if not all(marker in source for marker in [b'plugin/install', b'plugin/installed']):
        raise ValueError('Cannot establish the app uses the tested plugin protocol methods.')
    return info, embedded


def check(app: Path, chat: bool, keep: bool) -> None:
    info, embedded = app_metadata(app)
    os.environ['CODEX_TEST_BIN'] = str(embedded)
    version = subprocess.check_output([binary(), '--version'], text=True).strip()
    print(f"Desktop bundle {info['CFBundleShortVersionString']} (build {info['CFBundleVersion']}), {info['CFBundleIdentifier']}")
    print(f'Bundled runtime: {version}; {embedded}')
    print('Scope: actual Desktop-bundled app-server/runtime, not GUI install or composer interaction.')
    real_home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    before = config_fingerprint(real_home)
    with tempfile.TemporaryDirectory(prefix='ar-desktop-runtime-') as tmp:
        root = Path(tmp)
        home = root / 'codex-home'; home.mkdir()
        work = root / 'work'; work.mkdir()
        package = root / 'package'; export(package)
        env = dict(os.environ, CODEX_HOME=str(home))
        env.pop('OPENAI_API_KEY', None)
        command(env, work, 'plugin', 'marketplace', 'add', str(package), '--json')
        server = Server(env, work)
        try:
            catalog = server.call('plugin/list', {'cwds': [str(package)], 'marketplaceKinds': ['local'], 'forceRefetch': False})
            assert not catalog.get('marketplaceLoadErrors'), catalog
            market = next(m for m in catalog['marketplaces'] if m['name'] == 'ad-remaker')
            entry = next(p for p in market['plugins'] if p['id'] == PLUGIN)
            assert entry['availability'] == 'AVAILABLE' and not entry['installed'], entry
            installed = server.call('plugin/install', {'pluginName': 'ad-remaker', 'marketplacePath': market['path']})
            assert installed['appsNeedingAuth'] == [], 'Unexpected provider authentication requirement.'
            inventory = server.call('plugin/installed', {'cwds': [str(work)]})
            entries = [p for m in inventory['marketplaces'] for p in m['plugins'] if p['id'] == PLUGIN]
            assert len(entries) == 1 and entries[0]['installed'] and entries[0]['enabled'], entries
            print('PASS Desktop backend plugin/list -> plugin/install -> plugin/installed; enabled, no apps needing auth')
            discovery = server.call('skills/list', {'cwds': [str(work)], 'forceReload': True})
            assert not any(row['errors'] for row in discovery['data'])
            skills = [s for row in discovery['data'] for s in row['skills'] if s.get('pluginId') == PLUGIN and s['enabled']]
            names = {f'ad-remaker:{p.parent.name}' for p in (ROOT / 'skills').glob('*/SKILL.md')}
            assert {s['name'] for s in skills} == names
            for skill in skills:
                installed_entry = Path(skill['path'])
                name = installed_entry.parent.name
                for source in (ROOT / 'skills' / name).rglob('*'):
                    if source.is_file() and '__pycache__' not in source.parts:
                        target = installed_entry.parent / source.relative_to(ROOT / 'skills' / name)
                        assert target.read_bytes() == source.read_bytes(), f'Missing/changed Desktop support file: {source.name}'
            print('PASS Desktop runtime six Skills discovered; all support/rule files byte-identical')
            server.call('thread/start', {'cwd': str(work), 'ephemeral': True, 'model': 'gpt-6.1-sol'})
            status = server.call('mcpServerStatus/list', {})
            assert status['data'] == [] and status.get('nextCursor') is None, status
            print('PASS Desktop runtime thread startup: zero MCP servers, no model turn started')
            server.call('plugin/uninstall', {'pluginId': PLUGIN})
            inventory = server.call('plugin/installed', {'cwds': [str(work)]})
            assert not any(p['id'] == PLUGIN and p['installed'] for m in inventory['marketplaces'] for p in m['plugins'])
            print('PASS Desktop backend uninstall; isolated configuration cleaned')
        finally:
            server.close()
    assert config_fingerprint(real_home) == before
    print('PASS real user config/auth/plugin-registration fingerprints unchanged')
    if chat:
        args = [sys.executable, str(ROOT / 'tests/check_codex_chat.py'), '--chat', '--workflow-only', '--model', 'gpt-6.1-sol']
        if keep:
            args.append('--keep')
        subprocess.run(args, env=dict(os.environ), check=True)
        print('PASS Desktop-bundled runtime explicit workflow/rule reads and pre-dispatch canary; GUI remains untested')
    else:
        print('SKIPPED Desktop runtime model invocation: add --chat for guarded canary/workflow.')
    print('OPEN required Desktop GUI installation/discovery/composer validation; this runtime check cannot close issue #22.')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=Path('/Applications/ChatGPT.app'))
    parser.add_argument('--chat', action='store_true')
    parser.add_argument('--keep', action='store_true')
    args = parser.parse_args()
    check(args.app, args.chat, args.keep)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
