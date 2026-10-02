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
Restart the MCP server and reconnect the client after changing tool registrations so the client fetches the current `tools/list` result.

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

## Available tools

The server currently registers these seven read-only tools. `tools/list` is the protocol-level source for their input schemas; `list_capabilities` returns the same names and descriptions with the route and safety catalogs.

| Tool | Inputs | Purpose |
| --- | --- | --- |
| `server_status` | None | Return service mode, tool names/count, and catalog/schema versions. |
| `list_capabilities` | None | Return the tool inventory, analysis routes, skill catalog, and safety boundaries. |
| `list_skills` | Optional `domain`, `risk_level` | List catalogued skills, with exact domain and risk-level filters. |
| `get_evidence_schema` | None | Return the canonical JSON Schema for evidence reports. |
| `triage_artifact_metadata` | `artifact_type`, `name`; optional `sha256`, `size_bytes` | Validate metadata and select a specialist route. It never reads artifact bytes. |
| `validate_evidence_report` | `report` | Validate a JSON report up to 1,000,000 serialized bytes and return at most 50 errors. |
| `get_skill` | Exact catalogued `name` | Return one canonical skill document. |

Every tool advertises read-only and closed-world annotations. These are client hints; server-side validation and the fixed path allowlist enforce the actual boundary.
