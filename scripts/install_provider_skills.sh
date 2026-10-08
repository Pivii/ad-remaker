#!/usr/bin/env bash
# Install official vendor Skills into the Ad Remaker Hermes profile at their pinned commits.
# The pin table in skills/providers/SKILL.md is the only source of pins; this script never edits it.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PINS_FILE="${ROOT}/skills/providers/SKILL.md"
PROFILE="ad-remaker"
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: install_provider_skills.sh [--dry-run] [--profile NAME] VENDOR...

Install the official Skill of each VENDOR at the commit pinned in
skills/providers/SKILL.md, then run `hermes skills audit`.
Install only the vendors you pay for; free mode needs no vendor Skill.

Options:
  --dry-run       Validate the vendors and print the hermes commands without running them.
  --profile NAME  Hermes profile to install into (default: ad-remaker).
  -h, --help      Show this help.

Exit status: 0 success, 1 install or audit failure, 2 usage error or unknown vendor,
3 vendor whose Skill is not installable (Install is not `hermes` in the pin table).
Nothing is installed when the status is 2 or 3.
EOF
}

# Print one "vendor repository path ref install" line per row of the pin table.
pin_rows() {
  awk -F'|' '
    /<!-- provider-pins:begin -->/ { inside = 1; next }
    /<!-- provider-pins:end -->/ { inside = 0 }
    inside && /^\|/ {
      for (i = 2; i <= 6; i++) gsub(/^[ \t]+|[ \t]+$/, "", $i)
      if ($2 == "Vendor" || $2 ~ /^-+$/) next
      print $2, $3, $4, $5, $6
    }
  ' "$PINS_FILE"
}

vendors=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --profile)
      [ "$#" -ge 2 ] && [ -n "$2" ] || { echo "error: --profile needs a name" >&2; exit 2; }
      PROFILE="$2"
      shift
      ;;
    -h|--help) usage; exit 0 ;;
    --) shift; vendors+=("$@"); break ;;
    -*) echo "error: unknown option: $1" >&2; usage >&2; exit 2 ;;
    *) vendors+=("$1") ;;
  esac
  shift
done

if [ "${#vendors[@]}" -eq 0 ]; then
  echo "error: no vendor given. Free mode needs no vendor Skill." >&2
  usage >&2
  exit 2
fi

[ -f "$PINS_FILE" ] || { echo "error: pin table not found: $PINS_FILE" >&2; exit 2; }
rows="$(pin_rows)"
[ -n "$rows" ] || { echo "error: no rows in the pin table of $PINS_FILE" >&2; exit 2; }
known="$(printf '%s\n' "$rows" | awk '{ print $1 }' | tr '\n' ' ')"

# Validate every requested vendor before installing anything.
status=0
urls=()
names=()
seen=" "
for vendor in "${vendors[@]}"; do
  case "$seen" in *" $vendor "*) continue ;; esac
  seen="${seen}${vendor} "
  row="$(printf '%s\n' "$rows" | awk -v v="$vendor" '$1 == v')"
  if [ -z "$row" ]; then
    echo "error: unknown vendor '$vendor'. Known vendors: $known" >&2
    status=2
    continue
  fi
  read -r _ repo path ref install <<<"$row"
  if [ "$install" != "hermes" ]; then
    echo "error: vendor '$vendor' is not installable with Hermes. See its entry in skills/providers/SKILL.md." >&2
    [ "$status" -eq 2 ] || status=3
    continue
  fi
  if [ "$repo" = "none" ] || [ "$path" = "none" ] || ! printf '%s' "$ref" | grep -Eq '^[0-9a-f]{40}$'; then
    echo "error: vendor '$vendor' has no valid pin (ref: $ref). See skills/providers/SKILL.md." >&2
    [ "$status" -eq 2 ] || status=3
    continue
  fi
  urls+=("https://raw.githubusercontent.com/${repo}/${ref}/${path}/SKILL.md")
  names+=("${path##*/}")
done
[ "$status" -eq 0 ] || exit "$status"

if [ "$DRY_RUN" -eq 1 ]; then
  for url in "${urls[@]}"; do
    echo "hermes -p $PROFILE skills install $url --yes"
  done
  echo "hermes -p $PROFILE skills audit"
  exit 0
fi

command -v hermes >/dev/null 2>&1 || { echo "error: hermes is not on PATH" >&2; exit 1; }

# hermes v0.20.2 can report an install failure without a non-zero exit status,
# so each install is confirmed against `hermes skills list` as well. The list is
# captured and searched without a pipe: piping into `grep -q` lets grep exit early,
# the writer then gets SIGPIPE, and pipefail turns a found Skill into a failure.
failed=0
for i in "${!urls[@]}"; do
  echo "Installing ${names[$i]} from ${urls[$i]}"
  if ! hermes -p "$PROFILE" skills install "${urls[$i]}" --yes; then
    echo "error: hermes skills install failed for ${names[$i]}" >&2
    failed=1
  elif ! listed="$(hermes -p "$PROFILE" skills list)"; then
    echo "error: hermes skills list failed after installing ${names[$i]}" >&2
    failed=1
  elif ! grep -qw -- "${names[$i]}" <<<"$listed"; then
    echo "error: ${names[$i]} is not listed after install; check the output above" >&2
    failed=1
  fi
done

echo "Auditing installed hub Skills"
hermes -p "$PROFILE" skills audit || failed=1
exit "$failed"
