import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    auth_mode: str
    issuer_url: str | None
    resource_url: str | None
    introspection_url: str | None
    introspection_client_id: str | None
    introspection_client_secret: str | None
    required_scope: str
    repo_root: Path

    @classmethod
    def from_env(cls) -> "Settings":
        root = Path(os.environ.get("ZREPRO_ROOT", Path(__file__).resolve().parents[4])).resolve()
        value = cls(
            host=os.environ.get("ZREPRO_MCP_HOST", "127.0.0.1"),
            port=int(os.environ.get("ZREPRO_MCP_PORT", "8787")),
            auth_mode=os.environ.get("ZREPRO_MCP_AUTH_MODE", "local").lower(),
            issuer_url=os.environ.get("ZREPRO_MCP_ISSUER_URL"),
            resource_url=os.environ.get("ZREPRO_MCP_RESOURCE_URL"),
            introspection_url=os.environ.get("ZREPRO_MCP_INTROSPECTION_URL"),
            introspection_client_id=os.environ.get("ZREPRO_MCP_INTROSPECTION_CLIENT_ID"),
            introspection_client_secret=os.environ.get("ZREPRO_MCP_INTROSPECTION_CLIENT_SECRET"),
            required_scope=os.environ.get("ZREPRO_MCP_REQUIRED_SCOPE", "zrepro:read"),
            repo_root=root,
        )
        value.validate()
        return value

    def validate(self) -> None:
        if self.auth_mode not in {"local", "introspection"}:
            raise ValueError("ZREPRO_MCP_AUTH_MODE must be local or introspection")
        if self.auth_mode == "local" and self.host not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("local auth mode may bind only to loopback")
        if self.auth_mode == "introspection":
            required = {
                "ZREPRO_MCP_ISSUER_URL": self.issuer_url,
                "ZREPRO_MCP_RESOURCE_URL": self.resource_url,
                "ZREPRO_MCP_INTROSPECTION_URL": self.introspection_url,
                "ZREPRO_MCP_INTROSPECTION_CLIENT_ID": self.introspection_client_id,
                "ZREPRO_MCP_INTROSPECTION_CLIENT_SECRET": self.introspection_client_secret,
            }
            missing = [name for name, value in required.items() if not value]
            if missing:
                raise ValueError("missing production auth settings: " + ", ".join(missing))
        if not (self.repo_root / "catalog/re-skills.json").is_file():
            raise ValueError(f"invalid ZREPRO_ROOT: {self.repo_root}")
