# Changelog

All notable changes to this template/framework are documented here.

## [Unreleased]

### Added
- Production-oriented MCP gateway under `services/mcp` using Streamable HTTP.
- Read-only MCP tools for service status, capability discovery, artifact metadata routing, canonical skill retrieval and evidence-report validation.
- Fail-closed local/remote configuration: unauthenticated mode is loopback-only; remote mode requires OAuth resource-server configuration and RFC 7662 introspection.
- Required MCP tests in the protected `repository-baseline` CI context.
- Non-root, digest-pinned MCP container definition and deployment contract.
- ZEAZ cross-agent engineering execution framework and validated reverse-engineering skill catalog.
- Platform/artifact specialists for Windows PE, Linux ELF, Android, Apple, Samsung, Knox, firmware, documents, memory, protocols and safe fuzzing.
- Machine-readable RE evidence schema, catalog index, synthetic fixtures/reports and benchmark/reference scenarios.
- Reverse-engineering validator with CI tests, SBOM and provenance.
- Language adoption starter packs for Python, Node.js/TypeScript, Go and Rust.
- Kubernetes/Helm adoption starter pack.
- OpenSSF Scorecard advisory workflow using official v2.4.4 commit pin, SARIF artifact upload and GitHub Code Scanning upload.
- Scorecard supply-chain note documenting the upstream mutable container-tag limitation.
- GitHub administration automation and repository rollout guidance.

### Changed
- Expanded the skill catalog into a validated capability graph.
- Added specialist routing for platform, firmware, document, memory, protocol and fuzzing domains.
- Added static-first handling and contained runtime requirements for untrusted artifacts.
- Added platform/device/build/management context requirements.
- Updated `make validate-template` and CI to enforce RE catalog/evidence integrity.
- Extended project profile guidance with starter-pack references.

### Fixed
- Rejected malformed introspection responses without an unhandled verifier exception.
- Matched MCP fuzzing metadata routing to the canonical reference scenario.
- Required integer artifact sizes at the MCP boundary instead of silently coercing booleans, strings, or floats.
- Updated generated security-policy routing, preserved distinct CODEOWNERS tokens, and restored bootstrap outputs after caught write failures.
- Rejected invalid catalog shapes and domains, and excluded generated dependency documents from source-link validation.
- Explicitly targeted GitHub.com in the repository administration helper.
- Corrected generated README link validation.
- Removed wording that could imply green CI alone establishes readiness.
- Clarified that imports, strings, permissions, entitlements and decompiler output do not alone prove runtime behavior.

### Security
- Excluded local credential files and generated dependencies from Docker build contexts, with an executable synthetic context regression test.
- Extended the existing protected CodeQL check to Python and enabled the repository's security-extended query configuration.
- Checked tracked environment-file variants and private-key filenames using null-delimited Git index output, with placeholder examples allowed.
- Refreshed pip before CI dependency installation and documented the same local setup step.
- MCP remote mode validates bearer tokens through external RFC 7662 introspection, required scopes and resource binding.
- MCP local mode refuses non-loopback binding.
- MCP tool surface intentionally excludes arbitrary command execution, credential extraction, bypass operations, uncontrolled fuzzing and dynamic execution.
- Added fail-closed repository administration verification.
- Added reverse-engineering containment rules and synthetic-only public fixtures.
- Added advisory OpenSSF Scorecard scanning with least-privilege workflow permissions and non-publishing configuration.
- Explicitly documented that Scorecard v2.4.4's action commit pin does not digest-pin its internal container image.
- Excluded unauthorized account/device/DRM/enrollment/attestation/Verified Boot bypass, credential extraction, third-party production fuzzing, destructive flashing and uncontrolled propagation.
