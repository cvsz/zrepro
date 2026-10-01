#!/usr/bin/env python3
"""Validate zRepro skill metadata, component registration, and safe RE fixtures."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
COMPONENTS_DIR = ROOT / "components.d"
FIXTURES_DIR = ROOT / "fixtures" / "re"
SCHEMA_PATH = ROOT / "schemas" / "re-evidence-report.schema.json"

REQUIRED_METADATA = {
    "name",
    "title",
    "description",
    "version",
    "license",
    "tags",
    "supported_harnesses",
    "risk_level",
    "requires_network",
    "requires_credentials",
    "evidence_required",
}
ALLOWED_RISK = {"low", "medium", "high"}
REQUIRED_FIXTURE_TYPES = {"pe", "elf", "macho", "apk", "samsung-oneui", "knox-policy"}
COMPONENT_PATH_RE = re.compile(r"^\s*-\s+path:\s+(skills/[^/]+/)\s*$")


def parse_scalar(value: str):
    value = value.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [item.strip() for item in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc

    data: dict[str, object] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported metadata line: {line!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = parse_scalar(value)
    return data


def validate_skills() -> list[str]:
    errors: list[str] = []
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        return ["no canonical skills found"]

    for skill_file in skill_files:
        rel = skill_file.relative_to(ROOT)
        try:
            meta = parse_frontmatter(skill_file)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue

        missing = sorted(REQUIRED_METADATA - set(meta))
        if missing:
            errors.append(f"{rel}: missing metadata: {', '.join(missing)}")

        expected_name = skill_file.parent.name
        if meta.get("name") != expected_name:
            errors.append(f"{rel}: name must match directory ({expected_name})")

        if meta.get("risk_level") not in ALLOWED_RISK:
            errors.append(f"{rel}: invalid risk_level: {meta.get('risk_level')!r}")

        for key in ("requires_network", "requires_credentials", "evidence_required"):
            if key in meta and not isinstance(meta[key], bool):
                errors.append(f"{rel}: {key} must be true or false")

        for key in ("tags", "supported_harnesses"):
            if key in meta and (not isinstance(meta[key], list) or not meta[key]):
                errors.append(f"{rel}: {key} must be a non-empty inline list")

    return errors


def component_registrations() -> dict[str, list[str]]:
    registrations: dict[str, list[str]] = {}
    for manifest in sorted(COMPONENTS_DIR.glob("*.yml")):
        for line in manifest.read_text(encoding="utf-8").splitlines():
            match = COMPONENT_PATH_RE.match(line)
            if match:
                skill = Path(match.group(1).rstrip("/")).name
                registrations.setdefault(skill, []).append(manifest.name)
    return registrations


def validate_component_registration() -> list[str]:
    errors: list[str] = []
    canonical = {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}
    registrations = component_registrations()

    for skill in sorted(canonical):
        manifests = registrations.get(skill, [])
        if len(manifests) != 1:
            errors.append(
                f"skill {skill}: expected exactly one component registration, found "
                f"{len(manifests)} ({', '.join(manifests) or 'none'})"
            )

    for skill, manifests in sorted(registrations.items()):
        if skill not in canonical:
            errors.append(f"component registration references missing skill: {skill} ({', '.join(manifests)})")

    return errors


def validate_schema() -> list[str]:
    errors: list[str] = []
    if not SCHEMA_PATH.exists():
        return [f"missing evidence schema: {SCHEMA_PATH.relative_to(ROOT)}"]
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{SCHEMA_PATH.relative_to(ROOT)}: invalid JSON: {exc}"]

    required = set(schema.get("required", []))
    expected = {"schema_version", "artifact", "scope", "findings", "evidence_state"}
    missing = expected - required
    if missing:
        errors.append(f"evidence schema missing required fields: {', '.join(sorted(missing))}")
    return errors


def validate_fixtures() -> list[str]:
    errors: list[str] = []
    if not FIXTURES_DIR.exists():
        return [f"missing fixture directory: {FIXTURES_DIR.relative_to(ROOT)}"]

    seen: set[str] = set()
    for path in sorted(FIXTURES_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue

        fixture_type = data.get("fixture_type")
        if fixture_type:
            seen.add(fixture_type)
        if data.get("safe_synthetic") is not True:
            errors.append(f"{path.relative_to(ROOT)}: safe_synthetic must be true")
        if data.get("contains_executable_bytes") is not False:
            errors.append(f"{path.relative_to(ROOT)}: contains_executable_bytes must be false")
        if not data.get("expected_observations"):
            errors.append(f"{path.relative_to(ROOT)}: expected_observations must be non-empty")

    missing = REQUIRED_FIXTURE_TYPES - seen
    if missing:
        errors.append(f"missing required fixture types: {', '.join(sorted(missing))}")
    return errors


def main() -> int:
    errors = (
        validate_skills()
        + validate_component_registration()
        + validate_schema()
        + validate_fixtures()
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Reverse-engineering skill catalog, evidence schema, and synthetic fixtures are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
