from pathlib import Path

import pytest

from zrepro_mcp.config import Settings


def test_local_mode_refuses_public_bind() -> None:
    settings = Settings(
        host="0.0.0.0",
        port=8787,
        auth_mode="local",
        issuer_url=None,
        resource_url=None,
        introspection_url=None,
        introspection_client_id=None,
        introspection_client_secret=None,
        required_scope="zrepro:read",
        repo_root=Path("."),
    )
    with pytest.raises(ValueError, match="loopback"):
        settings.validate()
