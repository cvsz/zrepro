import hashlib
import itertools
import json
import unicodedata
from copy import deepcopy
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

MAX_ARTIFACT_TYPE_LENGTH = 64
MAX_ARTIFACT_NAME_LENGTH = 255
MAX_REPORT_BYTES = 1_000_000
MAX_VALIDATION_ERRORS = 50

TOOL_CATALOG = (
    {
        "name": "server_status",
        "title": "Server status",
        "description": "Return service mode and catalog/schema versions without local filesystem paths.",
    },
    {
        "name": "list_capabilities",
        "title": "List capabilities",
        "description": "List the registered MCP tools, analysis routes, skill catalog, and safety boundaries.",
    },
    {
        "name": "list_skills",
        "title": "List skills",
        "description": "List canonical zRepro skills, optionally filtered by domain or risk level.",
    },
    {
        "name": "get_evidence_schema",
        "title": "Get evidence schema",
        "description": "Return the canonical JSON Schema used to validate zRepro evidence reports.",
    },
    {
        "name": "triage_artifact_metadata",
        "title": "Triage artifact metadata",
        "description": "Route bounded artifact metadata to a specialist skill; does not read or execute artifacts.",
    },
    {
        "name": "validate_evidence_report",
        "title": "Validate evidence report",
        "description": "Validate a JSON evidence report and return bounded, deterministic validation details.",
    },
    {
        "name": "get_skill",
        "title": "Get skill",
        "description": "Return the Markdown content of one skill named in the canonical catalog.",
    },
)


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
            "tool_count": len(TOOL_CATALOG),
            "tool_names": [tool["name"] for tool in TOOL_CATALOG],
            "catalog_schema_version": self.catalog.get("schema_version"),
            "evidence_schema_version": (
                self.evidence_schema.get("properties", {})
                .get("schema_version", {})
                .get("const", "unknown")
            ),
            "evidence_schema_id": self.evidence_schema.get("$id", "unknown"),
            "mode": "read-only-evidence",
        }

    def list_capabilities(self) -> dict[str, Any]:
        return {
            "tools": [dict(tool) for tool in TOOL_CATALOG],
            "routes": dict(ROUTES),
            "catalog": deepcopy(self.catalog),
            "safety": {
                "arbitrary_command_execution": False,
                "artifact_content_analysis": False,
                "credential_extraction": False,
                "dynamic_tracing": False,
                "ownership_or_drm_bypass": False,
                "third_party_production_fuzzing": False,
                "rva": {"role": "diagnostic-only", "application_invoked": False},
                "dynamic_execution": "not exposed by this service revision",
            },
        }

    def list_skills(
        self,
        *,
        domain: str | None = None,
        risk_level: str | None = None,
    ) -> dict[str, Any]:
        normalized_domain = domain.strip().casefold() if domain is not None else None
        normalized_risk = risk_level.strip().casefold() if risk_level is not None else None
        if domain is not None and not normalized_domain:
            raise ValueError("domain cannot be empty")
        if risk_level is not None and normalized_risk not in {"low", "medium", "high"}:
            raise ValueError("risk_level must be low, medium, or high")

        skills = self.catalog.get("skills", [])
        matches = [
            dict(skill)
            for skill in skills
            if (normalized_domain is None or skill.get("domain", "").casefold() == normalized_domain)
            and (normalized_risk is None or skill.get("risk_level", "").casefold() == normalized_risk)
        ]
        return {
            "catalog_schema_version": self.catalog.get("schema_version"),
            "count": len(matches),
            "skills": matches,
        }

    def get_evidence_schema(self) -> dict[str, Any]:
        return deepcopy(self.evidence_schema)

    def triage_metadata(
        self,
        *,
        artifact_type: str,
        name: str,
        sha256: str | None = None,
        size_bytes: int | None = None,
    ) -> dict[str, Any]:
        artifact_type = self._validated_label(
            artifact_type, "artifact_type", MAX_ARTIFACT_TYPE_LENGTH
        ).lower()
        name = self._validated_label(name, "name", MAX_ARTIFACT_NAME_LENGTH)
        route = ROUTES.get(artifact_type, "zeaz-re-triage")
        if sha256 is not None and (
            not isinstance(sha256, str)
            or len(sha256) != 64
            or any(c not in "0123456789abcdefABCDEF" for c in sha256)
        ):
            raise ValueError("sha256 must be exactly 64 hexadecimal characters")
        if size_bytes is not None and (not isinstance(size_bytes, int) or isinstance(size_bytes, bool)):
            raise TypeError("size_bytes must be an integer")
        if size_bytes is not None and size_bytes < 0:
            raise ValueError("size_bytes must be a non-negative integer")
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
        if not isinstance(report, dict):
            raise TypeError("report must be a JSON object")
        try:
            canonical_json = json.dumps(
                report,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
            canonical_bytes = canonical_json.encode("utf-8")
        except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
            raise ValueError("report must contain only JSON-compatible values") from None
        if len(canonical_bytes) > MAX_REPORT_BYTES:
            raise ValueError(f"report exceeds the {MAX_REPORT_BYTES}-byte validation limit")

        normalized_report = json.loads(canonical_json)
        collected_errors = list(
            itertools.islice(self.validator.iter_errors(normalized_report), MAX_VALIDATION_ERRORS + 1)
        )
        errors = sorted(
            collected_errors[:MAX_VALIDATION_ERRORS],
            key=lambda error: tuple(
                (type(part).__name__, str(part)) for part in error.absolute_path
            ),
        )
        return {
            "valid": not collected_errors,
            "schema_id": self.evidence_schema.get("$id", "unknown"),
            "returned_error_count": len(errors),
            "errors_truncated": len(collected_errors) > MAX_VALIDATION_ERRORS,
            "errors": [
                {
                    "path": "".join(
                        f"/{str(part).replace('~', '~0').replace('/', '~1')}"
                        for part in error.absolute_path
                    ),
                    "rule": error.validator,
                    "message": error.message[:500],
                }
                for error in errors
            ],
            "report_sha256": hashlib.sha256(canonical_bytes).hexdigest(),
        }

    def skill(self, name: str) -> dict[str, Any]:
        if not isinstance(name, str):
            raise TypeError("skill name must be a string")
        safe = name.strip()
        if (
            not safe
            or len(safe) > 128
            or any(unicodedata.category(character) == "Cc" for character in safe)
            or "/" in safe
            or "\\" in safe
            or safe.startswith(".")
        ):
            raise ValueError("invalid skill name")
        known_skills = {
            item.get("name")
            for item in self.catalog.get("skills", [])
            if isinstance(item, dict)
        }
        if safe not in known_skills:
            raise ValueError("unknown skill")
        root = self.root.resolve()
        try:
            skills_root = (root / "skills").resolve(strict=True)
            if not skills_root.is_relative_to(root):
                raise ValueError("unknown skill")
            path = (skills_root / safe / "SKILL.md").resolve(strict=True)
        except (OSError, RuntimeError):
            raise ValueError("unknown skill") from None
        if not path.is_relative_to(skills_root) or not path.is_file():
            raise ValueError("unknown skill")
        return {"name": safe, "content": path.read_text(encoding="utf-8")}

    @staticmethod
    def _validated_label(value: str, label: str, maximum: int) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{label} must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{label} cannot be empty")
        if len(normalized) > maximum:
            raise ValueError(f"{label} exceeds the {maximum}-character limit")
        if any(unicodedata.category(character) == "Cc" for character in normalized):
            raise ValueError(f"{label} cannot contain control characters")
        return normalized
