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

            if payload.get("active") is not True:
                return None

            exp_raw = payload.get("exp")
            exp = int(exp_raw) if exp_raw is not None else None
            if exp is not None and exp <= int(time.time()):
                return None

            issuer_raw = payload.get("iss", "")
            if issuer_raw is not None and not isinstance(issuer_raw, str):
                return None
            issuer = issuer_raw.rstrip("/")
            if issuer and issuer != self.issuer_url:
                return None

            aud = payload.get("aud", payload.get("resource"))
            if isinstance(aud, str):
                audiences = [aud]
            elif isinstance(aud, list) and all(isinstance(item, str) for item in aud):
                audiences = aud
            else:
                return None
            normalized = {item.rstrip("/") for item in audiences}
            if self.resource_url not in normalized:
                return None

            scope_value = payload.get("scope", "")
            if isinstance(scope_value, str):
                scopes = scope_value.split()
            elif isinstance(scope_value, list) and all(isinstance(item, str) for item in scope_value):
                scopes = scope_value
            else:
                return None

            client_id_value = payload.get("client_id") or payload.get("azp")
            if not isinstance(client_id_value, str) or not client_id_value:
                return None

            subject_value = payload.get("sub")
            if subject_value is not None and not isinstance(subject_value, str):
                return None
        except (httpx.HTTPError, ValueError, TypeError, OverflowError):
            return None

        return AccessToken(
            token=token,
            client_id=client_id_value,
            scopes=scopes,
            expires_at=exp,
            resource=self.resource_url,
            subject=subject_value,
            claims={"iss": issuer} if issuer else None,
        )
