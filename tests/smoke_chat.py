#!/usr/bin/env python3
"""Run Hermes with test-only substitutes before any mutating tool executes."""

import json
import sys
import threading
from pathlib import Path


READ_ONLY_TOOLS = frozenset({"skills_list", "skill_view", "clarify"})


class SmokeGuard:
    def __init__(self, log_path):
        self.log_path = Path(log_path)
        self.lock = threading.Lock()

    def dispatch(self, name, arguments, execute):
        allowed = name in READ_ONLY_TOOLS
        # A failed write raises before dispatch. Unlike a fail-open observer hook,
        # this wrapper cannot accidentally execute a tool when recording fails.
        with self.lock, self.log_path.open("a", encoding="utf-8") as log:
            log.write(json.dumps({"name": name, "arguments": arguments, "stubbed": not allowed}) + "\n")
        if allowed:
            return execute(arguments)
        return json.dumps({"error": "Smoke test substitute: this tool was not executed. No vendor CLI or account is connected in this test. Read the Skills and explain the next steps; do not retry the tool."})


def install_guard(executor, registry, guard):
    middleware = executor._run_agent_tool_execution_middleware
    dispatch = registry.dispatch

    def guarded_middleware(agent, *, function_name, function_args, execute, **kwargs):
        return middleware(
            agent,
            function_name=function_name,
            function_args=function_args,
            execute=lambda args: guard.dispatch(function_name, args, execute),
            **kwargs,
        )

    def guarded_dispatch(name, arguments, **kwargs):
        return guard.dispatch(name, arguments, lambda args: dispatch(name, args, **kwargs))

    executor._run_agent_tool_execution_middleware = guarded_middleware
    registry.dispatch = guarded_dispatch


def main():
    install_root, log_directory, *hermes_args = sys.argv[1:]
    sys.path.insert(0, install_root)
    sys.argv = ["hermes", *hermes_args]
    # Hermes applies -p during this import, before any other Hermes module is
    # imported. All following module state belongs to the throwaway profile.
    from hermes_cli.main import main as hermes_main
    from agent import tool_executor
    from tools.registry import registry

    guard = SmokeGuard(Path(log_directory) / "guard.jsonl")
    install_guard(tool_executor, registry, guard)
    print("SMOKE_GUARD_READY", flush=True)
    hermes_main()


if __name__ == "__main__":
    main()
