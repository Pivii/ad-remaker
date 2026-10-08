#!/usr/bin/env python3
"""Validate the Ad Remaker Hermes profile distribution."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # PyYAML is optional.
    yaml = None

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "SOUL.md",
    "config.yaml",
    "cron/jobs.json",
    "distribution.yaml",
    "docs/ad-remaker-complete-operating-report.md",
    "docs/architecture.md",
    "docs/decisions/ADR-001-profile-distribution.md",
    "docs/decisions/ADR-002-provider-skill-layers.md",
    "docs/decisions/README.md",
    "docs/provenance/README.md",
    "docs/provenance/brandsearch.md",
    "docs/provenance/fal.md",
    "docs/provenance/higgsfield.md",
    "docs/provenance/kie-ai.md",
    "docs/provenance/pika.md",
    "docs/provenance/trendtrack.md",
    "docs/service-matrix.md",
    "mcp.json",
    "scripts/install_provider_skills.sh",
    "scripts/validate_distribution.py",
    "skills/README.md",
    "skills/provider-policy/SKILL.md",
    "skills/providers/SKILL.md",
    "tests/README.md",
    "tests/fixtures/README.md",
)

FORBIDDEN_REPORT = "docs/ad-remaker-fonctionnement-complet.md"

# Removed by ADR-002; their source texts live in docs/provenance/.
REMOVED_SKILLS = (
    "brandsearch-usage",
    "fal-usage",
    "higgsfield-usage",
    "kie-ai-usage",
    "pika-usage",
    "trendtrack-usage",
)

PROVIDER_PINS_FILE = "skills/providers/SKILL.md"
PROVIDER_PINS_BEGIN = "<!-- provider-pins:begin -->"
PROVIDER_PINS_END = "<!-- provider-pins:end -->"
PROVIDER_PINS_HEADER = ["Vendor", "Repository", "Skill path", "Pinned ref", "Install", "License", "Checked"]
PROVIDER_INSTALL_VALUES = {"hermes", "no"}
PROVIDER_VENDORS = {"brandsearch", "fal", "higgsfield", "kie-ai", "meta-ads", "pika", "trendtrack"}
FORBIDDEN_FILE_NAMES = {
    ".env",
    "auth.json",
    "credentials.json",
    "secrets.json",
    "state.db",
}
FORBIDDEN_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".log"}
FORBIDDEN_ROOT_DIRS = {
    ".worktrees",
    "audio_cache",
    "backups",
    "browser-profile",
    "browser_profiles",
    "browser_screenshots",
    "cache",
    "checkpoints",
    "document_cache",
    "hermes-agent",
    "home",
    "image_cache",
    "local",
    "logs",
    "mcp-tokens",
    "memories",
    "memory",
    "plans",
    "platforms",
    "profiles",
    "proxy",
    "sandboxes",
    "sessions",
    "state",
    "vault",
    "workspace",
}
IGNORED_DIRS = {".git", ".pytest_cache", "__pycache__"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(relative_path: str, errors: list[str]) -> Any:
    path = ROOT / relative_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(errors, f"{relative_path}: invalid JSON: {exc}")
        return None


def fallback_yaml_mapping(text: str, relative_path: str, errors: list[str]) -> dict[str, Any] | None:
    """Parse the top-level mapping needed for dependency-free shape checks."""
    result: dict[str, Any] = {}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[0].isspace():
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", raw_line)
        if not match:
            fail(errors, f"{relative_path}:{line_number}: unsupported or invalid top-level YAML")
            return None
        key, raw_value = match.groups()
        raw_value = (raw_value or "").strip()
        if not raw_value:
            value: Any = {}
        elif raw_value == "[]":
            value = []
        elif raw_value == "{}":
            value = {}
        elif raw_value.lower() in {"true", "false"}:
            value = raw_value.lower() == "true"
        else:
            value = raw_value.strip("\"'")
        result[key] = value
    return result


def load_yaml_mapping(relative_path: str, errors: list[str]) -> dict[str, Any] | None:
    path = ROOT / relative_path
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(errors, f"{relative_path}: cannot read YAML: {exc}")
        return None

    if yaml is None:
        data = fallback_yaml_mapping(text, relative_path, errors)
    else:
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            fail(errors, f"{relative_path}: invalid YAML: {exc}")
            return None

    if not isinstance(data, dict):
        fail(errors, f"{relative_path}: top-level YAML value must be a mapping")
        return None
    return data


def validate_required_files(errors: list[str]) -> None:
    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path
        if not path.is_file():
            fail(errors, f"missing required file: {relative_path}")
        elif path.stat().st_size == 0:
            fail(errors, f"required file is empty: {relative_path}")

    if (ROOT / FORBIDDEN_REPORT).exists():
        fail(errors, f"obsolete French-facing report path must not exist: {FORBIDDEN_REPORT}")


def validate_yaml_files(errors: list[str]) -> None:
    manifest = load_yaml_mapping("distribution.yaml", errors)
    if manifest is not None:
        required = {
            "name": str,
            "version": str,
            "description": str,
            "hermes_requires": str,
            "author": str,
            "license": str,
            "env_requires": list,
        }
        for key, expected_type in required.items():
            if key not in manifest:
                fail(errors, f"distribution.yaml: missing required key {key!r}")
            elif not isinstance(manifest[key], expected_type):
                fail(errors, f"distribution.yaml: {key!r} must be {expected_type.__name__}")
        if manifest.get("name") != "ad-remaker":
            fail(errors, "distribution.yaml: 'name' must be 'ad-remaker'")

    config = load_yaml_mapping("config.yaml", errors)
    if config is not None:
        for key in ("agent", "approvals", "security"):
            if key not in config:
                fail(errors, f"config.yaml: missing required top-level mapping {key!r}")
            elif not isinstance(config[key], dict):
                fail(errors, f"config.yaml: {key!r} must be a mapping")


def validate_json_files(errors: list[str]) -> None:
    mcp = load_json("mcp.json", errors)
    if mcp is not None:
        if not isinstance(mcp, dict):
            fail(errors, "mcp.json: top-level value must be an object")
        elif not isinstance(mcp.get("servers"), dict):
            fail(errors, "mcp.json: 'servers' must be an object")

    jobs = load_json("cron/jobs.json", errors)
    if jobs is not None:
        if not isinstance(jobs, dict):
            fail(errors, "cron/jobs.json: top-level value must be an object")
        elif not isinstance(jobs.get("jobs"), list):
            fail(errors, "cron/jobs.json: 'jobs' must be an array")


def parse_skill_frontmatter(path: Path, errors: list[str]) -> dict[str, Any] | None:
    relative_path = path.relative_to(ROOT).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(errors, f"{relative_path}: cannot read Skill: {exc}")
        return None

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(errors, f"{relative_path}: Skill must begin with YAML frontmatter")
        return None
    try:
        closing_index = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        fail(errors, f"{relative_path}: Skill frontmatter has no closing delimiter")
        return None

    frontmatter_text = "\n".join(lines[1:closing_index])
    if yaml is not None:
        try:
            data = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as exc:
            fail(errors, f"{relative_path}: invalid Skill frontmatter: {exc}")
            return None
        if not isinstance(data, dict):
            fail(errors, f"{relative_path}: Skill frontmatter must be a mapping")
            return None
        return data

    data: dict[str, Any] = {}
    for key in ("name", "description"):
        match = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", frontmatter_text)
        if match:
            data[key] = match.group(1).strip("\"'")
    return data


def validate_skills(errors: list[str]) -> None:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        fail(errors, "missing required directory: skills")
        return

    skill_directories = sorted(path for path in skills_dir.iterdir() if path.is_dir() and not path.name.startswith("."))
    if not skill_directories:
        fail(errors, "skills: at least one Skill directory is required")
        return

    for skill_dir in skill_directories:
        skill_file = skill_dir / "SKILL.md"
        relative_skill = skill_file.relative_to(ROOT).as_posix()
        if not skill_file.is_file():
            fail(errors, f"missing Skill entry point: {relative_skill}")
            continue
        metadata = parse_skill_frontmatter(skill_file, errors)
        if metadata is None:
            continue
        for key in ("name", "description"):
            value = metadata.get(key)
            if not isinstance(value, str) or not value.strip():
                fail(errors, f"{relative_skill}: frontmatter {key!r} must be a non-empty string")
        if metadata.get("name") != skill_dir.name:
            fail(errors, f"{relative_skill}: frontmatter name must match directory name {skill_dir.name!r}")

    for name in REMOVED_SKILLS:
        if (skills_dir / name).exists():
            fail(errors, f"skills/{name}: removed by ADR-002; use provider-policy and providers instead")


def validate_provider_pins(errors: list[str]) -> None:
    """Check the pin table that scripts/install_provider_skills.sh reads."""
    path = ROOT / PROVIDER_PINS_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(errors, f"{PROVIDER_PINS_FILE}: cannot read pin table: {exc}")
        return
    if text.count(PROVIDER_PINS_BEGIN) != 1 or text.count(PROVIDER_PINS_END) != 1:
        fail(errors, f"{PROVIDER_PINS_FILE}: pin table markers must appear exactly once")
        return
    block = text.split(PROVIDER_PINS_BEGIN, 1)[1].split(PROVIDER_PINS_END, 1)[0]
    table = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    if len(table) < 2 or [cell.strip() for cell in table[0].strip("|").split("|")] != PROVIDER_PINS_HEADER:
        fail(errors, f"{PROVIDER_PINS_FILE}: pin table header must be {' | '.join(PROVIDER_PINS_HEADER)}")
        return

    seen: set[str] = set()
    for line in table[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(PROVIDER_PINS_HEADER):
            fail(errors, f"{PROVIDER_PINS_FILE}: pin row must have {len(PROVIDER_PINS_HEADER)} cells: {line}")
            continue
        vendor, repository, skill_path, ref, install, license_note, checked = cells
        where = f"{PROVIDER_PINS_FILE}: vendor {vendor!r}"
        if vendor in seen:
            fail(errors, f"{where}: duplicate row")
        seen.add(vendor)
        if not re.fullmatch(r"[a-z][a-z0-9-]*", vendor):
            fail(errors, f"{where}: vendor key must be lowercase letters, digits, and hyphens")
        if ref == "none":
            if repository != "none" or skill_path != "none":
                fail(errors, f"{where}: a row without a pin must use 'none' for repository and Skill path")
        elif re.fullmatch(r"[0-9a-f]{40}", ref):
            if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
                fail(errors, f"{where}: repository must be owner/name")
            if not re.fullmatch(r"[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*", skill_path) or ".." in skill_path:
                fail(errors, f"{where}: Skill path must be a relative path inside the repository")
        else:
            fail(errors, f"{where}: pinned ref must be a full 40-character commit SHA or 'none'")
        if install not in PROVIDER_INSTALL_VALUES:
            fail(errors, f"{where}: Install must be one of {', '.join(sorted(PROVIDER_INSTALL_VALUES))}")
        elif install == "hermes" and ref == "none":
            fail(errors, f"{where}: Install 'hermes' requires a pinned commit")
        if not license_note:
            fail(errors, f"{where}: license note is required")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", checked) and not (checked == "pending" and ref == "none"):
            fail(errors, f"{where}: check date must be YYYY-MM-DD ('pending' only for a row without a pin)")

    missing = PROVIDER_VENDORS - seen
    if missing:
        fail(errors, f"{PROVIDER_PINS_FILE}: pin table is missing vendors: {', '.join(sorted(missing))}")


def validate_forbidden_files(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if relative.parts and relative.parts[0] in FORBIDDEN_ROOT_DIRS:
            fail(errors, f"forbidden runtime-state path: {relative.as_posix()}")
            continue
        if not path.is_file():
            continue
        lower_name = path.name.lower()
        if lower_name in FORBIDDEN_FILE_NAMES or lower_name.startswith(".env."):
            if lower_name not in {".env.example", ".env.sample", ".env.template"}:
                fail(errors, f"forbidden secret/state file: {relative.as_posix()}")
        elif path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(errors, f"forbidden secret/state file: {relative.as_posix()}")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_yaml_files(errors)
    validate_json_files(errors)
    validate_skills(errors)
    validate_provider_pins(errors)
    validate_forbidden_files(errors)

    if errors:
        print(f"Distribution validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    parser_name = "PyYAML" if yaml is not None else "stdlib fallback"
    print(f"Distribution validation passed ({parser_name}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
