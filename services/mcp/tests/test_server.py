import asyncio
from pathlib import Path

from zrepro_mcp.config import Settings
from zrepro_mcp.core import TOOL_CATALOG
from zrepro_mcp.server import build_server

ROOT = Path(__file__).resolve().parents[3]


def test_registered_tools_match_catalog_and_are_read_only() -> None:
    settings = Settings(
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

    tools = asyncio.run(build_server(settings).list_tools())

    assert [tool.name for tool in tools] == [item["name"] for item in TOOL_CATALOG]
    for tool, metadata in zip(tools, TOOL_CATALOG, strict=True):
        assert tool.title == metadata["title"]
        assert tool.description == metadata["description"]
        assert tool.annotations.read_only_hint is True
        assert tool.annotations.open_world_hint is False

    triage_schema = next(tool.input_schema for tool in tools if tool.name == "triage_artifact_metadata")
    artifact_type_schema = triage_schema["properties"]["artifact_type"]
    hash_schema = triage_schema["properties"]["sha256"]["anyOf"][0]
    assert artifact_type_schema["minLength"] == 1
    assert artifact_type_schema["maxLength"] == 64
    assert hash_schema["pattern"] == r"^[0-9a-fA-F]{64}$"
