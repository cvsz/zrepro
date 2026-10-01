#!/usr/bin/env python3
"""Validate zRepro RE skills, registrations, fixtures, reports, catalog and benchmarks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

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
ALLOWED_EVIDENCE_STATES = {
    "VERIFIED", "PARTIALLY VERIFIED", "UNVERIFIED", "BLOCKED", "NOT APPLICABLE",
}
ALLOWED_CONFIDENCE = {"confirmed", "probable", "hypothesis"}
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


def validate_schema() -> list[str]:
    if not SCHEMA_PATH.exists():
        return [f"missing evidence schema: {SCHEMA_PATH.relative_to(ROOT)}"]
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{SCHEMA_PATH.relative_to(ROOT)}: invalid JSON: {exc}"]
    expected = {"schema_version", "artifact", "scope", "findings", "evidence_state"}
    missing = expected - set(schema.get("required", []))
    return [] if not missing else [f"evidence schema missing required fields: {', '.join(sorted(missing))}"]


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


def validate_reports() -> list[str]:
    errors: list[str] = []
    existing = {p.name for p in REPORTS_DIR.glob("*.json")}
    missing_reports = REQUIRED_REPORTS - existing
    if missing_reports:
        errors.append(f"missing required report fixtures: {', '.join(sorted(missing_reports))}")

    required = {"schema_version", "artifact", "scope", "findings", "evidence_state"}
    for path in sorted(REPORTS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        missing = required - set(data)
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing fields: {', '.join(sorted(missing))}")
            continue
        if data.get("schema_version") != "1.0":
            errors.append(f"{path.relative_to(ROOT)}: schema_version must be 1.0")
        if data.get("evidence_state") not in ALLOWED_EVIDENCE_STATES:
            errors.append(f"{path.relative_to(ROOT)}: invalid evidence_state")
        findings = data.get("findings")
        if not isinstance(findings, list):
            errors.append(f"{path.relative_to(ROOT)}: findings must be a list")
            continue
        for finding in findings:
            if finding.get("confidence") not in ALLOWED_CONFIDENCE:
                errors.append(f"{path.relative_to(ROOT)}: invalid finding confidence")
            evidence = finding.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"{path.relative_to(ROOT)}: each finding requires evidence")
                continue
            for item in evidence:
                source = item.get("source")
                if isinstance(source, str) and source.startswith("fixtures/re/") and not (ROOT / source).exists():
                    errors.append(f"{path.relative_to(ROOT)}: missing evidence source: {source}")
    return errors


def validate_catalog_index(skills: dict[str, dict[str, object]]) -> list[str]:
    errors: list[str] = []
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [f"invalid or missing catalog index: {exc}"]
    entries = catalog.get("skills", [])
    names = [entry.get("name") for entry in entries]
    if len(names) != len(set(names)):
        errors.append("catalog index contains duplicate skill names")
    if set(names) != set(skills):
        errors.append("catalog index skill set does not match canonical skills")
    by_name = {entry.get("name"): entry for entry in entries}
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
