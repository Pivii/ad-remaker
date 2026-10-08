#!/usr/bin/env python3
"""Isolated, model-free Codex install/discovery/cleanup acceptance check."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from export_codex_package import export

PLUGIN = 'ad-remaker@ad-remaker'

def binary() -> str:
    return os.environ.get('CODEX_TEST_BIN', 'codex')


class Server:
    def __init__(self, env: dict[str, str], cwd: Path):
        self.process = subprocess.Popen([binary(), 'app-server'], cwd=cwd, env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True)
        self.messages: queue.Queue = queue.Queue()
        self.counter = 0
        def read():
            for line in self.process.stdout:
                self.messages.put(json.loads(line))
            self.messages.put(None)
        threading.Thread(target=read, daemon=True).start()
        try:
            self.call('initialize', {'clientInfo': {'name': 'ad-remaker-check', 'version': '1'},
                                    'capabilities': {'experimentalApi': True}})
            self.send({'method': 'initialized'})
        except BaseException:
            self.close()
            raise

    def send(self, value: dict) -> None:
        self.process.stdin.write(json.dumps(value) + '\n')
        self.process.stdin.flush()

    def call(self, method: str, params: dict) -> dict:
        self.counter += 1
        current = self.counter
        self.send({'id': current, 'method': method, 'params': params})
        while True:
            message = self.messages.get(timeout=30)
            if message is None:
                raise RuntimeError('Codex app-server stopped before response.')
            if message.get('id') != current:
                continue
            if 'error' in message:
                raise RuntimeError(f'{method}: {message["error"]}')
            return message['result']

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()


def command(env: dict[str, str], cwd: Path, *args: str) -> dict:
    result = subprocess.run([binary(), *args], cwd=cwd, env=env,
                            text=True, capture_output=True, timeout=90)
    if result.returncode:
        raise RuntimeError(f'codex {" ".join(args)}: {result.stderr}')
    return json.loads(result.stdout)


def config_fingerprint(home: Path) -> dict[str, str | None]:
    paths = {'config.toml', 'auth.json', 'plugins/installed_plugins.json'}
    paths.update(p.name for p in home.glob('*.config.toml'))
    return {name: hashlib.sha256((home / name).read_bytes()).hexdigest()
            if (home / name).is_file() else None for name in paths}


def check(source: str | None = None, ref: str | None = None) -> None:
    real_home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    before = config_fingerprint(real_home)
    with tempfile.TemporaryDirectory(prefix='ar-codex-check-') as tmp:
        root = Path(tmp)
        home = root / 'codex-home'
        home.mkdir()
        work = root / 'work'
        work.mkdir()
        env = dict(os.environ, CODEX_HOME=str(home))
        env.pop('OPENAI_API_KEY', None)
        package = root / 'package'
        export(package)
        # Ignored runtime sentinels live in an isolated copy, never the user's clone.
        dirty = root / 'dirty'
        shutil.copytree(ROOT, dirty, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        for relative, mutate, error in [
            ('skills/provider-policy/references/agent-rules.md', lambda text: text + '\nstale rule\n', 'generated rules differ'),
            ('.codex-plugin/plugin.json', lambda text: json.dumps(dict(json.loads(text), version='0.0.0-invalid')), 'identity/version/skills'),
            ('.codex-plugin/plugin.json', lambda text: json.dumps(dict(json.loads(text), mcpServers={'unsafe': {'url': 'https://example.invalid'}})), 'identity/version/skills'),
        ]:
            target = dirty / relative
            original = target.read_text()
            target.write_text(mutate(original))
            result = subprocess.run([sys.executable, str(dirty / 'scripts/validate_distribution.py')], capture_output=True, text=True)
            target.write_text(original)
            assert result.returncode == 1 and error in result.stderr, result.stderr
        print('PASS validator rejects rule drift, version mismatch and nonempty Codex MCP mapping')
        subprocess.run(['git', 'init', '-q', str(dirty)], check=True)
        subprocess.run(['git', '-C', str(dirty), 'add', '.'], check=True)
        for path in ['.claude/worktrees/nested/skills/extra/SKILL.md',
                     'local/brands/private/customer.txt', 'sessions/history.json',
                     'memory/private.txt', 'outputs/video.mp4', '.env', 'auth.json']:
            sentinel = dirty / path
            sentinel.parent.mkdir(parents=True, exist_ok=True)
            sentinel.write_text('test-only private sentinel')
        ignored = subprocess.check_output(['git', '-C', str(dirty), 'check-ignore', '.claude/worktrees/nested/skills/extra/SKILL.md', 'local/brands/private/customer.txt', 'sessions/history.json', 'memory/private.txt', 'outputs/video.mp4', '.env', 'auth.json'], text=True).splitlines()
        assert len(ignored) == 7, ignored
        clean = root / 'sentinel-export'
        subprocess.run([sys.executable, str(dirty / 'scripts/export_codex_package.py'), str(clean)], check=True)
        actual = {p.relative_to(clean).as_posix() for p in clean.rglob('*') if p.is_file()}
        expected = {p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file()}
        assert actual == expected, 'Runtime sentinel escaped export allowlist.'
        print('PASS clean export excludes ignored worktrees/runtime/secret sentinels')
        args = ['plugin', 'marketplace', 'add', source or str(package), '--json']
        if ref:
            args.extend(['--ref', ref])
        command(env, work, *args)
        installed = command(env, work, 'plugin', 'add', PLUGIN, '--json')
        cached = Path(installed['installedPath'])
        for file in package.rglob('*'):
            if file.is_file() and file.relative_to(package).parts[0] == 'skills':
                target = cached / file.relative_to(package)
                assert target.read_bytes() == file.read_bytes(), f'Missing/changed support file: {file}'
        forbidden = {'.env', 'auth.json', 'sessions', 'memory', 'memories', 'local', 'outputs', 'worktrees', 'mcp-tokens', 'vault'}
        unexpected = [p.relative_to(cached).as_posix() for p in cached.rglob('*') if set(p.relative_to(cached).parts) & forbidden]
        assert not unexpected, 'Runtime/secret paths in installed cache: ' + ', '.join(unexpected)
        git_metadata = cached / '.git'
        if git_metadata.exists():
            assert source, 'Local export must not include Git metadata.'
            assert git_metadata.is_dir(), 'Unexpected Git metadata link/file in cached plugin.'
            import configparser
            from urllib.parse import urlsplit
            from validate_distribution import TOKEN_SHAPE
            git_config = configparser.RawConfigParser()
            config_text = (git_metadata / 'config').read_text()
            assert not TOKEN_SHAPE.search(config_text), 'Token-shaped value in Git cache config.'
            git_config.read_string(config_text)
            for section in git_config.sections():
                for key, value in git_config.items(section):
                    assert key.lower() not in {'extraheader', 'password', 'token', 'secret', 'authorization'}, 'Credential field in Git cache config.'
                    if key.lower() == 'url':
                        parsed = urlsplit(value)
                        assert not parsed.username and not parsed.password and not parsed.query, 'Credentials/query in Git remote URL.'
            print('NOTE Codex Git cache includes installer-created .git metadata; config/remote URLs contain no embedded credentials')
        print('PASS installed support files byte-identical; no ignored worktree, secret, or user runtime paths')
        listing = command(env, work, 'plugin', 'list', '--marketplace', 'ad-remaker', '--json')
        assert any(p['pluginId'] == PLUGIN and p['enabled'] for p in listing['installed'])
        server = Server(env, work)
        try:
            discovery = server.call('skills/list', {'cwds': [str(work)], 'forceReload': True})
            assert not any(row['errors'] for row in discovery['data'])
            skills = [skill for row in discovery['data'] for skill in row['skills'] if skill.get('pluginId') == PLUGIN]
            names = {f'ad-remaker:{p.parent.name}' for p in (ROOT / 'skills').glob('*/SKILL.md')}
            assert {s['name'] for s in skills if s['enabled']} == names
            print('PASS Codex skills/list: ' + ', '.join(sorted(names)))
            server.call('thread/start', {'cwd': str(work), 'ephemeral': True, 'model': 'gpt-6.1-sol'})
            status = server.call('mcpServerStatus/list', {})
            assert status['data'] == [] and status.get('nextCursor') is None, status
            print('PASS thread startup: zero MCP servers (no model turn started)')
        finally:
            server.close()
        # Parse deliberate vendor opt-in/disable/remove without starting a server.
        pika_url = json.loads((ROOT / '.mcp.json').read_text())['mcpServers']['pika']['url']
        config_path = home / 'config.toml'
        with config_path.open('a') as config:
            config.write('\n[mcp_servers.pika]\nenabled = false\nurl = ' + json.dumps(pika_url) + '\n')
        configured = command(env, work, 'mcp', 'get', 'pika', '--json')
        assert configured['transport']['url'] == pika_url and configured['enabled'] is False, configured
        subprocess.run([binary(), 'mcp', 'remove', 'pika'], cwd=work, env=env, check=True, capture_output=True)
        print('PASS vendor opt-in/disable/remove configuration parsed; no login or provider call')
        # Upgrade refreshes a Git snapshot; add reinstalls the selected version.
        if source:
            upgrade = command(env, work, 'plugin', 'marketplace', 'upgrade', 'ad-remaker', '--json')
            print('PASS Git marketplace upgrade: ' + json.dumps(upgrade))
        else:
            manifest_path = package / '.codex-plugin/plugin.json'
            manifest = json.loads(manifest_path.read_text())
            manifest['version'] += '-update-check'
            manifest_path.write_text(json.dumps(manifest))
        command(env, work, 'plugin', 'remove', PLUGIN, '--json')
        updated = command(env, work, 'plugin', 'add', PLUGIN, '--json')
        cached = Path(updated['installedPath'])
        if not source:
            assert updated['version'].endswith('-update-check'), updated
        print('PASS update by reinstall: ' + updated['version'])
        command(env, work, 'plugin', 'remove', PLUGIN, '--json')
        listing = command(env, work, 'plugin', 'list', '--marketplace', 'ad-remaker', '--json')
        assert not any(p['pluginId'] == PLUGIN for p in listing['installed'])
        assert not cached.exists(), 'Uninstall did not remove plugin cache.'
        command(env, work, 'plugin', 'marketplace', 'remove', 'ad-remaker', '--json')
        print('PASS uninstall removes plugin/cache/marketplace; isolated CODEX_HOME cleaned')
    assert config_fingerprint(real_home) == before, 'Real user Codex configuration changed.'
    print('PASS real user Codex config/auth/plugin-registration fingerprints unchanged')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', help='Authenticated private Git source instead of local artifact')
    parser.add_argument('--ref', help='Git ref, only with --source')
    args = parser.parse_args()
    if args.ref and not args.source:
        parser.error('--ref requires --source')
    print(subprocess.check_output([binary(), '--version'], text=True).strip())
    check(args.source, args.ref)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
