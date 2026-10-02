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

The service registers seven read-only tools:

- `server_status` — report mode, tool inventory, and catalog/schema versions.
- `list_capabilities` — list tools, routes, skills, and safety boundaries.
- `list_skills` — list canonical skills, optionally filtered by domain or risk level.
- `get_evidence_schema` — return the canonical evidence-report JSON Schema.
- `triage_artifact_metadata` — validate metadata and choose a specialist route without reading artifact bytes.
- `validate_evidence_report` — validate a bounded JSON report and return up to 50 errors.
- `get_skill` — return one skill selected by exact catalog name.

MCP clients receive parameter schemas from `tools/list`. `list_capabilities` provides the human-readable inventory. Restart the server and reconnect the client after tool registration changes to refresh the client's inventory.

This initial production surface is intentionally read-only. It routes metadata and retrieves catalogued documents; it does not inspect artifact bytes or perform dynamic tracing. RVA data is diagnostic-only and is not invoked by the application. It does **not** expose shell execution, arbitrary file reads, credential extraction, dynamic execution, flashing, bypass workflows, or uncontrolled fuzzing.

## Run locally

```bash
cd services/mcp
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip
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

## Container build context

Build the service image from the repository root with `docker build -f services/mcp/Dockerfile .`. The root `.dockerignore` excludes local environment files (including examples), private-key filenames, Git metadata, and generated dependency directories. `.gitignore` alone does not protect image contexts. Keep credentials in runtime secret injection.

The repository's synthetic Docker context test checks these exclusions without downloading a base image. It is skipped when Docker is unavailable; an executed passing result is required to claim that the build-context boundary was verified.
