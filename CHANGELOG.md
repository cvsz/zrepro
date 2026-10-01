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
- Artifact triage skill with authorization, hashing and evidence-state requirements.
- Static binary/bytecode reverse-engineering skill.
- Contained dynamic-analysis skill with explicit lab preconditions and stop conditions.
- Android/mobile reverse-engineering skill.
- Defensive detection-engineering skill.
- Apple platform reverse-engineering skill, analyst and playbook for Mach-O, macOS/iOS/iPadOS bundles, code signing, entitlements, Objective-C and Swift.
- Samsung platform reverse-engineering skill, analyst and playbook for Galaxy/One UI packages, Samsung frameworks/services and ARM/ARM64 native libraries.
- Samsung Knox reverse-engineering skill, analyst and playbook for Knox SDK/KPE, EMM/MDM policy state and attestation-flow analysis.
- Component-catalog and skill-finder routing for Apple, Samsung and Knox specialists.

### Changed

- Reorganized reusable AI documentation into `agents/`, `guides/`, `playbooks/`, and `prompts/`.
- Expanded skill catalog into a reverse-engineering capability graph rather than a flat resource list.
- Added static-first routing for untrusted artifacts.
- Added platform-specific evidence requirements for OS/device/model/build/management context.
- Added Knox policy-state distinction: declared, assigned, effective and observed.
- Pinned baseline first-party GitHub Actions to immutable commit SHAs.
- Expanded CODEOWNERS coverage for repository policy, AI, skills, components, and plugin manifests.
- Clarified that release-note configuration is not an artifact-publishing workflow.
- Documented branch/security administration as an explicit evidence gate rather than a documentation-only checklist.

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
