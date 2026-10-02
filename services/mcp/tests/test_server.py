import asyncio
from pathlib import Path

import httpx
import pytest
from mcp.server.auth.provider import AccessToken
from mcp.server.mcpserver.exceptions import ToolError

from zrepro_mcp.auth import IntrospectionTokenVerifier
from zrepro_mcp.config import Settings
from zrepro_mcp.core import TOOL_CATALOG
from zrepro_mcp.server import build_server

ROOT = Path(__file__).resolve().parents[3]


def local_settings() -> Settings:
    return Settings(
        host="127.0.0.1",
        port=8787,
        auth_mode="local",
        issuer_url=None,
        resource_url=None,
        introspection_url=None,
        introspection_client_id=None,
        introspection_client_secret=None,
        required_scope="zrepro:read",
        repo_root=ROOT,
    )


def test_registered_tools_match_catalog_and_are_read_only() -> None:
    tools = asyncio.run(build_server(local_settings()).list_tools())

    assert [tool.name for tool in tools] == [item["name"] for item in TOOL_CATALOG]
    for tool, metadata in zip(tools, TOOL_CATALOG, strict=True):
        assert tool.title == metadata["title"]
        assert tool.description == metadata["description"]
        assert tool.annotations.read_only_hint is True
        assert tool.annotations.open_world_hint is False

    triage_schema = next(
        tool.input_schema for tool in tools if tool.name == "triage_artifact_metadata"
    )
    artifact_type_schema = triage_schema["properties"]["artifact_type"]
    hash_schema = triage_schema["properties"]["sha256"]["anyOf"][0]
    assert artifact_type_schema["minLength"] == 1
    assert artifact_type_schema["maxLength"] == 64
    assert hash_schema["pattern"] == r"^[0-9a-fA-F]{64}$"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("size", "expected_error"),
    [(True, True), (False, True), ("123", True), (1.0, True), (0, False), (123, False)],
)
async def test_tool_boundary_requires_integer_artifact_size(size, expected_error) -> None:
    server = build_server(local_settings())
    arguments = {"artifact_type": "pe", "name": "synthetic", "size_bytes": size}
    if expected_error:
        with pytest.raises(ToolError, match="valid integer"):
            await server.call_tool("triage_artifact_metadata", arguments)
    else:
        result = await server.call_tool("triage_artifact_metadata", arguments)
        assert result.is_error is False
        assert result.structured_content["artifact"]["size_bytes"] == size


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("credential", "expected_status"),
    [(None, 401), ("invalid", 401), ("wrong-scope", 403), ("wrong-resource", 401), ("valid", 200)],
)
async def test_http_transport_enforces_bearer_scope_and_resource(
    monkeypatch, credential, expected_status
) -> None:
    async def verify(self, token):
        if token == "invalid":
            return None
        return AccessToken(
            token=token,
            client_id="example-client",
            scopes=[] if token == "wrong-scope" else ["zrepro:read"],
            resource="https://other.example.com/mcp"
            if token == "wrong-resource"
            else self.resource_url,
        )

    monkeypatch.setattr(IntrospectionTokenVerifier, "verify_token", verify)
    settings = Settings(
        host="0.0.0.0",
        port=8787,
        auth_mode="introspection",
        issuer_url="https://idp.example.com/",
        resource_url="https://mcp.example.com/mcp",
        introspection_url="https://idp.example.com/introspect",
        introspection_client_id="example-client",
        introspection_client_secret="REPLACE_ME",
        required_scope="zrepro:read",
        repo_root=ROOT,
    )
    settings.validate()
    app = build_server(settings).streamable_http_app(
        host=settings.host, json_response=True, stateless_http=True
    )
    headers = {"Accept": "application/json, text/event-stream"}
    if credential:
        headers["Authorization"] = f"Bearer {credential}"
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="https://mcp.example.com"
        ) as client,
    ):
        response = await client.post(
            "/mcp",
            headers=headers,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "synthetic-test", "version": "1.0"},
                },
            },
        )
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json()["result"]["serverInfo"]["name"] == "zRepro"
