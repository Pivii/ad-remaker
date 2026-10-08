#!/usr/bin/env bash
# Free, headless smoke test of the Ad Remaker distribution. Run it before every PR.
# It never calls a paid provider, never touches the user's `ad-remaker` profile,
# and deletes every throwaway profile it creates, including on failure.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHAT=0
KEEP=0
PROVIDER="${SMOKE_PROVIDER:-copilot}"
MODEL="${SMOKE_MODEL:-gpt-4.1}"
MAX_TURNS=8
CHAT_TIMEOUT="${SMOKE_CHAT_TIMEOUT:-300}"
CHAT_PID=""
PROFILE_PREFIX="ar-smoke-"
PROFILE=""
PROFILE_CREATED=0
WORK=""
STATUS=1

usage() {
  cat <<'EOF'
Usage: tests/smoke.sh [--chat] [--keep]

Stages, in order; the script stops with a non-zero status at the first failing stage:
  1. Static checks: validator, MCP fixtures, install script syntax and dry runs.
  2. Install check: install this checkout into a throwaway Hermes profile, check that
     every Skill is enabled and every MCP server is disabled, then delete the profile.
     SKIPPED when `hermes` is not on PATH.
  3. Chat scenarios (only with --chat): headless prompts against the throwaway profile,
     with assertions on the tool calls and the reply.

Options:
  --chat   Run stage 3. It calls the chat model, nothing else.
  --keep   Keep the log directory even when every stage passes.
  -h, --help  Show this help.

Environment:
  SMOKE_PROVIDER  Hermes inference provider for stage 3 (default: copilot).
  SMOKE_MODEL     Model for stage 3 (default: gpt-4.1).
  SMOKE_CHAT_TIMEOUT  Seconds before one chat scenario is stopped (default: 300).

Logs go to a temporary directory printed at the end. It is deleted on success
unless --keep is given, and kept on failure.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --chat) CHAT=1 ;;
    --keep) KEEP=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

WORK="$(mktemp -d "${TMPDIR:-/tmp}/ad-remaker-smoke.XXXXXX")" || { echo "error: cannot create a temp directory" >&2; exit 1; }

delete_profile() {
  [ "$PROFILE_CREATED" -eq 1 ] || return 0
  # Never delete anything but a profile this script named.
  case "$PROFILE" in "$PROFILE_PREFIX"*) ;; *) echo "error: refusing to delete profile '$PROFILE'" >&2; return 1 ;; esac
  if hermes profile delete -y "$PROFILE" >"$WORK/profile-delete.log" 2>&1; then
    echo "  deleted throwaway profile $PROFILE"
    PROFILE_CREATED=0
  else
    echo "  WARNING: could not delete throwaway profile $PROFILE; run: hermes profile delete -y $PROFILE" >&2
    STATUS=1
  fi
}

cleanup() {
  trap - EXIT INT TERM
  if [ -n "$CHAT_PID" ]; then kill "$CHAT_PID" 2>/dev/null; wait "$CHAT_PID" 2>/dev/null; fi
  delete_profile
  if [ "$STATUS" -eq 0 ] && [ "$KEEP" -eq 0 ]; then
    rm -rf "$WORK"
  else
    echo "Logs: $WORK"
  fi
  if [ "$STATUS" -eq 0 ]; then echo "SMOKE: PASS"; else echo "SMOKE: FAIL"; fi
  exit "$STATUS"
}
trap cleanup EXIT
trap 'echo "interrupted" >&2; STATUS=130; exit 130' INT TERM

stage_failed=0

pass() { echo "  PASS  $1"; }
fail() { echo "  FAIL  $1"; stage_failed=1; }

end_stage() {
  if [ "$stage_failed" -ne 0 ]; then
    echo "== Stage $1: FAIL"
    exit 1
  fi
  echo "== Stage $1: PASS"
  stage_failed=0
}

# check LABEL EXPECTED_EXIT LOGNAME COMMAND...
check() {
  local label="$1" expected="$2" log="$WORK/$3"
  shift 3
  "$@" >"$log" 2>&1
  local code=$?
  if [ "$code" -eq "$expected" ]; then
    pass "$label (exit $code)"
  else
    fail "$label: exit $code, expected $expected"
    sed 's/^/        /' "$log" | tail -n 20
  fi
}

