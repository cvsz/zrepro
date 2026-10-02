import json
from pathlib import Path

import pytest

from zrepro_mcp.core import MAX_REPORT_BYTES, ZReproCore

ROOT = Path(__file__).resolve().parents[3]


def test_status_does_not_disclose_checkout_path() -> None:
    status = ZReproCore(ROOT).status()

    assert "repo_root" not in status
    assert str(ROOT) not in json.dumps(status)


def test_artifact_metadata_rejects_invalid_hash_size_and_labels() -> None:
    core = ZReproCore(ROOT)
    for digest in ("bad", ""):
        with pytest.raises(ValueError, match="sha256"):
            core.triage_metadata(artifact_type="pe", name="x", sha256=digest)
    with pytest.raises(ValueError, match="name"):
        core.triage_metadata(artifact_type="pe", name="  ")
    with pytest.raises(ValueError, match="size_bytes"):
        core.triage_metadata(artifact_type="pe", name="x", size_bytes=-1)
    with pytest.raises(ValueError, match="control characters"):
        core.triage_metadata(artifact_type="pe", name="x\n.exe")


def test_evidence_validation_bounds_input_and_error_output() -> None:
    core = ZReproCore(ROOT)
    with pytest.raises(ValueError, match="JSON-compatible"):
        core.validate_report({"not_json": float("nan")})
    with pytest.raises(ValueError, match="validation limit"):
        core.validate_report({"padding": "x" * MAX_REPORT_BYTES})

    result = core.validate_report({"findings": [{} for _ in range(60)]})

    assert result["valid"] is False
    assert result["returned_error_count"] == 50
    assert result["errors_truncated"] is True
    assert len(result["report_sha256"]) == 64
    assert all("rule" in error and len(error["message"]) <= 500 for error in result["errors"])


def test_skill_retrieval_is_catalogued_and_confined_to_skills_tree(tmp_path: Path) -> None:
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
    (root / "skills" / "in-repo-link" / "SKILL.md").symlink_to(root / "docs" / "SKILL.md")
    (root / "skills" / "uncatalogued").mkdir()
    (root / "skills" / "uncatalogued" / "SKILL.md").write_text(
        "not catalogued", encoding="utf-8"
    )
    core = ZReproCore(root)

    for name in ("allowed", "in-repo-link", "uncatalogued"):
        with pytest.raises(ValueError, match="unknown skill"):
            core.skill(name)
