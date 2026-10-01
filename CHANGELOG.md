# Changelog

All notable changes to this template/framework are documented here.

The format follows Keep a Changelog conventions; generated projects should adopt an explicit versioning policy appropriate to their product.

## [Unreleased]

### Added

- Safe project identity bootstrap with explicit dry-run/apply and idempotence tests.
- Generated README/ABOUT templates and startup/profile documentation.
- CI bootstrap test coverage and fail-closed Makefile placeholders.
- ZEAZ cross-agent engineering execution framework.
- Claude Code and OpenCode adapters.
- Reusable AI guides, playbooks, prompts, skills, component manifests, and plugin-source manifests.
- Repository structure and local Markdown-link validator.
- GitHub administration automation with dry-run, explicit apply, and read-back verification.
- Repository rollout guidance for applying the baseline safely to existing repositories.
- Evidence-driven reverse-engineering orchestration and reusable specialist skills.
- Artifact triage, static, contained dynamic, Android/mobile, Apple, Samsung, Knox, and defensive-detection skills.
- Apple, Samsung, and Knox specialist agents/playbooks.
- Machine-readable reverse-engineering evidence-report schema.
- Safe metadata-only synthetic fixture corpus for PE, ELF, Mach-O, APK, Samsung One UI, and Knox.
- Sample evidence-report fixtures for the supported synthetic artifact classes.
- Standard-library reverse-engineering catalog/fixture/report validator with unit-test and CI integration.
- Reverse-engineering tool capability/version-discipline matrix.
- SPDX SBOM and source-provenance note for the repository-local validator.

### Changed

- Reorganized reusable AI documentation into `agents/`, `guides/`, `playbooks/`, and `prompts/`.
- Expanded the skill catalog into a validated reverse-engineering capability graph.
- Added static-first routing for untrusted artifacts.
- Added platform-specific evidence requirements for OS/device/model/build/management context.
- Added Knox policy-state distinction: declared, assigned, effective and observed.
- Updated `make validate-template` and CI to validate the RE catalog, fixtures, reports and supply-chain evidence.
- Corrected the engineering component manifest repository identity from `cvsz/ztemplate` to `cvsz/zrepro`.
- Pinned baseline first-party GitHub Actions to immutable commit SHAs.
- Expanded CODEOWNERS coverage for repository policy, AI, skills, components, and plugin manifests.

### Fixed

- Corrected generated README link validation so template links are resolved from their generated root location.
- Removed stale wording that could imply green CI or configuration files alone establish production readiness.
- Removed ambiguity that imports, strings, permissions, entitlements, API references or decompiler output alone prove runtime behavior.

### Security

- Added fail-closed repository-administration verification.
- Added protected-branch controls for required reviews/checks, conversation resolution, force-push prevention, and deletion prevention.
- Added documented verification for Dependabot, private vulnerability reporting, secret scanning/push protection, and least-privilege Actions permissions where supported.
- Added reverse-engineering containment rules for untrusted artifacts and dynamic execution.
- Explicitly excluded bypass of Apple Activation Lock/Apple ID/FairPlay, Samsung FRP/Samsung Account, Knox enrollment/policy/attestation, unauthorized bootloader/Verified Boot controls, and credential/private-key extraction.
