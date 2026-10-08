#!/usr/bin/env python3
"""Regression checks for smoke-test failures, with no real Hermes or provider calls."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from smoke_chat import SmokeGuard, install_guard
from smoke_session import extract


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / "tests/smoke.sh").read_text()


class SmokeRegressionTests(unittest.TestCase):
    def test_sensitive_tools_never_reach_handlers(self):
        with tempfile.TemporaryDirectory() as temporary:
            executed = []
            def middleware(agent, *, function_name, function_args, execute, **kwargs):
                return execute(function_args)
            def dispatch(name, arguments, **kwargs):
                executed.append(name)
                return "read-only result"
            executor = SimpleNamespace(_run_agent_tool_execution_middleware=middleware)
            registry = SimpleNamespace(dispatch=dispatch)
            install_guard(executor, registry, SmokeGuard(Path(temporary) / "guard.jsonl"))
            for name in ("image_generate", "mcp_meta_ads_activate", "terminal", "execute_code", "delegate_task", "tool_call"):
                result = executor._run_agent_tool_execution_middleware(
                    None, function_name=name, function_args={"command": "meta ads campaign update 123 --status ACTIVE"},
                    execute=lambda args: executed.append("unsafe handler"),
                )
                self.assertIn("not executed", result)
                registry.dispatch(name, {})
            self.assertEqual(executed, [])
            self.assertEqual(registry.dispatch("skill_view", {"name": "providers"}), "read-only result")
            self.assertEqual(executed, ["skill_view"])

    def test_recording_failure_cannot_execute_a_tool(self):
        with tempfile.TemporaryDirectory() as temporary:
            executed = []
            guard = SmokeGuard(Path(temporary) / "missing-directory/guard.jsonl")
            with self.assertRaises(OSError):
                guard.dispatch("terminal", {}, lambda args: executed.append("unsafe"))
            self.assertEqual(executed, [])

    def test_invalid_exports_fail_the_actual_scenario(self):
        function = SCRIPT.split("run_scenario() {", 1)[1].split('\necho "== Stage 3:', 1)[0]
        for evidence in ("not json", "", '{"messages": []}', '{"messages": "invalid"}'):
            with self.subTest(evidence=evidence), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                hermes = directory / "hermes"
                hermes.write_text("#!/usr/bin/env python3\nimport os,sys,pathlib\npathlib.Path(sys.argv[-2]).write_text(os.environ['FAKE_EVIDENCE'])\n")
                hermes.chmod(0o755)
                chat = directory / "chat"
                chat.write_text("#!/usr/bin/env python3\nprint('SMOKE_GUARD_READY')\nprint('API call #1:')\nprint('Session: fake')\n")
                chat.chmod(0o755)
                harness = '''set -uo pipefail
stage_failed=0
pass() { echo "PASS $*"; }
fail() { stage_failed=1; echo "FAIL $*"; }
stop_child() { kill "$1" 2>/dev/null || true; wait "$1" 2>/dev/null || true; }
run_scenario() {''' + function + '''
run_scenario meta-launch "" "" "test"
exit "$stage_failed"
'''
                env = {**os.environ, "PATH": str(directory) + os.pathsep + os.environ["PATH"],
                       "FAKE_EVIDENCE": evidence, "ROOT": str(ROOT), "WORK": str(directory),
                       "HERMES_PYTHON": str(chat), "hermes_install": str(directory),
                       "PROFILE": "ar-smoke-fake", "PROVIDER": "fake", "MODEL": "fake", "MAX_TURNS": "1", "CHAT_TIMEOUT": "5"}
                result = subprocess.run(["bash", "-c", harness], env=env, text=True, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("invalid session evidence", result.stdout)
                self.assertNotIn("PASS meta-launch", result.stdout)

    def test_valid_export_uses_complete_tool_arguments(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            arguments = {"file_path": "SKILL.md", "name": "providers"}
            (directory / "session.jsonl").write_text(json.dumps({"messages": [
                {"role": "assistant", "tool_calls": [{"function": {"name": "skill_view", "arguments": json.dumps(arguments)}}]},
                {"role": "assistant", "content": "A complete answer."},
            ]}))
            extract(directory)
            self.assertEqual((directory / "skills.txt").read_text(), "providers\n")
            self.assertIn("SKILL.md", (directory / "calls.txt").read_text())

    def test_interrupted_partial_install_is_deleted(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            hermes = directory / "hermes"
            hermes.write_text('''#!/usr/bin/env python3
import os,sys,pathlib,signal,time
store=pathlib.Path(os.environ['FAKE_PROFILES'])
if sys.argv[1:3] == ['profile','list']:
    print('\\n'.join(p.name for p in store.iterdir()))
elif sys.argv[1:3] == ['profile','install']:
    name=sys.argv[sys.argv.index('--name')+1]
    (store/name).mkdir()
    os.kill(os.getppid(),signal.SIGTERM)
    time.sleep(30)
elif sys.argv[1:3] == ['profile','delete']:
    (store/sys.argv[-1]).rmdir()
''')
            hermes.chmod(0o755)
            profiles = directory / "profiles"
            profiles.mkdir()
            initialization = SCRIPT.split("# ---------------------------------------------------------------- stage 1", 1)[0]
            stage = SCRIPT.split("# ---------------------------------------------------------------- stage 2", 1)[1].split("# Keep the throwaway profile free-only", 1)[0]
            env = {**os.environ, "PATH": str(directory) + os.pathsep + os.environ["PATH"], "FAKE_PROFILES": str(profiles), "TMPDIR": str(directory)}
            result = subprocess.run(["bash", "-c", initialization + stage], env=env, text=True, capture_output=True, timeout=12)
            self.assertEqual(result.returncode, 130, result.stdout + result.stderr)
            self.assertEqual(list(profiles.iterdir()), [], result.stdout + result.stderr)
            self.assertIn("deleted throwaway profile", result.stdout)

    def test_pin_lookup_reads_an_updated_table(self):
        assignment = SCRIPT.split('pika_pin="$(awk', 1)[1].split('\nif ! printf', 1)[0]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            providers = root / "skills/providers"
            providers.mkdir(parents=True)
            updated = "a" * 40
            (providers / "SKILL.md").write_text("<!-- provider-pins:begin -->\n| pika | org/repo | path | " + updated + " | hermes | MIT | 2026-10-08 |\n<!-- provider-pins:end -->\n")
            result = subprocess.run(["bash", "-c", 'pika_pin="$(awk' + assignment + '\nprintf "%s" "$pika_pin"'], env={**os.environ, "ROOT": str(root)}, text=True, capture_output=True, check=True)
            self.assertEqual(result.stdout, updated)


if __name__ == "__main__":
    unittest.main()
