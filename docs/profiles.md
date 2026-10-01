# Project Profiles

Profiles are adoption guides, not production-ready starter applications. Every generated project must replace placeholders and verify its own runtime/security/operations.

## Common baseline for every profile
- initialize identity with `scripts/bootstrap.py`
- run `make validate-template`
- configure real CODEOWNERS/security contacts
- apply and verify GitHub administration controls
- customize CI/security checks for the real stack
- replace placeholder Dockerfile/Makefile application targets
- complete architecture/development/release documentation
- establish rollback and recovery evidence appropriate to the system

## Language adoption packs
Use only when the generated repository actually uses the language:
- [Python](../starter-packs/python/README.md)
- [Node.js / TypeScript](../starter-packs/node/README.md)
- [Go](../starter-packs/go/README.md)
- [Rust](../starter-packs/rust/README.md)

These packs define adoption gates, not a preselected framework.

## Service / API
Add runtime pinning, deterministic dependency installation, contract tests, authn/authz tests, migration handling, health/readiness, deployment/rollback, observability and backup/restore where stateful.

## Web application
Add frontend build/lint/typecheck/test, browser/E2E coverage, accessibility checks, session/CSRF/security headers, backend integration verification and deployment/monitoring evidence.

## Library / SDK
Add supported runtime matrix, compatibility tests, packaging validation, version/deprecation policy and artifact provenance/signing when applicable.

## Monorepo
Add workspace-aware change detection, ownership boundaries, dependency graph validation and release/version policy without hiding required cross-package integration tests.

## Infrastructure / platform
Add IaC formatting/validation/plan checks, ownership boundaries, least-privilege credentials, approvals, rollback/failover/recovery and drift detection.

For Kubernetes deployments, use the [Kubernetes / Helm starter pack](../starter-packs/kubernetes-helm/README.md).

Choose the smallest profile that matches the product. Do not add modules merely for checklist completeness.
