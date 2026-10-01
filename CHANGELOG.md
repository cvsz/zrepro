# Changelog

All notable changes to this template/framework are documented here.

## [Unreleased]

### Added
- ZEAZ cross-agent engineering execution framework and reusable skills/playbooks.
- Evidence-driven artifact triage, static/dynamic, Android, Apple, Samsung and Knox analysis.
- Windows PE/COFF and Linux ELF specialist skills, agents and playbooks.
- Firmware/update-image specialist workflow.
- PDF/Office/document artifact analysis workflow.
- Memory-forensics specialist workflow.
- Protocol/interface reconstruction workflow.
- Safe bounded fuzzing guidance.
- Defensive detection-engineering skill.
- Machine-readable reverse-engineering evidence-report schema.
- Safe metadata-only fixture/report corpus across PE, ELF, Mach-O, APK, Samsung, Knox, firmware, document, memory, protocol and fuzzing domains.
- Machine-readable skill/version/risk catalog.
- Synthetic benchmark/reference scenario framework.
- Standard-library catalog/fixture/report/benchmark validator with CI tests.
- Reverse-engineering tool capability matrix.
- SPDX SBOM and source provenance for the validator.
- GitHub administration automation and repository rollout guidance.

### Changed
- Expanded the skill catalog into a validated capability graph.
- Added specialist routing for Windows, Linux, firmware, documents, memory, protocols and fuzzing.
- Added static-first handling and contained runtime requirements for untrusted artifacts.
- Added platform/device/build/management context requirements.
- Added Knox declared/assigned/effective/observed policy semantics.
- Updated `make validate-template` and CI to enforce RE catalog and evidence integrity.
- Corrected component repository identity to `cvsz/zrepro`.

### Fixed
- Corrected generated README link validation.
- Removed wording that could imply green CI alone establishes readiness.
- Clarified that imports, strings, permissions, entitlements and decompiler output do not alone prove runtime behavior.

### Security
- Added fail-closed repository administration verification.
- Added reverse-engineering containment rules and synthetic-only public fixtures.
- Excluded unauthorized account/device/DRM/enrollment/attestation/Verified Boot bypass, credential extraction, third-party production fuzzing, destructive flashing and uncontrolled propagation.
