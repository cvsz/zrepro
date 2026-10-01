# Roadmap

zRepro remains a reusable engineering foundation while adding evidence-driven reverse-engineering capabilities.

## Foundation

- [x] Repository documentation baseline
- [x] Security and contribution policies
- [x] Issue and pull request templates
- [x] CI and security workflow baseline
- [x] Dependabot configuration
- [x] Release guidance and release-note configuration
- [x] Immutable SHA pinning for baseline GitHub Actions
- [x] Repository structure and local Markdown-link validation
- [x] GitHub administration apply/verify automation
- [x] Protected-default-branch policy baseline
- [x] ZEAZ cross-agent execution framework
- [x] Reusable AI guides/playbooks/prompts
- [x] Discovery-first skills/component/plugin catalog scaffold
- [x] Safe rollout guidance for existing repositories

## Reverse-engineering framework

- [x] Artifact triage and evidence contract
- [x] Static reverse-engineering skill
- [x] Dynamic analysis skill with containment requirements
- [x] Android/mobile analysis skill
- [x] Defensive detection-engineering skill
- [x] Reverse Engineering Orchestrator agent
- [x] Static Binary Analyst agent
- [x] Runtime Behavior Analyst agent
- [x] Unified reverse-engineering playbook and routing

## Platform specialization

### Apple
- [x] macOS / iOS / iPadOS specialist skill
- [x] Mach-O / dylib / bundle analysis workflow
- [x] Objective-C and Swift metadata guidance
- [x] code-signing / entitlement / provisioning evidence rules
- [x] Apple Platform Analyst agent
- [x] Apple platform playbook

### Samsung
- [x] Galaxy / One UI specialist skill
- [x] Samsung framework/service differentiation
- [x] ARM/ARM64 native library workflow
- [x] device/build-aware evidence requirements
- [x] Samsung Platform Analyst agent
- [x] Samsung platform playbook

### Knox
- [x] Knox SDK / KPE specialist skill
- [x] Knox Manage / EMM / MDM routing
- [x] declared / assigned / effective / observed policy model
- [x] attestation analysis workflow
- [x] Knox Platform Analyst agent
- [x] Knox playbook

## Validation and automation next

- [ ] Add machine-readable schema validation for all canonical skill frontmatter
- [ ] Add CI test ensuring every skill is registered exactly once in component/catalog indexes
- [ ] Add CI test ensuring all agent/playbook links resolve
- [ ] Add reference fixture corpus containing only safe synthetic/non-malicious artifacts
- [ ] Add deterministic evidence-report schema
- [ ] Add sample report fixtures for PE/ELF/Mach-O/APK
- [ ] Add Apple bundle/Mach-O synthetic fixture validation
- [ ] Add Samsung APK/One UI integration fixture validation
- [ ] Add Knox policy-state synthetic fixture validation
- [ ] Add tool-capability matrix with version compatibility
- [ ] Add SBOM/provenance for executable helper tooling if helper code is introduced

## Reusable project startup

- [x] Identity bootstrap with dry-run, explicit apply, and idempotence
- [x] Safe ownership/security issue-link replacement
- [x] Optional project profiles and adoption guide
- [x] Bootstrap tests in baseline CI
- [x] Repository administration verification helper
- [ ] Validate production-capable per-stack adapters in generated repositories
- [ ] Add end-to-end fixture verification for each adopted stack

## Future optional modules

- [ ] Windows/PE specialist
- [ ] Linux/ELF specialist
- [ ] embedded/firmware specialist
- [ ] document/PDF/Office analysis specialist
- [ ] memory-forensics specialist
- [ ] protocol/interface reconstruction specialist
- [ ] safe fuzzing harness guidance
- [ ] language-specific starter packs
- [ ] Kubernetes/Helm starter packs
- [ ] release signing and artifact attestation
- [ ] OpenSSF Scorecard workflow
- [ ] container vulnerability scanning
- [ ] machine-readable catalog/version index at scale
- [ ] benchmark/reference-set framework

Generated repositories should adopt only modules appropriate to their scope, authorization, threat model, operating environment and compliance requirements.
