import json
from pathlib import Path

import pytest

from zrepro_mcp.core import MAX_REPORT_BYTES, TOOL_CATALOG, ZReproCore

ROOT = Path(__file__).resolve().parents[3]


def test_triage_routes_pe() -> None:
    result = ZReproCore(ROOT).triage_metadata(
        artifact_type="pe",
        name="sample.exe",
        sha256="a" * 64,
        size_bytes=123,
    )
    assert result["route"] == "zeaz-re-windows"
    assert result["evidence_state"] == "UNVERIFIED"


def test_rejects_bad_hash() -> None:
    core = ZReproCore(ROOT)
    try:
        core.triage_metadata(artifact_type="elf", name="x", sha256="bad")
    except ValueError as exc:
        assert "sha256" in str(exc)
    else:
        raise AssertionError("bad hash accepted")


def test_rejects_empty_hash_and_invalid_metadata() -> None:
    core = ZReproCore(ROOT)
    with pytest.raises(ValueError, match="sha256"):
        core.triage_metadata(artifact_type="pe", name="x", sha256="")
    with pytest.raises(ValueError, match="name"):
        core.triage_metadata(artifact_type="pe", name="  ")
    with pytest.raises(ValueError, match="size_bytes"):
        core.triage_metadata(artifact_type="pe", name="x", size_bytes=-1)
    with pytest.raises(ValueError, match="control characters"):
        core.triage_metadata(artifact_type="pe", name="x\n.exe")


def test_status_and_capabilities_expose_complete_tool_inventory() -> None:
    core = ZReproCore(ROOT)
    expected_names = [tool["name"] for tool in TOOL_CATALOG]

    status = core.status()
    capabilities = core.list_capabilities()

    assert status["tool_count"] == 7
    assert status["tool_names"] == expected_names
    assert "repo_root" not in status
    assert status["evidence_schema_version"] == "1.0"
    assert [tool["name"] for tool in capabilities["tools"]] == expected_names
    assert capabilities["safety"]["arbitrary_command_execution"] is False


def test_list_skills_supports_case_insensitive_filters() -> None:
    core = ZReproCore(ROOT)

    by_domain = core.list_skills(domain="WINDOWS-PE")
    by_risk = core.list_skills(risk_level="HIGH")

    assert [item["name"] for item in by_domain["skills"]] == ["zeaz-re-windows"]
    assert by_risk["count"] > 0
    assert all(item["risk_level"] == "high" for item in by_risk["skills"])
    with pytest.raises(ValueError, match="risk_level"):
        core.list_skills(risk_level="critical")


def test_evidence_schema_is_returned_as_a_copy() -> None:
    core = ZReproCore(ROOT)
    schema = core.get_evidence_schema()
    schema.clear()
    assert core.get_evidence_schema().get("$id")


def test_sample_report_validates() -> None:
    core = ZReproCore(ROOT)
    report = json.loads((ROOT / "fixtures/re/reports/pe.report.json").read_text())
    result = core.validate_report(report)
    assert result["valid"] is True


def test_invalid_report_errors_are_bounded_and_deterministic() -> None:
    core = ZReproCore(ROOT)
    report = {"findings": [{} for _ in range(60)]}

    result = core.validate_report(report)

    assert result["valid"] is False
    assert result["returned_error_count"] == 50
    assert result["errors_truncated"] is True
    assert len(result["report_sha256"]) == 64
    assert all("rule" in error and len(error["message"]) <= 500 for error in result["errors"])


def test_report_validation_rejects_non_json_and_oversized_values() -> None:
    core = ZReproCore(ROOT)
    with pytest.raises(ValueError, match="JSON-compatible"):
        core.validate_report({"not_json": float("nan")})
    with pytest.raises(ValueError, match="validation limit"):
        core.validate_report({"padding": "x" * MAX_REPORT_BYTES})


def test_skill_retrieval_requires_catalog_entry_and_rejects_symlink_escape(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    (root / "catalog").mkdir(parents=True)
    (root / "schemas").mkdir()
    (root / "skills" / "allowed").mkdir(parents=True)
    (root / "skills" / "in-repo-link").mkdir()
    (root / "docs").mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("outside", encoding="utf-8")
    (root / "docs" / "SKILL.md").write_text("inside repo, outside skills", encoding="utf-8")
    (root / "catalog" / "re-skills.json").write_text(
        json.dumps({"skills": [{"name": "allowed"}, {"name": "in-repo-link"}]}),
        encoding="utf-8",
    )
    (root / "schemas" / "re-evidence-report.schema.json").write_text("{}", encoding="utf-8")
    (root / "skills" / "allowed" / "SKILL.md").symlink_to(outside)
    (root / "skills" / "in-repo-link" / "SKILL.md").symlink_to(
        root / "docs" / "SKILL.md"
    )
    (root / "skills" / "uncatalogued").mkdir()
    (root / "skills" / "uncatalogued" / "SKILL.md").write_text(
        "not catalogued", encoding="utf-8"
    )
    core = ZReproCore(root)

    with pytest.raises(ValueError, match="unknown skill"):
        core.skill("allowed")
    with pytest.raises(ValueError, match="unknown skill"):
        core.skill("in-repo-link")
    with pytest.raises(ValueError, match="unknown skill"):
        core.skill("uncatalogued")
