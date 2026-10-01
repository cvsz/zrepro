from pathlib import Path

from zrepro_mcp.core import ZReproCore


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


def test_sample_report_validates() -> None:
    core = ZReproCore(ROOT)
    import json
    report = json.loads((ROOT / "fixtures/re/reports/pe.report.json").read_text())
    result = core.validate_report(report)
    assert result["valid"] is True
