from __future__ import annotations

from typing import Annotated, Any, Literal

from mcp.server import MCPServer
from mcp.server.auth.settings import AuthSettings
from mcp.types import ToolAnnotations
from pydantic import AnyHttpUrl, Field

from .auth import IntrospectionTokenVerifier
from .config import Settings
from .core import (
    MAX_ARTIFACT_NAME_LENGTH,
    MAX_ARTIFACT_TYPE_LENGTH,
    TOOL_CATALOG,
    ZReproCore,
)

_TOOL_METADATA = {tool["name"]: tool for tool in TOOL_CATALOG}
_READ_ONLY_ANNOTATIONS = ToolAnnotations(
    read_only_hint=True,
    open_world_hint=False,
)


def _tool_options(name: str) -> dict[str, Any]:
    metadata = _TOOL_METADATA[name]
    return {
        "name": metadata["name"],
        "title": metadata["title"],
        "description": metadata["description"],
        "annotations": _READ_ONLY_ANNOTATIONS,
    }


def build_server(settings: Settings) -> MCPServer:
    kwargs: dict[str, Any] = {}
    if settings.auth_mode == "introspection":
        verifier = IntrospectionTokenVerifier(
            endpoint=settings.introspection_url or "",
            client_id=settings.introspection_client_id or "",
            client_secret=settings.introspection_client_secret or "",
            resource_url=settings.resource_url or "",
            issuer_url=settings.issuer_url or "",
        )
        kwargs = {
            "token_verifier": verifier,
            "auth": AuthSettings(
                issuer_url=AnyHttpUrl(settings.issuer_url or ""),
                resource_server_url=AnyHttpUrl(settings.resource_url or ""),
                required_scopes=[settings.required_scope],
                validate_token_resource=True,
            ),
        }

    mcp = MCPServer("zRepro", **kwargs)
    core = ZReproCore(settings.repo_root)

    @mcp.tool(**_tool_options("server_status"))
    def server_status() -> dict[str, Any]:
        """Return service mode, registered tools, and catalog/schema versions."""
        return core.status()

    @mcp.tool(**_tool_options("list_capabilities"))
    def list_capabilities() -> dict[str, Any]:
        """List the complete registered tool inventory, routes, skills, and safety boundaries."""
        return core.list_capabilities()

    @mcp.tool(**_tool_options("list_skills"))
    def list_skills(
        domain: Annotated[
            str | None,
            Field(
                description="Optional exact skill domain filter, for example 'windows-pe'.",
                min_length=1,
                max_length=64,
            ),
        ] = None,
        risk_level: Annotated[
            Literal["low", "medium", "high"] | None,
            Field(description="Optional risk-level filter."),
        ] = None,
    ) -> dict[str, Any]:
        """List catalogued specialist skills, optionally filtered by domain or risk level."""
        return core.list_skills(domain=domain, risk_level=risk_level)

    @mcp.tool(**_tool_options("get_evidence_schema"))
    def get_evidence_schema() -> dict[str, Any]:
        """Return the canonical JSON Schema for zRepro evidence reports."""
        return core.get_evidence_schema()

    @mcp.tool(**_tool_options("triage_artifact_metadata"))
    def triage_artifact_metadata(
        artifact_type: Annotated[
            str,
            Field(
                description="Artifact family such as pe, elf, apk, firmware, document, or protocol.",
                min_length=1,
                max_length=MAX_ARTIFACT_TYPE_LENGTH,
            ),
        ],
        name: Annotated[
            str,
            Field(
                description="Artifact filename or caller-provided label; artifact contents are not read.",
                min_length=1,
                max_length=MAX_ARTIFACT_NAME_LENGTH,
            ),
        ],
        sha256: Annotated[
            str | None,
            Field(
                description="Optional SHA-256 digest as exactly 64 hexadecimal characters.",
                min_length=64,
                max_length=64,
                pattern=r"^[0-9a-fA-F]{64}$",
            ),
        ] = None,
        size_bytes: Annotated[
            int | None,
            Field(description="Optional non-negative artifact size in bytes.", ge=0),
        ] = None,
    ) -> dict[str, Any]:
        """Route validated artifact metadata to a specialist skill without reading the artifact."""
        return core.triage_metadata(
            artifact_type=artifact_type,
            name=name,
            sha256=sha256,
            size_bytes=size_bytes,
        )

    @mcp.tool(**_tool_options("validate_evidence_report"))
    def validate_evidence_report(
        report: Annotated[
            dict[str, Any],
            Field(description="JSON object to validate against the canonical evidence-report schema."),
        ],
    ) -> dict[str, Any]:
        """Validate a bounded JSON evidence report and return up to 50 schema errors."""
        return core.validate_report(report)

    @mcp.tool(**_tool_options("get_skill"))
    def get_skill(
        name: Annotated[
            str,
            Field(
                description="Exact skill name from the canonical zRepro catalog.",
                min_length=1,
                max_length=128,
            ),
        ]
    ) -> dict[str, Any]:
        """Return the Markdown content for one catalogued skill by exact name."""
        return core.skill(name)

    return mcp


def main() -> None:
    settings = Settings.from_env()
    mcp = build_server(settings)
    mcp.run(
        transport="streamable-http",
        host=settings.host,
        port=settings.port,
        json_response=True,
        stateless_http=True,
    )


if __name__ == "__main__":
    main()
