# About zRepro

zRepro is a reusable engineering and reverse-engineering foundation maintained under the `cvsz` namespace.

## Focus

- secure repository foundations
- AI/agent execution contracts
- evidence-driven engineering
- static and dynamic reverse engineering
- binary and bytecode analysis
- Android/mobile analysis
- Apple platform analysis
- Samsung Galaxy / One UI analysis
- Samsung Knox enterprise integration analysis
- defensive detection engineering
- reproducible validation and CI/security governance

## Engineering philosophy

zRepro is designed around:

- explicit authorization
- secure-by-default operation
- least privilege
- static-first analysis
- containment for untrusted runtime execution
- reproducible tooling
- evidence-backed claims
- modular reusable skills
- testable and reviewable change sets
- explicit uncertainty
- separation of implementation, verification, deployment and production readiness

Security/quality failures should be fixed rather than bypassed.

## Reverse-engineering philosophy

The framework converts reverse-engineering knowledge into reusable agent workflows instead of treating a tool list as a methodology.

For material findings, preserve:
- artifact identity/hash;
- tool/version;
- analysis method;
- evidence location;
- confidence;
- environment/platform context;
- unresolved assumptions.

Capability metadata does not equal runtime behavior. Examples include imports, strings, permissions, entitlements, SDK references and decompiler output.

## Platform scope

Current specialist layers:
- generic native/static analysis
- dynamic runtime analysis
- Android/mobile
- Apple macOS/iOS/iPadOS
- Samsung Galaxy / One UI
- Samsung Knox / KPE / EMM / MDM / attestation
- defensive detection engineering

## Safety boundaries

The project does not grant authorization to bypass account, device-ownership, DRM, enrollment, enterprise policy, attestation, Verified Boot, or similar protections.

Dynamic analysis must use an authorized contained environment with test-only data and credentials.

## Template direction

zRepro still includes the reusable repository/template foundation:
- governance and ownership
- security policy
- protected change flow
- CI/security automation
- dependency maintenance
- release/recovery guidance
- architecture documentation
- AI-agent operating contracts
- evidence-state semantics
- repository administration verification
- safe rollout guidance

The framework itself does not make a generated system production ready. Readiness remains evidence-based and environment-specific.

## GitHub

- Repository namespace: `github.com/cvsz`
- Project: `cvsz/zrepro`

---

This document intentionally contains public-safe technical/project information only. Credentials, private account data, personal secrets, enterprise keys, sensitive device data and private samples must not be added to the public repository.
