import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROUTES = {
    "pe": "zeaz-re-windows",
    "elf": "zeaz-re-linux",
    "macho": "zeaz-re-apple",
    "apk": "zeaz-re-mobile",
    "samsung-oneui": "zeaz-re-samsung",
    "knox-policy": "zeaz-re-knox",
    "firmware": "zeaz-re-firmware",
    "document": "zeaz-re-document",
    "memory": "zeaz-re-memory",
    "protocol": "zeaz-re-protocol",
}


class ZReproCore:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.catalog = self._load_json("catalog/re-skills.json")
        self.evidence_schema = self._load_json("schemas/re-evidence-report.schema.json")
        self.validator = Draft202012Validator(self.evidence_schema)

    def _load_json(self, relative: str) -> Any:
        with (self.root / relative).open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def status(self) -> dict[str, Any]:
        return {
            "service": "zrepro-mcp",
            "repo_root": str(self.root),
            "catalog_schema_version": self.catalog.get("schema_version"),
            "evidence_schema_version": self.evidence_schema.get("$id", "unknown"),
            "mode": "read-only-evidence",
        }

    def list_capabilities(self) -> dict[str, Any]:
        return {
            "routes": ROUTES,
            "catalog": self.catalog,
            "safety": {
                "arbitrary_command_execution": False,
                "credential_extraction": False,
                "ownership_or_drm_bypass": False,
                "third_party_production_fuzzing": False,
                "dynamic_execution": "not exposed by this service revision",
            },
        }

    def triage_metadata(
        self,
        *,
        artifact_type: str,
        name: str,
        sha256: str | None = None,
        size_bytes: int | None = None,
    ) -> dict[str, Any]:
        artifact_type = artifact_type.lower().strip()
        route = ROUTES.get(artifact_type, "zeaz-re-triage")
        if sha256 and (
            len(sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in sha256)
        ):
            raise ValueError("sha256 must be exactly 64 hexadecimal characters")
        return {
            "artifact": {
                "name": name,
                "type": artifact_type,
                "sha256": sha256.lower() if sha256 else None,
                "size_bytes": size_bytes,
            },
            "route": route,
            "evidence_state": "UNVERIFIED",
            "next_step": (
                "Use the routed skill and attach tool/version/method evidence "
                "before confirming findings."
            ),
        }

    def validate_report(self, report: dict[str, Any]) -> dict[str, Any]:
        errors = sorted(self.validator.iter_errors(report), key=lambda e: list(e.absolute_path))
        return {
            "valid": not errors,
            "errors": [
                {
                    "path": "/".join(str(part) for part in error.absolute_path),
                    "message": error.message,
                }
                for error in errors[:50]
            ],
            "report_sha256": hashlib.sha256(
                json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest(),
        }

    def skill(self, name: str) -> dict[str, Any]:
        safe = name.strip()
        if not safe or "/" in safe or "\\" in safe or safe.startswith("."):
            raise ValueError("invalid skill name")
        path = self.root / "skills" / safe / "SKILL.md"
        if not path.is_file():
            raise ValueError("unknown skill")
        return {"name": safe, "content": path.read_text(encoding="utf-8")}
