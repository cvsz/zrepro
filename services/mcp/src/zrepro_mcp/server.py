from __future__ import annotations

from typing import Any

from mcp.server import MCPServer
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl

from .auth import IntrospectionTokenVerifier
from .config import Settings
from .core import ZReproCore


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

    @mcp.tool()
    def server_status() -> dict[str, Any]:
        """Return the zRepro MCP service and evidence-catalog status."""
        return core.status()

    @mcp.tool()
    def list_capabilities() -> dict[str, Any]:
        """List supported analysis routes and explicit safety boundaries."""
        return core.list_capabilities()

    @mcp.tool()
    def triage_artifact_metadata(
        artifact_type: str,
        name: str,
        sha256: str | None = None,
        size_bytes: int | None = None,
    ) -> dict[str, Any]:
        """Route authorized artifact metadata to the correct zRepro specialist skill."""
        return core.triage_metadata(
            artifact_type=artifact_type,
            name=name,
            sha256=sha256,
            size_bytes=size_bytes,
        )

    @mcp.tool()
    def validate_evidence_report(report: dict[str, Any]) -> dict[str, Any]:
        """Validate a zRepro evidence report against the canonical JSON schema."""
        return core.validate_report(report)

    @mcp.tool()
    def get_skill(name: str) -> dict[str, Any]:
        """Return one canonical zRepro skill by exact skill name."""
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
