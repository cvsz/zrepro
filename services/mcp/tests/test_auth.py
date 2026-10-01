import pytest

from zrepro_mcp.auth import IntrospectionTokenVerifier


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self):
        return self.payload


class FakeClient:
    def __init__(self, payload):
        self.payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def post(self, *args, **kwargs):
        return FakeResponse(self.payload)


@pytest.mark.asyncio
async def test_malformed_exp_is_rejected(monkeypatch) -> None:
    payload = {
        "active": True,
        "exp": "not-an-integer",
        "iss": "https://idp.example.com/",
        "aud": "https://mcp.example.com/mcp",
        "scope": "zrepro:read",
        "client_id": "client",
        "sub": "user-1",
    }

    monkeypatch.setattr(
        "zrepro_mcp.auth.httpx.AsyncClient",
        lambda **kwargs: FakeClient(payload),
    )

    verifier = IntrospectionTokenVerifier(
        endpoint="https://idp.example.com/oauth2/introspect",
        client_id="service",
        client_secret="secret",
        resource_url="https://mcp.example.com/mcp",
        issuer_url="https://idp.example.com/",
    )

    assert await verifier.verify_token("token") is None
