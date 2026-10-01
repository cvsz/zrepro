# Roadmap

zRepro remains a reusable engineering foundation while adding evidence-driven reverse-engineering capabilities.

## Foundation
- [x] Repository documentation/security/governance baseline
- [x] CI, Dependabot, release guidance and immutable Action pins
- [x] Repository/link validation and GitHub administration verification
- [x] ZEAZ cross-agent execution framework
- [x] Discovery-first skill/component/plugin catalog scaffold
- [x] Safe rollout guidance
- [x] Language adoption starter packs: Python, Node.js/TypeScript, Go, Rust
- [x] Kubernetes/Helm adoption starter pack
- [x] OpenSSF Scorecard advisory workflow

## AI / MCP service
- [x] Streamable HTTP MCP service using the current official Python SDK
- [x] Read-only zRepro tool surface for status, routing, skill retrieval and evidence validation
- [x] Loopback-only unauthenticated local mode
- [x] Production OAuth resource-server mode using RFC 7662 token introspection
- [x] Required-scope and resource/audience validation
- [x] Non-root digest-pinned container definition
- [x] MCP unit tests and required CI integration
- [x] Production deployment/security contract documentation
- [ ] Live HTTPS/OAuth/rate-limit/monitoring evidence from an actual deployed environment
- [ ] Tenant/subject authorization policy when multi-tenant storage or jobs are introduced
- [ ] Controlled worker execution surface for explicitly authorized dynamic-analysis jobs

## Reverse-engineering framework
- [x] Artifact triage and evidence contract
- [x] Static and contained dynamic analysis
- [x] Android/mobile analysis
- [x] Defensive detection engineering
- [x] Orchestrator, static analyst and runtime analyst
- [x] Unified routing/playbook

## Platform and artifact specialists
- [x] Apple macOS/iOS/iPadOS/Mach-O
- [x] Samsung Galaxy/One UI
- [x] Samsung Knox/KPE/EMM/MDM/attestation
- [x] Windows PE/COFF
- [x] Linux ELF
- [x] Embedded/firmware
- [x] PDF/Office/document artifacts
- [x] Memory forensics
- [x] Protocol/interface reconstruction
- [x] Safe fuzzing guidance

## Validation and automation
- [x] Canonical skill frontmatter validation
- [x] Exactly-once component registration validation
- [x] Agent/playbook Markdown-link validation
- [x] Safe metadata-only fixture corpus
- [x] Deterministic evidence-report schema
- [x] Sample reports across supported fixture domains
- [x] Tool capability/version-discipline matrix
- [x] Validator SBOM and source provenance
- [x] CI execution of catalog/fixture/report validation
- [x] Machine-readable catalog/version/risk index
- [x] Benchmark/reference scenario framework

## Reusable project startup
- [x] Identity bootstrap with dry-run/apply/idempotence
- [x] Ownership/security replacement
- [x] Optional project profiles/adoption guide
- [x] Bootstrap tests
- [x] Repository administration verification helper

The following remain conditional on the generated repository or actual artifact/deployment set, not core zRepro completion gates:
- production-capable per-stack implementation
- end-to-end application fixtures for the adopted stack
- artifact signing/attestation when distributable artifacts exist
- container vulnerability scanning when container artifacts exist
- richer benchmark metrics when representative executable-safe scenarios exist
- live MCP deployment evidence (TLS, IdP, rate limiting, observability, rollback)

Generated repositories should adopt only modules appropriate to authorization, stack, threat model and operating environment.
