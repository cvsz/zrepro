import json
from pathlib import Path

import pytest

from zrepro_mcp.core import TOOL_CATALOG, ZReproCore

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
    assert capabilities["safety"]["artifact_content_analysis"] is False
    assert capabilities["safety"]["dynamic_tracing"] is False
    assert capabilities["safety"]["rva"] == {
        "role": "diagnostic-only",
        "application_invoked": False,
    }


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
