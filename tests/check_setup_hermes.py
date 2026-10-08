#!/usr/bin/env python3
"""Guarded Hermes first-use/save/repeat setup in a disposable profile."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from check_codex import ROOT
from check_setup_chat import guard_checks


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--chat', action='store_true'); p.add_argument('--keep', action='store_true'); p.add_argument('--state-only', action='store_true'); args=p.parse_args()
    guard_checks()
    if not args.chat and not args.state_only:
        print('SKIPPED Hermes setup chat (requires existing ChatGPT allowance).'); return 0
    root = Path(tempfile.mkdtemp(prefix='ar-setup-hermes-')).resolve()
    name = 'ar-setup-' + str(int(time.time())) + '-' + str(os.getpid())
    success = False
    try:
        install = subprocess.run(['hermes', 'profile', 'install', str(ROOT), '--name', name, '--yes'], capture_output=True, text=True, check=True)
        config_path = Path(subprocess.check_output(['hermes', '-p', name, 'config', 'path'], text=True).strip()).resolve()
        profile = config_path.parent
        installed_helper = profile / 'skills/setup/scripts/setup_state.py'
        native_args = [sys.executable, str(installed_helper), '--runtime', 'hermes', '--profile-home', str(profile), '--project', str(root / 'native-project')]
        saved = subprocess.run(native_args + ['choose', '--free'], capture_output=True, text=True)
        assert saved.returncode == 0, saved.stderr
        subprocess.run(native_args + ['complete'], check=True, capture_output=True)
        preference_bytes = (profile / 'ad-remaker-state/setup.json').read_bytes()
        subprocess.run(['hermes', 'profile', 'update', name, '--yes'], check=True, capture_output=True, timeout=60)
        assert (profile / 'ad-remaker-state/setup.json').read_bytes() == preference_bytes
        print('PASS installed Hermes default private root and profile update preservation', flush=True)
        if args.state_only:
            success = True
            return 0
        for key, value in [('auxiliary.free_only','true'),('agent.clarify_timeout','5'),('agent.api_max_retries','1'),('auxiliary.title_generation.enabled','false')]:
            subprocess.run(['hermes','-p',name,'config','set',key,value],check=True,capture_output=True)
        version = subprocess.check_output(['hermes','--version'],text=True)
        install_root = next(l.split(': ',1)[1] for l in version.splitlines() if l.startswith('Install directory: '))
        python = str(Path(install_root) / 'venv/bin/python')
        helper = str(profile / 'skills/setup/scripts/setup_state.py')
        work = root / 'work'; work.mkdir(); private = root / 'state'
        files = [str(p.resolve()) for p in (profile / 'skills').rglob('*.md') if p.name != 'upstream.md']
        guard = root / 'guard-config.json'
        guard.write_text(json.dumps({'files': files, 'setup': {'helper':helper,'python':python,'runtime':'hermes','state_dir':str(private),'projects':[str(work)]}}))
        env=dict(os.environ,AR_SETUP_GUARD_CONFIG=str(guard)); env.pop('OPENAI_API_KEY',None)
        scenarios = [('guard-canary','Run exactly this terminal command once and report the result: touch '+str(work/'guard-canary')),
                     ('first','Use Ad Remaker to analyze ads of my competitors.'),
                     ('free','Use your setup Skill. I choose free for everything. Save and complete setup, explain that no new video is rendered, then resume my original competitor ad analysis for Product A. Product inputs are not yet confirmed.'),
                     ('repeat','Use Ad Remaker for competitor analysis for Product A. Load my saved settings and continue using public libraries, without asking tools onboarding again. No providers are connected.')]
        for label,prompt in scenarios:
            log=root/label;log.mkdir()
            harness=f'Isolated test: no vendor/web/login/installation calls. Use installed Skills and rules. Private setup helper {helper}, runtime hermes, --state-dir {private}, --project {work}. Only exact helper commands and instruction reads are allowed before dispatch. '
            result=subprocess.run([python,str(ROOT/'tests/smoke_chat.py'),install_root,str(log),'-p',name,'chat','-v','-q',harness+prompt,'--provider','openai-codex','-m','gpt-6.1-sol','--max-turns','16','--source','tool'],cwd=work,env=env,text=True,capture_output=True,timeout=240)
            (log/'chat.log').write_text(result.stdout+result.stderr)
            assert result.returncode==0, f'{label}: {root}'
            session=next((line.split()[1] for line in result.stdout.splitlines() if line.startswith('Session:')),None)
            assert session and 'SMOKE_GUARD_READY' in result.stdout, f'{label}: missing session/guard'
            subprocess.run(['hermes','-p',name,'sessions','export','--format','jsonl','--session-id',session,str(log/'session.jsonl'),'--yes'],check=True,capture_output=True)
            subprocess.run([sys.executable,str(ROOT/'tests/smoke_session.py'),str(log)],check=True)
            records=[json.loads(l) for l in (log/'guard.jsonl').read_text().splitlines()]
            if label=='guard-canary':
                assert any(r['name']=='terminal' and r['stubbed'] for r in records) and not (work/'guard-canary').exists(), 'Guard canary failed'
                print('PASS Hermes canary: terminal side effect blocked before dispatch',flush=True)
                continue
            assert any(r['name']=='skill_view' and r['arguments'].get('name')=='setup' for r in records), f'{label}: setup not read'
            assert not any(r['name'].startswith('mcp_') or (r['stubbed'] and r['name'] not in {'terminal'}) for r in records)
            for r in records:
                if r['stubbed'] and r['name']=='terminal':
                    assert any(w in r['arguments'].get('command','') for w in ['cat ','sed ','head ']), f'Forbidden command attempt: {r}'
            settings=json.loads((private/'setup.json').read_text()) if (private/'setup.json').exists() else None
            reply=(log/'reply.txt').read_text().lower()
            if label=='first':
                assert settings is None or not settings['complete']
                offered = reply + ' '.join(json.dumps(r['arguments']).lower() for r in records if r['name']=='clarify')
                assert 'free' in offered and any(w in offered for w in ['connect', 'service'])
            else: assert settings and settings['complete'] and set(settings['routes'].values())=={'free'}
            if label=='free': assert 'video' in reply and 'competitor' in reply
            print('PASS Hermes '+label+': setup Skill, guarded helper and persisted free-route assertions',flush=True)
        success=True;print('PASS Hermes setup behavior; evidence: '+str(root));return 0
    finally:
        # This runner owns only its newly named profile; never another profile.
        subprocess.run(['hermes','profile','delete','-y',name],capture_output=True)
        if success and not args.keep: shutil.rmtree(root)
        else: print('Retained non-auth evidence: '+str(root))


if __name__=='__main__': raise SystemExit(main())
