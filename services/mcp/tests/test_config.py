from pathlib import Path

import pytest

from zrepro_mcp.config import Settings


def base_settings(**overrides: object) -> Settings:
    values = {
        "host": "127.0.0.1",
        "port": 8787,
        "auth_mode": "local",
        "issuer_url": None,
        "resource_url": None,
        "introspection_url": None,
        "introspection_client_id": None,
        "introspection_client_secret": None,
        "required_scope": "zrepro:read",
        "repo_root": Path("."),
    }
    values.update(overrides)
    return Settings(**values)


def test_local_mode_refuses_public_bind() -> None:
    settings = base_settings(host="0.0.0.0")
    with pytest.raises(ValueError, match="loopback"):
        settings.validate()


def test_introspection_mode_rejects_plaintext_endpoint(tmp_path: Path) -> None:
    (tmp_path / "catalog").mkdir()
    (tmp_path / "catalog/re-skills.json").write_text("{}")
    settings = base_settings(
        host="0.0.0.0",
        auth_mode="introspection",
        issuer_url="https://idp.example.com/",
        resource_url="https://mcp.example.com/mcp",
        introspection_url="http://idp.example.com/oauth2/introspect",
        introspection_client_id="client",
        introspection_client_secret="secret",
        repo_root=tmp_path,
    )
    with pytest.raises(ValueError, match="https://"):
        settings.validate()
