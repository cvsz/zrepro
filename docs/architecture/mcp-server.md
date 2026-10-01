# zRepro MCP Server

The MCP service is a production-oriented, read-only AI gateway over the evidence-driven zRepro framework.

## Trust boundary

```text
AI client
  -> HTTPS / Streamable HTTP
  -> OAuth 2.1 bearer validation
  -> zRepro MCP tools
  -> canonical catalog / skills / evidence schema
```

The deployed HTTP service is an OAuth resource server. It does not issue tokens. Production mode uses RFC 7662 token introspection against an external authorization server and requires the `zrepro:read` scope by default.

Local mode deliberately has no HTTP authentication and is therefore restricted in code to loopback binding only.

## Exposed tools

- `server_status`
- `list_capabilities`
- `triage_artifact_metadata`
- `validate_evidence_report`
- `get_skill`

This initial production surface is intentionally read-only. It does **not** expose shell execution, arbitrary file reads, credential extraction, dynamic execution, flashing, bypass workflows, or uncontrolled fuzzing.

## Run locally

```bash
cd services/mcp
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
ZREPRO_ROOT=../.. zrepro-mcp
```

The endpoint is `http://127.0.0.1:8787/mcp`.

## Production configuration

Required:
- HTTPS termination before the service
- `ZREPRO_MCP_AUTH_MODE=introspection`
- public `ZREPRO_MCP_RESOURCE_URL`
- external issuer URL
- RFC 7662 introspection endpoint
- client credentials supplied from a secret manager, never committed
- network policy/rate limiting at the ingress or API gateway
- structured platform logs and alerting
- container/image vulnerability scanning in the deployment pipeline

The MCP Python SDK's Streamable HTTP transport is the deployment transport and its authorization model treats the MCP server as an OAuth resource server. zRepro follows that model rather than embedding a login/authorization server.

## Production readiness state

Repository code can verify fail-closed configuration and tool behavior. A deployment is not production-verified until live evidence confirms TLS, token rejection/acceptance, rate limiting, tenant/subject authorization policy, monitoring, rollback, and the target environment's incident/DR requirements.

No generated project inherits a production-ready claim solely by using this service.
