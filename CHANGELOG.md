# Changelog

All notable changes to this template/framework are documented here.

## [Unreleased]

### Added
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
- Corrected generated README link validation.
- Removed wording that could imply green CI alone establishes readiness.
- Clarified that imports, strings, permissions, entitlements and decompiler output do not alone prove runtime behavior.

### Security
- Added fail-closed repository administration verification.
- Added reverse-engineering containment rules and synthetic-only public fixtures.
- Added advisory OpenSSF Scorecard scanning with least-privilege workflow permissions and non-publishing configuration.
- Explicitly documented that Scorecard v2.4.4's action commit pin does not digest-pin its internal container image.
- Excluded unauthorized account/device/DRM/enrollment/attestation/Verified Boot bypass, credential extraction, third-party production fuzzing, destructive flashing and uncontrolled propagation.
