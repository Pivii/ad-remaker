#!/usr/bin/env python3
"""Model-free private setup state, persistence, isolation and recovery checks."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'skills/setup/scripts/setup_state.py'
spec = importlib.util.spec_from_file_location('setup_state', HELPER)
state = importlib.util.module_from_spec(spec); spec.loader.exec_module(state)


def main():
    with tempfile.TemporaryDirectory(prefix='ar-setup-check-') as tmp:
        base = Path(tmp).resolve(); root = base / 'private'; project = base / 'product-a'; project.mkdir()
        def run(*args, code=0, private=root, workspace=project, runtime='codex'):
            command = [sys.executable, str(HELPER), '--runtime', runtime, '--state-dir', str(private), '--project', str(workspace), *args]
            result = subprocess.run(command, text=True, capture_output=True)
            assert result.returncode == code, (args, result.stderr)
            return json.loads(result.stdout) if not code else result.stderr
        assert not run('status')['preferences']['complete'] and not root.exists()
        reordered = subprocess.run([sys.executable, str(HELPER), 'status', '--runtime', 'codex', '--state-dir', str(root), '--project', str(project)], text=True, capture_output=True)
        assert reordered.returncode == 0 and not root.exists()
        run('task', '--task', 'Analyze Product A competitors after setup')
        run('choose', '--research', 'free')
        run('complete', code=2)
        assert run('status')['project']['pending_task'].startswith('Analyze Product A')
        assert run('status')['preferences']['routes'] == {'research': 'free'}
        print('PASS absent state does not choose free; partial answers/task survive interruption')
        run('choose', '--free'); run('complete')
        assert run('status')['preferences']['complete']
        first = (root / 'setup.json').read_bytes()
        assert run('resolve')['routes'] == dict.fromkeys(state.ROUTES, 'free')
        other = base / 'product-b'; other.mkdir()
        assert run('status', workspace=other)['preferences']['complete']
        assert run('status', workspace=other)['project']['products'] == {}
        assert (root / 'setup.json').read_bytes() == first
        assert not any(project.iterdir())
        print('PASS free persists across sessions/projects/update reads; no private files in project Git')
        brief_a = json.dumps({'name': 'Product A', 'competitors': ['A Rival'], 'approved_claims': []})
        run('product', '--product', 'a', '--brief', brief_a, '--overrides', '{"generation":"pika"}')
        run('product', '--product', 'b', '--brief', '{"name":"Product B","competitors":["B Rival"]}')
        run('resolve', code=2)
        resolved = run('resolve', '--product', 'a', '--task-routes', '{"generation":"free"}')
        assert resolved['routes']['generation'] == 'free'
        assert run('resolve', '--product', 'a')['routes']['generation'] == 'pika'
        assert run('resolve', '--product', 'b')['routes']['generation'] == 'free'
        run('product', '--product', 'a', '--brief', brief_a)
        assert run('resolve', '--product', 'a')['routes']['generation'] == 'pika'
        assert (root / 'setup.json').read_bytes() == first
        run('choose', '--research', 'trendtrack', '--generation', 'deferred', '--fallback', 'free')
        assert run('status')['project']['products']['a']['brief']['competitors'] == ['A Rival']
        assert run('resolve', '--product', 'b')['routes']['research'] == 'trendtrack'
        print('PASS explicit task > product > user precedence; separate products; targeted edits preserve unrelated state')
        run('connection', '--provider', 'trendtrack', '--status', 'verified')
        assert not run('status')['connection_history_is_current']
        assert run('resolve', '--product', 'b')['connection_check_required']
        run('connection', '--provider', 'trendtrack', '--status', 'blocked')
        assert run('resolve', '--product', 'b')['routes']['research'] == 'trendtrack'
        print('PASS historical connection never current; blocked connection preserves selected route')
        for corrupt in ['{', json.dumps(dict(state.empty(), schema_version=2)), json.dumps(dict(state.empty(), token='secret'))]:
            path = root / 'setup.json'; path.write_text(corrupt)
            run('status', code=2); run('choose', '--free', code=2)
            assert path.read_text() == corrupt
        run('choose', '--free', private=base / 'recovery'); run('complete', private=base / 'recovery')
        print('PASS corrupt/incompatible/unknown field state preserved; explicit fresh-root recovery')
        (root / 'setup.json').write_text(json.dumps(state.empty()))
        run('product', '--product', '../escape', '--brief', '{"name":"X"}', code=2)
        run('product', '--product', 'secret', '--brief', '{"name":"X","api_key":"bad"}', code=2)
        run('task', '--task', 'password=secret', code=2)
        run('choose', '--free', private=ROOT / 'local/setup', code=2)
        run('choose', '--free', private=project / 'private', code=2)
        outside = base / 'outside'; outside.mkdir()
        link = root / 'projects'; link.rename(root / 'old-projects'); link.symlink_to(outside, target_is_directory=True)
        run('status', code=2); run('product', '--product', 'a', '--brief', brief_a, code=2)
        assert not any(outside.iterdir())
        for n in ['one', 'two']:
            run('choose', '--free', runtime='hermes', private=base / n / 'ad-remaker-state')
        run('choose', '--research', 'trendtrack', runtime='hermes', private=base / 'one/ad-remaker-state')
        assert run('status', runtime='hermes', private=base / 'two/ad-remaker-state')['preferences']['routes']['research'] == 'free'
        assert state.state_root('hermes', profile_home=str(base / 'one')) != state.state_root('hermes', profile_home=str(base / 'two'))
        if os.name != 'nt':
            assert (base / 'recovery/setup.json').stat().st_mode & 0o777 == 0o600
        print('PASS credential/path/symlink rejection; profile isolation; private permissions')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