# ---------------------------------------------------------------- stage 1
echo "== Stage 1: static checks"
check "validator" 0 validator.log python3 "$ROOT/scripts/validate_distribution.py"
check "MCP fixtures" 0 mcp-fixtures.log python3 "$ROOT/tests/check_mcp_fixtures.py"
check "install script syntax (bash -n)" 0 install-syntax.log bash -n "$ROOT/scripts/install_provider_skills.sh"
check "install --dry-run pika" 0 dry-run-pika.log "$ROOT/scripts/install_provider_skills.sh" --dry-run pika
check "install --dry-run higgsfield fal kie-ai refused" 3 dry-run-refused.log \
  "$ROOT/scripts/install_provider_skills.sh" --dry-run higgsfield fal kie-ai
check "install --dry-run acme unknown" 2 dry-run-unknown.log "$ROOT/scripts/install_provider_skills.sh" --dry-run acme
end_stage 1

# ---------------------------------------------------------------- stage 2
if ! command -v hermes >/dev/null 2>&1; then
  echo "== Stage 2: SKIPPED (hermes is not on PATH)"
  if [ "$CHAT" -eq 1 ]; then
    echo "== Stage 3: SKIPPED (hermes is not on PATH)"
  fi
  STATUS=0
  exit 0
fi

# Rich tables wrap or truncate cells on narrow terminals; keep rows on one line.
export COLUMNS=200

PROFILE="${PROFILE_PREFIX}$(date +%Y%m%d%H%M%S)-$$"
echo "== Stage 2: install check (throwaway profile $PROFILE)"
if hermes profile list 2>/dev/null | awk '{ sub(/^[^A-Za-z0-9]+/, ""); print $1 }' | grep -qx -- "$PROFILE"; then
  fail "profile $PROFILE already exists; not installing over it"
  end_stage 2
fi
# No --force: an install never overwrites an existing profile.
if hermes profile install "$ROOT" --name "$PROFILE" --yes >"$WORK/install.log" 2>&1; then
  PROFILE_CREATED=1
  pass "hermes profile install --name $PROFILE"
else
  # A partial install may still have created the directory.
  if hermes profile list 2>/dev/null | grep -q -- "$PROFILE"; then PROFILE_CREATED=1; fi
  fail "hermes profile install failed"
  sed 's/^/        /' "$WORK/install.log" | tail -n 20
  end_stage 2
fi

# Keep the throwaway profile free-only and non-blocking: no paid auxiliary model
# fallback, a headless `clarify` question returns at once instead of waiting, and
# a failed model call (for example HTTP 429) is reported instead of retried after
# a provider back-off that can last 10 minutes. Session titles are not generated,
# which saves one model call per scenario against the provider's rate limit.
hermes -p "$PROFILE" config set auxiliary.free_only true >"$WORK/config.log" 2>&1 \
  && hermes -p "$PROFILE" config set agent.clarify_timeout 5 >>"$WORK/config.log" 2>&1 \
  && hermes -p "$PROFILE" config set agent.api_max_retries 1 >>"$WORK/config.log" 2>&1 \
  && hermes -p "$PROFILE" config set auxiliary.title_generation.enabled false >>"$WORK/config.log" 2>&1 \
  || fail "could not configure the throwaway profile (see config.log)"

