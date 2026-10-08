#!/usr/bin/env python3
"""Extract complete smoke-test evidence, rejecting empty or malformed exports."""

import json
import sys
from pathlib import Path


def extract(directory):
    directory = Path(directory)
    calls, skills, reply = [], set(), ""
    records = (directory / "session.jsonl").read_text(encoding="utf-8").splitlines()
    if not records:
        raise ValueError("session export is empty")
    for line in records:
        record = json.loads(line)
        if not isinstance(record, dict) or not isinstance(record.get("messages"), list):
            raise ValueError("session export must contain a messages list")
        for message in record["messages"]:
            if not isinstance(message, dict):
                raise ValueError("invalid session message")
            for call in message.get("tool_calls") or []:
                function = call.get("function") or call
                name = function.get("name")
                arguments = function.get("arguments", {})
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
                if not isinstance(name, str) or not isinstance(arguments, dict):
                    raise ValueError("invalid tool-call evidence")
                calls.append(name + "\t" + json.dumps(arguments))
                if name == "skill_view" and isinstance(arguments.get("name"), str):
                    skills.add(arguments["name"])
            if message.get("role") == "assistant" and isinstance(message.get("content"), str) and message["content"].strip():
                reply = message["content"]
    if not reply:
        raise ValueError("session export has no assistant response")
    (directory / "calls.txt").write_text("".join(call + "\n" for call in calls), encoding="utf-8")
    (directory / "skills.txt").write_text("".join(skill + "\n" for skill in sorted(skills)), encoding="utf-8")
    (directory / "reply.txt").write_text(reply, encoding="utf-8")


if __name__ == "__main__":
    try:
        extract(sys.argv[1])
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError) as error:
        sys.exit(f"invalid smoke session evidence: {error}")
