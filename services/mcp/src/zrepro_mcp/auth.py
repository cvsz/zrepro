from __future__ import annotations

import time
from typing import Any

import httpx
from mcp.server.auth.provider import AccessToken, TokenVerifier


class IntrospectionTokenVerifier(TokenVerifier):
    """RFC 7662 verifier. The authorization server remains external to zRepro."""

    def __init__(
        self,
        *,
        endpoint: str,
        client_id: str,
        client_secret: str,
        resource_url: str,
        issuer_url: str,
        timeout: float = 5.0,
    ) -> None:
        self.endpoint = endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.resource_url = resource_url.rstrip("/")
        self.issuer_url = issuer_url.rstrip("/")
        self.timeout = timeout

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoint,
                    data={"token": token},
                    auth=(self.client_id, self.client_secret),
                    headers={"Accept": "application/json"},
                )
            response.raise_for_status()
            payload: dict[str, Any] = response.json()
        except (httpx.HTTPError, ValueError, TypeError):
            return None

        if payload.get("active") is not True:
            return None

        exp = payload.get("exp")
        if exp is not None and int(exp) <= int(time.time()):
            return None

        issuer = str(payload.get("iss", "")).rstrip("/")
        if issuer and issuer != self.issuer_url:
            return None

        aud = payload.get("aud", payload.get("resource"))
        audiences = [aud] if isinstance(aud, str) else list(aud or [])
        normalized = {str(item).rstrip("/") for item in audiences}
        if self.resource_url not in normalized:
            return None

        scope_value = payload.get("scope", "")
        scopes = scope_value.split() if isinstance(scope_value, str) else list(scope_value or [])
        client_id = str(payload.get("client_id") or payload.get("azp") or "")
        if not client_id:
            return None

        return AccessToken(
            token=token,
            client_id=client_id,
            scopes=scopes,
            expires_at=int(exp) if exp is not None else None,
            resource=self.resource_url,
            subject=str(payload["sub"]) if payload.get("sub") else None,
            claims={"iss": issuer} if issuer else None,
        )