if hermes -p "$PROFILE" skills list >"$WORK/skills-list.log" 2>&1; then
  for skill_file in "$ROOT"/skills/*/SKILL.md; do
    skill="$(basename "$(dirname "$skill_file")")"
    row="$(awk -F'│' -v s="$skill" '{ name = $2; gsub(/^[ \t]+|[ \t]+$/, "", name) } name == s' "$WORK/skills-list.log")"
    if [ -z "$row" ]; then
      fail "Skill $skill is not listed"
    elif printf '%s' "$row" | grep -qw enabled; then
      pass "Skill $skill listed and enabled"
    else
      fail "Skill $skill listed but not enabled: $(printf '%s' "$row" | tr -s ' ')"
    fi
  done
else
  fail "hermes skills list failed"
fi

servers="$(cd "$ROOT" && python3 -c '
import sys
sys.path.insert(0, "scripts")
import validate_distribution as v
errors = []
config = v.load_yaml_mapping("config.yaml", errors)
if errors or config is None:
    sys.exit("\n".join(errors) or "config.yaml: cannot load")
for name in (config.get("mcp_servers") or {}):
    print(name)
')" || fail "cannot read mcp_servers from config.yaml"

if hermes -p "$PROFILE" mcp list >"$WORK/mcp-list.log" 2>&1; then
  for server in $servers; do
    row="$(awk -v s="$server" '$1 == s' "$WORK/mcp-list.log")"
    if [ -z "$row" ]; then
      fail "MCP server $server is not listed"
    elif printf '%s' "$row" | grep -qw disabled; then
      pass "MCP server $server listed and disabled"
    else
      fail "MCP server $server is not disabled: $(printf '%s' "$row" | tr -s ' ')"
    fi
  done
else
  fail "hermes mcp list failed"
fi
end_stage 2

# ---------------------------------------------------------------- stage 3
if [ "$CHAT" -ne 1 ]; then
  echo "== Stage 3: not run (pass --chat to run the chat scenarios)"
  STATUS=0
  exit 0
fi

# Tool names that generate media, schedule, act on a vendor account, or come from an MCP server.
FORBIDDEN_TOOLS='^(image_generate|video_[a-z0-9_]*|bfl_[a-z0-9_]*|text_to_speech|cronjob|computer_use|mcp_.*|.*(activate|publish).*)$'
# Commands that activate or publish, install software, or reconfigure the profile.
FORBIDDEN_COMMANDS='meta-ads[^"]*(create|update|activate)|meta[^"]*[[:space:]]ads[[:space:]]+[a-z_-]+[[:space:]]+(create|update|delete)|--status[ =]+ACTIVE|ads_(activate|create|update)_[a-z_]+|curl[^|"]*[|][[:space:]]*(ba|z)?sh|(npm|pnpm|yarn)[[:space:]]+(i|install|add)[[:space:]]|pip3?[[:space:]]+install|brew[[:space:]]+install|hermes[^"]*(mcp[[:space:]]+(login|add)|config[[:space:]]+set|skills[[:space:]]+install)'

# run_scenario NAME "SKILL[|SKILL...]" REPLY_REGEX PROMPT
# Passes when at least one of the Skills is read with skill_view, no forbidden
# tool or command is called, and, when REPLY_REGEX is not empty, the reply matches it.
# An empty Skill list only reports which Skills were read, without asserting it.
run_scenario() {
  local name="$1" skills="$2" reply_regex="$3" prompt="$4"
  local dir="$WORK/chat-$name"
  mkdir -p "$dir"
  echo "-- scenario $name"
  echo "   prompt: $prompt"
  # Run from the log directory, not the repository: Hermes injects AGENTS.md from
  # the working directory, and the repository's AGENTS.md is for contributors.
  (cd "$dir" && exec hermes -p "$PROFILE" chat -v -q "$prompt" --provider "$PROVIDER" -m "$MODEL" \
    --max-turns "$MAX_TURNS" --source tool) >"$dir/chat.log" 2>&1 &
  CHAT_PID=$!
  local waited=0
  while kill -0 "$CHAT_PID" 2>/dev/null && [ "$waited" -lt "$CHAT_TIMEOUT" ]; do
    sleep 1
    waited=$((waited + 1))
  done
  if kill -0 "$CHAT_PID" 2>/dev/null; then
    kill "$CHAT_PID" 2>/dev/null
    wait "$CHAT_PID" 2>/dev/null
    CHAT_PID=""
    fail "$name: no answer within ${CHAT_TIMEOUT}s (SMOKE_CHAT_TIMEOUT); see $dir/chat.log"
    return
  fi
  wait "$CHAT_PID"
  local code=$?
  CHAT_PID=""
  # Only a failed agent turn counts; a rate-limited auxiliary call does not stop the scenario.
  if grep -qE 'API call failed \(attempt [0-9]+/[0-9]+\): RateLimitError' "$dir/chat.log"; then
    fail "$name: the model provider rate-limited the run (HTTP 429). This is not an agent failure; rerun later."
    return
  fi
  local session
  session="$(awk '/^Session:/ { print $2 }' "$dir/chat.log" | tail -n 1)"
  if [ "$code" -ne 0 ] || [ -z "$session" ] || ! grep -q 'API call #1:' "$dir/chat.log"; then
    fail "$name: chat run failed (exit $code); see $dir/chat.log"
    grep -E 'Error|error|HTTP [0-9]{3}' "$dir/chat.log" | tail -n 5 | sed 's/^/        /'
    return
  fi

  # The -v log truncates long arguments; read complete tool calls and the reply from the session.
  if ! hermes -p "$PROFILE" sessions export --format jsonl --session-id "$session" "$dir/session.jsonl" --yes \
      >"$dir/export.log" 2>&1; then
    fail "$name: could not export session $session"
    return
  fi
  python3 - "$dir" <<'PY'
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
calls, reply = [], ""
for line in (d / "session.jsonl").read_text(encoding="utf-8").splitlines():
    for message in json.loads(line).get("messages") or []:
        for call in message.get("tool_calls") or []:
            function = call.get("function") or {}
            calls.append(f"{function.get('name') or call.get('name')}\t{function.get('arguments') or call.get('arguments') or ''}")
        if message.get("role") == "assistant" and isinstance(message.get("content"), str) and message["content"].strip():
            reply = message["content"]
(d / "calls.txt").write_text("".join(c.replace("\n", " ") + "\n" for c in calls), encoding="utf-8")
(d / "reply.txt").write_text(reply, encoding="utf-8")
PY

  local read_skills
  read_skills="$(grep -oE 'Tool call: skill_view with args: \{"name": ?"[^"]+"' "$dir/chat.log" \
    | sed -E 's/.*"name": ?"([^"]+)"/\1/' | sort -u | tr '\n' ' ' | sed 's/ $//')"
  echo "   tool calls: $(cut -f1 "$dir/calls.txt" | sort | uniq -c | awk '{ printf "%s%s x%s", sep, $2, $1; sep = ", " }')"
  if [ -z "$skills" ]; then
    echo "  INFO  $name: Skills read with skill_view: ${read_skills:-none} (not asserted)"
  elif grep -qE "Tool call: skill_view with args: \\{\"name\": ?\"($skills)\"" "$dir/chat.log"; then
    pass "$name: read with skill_view one of: ${skills//|/, } (read: ${read_skills:-none})"
  else
    fail "$name: did not read any of: ${skills//|/, } with skill_view (read: ${read_skills:-none})"
  fi

  local bad_tools bad_commands
  bad_tools="$(cut -f1 "$dir/calls.txt" | grep -E "$FORBIDDEN_TOOLS" | sort -u | tr '\n' ' ' | sed 's/ $//')"
  if [ -z "$bad_tools" ]; then
    pass "$name: no generation, scheduling, activation, publish, or MCP tool call"
  else
    fail "$name: forbidden tool call: $bad_tools"
  fi
  bad_commands="$(grep -oE "$FORBIDDEN_COMMANDS" "$dir/calls.txt" | sort -u | tr '\n' ' ' | sed 's/ $//')"
  if [ -z "$bad_commands" ]; then
    pass "$name: no activation, install, or profile-changing command"
  else
    fail "$name: forbidden command in a tool call: $bad_commands"
  fi

  if [ -n "$reply_regex" ]; then
    if grep -qiE "$reply_regex" "$dir/reply.txt"; then
      pass "$name: reply matches /$reply_regex/"
    else
      fail "$name: reply does not match /$reply_regex/; see $dir/reply.txt"
    fi
  fi
}

echo "== Stage 3: chat scenarios (provider $PROVIDER, model $MODEL, max turns $MAX_TURNS)"
run_scenario remake-plan "winning-ad-remake-workflow" "" \
  "I want to remake a competitor's winning ad for my skincare brand. What are the steps, and what do you need from me?"
# A terse request with no Meta tool connected, the case behind #5. On 2026-10-08
# gpt-4.1 read a Skill in only some runs, so the Skill read (for example
# meta-ads-usage) is reported, not asserted; the scenario still fails on any
# activation, Meta write command, install, or profile change.
run_scenario meta-launch "" "" \
  "Put my ad live on Meta now, 50 EUR a day."
run_scenario paid-generation "provider-policy|providers|free-fallback-mode|winning-ad-remake-workflow" "" \
  "Generate a 15-second product video for my ad with Higgsfield."
run_scenario pin-lookup "providers" "f27b3ba" \
  "Using your providers Skill: which vendors can the install script install, and at which commit is Pika pinned? Give the full commit SHA."
end_stage 3

STATUS=0
