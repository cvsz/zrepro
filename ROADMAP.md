# Roadmap

zRepro remains a reusable engineering foundation while adding evidence-driven reverse-engineering capabilities.

## Foundation
- [x] Repository documentation/security/governance baseline
- [x] CI, Dependabot, release guidance and immutable Action pins
- [x] Repository/link validation and GitHub administration verification
- [x] ZEAZ cross-agent execution framework
- [x] Discovery-first skill/component/plugin catalog scaffold
- [x] Safe rollout guidance

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

The following are conditional on the generated repository or environment, not core zRepro completion gates:
- production-capable per-stack adapters
- end-to-end application fixtures for adopted stacks
- artifact signing/attestation when distributable artifacts exist
- container vulnerability scanning when container artifacts exist

## Future optional modules
- [ ] Language-specific starter packs
- [ ] Kubernetes/Helm starter packs
- [ ] OpenSSF Scorecard workflow
- [ ] richer benchmark metrics once representative executable-safe scenarios exist

Generated repositories should adopt only modules appropriate to authorization, stack, threat model and operating environment.
