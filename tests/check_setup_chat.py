#!/usr/bin/env python3
"""Isolated setup behavior, exact helper writes only; no real vendor dispatch."""
from __future__ import annotations
import argparse
import json
import hashlib
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

from check_codex import ROOT, PLUGIN, command, export, config_fingerprint, binary
from setup_guard import helper_command


def guard_checks():
    with tempfile.TemporaryDirectory(prefix='ar-setup-guard-') as tmp:
        root = Path(tmp).resolve()
        c = {'helper': str(ROOT / 'skills/setup/scripts/setup_state.py'), 'state_dir': str(root / 'state'),
             'projects': [str(root / 'work')], 'runtime': 'codex', 'python': sys.executable}
        words = [sys.executable, c['helper'], '--runtime', 'codex', '--state-dir', c['state_dir'], '--project', c['projects'][0], 'choose', '--free']
        good = shlex.join(words)
        assert helper_command(good, c)
        for bad in [good + '; touch /tmp/escape', good + ' > /tmp/escape', good.replace(c['state_dir'], str(root / 'escape')),
                    good.replace(c['projects'][0], '/tmp/escape'), good.replace('codex', 'hermes'),
                    good.replace('choose --free', 'task --task "$(touch /tmp/escape)"'),
                    good.replace(c['helper'], '/tmp/arbitrary.py'), good + ' --profile-home /tmp/escape',
                    good.replace('choose --free', 'login'), 'curl https://example.com', 'python3 -c "print(1)"']:
            assert not helper_command(bad, c), bad
        assert not (root / 'state').exists()
    print('PASS setup guard: exact parsed helper only; scratch/runtime/project/profile/chains/redirection/expansion rejected')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chat', action='store_true')
    parser.add_argument('--runtime', choices=['codex', 'claude'], default='codex')
    parser.add_argument('--keep', action='store_true')
    parser.add_argument('--scenario', choices=['guard-canary', 'first', 'free', 'repeat', 'second-product', 'mock-connected', 'mock-failed', 'explicit-and-connections', 'infer-product'], help='Only this scenario (all by default); state prerequisites seeded by deterministic helper')
    args = parser.parse_args(); guard_checks()
    if not args.chat:
        print('SKIPPED setup model behavior: --chat uses existing subscription allowance only.'); return 0
    root = Path(tempfile.mkdtemp(prefix='ar-setup-chat-')).resolve(); success = False
    home = root / 'client-home'; home.mkdir(mode=0o700)
    work = root / 'work'; work.mkdir(); second = root / 'second'; second.mkdir()
    private = root / 'state'
    product_doc = work / 'README.md'
    product_doc.write_text('# Product C\nProduct C is a focus timer for builders in France.\nWe claim it doubles productivity; this claim has no supporting study here.\nCompetitors and approved claims have not been confirmed.\n')
    real_home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    fingerprint = config_fingerprint(real_home)
    claude_before = None
    credential_source = None
    try:
        env = dict(os.environ)
        for key in ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_ORG_ID', 'OPENAI_PROJECT_ID', 'ANTHROPIC_API_KEY', 'ANTHROPIC_BASE_URL', 'ANTHROPIC_AUTH_TOKEN']:
            env.pop(key, None)
        package = root / 'package'
        if args.runtime == 'codex':
            auth = real_home / 'auth.json'
            if not auth.is_file() or json.loads(auth.read_text()).get('auth_mode') != 'chatgpt':
                raise RuntimeError('Existing ChatGPT file auth required; no login/API fallback.')
            shutil.copyfile(auth, home / 'auth.json'); (home / 'auth.json').chmod(0o600)
            env['CODEX_HOME'] = str(home)
            export(package)
            command(env, work, 'plugin', 'marketplace', 'add', str(package), '--json')
            cache = Path(command(env, work, 'plugin', 'add', PLUGIN, '--json')['installedPath'])
            with (home / 'config.toml').open('a') as f:
                f.write('\n[features]\nskip_host_skill_discovery = true\nshell_snapshot = false\napps = false\nbrowser_use = false\ncomputer_use = false\ncode_mode = false\ncode_mode_host = true\n')
        else:
            env['CLAUDE_CONFIG_DIR'] = str(home)
            package.mkdir(); shutil.copytree(ROOT / 'skills', package / 'skills')
            shutil.copytree(ROOT / '.claude-plugin', package / '.claude-plugin')
            shutil.copytree(ROOT / 'agents', package / 'agents')
            cache = package
            credential_file = Path.home() / '.claude/.credentials.json'
            if credential_file.is_file():
                credential_source = credential_file
                raw_credentials = credential_file.read_text()
            else:
                found = subprocess.run(['security', 'find-generic-password', '-s', 'Claude Code-credentials', '-w'], capture_output=True, text=True)
                if found.returncode:
                    raise RuntimeError('Existing Claude subscription credentials unavailable; no login/API fallback.')
                raw_credentials = found.stdout
            claude_before = hashlib.sha256(raw_credentials.encode()).hexdigest()
            credentials = json.loads(raw_credentials)
            if not credentials.get('claudeAiOauth'):
                raise RuntimeError('Existing Claude OAuth required; no API-key fallback.')
            (home / '.credentials.json').write_text(json.dumps({'claudeAiOauth': credentials['claudeAiOauth']}))
            (home / '.credentials.json').chmod(0o600)
            del raw_credentials, credentials
            # Claude uses subscription keychain auth on this host. Require an
            # affirmative OAuth status before a model turn; no API fallback.
            status = subprocess.run(['claude', 'auth', 'status'], env=env, cwd=work, capture_output=True, text=True)
            # Auth status is inspected but personal identity is not retained.
            auth_status = json.loads(status.stdout)
            if status.returncode or not auth_status.get('loggedIn') or auth_status.get('authMethod') not in {'claude.ai', 'oauth'}:
                raise RuntimeError('Isolated Claude subscription auth unavailable; no login/API fallback.')
        files = [str(p.resolve()) for p in (cache / 'skills').rglob('*.md') if p.name != 'upstream.md']
        files.append(str(product_doc))
        helper = str((cache / 'skills/setup/scripts/setup_state.py').resolve())
        guard_log = root / 'guard.jsonl'; guard_config = root / 'guard.json'
        setup = {'helper': helper, 'python': sys.executable, 'state_dir': str(private), 'projects': [str(work), str(second)], 'runtime': args.runtime}
        guard_config.write_text(json.dumps({'files': files, 'skills': ['ad-remaker:' + p.parent.name for p in (cache / 'skills').glob('*/SKILL.md')], 'log': str(guard_log), 'setup': setup}))
        hook = shlex.join([sys.executable, str(ROOT / 'tests/setup_guard.py'), str(guard_config)])
        hooks = {'hooks': {'PreToolUse': [{'matcher': '.*', 'hooks': [{'type': 'command', 'command': hook}]}]}}
        if args.runtime == 'codex':
            (home / 'hooks.json').write_text(json.dumps(hooks))
        else:
            (home / 'settings.json').write_text(json.dumps(hooks))
        base = [sys.executable, helper, '--runtime', args.runtime, '--state-dir', str(private), '--project', str(work)]
        def seed(*words):
            subprocess.run(base + list(words), check=True, capture_output=True)
        scenarios = [
            ('guard-canary', 'Run exactly this shell command once and report its result: touch ' + str(work / 'guard-canary'), work),
            ('first', 'Use Ad Remaker to analyze the ads of my competitors.', work),
            ('free', 'Use your setup Skill. I choose free for everything. Save that choice and complete setup, explain the render limitation, then resume my original request: analyze competitor ads for Product A. My product brief is not yet confirmed.', work),
            ('repeat', 'Use Ad Remaker to analyze Product A competitors. Load my saved choices. Do not repeat tools onboarding; ask only for missing product inputs. No providers are connected.', work),
            ('infer-product', 'Use Ad Remaker setup for product context in this project. Read the relevant README, propose its product facts and ask me to confirm them before saving. Do not treat its unsupported productivity claim as approved.', work),
            ('second-product', 'Use your setup Skill for product context only. My confirmed product is Product B, audience builders, competitor B Rival, approved claims none. Save this confirmed brief under product ID b. Keep my tools choices. Do not scan other repositories.', second),
            ('mock-connected', 'Use your setup Skill for tools only. Test-only mock capability observation: TrendTrack tools are discovered and authenticated, but no documented zero-credit verification exists. I choose TrendTrack research, deferred video, manual files delivery, fallback ask. Save choices; reuse existing auth, no login or service call. Keep status configured/unverified, not verified.', work),
            ('mock-failed', 'Use Ad Remaker to analyze competitors using saved routes. Test-only mock current observation: TrendTrack authentication has failed. No automatic fallback is authorized. Explain the blocker and offer recovery/later/free for this task without changing my saved preference or calling a service.', work),
        ]
        if args.scenario:
            selected = {'guard-canary', args.scenario}
            if args.scenario == 'explicit-and-connections':
                selected.update({'free', 'second-product', 'mock-connected', 'mock-failed'})
            scenarios = [s for s in scenarios if s[0] in selected]
            if args.scenario in {'repeat', 'second-product', 'mock-connected', 'mock-failed', 'infer-product'}:
                seed('choose', '--free'); seed('complete')
            if args.scenario == 'mock-failed': seed('choose', '--research', 'trendtrack', '--fallback', 'ask')
        print(f'{args.runtime}: existing subscription model allowance only; no API/vendor billing.')
        for name, prompt, cwd in scenarios:
            before = len(guard_log.read_text().splitlines()) if guard_log.exists() else 0
            instructions = ('Isolated behavior harness: all real provider, web, login, install and arbitrary shell/file tools are denied before dispatch. '
                'Instruction reads and the installed setup helper with exactly the following private scratch arguments are allowed. '
                'Runtime ' + args.runtime + '; helper ' + helper + '; private root ' + str(private) + '; project ' + str(cwd) + '. '
                'Use --runtime ' + args.runtime + ' --state-dir ' + str(private) + ' --project ' + str(cwd) + '. '
                'Read installed Skills/rule references before acting. Only cat with absolute paths, Read (Claude), and exact python helper commands are permitted. '
                'Synthetic products, no external research in this check.\n')
            if name == 'free':
                selector = '$ad-remaker:setup' if args.runtime == 'codex' else '/ad-remaker:setup'
                prompt = prompt.replace('Use your setup Skill.', selector, 1)
            if name == 'guard-canary':
                instructions = ''
            if args.runtime == 'codex':
                argv = [binary(), 'exec', '--model', 'gpt-6.1-sol', '--sandbox', 'workspace-write', '--skip-git-repo-check', '--ephemeral', '--json', '--dangerously-bypass-hook-trust', '-c', 'web_search="disabled"', '-c', 'model_reasoning_effort="low"', '--output-last-message', str(root / (name + '-reply.txt')), instructions + prompt]
            else:
                argv = ['claude', '-p', '--plugin-dir', str(package), '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}', '--settings', str(home / 'settings.json'), '--setting-sources', '', '--tools', 'Bash,Read,Skill', '--permission-mode', 'acceptEdits', '--output-format', 'json', '--max-turns', '18', '--append-system-prompt', instructions, prompt]
            result = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=240)
            (root / (name + '-events.jsonl')).write_text(result.stdout); (root / (name + '-stderr.txt')).write_text(result.stderr)
            assert result.returncode == 0, f'{name}: client failed; see {root}'
            if args.runtime == 'claude':
                response = json.loads(result.stdout); (root / (name + '-reply.txt')).write_text(response.get('result', ''))
                assert not response.get('is_error'), f'{name}: {response}'
            records = [json.loads(l) for l in guard_log.read_text().splitlines()[before:]] if guard_log.exists() else []
            reply = (root / (name + '-reply.txt')).read_text().lower()
            assert reply.strip()
            if name == 'guard-canary':
                assert any(r['blocked'] for r in records) and not (work / 'guard-canary').exists(), 'Pre-dispatch guard failed; stop.'
                print('PASS canary: prohibited shell write blocked before dispatch')
                continue
            assert any('setup/' in p or p == 'skill:ad-remaker:setup' for r in records for p in r['reads']), f'{name}: no setup read (implicit discovery not verified); {root}'
            for record in records:
                if record['blocked']:
                    cmd = json.dumps(record.get('input', {})).lower()
                    assert record['tool'] in {'Bash', 'Read'} and any(w in cmd for w in ['cat ', 'sed ', 'head ', 'file_path']), f'{name}: forbidden attempt {record}'
            state = json.loads((private / 'setup.json').read_text()) if (private / 'setup.json').exists() else None
            if name == 'first':
                assert state is None or not state['complete']
                assert 'free' in reply and any(w in reply for w in ['connect', 'service'])
            elif name == 'free':
                assert state and state['complete'] and set(state['routes'].values()) == {'free'}
                assert 'video' in reply and any(w in reply for w in ['render', 'prompts']) and 'competitor' in reply
            elif name == 'repeat':
                assert state and state['complete'] and set(state['routes'].values()) == {'free'}
                assert 'free' in reply or 'public' in reply
            elif name == 'infer-product':
                assert str(product_doc) in {p for r in records for p in r['reads']}
                assert 'product c' in reply and any(w in reply for w in ['confirm', 'correct'])
                project_records = list((private / 'projects').glob('*.json')) if (private / 'projects').exists() else []
                assert not any('doubles productivity' in claim for file in project_records for item in json.loads(file.read_text())['products'].values() for claim in item['brief'].get('approved_claims', []))
            elif name == 'second-product':
                sys.path.insert(0, str(cache / 'skills/setup/scripts')); import setup_state
                product = setup_state.load(setup_state.project_file(private, second), True)
                assert product['products']['b']['brief']['name'] == 'Product B'
                assert state['routes']['research'] == 'free'
            elif name == 'mock-connected':
                assert state['routes']['research'] == 'trendtrack' and state['routes']['generation'] == 'deferred'
                assert not any(v['status'] == 'verified' for v in state['connections'].values())
                assert 'unverified' in reply or 'configured' in reply
            elif name == 'mock-failed':
                assert state['routes']['research'] == 'trendtrack'
                assert 'free' in reply and any(w in reply for w in ['auth', 'blocked', 'failed'])
            print('PASS ' + name + ': setup reads, scratch state assertions, no provider/arbitrary dispatch')
        if args.runtime == 'claude':
            original = credential_source.read_text() if credential_source else subprocess.check_output(['security', 'find-generic-password', '-s', 'Claude Code-credentials', '-w'], text=True)
            assert hashlib.sha256(original.encode()).hexdigest() == claude_before, 'Real Claude credential storage changed.'
            del original
        assert config_fingerprint(real_home) == fingerprint
        success = True; print('PASS setup behavior; evidence: ' + str(root)); return 0
    finally:
        shutil.rmtree(home, ignore_errors=True); shutil.rmtree(root / 'package', ignore_errors=True)
        if success and not args.keep: shutil.rmtree(root)
        else: print('Retained non-auth test evidence: ' + str(root))


if __name__ == '__main__':
    raise SystemExit(main())
