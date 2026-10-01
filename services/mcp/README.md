# zRepro MCP service

This package exposes the safe, evidence-oriented zRepro surface to MCP clients.

## Local development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
ZREPRO_ROOT=../.. zrepro-mcp
```

Connect to `http://127.0.0.1:8787/mcp`.

Local mode has no HTTP bearer authentication and is hard-restricted to loopback. It cannot be bound to `0.0.0.0`.

## Remote deployment

Set `ZREPRO_MCP_AUTH_MODE=introspection` and supply the issuer, resource URL, RFC 7662 introspection endpoint, introspection client credentials and required scope. Put TLS, rate limiting and network policy in front of the service.

Secrets must come from a secret manager or runtime environment, never source control.

## Validation

```bash
make validate-mcp
```

The protected repository CI also runs the same tests.

## Current execution boundary

The service is deliberately read-only. Dynamic analysis, fuzz campaigns, arbitrary file reads and shell execution are not exposed. Those require a future isolated worker/job system with explicit authorization, quotas, containment and evidence capture.
