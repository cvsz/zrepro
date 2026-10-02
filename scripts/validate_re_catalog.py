#!/usr/bin/env python3
"""Validate zRepro RE skills, registrations, fixtures, reports, catalog and benchmarks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
COMPONENTS_DIR = ROOT / "components.d"
FIXTURES_DIR = ROOT / "fixtures" / "re"
REPORTS_DIR = FIXTURES_DIR / "reports"
SCHEMA_PATH = ROOT / "schemas" / "re-evidence-report.schema.json"
SBOM_PATH = ROOT / "sbom" / "re-validator.spdx.json"
PROVENANCE_PATH = ROOT / "provenance" / "re-validator.md"
CATALOG_PATH = ROOT / "catalog" / "re-skills.json"
BENCHMARK_PATH = ROOT / "benchmarks" / "re" / "scenarios.json"

REQUIRED_METADATA = {
    "name", "title", "description", "version", "license", "tags",
    "supported_harnesses", "risk_level", "requires_network",
    "requires_credentials", "evidence_required",
}
ALLOWED_RISK = {"low", "medium", "high"}
SUPPORTED_SCHEMA_KEYWORDS = {
    "$schema", "$id", "title", "description", "type", "additionalProperties",
    "required", "properties", "items", "enum", "const", "minLength", "minItems", "pattern",
}
JSON_SCHEMA_TYPES = {"object", "array", "string", "boolean", "integer", "number", "null"}
REQUIRED_FIXTURE_TYPES = {
    "pe", "elf", "macho", "apk", "samsung-oneui", "knox-policy",
    "firmware", "document", "memory", "protocol", "fuzzing",
}
REQUIRED_REPORTS = {
    "pe.report.json", "elf.report.json", "macho.report.json", "apk.report.json",
    "samsung-oneui.report.json", "knox-policy.report.json",
    "firmware.report.json", "document.report.json", "memory.report.json",
    "protocol.report.json", "fuzzing.report.json",
}
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
    lines = path.read_text(encoding="utf-8").splitlines()
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


def skill_metadata() -> tuple[dict[str, dict[str, object]], list[str]]:
    result: dict[str, dict[str, object]] = {}
    errors: list[str] = []
    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
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
        result[expected_name] = meta

    if not result:
        errors.append("no canonical skills found")
    return result, errors


def component_registrations() -> dict[str, list[str]]:
    registrations: dict[str, list[str]] = {}
    for manifest in sorted(COMPONENTS_DIR.glob("*.yml")):
        for line in manifest.read_text(encoding="utf-8").splitlines():
            match = COMPONENT_PATH_RE.match(line)
            if match:
                skill = Path(match.group(1).rstrip("/")).name
                registrations.setdefault(skill, []).append(manifest.name)
    return registrations


def validate_component_registration(skills: dict[str, dict[str, object]]) -> list[str]:
    errors: list[str] = []
    registrations = component_registrations()
    for skill in sorted(skills):
        manifests = registrations.get(skill, [])
        if len(manifests) != 1:
            errors.append(
                f"skill {skill}: expected exactly one component registration, found "
                f"{len(manifests)} ({', '.join(manifests) or 'none'})"
            )
    for skill, manifests in sorted(registrations.items()):
        if skill not in skills:
            errors.append(f"component registration references missing skill: {skill} ({', '.join(manifests)})")
    return errors


def _validate_schema_definition(schema: object, path: str = "$schema") -> list[str]:
    if not isinstance(schema, dict):
        return [f"{path}: schema must be an object"]
    errors: list[str] = []
    unknown = set(schema) - SUPPORTED_SCHEMA_KEYWORDS
    if unknown:
        errors.append(f"{path}: unsupported schema keywords: {', '.join(sorted(unknown))}")

    for metadata in ("$schema", "$id", "title", "description"):
        if metadata in schema and not isinstance(schema[metadata], str):
            errors.append(f"{path}.{metadata}: must be a string")

    if "type" in schema:
        types = schema["type"]
        if isinstance(types, str):
            types = [types]
        if not isinstance(types, list) or not types or any(
            not isinstance(t, str) or t not in JSON_SCHEMA_TYPES for t in types
        ):
            errors.append(f"{path}.type: unsupported or invalid JSON Schema type")

    if "required" in schema:
        required = schema["required"]
        if not isinstance(required, list) or any(not isinstance(name, str) for name in required):
            errors.append(f"{path}.required: must be an array of strings")
        elif len(required) != len(set(required)):
            errors.append(f"{path}.required: contains duplicate property names")

    properties = schema.get("properties")
    if "properties" in schema and not isinstance(properties, dict):
        errors.append(f"{path}.properties: must be an object")
    elif isinstance(properties, dict):
        for name, subschema in properties.items():
            if not isinstance(name, str):
                errors.append(f"{path}.properties: property names must be strings")
            else:
                errors.extend(_validate_schema_definition(subschema, f"{path}.properties.{name}"))

    if "items" in schema:
        errors.extend(_validate_schema_definition(schema["items"], f"{path}.items"))

    additional = schema.get("additionalProperties")
    if "additionalProperties" in schema and not isinstance(additional, bool):
        errors.extend(_validate_schema_definition(additional, f"{path}.additionalProperties"))

    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        errors.append(f"{path}.enum: must be a non-empty array")
    for keyword in ("minLength", "minItems"):
        if keyword in schema and (
            not isinstance(schema[keyword], int)
            or isinstance(schema[keyword], bool)
            or schema[keyword] < 0
        ):
            errors.append(f"{path}.{keyword}: must be a non-negative integer")
    if "pattern" in schema:
        if not isinstance(schema["pattern"], str):
            errors.append(f"{path}.pattern: must be a string")
        else:
            try:
                re.compile(schema["pattern"])
            except re.error as exc:
                errors.append(f"{path}.pattern: invalid regular expression: {exc}")
    return errors


def _matches_json_type(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _validate_instance(value: object, schema: dict[str, object], path: str = "$",) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type is not None:
        types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_matches_json_type(value, item) for item in types):
            return [f"{path}: expected type {' or '.join(types)}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: value does not match const")
    enum = schema.get("enum")
    if isinstance(enum, list) and value not in enum:
        errors.append(f"{path}: value is not in the allowed enum")

    if isinstance(value, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for name in required:
                if name not in value:
                    errors.append(f"{path}.{name}: required property is missing")
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            properties = {}
        for name, child_schema in properties.items():
            if name in value and isinstance(child_schema, dict):
                errors.extend(_validate_instance(value[name], child_schema, f"{path}.{name}"))
        additional = schema.get("additionalProperties", True)
        for name, child_value in value.items():
            if name in properties:
                continue
            if additional is False:
                errors.append(f"{path}.{name}: additional property is not allowed")
            elif isinstance(additional, dict):
                errors.extend(_validate_instance(child_value, additional, f"{path}.{name}"))

    if isinstance(value, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(value) < min_items:
            errors.append(f"{path}: must contain at least {min_items} item(s)")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, child_value in enumerate(value):
                errors.extend(_validate_instance(child_value, item_schema, f"{path}[{index}]"))

    if isinstance(value, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(value) < min_length:
            errors.append(f"{path}: must contain at least {min_length} character(s)")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, value) is None:
            errors.append(f"{path}: value does not match the required pattern")
    return errors


def _load_evidence_schema() -> tuple[dict[str, object] | None, list[str]]:
    if not SCHEMA_PATH.exists():
        return None, [f"missing evidence schema: {SCHEMA_PATH.relative_to(ROOT)}"]
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"{SCHEMA_PATH.relative_to(ROOT)}: invalid JSON: {exc}"]
    if not isinstance(schema, dict):
        return None, [f"{SCHEMA_PATH.relative_to(ROOT)}: schema root must be an object"]
    errors = _validate_schema_definition(schema)
    expected = {"schema_version", "artifact", "scope", "findings", "evidence_state"}
    required = schema.get("required", [])
    missing = expected - set(required if isinstance(required, list) else [])
    if missing:
        errors.append(f"evidence schema missing required fields: {', '.join(sorted(missing))}")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("evidence schema must declare JSON Schema draft 2020-12")
    return schema, errors


def validate_schema() -> list[str]:
    _, errors = _load_evidence_schema()
    return errors


def validate_fixtures() -> list[str]:
    errors: list[str] = []
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


def _validate_fixture_source(source: str) -> str | None:
    """Return an error when an in-repo fixture reference escapes its corpus."""
    if not source.startswith("fixtures/re/"):
        return None
    if "\\" in source:
        return "fixture evidence source uses an unsupported path separator"
    relative = PurePosixPath(source)
    if ".." in relative.parts:
        return "fixture evidence source escapes fixtures/re"
    try:
        fixture_root = FIXTURES_DIR.resolve()
        candidate = ROOT.joinpath(*relative.parts).resolve()
        candidate.relative_to(fixture_root)
    except ValueError:
        return "fixture evidence source escapes fixtures/re"
    except (OSError, RuntimeError):
        return "fixture evidence source is an invalid path"
    try:
        if not candidate.is_file():
            return f"missing evidence source: {source}"
    except (OSError, RuntimeError, ValueError):
        return "fixture evidence source is an invalid path"
    return None


def validate_reports() -> list[str]:
    errors: list[str] = []
    schema, schema_errors = _load_evidence_schema()
    if schema_errors or schema is None:
        return [f"cannot validate evidence reports: {error}" for error in schema_errors]
    existing = {p.name for p in REPORTS_DIR.glob("*.json")}
    missing_reports = REQUIRED_REPORTS - existing
    if missing_reports:
        errors.append(f"missing required report fixtures: {', '.join(sorted(missing_reports))}")

    for path in sorted(REPORTS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        report_errors = _validate_instance(data, schema)
        if report_errors:
            errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in report_errors)
            continue
        findings = data.get("findings")
        if not isinstance(findings, list):
            errors.append(f"{path.relative_to(ROOT)}: findings cannot be inspected for fixture references")
            continue
        for finding in findings:
            if not isinstance(finding, dict) or not isinstance(finding.get("evidence"), list):
                errors.append(f"{path.relative_to(ROOT)}: finding evidence cannot be inspected for fixture references")
                continue
            for item in finding["evidence"]:
                if not isinstance(item, dict) or not isinstance(item.get("source"), str):
                    errors.append(f"{path.relative_to(ROOT)}: evidence source cannot be inspected")
                    continue
                source_error = _validate_fixture_source(item["source"])
                if source_error:
                    errors.append(f"{path.relative_to(ROOT)}: {source_error}")
    return errors


def validate_catalog_index(skills: dict[str, dict[str, object]]) -> list[str]:
    errors: list[str] = []
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [f"invalid or missing catalog index: {exc}"]
    if not isinstance(catalog, dict):
        return ["catalog index must be an object"]
    entries = catalog.get("skills")
    if not isinstance(entries, list) or not entries:
        return ["catalog index skills must be a non-empty list"]
    if any(not isinstance(entry, dict) for entry in entries):
        return ["catalog index skills must contain objects"]
    names = [entry.get("name") for entry in entries]
    if any(not isinstance(name, str) or not name.strip() for name in names):
        return ["catalog index skills must have non-empty string names"]
    if len(names) != len(set(names)):
        errors.append("catalog index contains duplicate skill names")
    if set(names) != set(skills):
        errors.append("catalog index skill set does not match canonical skills")
    by_name = {entry.get("name"): entry for entry in entries}
    for entry in entries:
        domain = entry.get("domain")
        if not isinstance(domain, str) or not domain.strip():
            errors.append(f"catalog index domain must be a non-empty string for {entry['name']}")
    for name, meta in skills.items():
        entry = by_name.get(name, {})
        if entry.get("version") != meta.get("version"):
            errors.append(f"catalog index version mismatch for {name}")
        if entry.get("risk_level") != meta.get("risk_level"):
            errors.append(f"catalog index risk mismatch for {name}")
    return errors


def validate_benchmarks(skills: dict[str, dict[str, object]]) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [f"invalid or missing benchmark scenarios: {exc}"]
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        return ["benchmark scenarios must be a non-empty list"]
    ids: set[str] = set()
    for scenario in scenarios:
        sid = scenario.get("id")
        if not sid or sid in ids:
            errors.append(f"invalid or duplicate benchmark id: {sid!r}")
        ids.add(sid)
        fixture = scenario.get("fixture")
        if not isinstance(fixture, str) or not (ROOT / fixture).exists():
            errors.append(f"benchmark {sid}: missing fixture {fixture!r}")
        expected_skill = scenario.get("expected_skill")
        if expected_skill not in skills:
            errors.append(f"benchmark {sid}: unknown expected_skill {expected_skill!r}")
        if not scenario.get("required_concept") or not scenario.get("forbidden_inference"):
            errors.append(f"benchmark {sid}: missing evidence semantics")
    return errors


def validate_supply_chain_evidence() -> list[str]:
    errors: list[str] = []
    if not SBOM_PATH.exists():
        errors.append(f"missing validator SBOM: {SBOM_PATH.relative_to(ROOT)}")
    else:
        try:
            sbom = json.loads(SBOM_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{SBOM_PATH.relative_to(ROOT)}: invalid JSON: {exc}")
        else:
            if sbom.get("spdxVersion") != "SPDX-2.3":
                errors.append(f"{SBOM_PATH.relative_to(ROOT)}: expected SPDX-2.3")
            if not sbom.get("packages"):
                errors.append(f"{SBOM_PATH.relative_to(ROOT)}: packages must be non-empty")
    if not PROVENANCE_PATH.exists():
        errors.append(f"missing validator provenance: {PROVENANCE_PATH.relative_to(ROOT)}")
    return errors


def main() -> int:
    skills, errors = skill_metadata()
    errors += validate_component_registration(skills)
    errors += validate_schema()
    errors += validate_fixtures()
    errors += validate_reports()
    errors += validate_catalog_index(skills)
    errors += validate_benchmarks(skills)
    errors += validate_supply_chain_evidence()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("RE skills, registrations, fixtures, reports, catalog, benchmarks and supply-chain evidence are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
