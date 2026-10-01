# ZEAZ AI Reusable Layer

## Base
- [ZEAZ-INTRODUCTION.md](../../ZEAZ-INTRODUCTION.md)
- [AGENTS.md](../../AGENTS.md)
- [CLAUDE.md](../../CLAUDE.md)
- [OPENCODE.md](../../OPENCODE.md)

## Agents
- [Reverse Engineering Orchestrator](agents/reverse-engineering-orchestrator.md)
- [Static Binary Analyst](agents/static-binary-analyst.md)
- [Runtime Behavior Analyst](agents/runtime-behavior-analyst.md)
- [Apple Platform Reverse Engineering Analyst](agents/apple-platform-analyst.md)
- [Samsung Platform Reverse Engineering Analyst](agents/samsung-platform-analyst.md)
- [Samsung Knox Platform Analyst](agents/knox-platform-analyst.md)
- [Windows PE Analyst](agents/windows-pe-analyst.md)
- [Linux ELF Analyst](agents/linux-elf-analyst.md)
- [Firmware Analyst](agents/firmware-analyst.md)
- [Document Artifact Analyst](agents/document-artifact-analyst.md)
- [Memory Forensics Analyst](agents/memory-forensics-analyst.md)
- [Protocol Reconstruction Analyst](agents/protocol-reconstruction-analyst.md)

## Guides
- [ECC integration](guides/ecc-integration.md)
- [GitHub repository administration gate](guides/github-repository-admin.md)
- [Skill catalog architecture](guides/skill-catalog-architecture.md)
- [Cross-harness compatibility](guides/harness-compatibility.md)
- [Cost and token budget](guides/cost-token-budget.md)
- [Reverse-engineering tool capability matrix](guides/tool-capability-matrix.md)
- [Reverse-engineering evidence report schema](guides/evidence-report-schema.md)
- [Reverse-engineering validator supply-chain note](guides/re-validator-supply-chain.md)
- [Repository rollout](../repository-rollout.md)

## Playbooks
- [Reverse Engineering](playbooks/reverse-engineering.md)
- [Windows PE Reverse Engineering](playbooks/windows-pe-reverse-engineering.md)
- [Linux ELF Reverse Engineering](playbooks/linux-elf-reverse-engineering.md)
- [Apple Platform Reverse Engineering](playbooks/apple-reverse-engineering.md)
- [Samsung Platform Reverse Engineering](playbooks/samsung-reverse-engineering.md)
- [Samsung Knox Reverse Engineering](playbooks/knox-reverse-engineering.md)
- [Firmware Reverse Engineering](playbooks/firmware-reverse-engineering.md)
- [Document Artifact Analysis](playbooks/document-artifact-analysis.md)
- [Memory Forensics](playbooks/memory-forensics.md)
- [Protocol Reconstruction](playbooks/protocol-reconstruction.md)
- [Safe Fuzzing](playbooks/safe-fuzzing.md)
- [Repository Production Readiness](playbooks/repository-production-readiness.md)
- [Security Audit](playbooks/security-audit.md)
- [Incident Response](playbooks/incident-response.md)
- [SaaS Release](playbooks/saas-release.md)
- [Kubernetes](playbooks/kubernetes.md)
- [GitHub PR / CI Recovery](playbooks/github-pr-ci-recovery.md)
- [CI Failure Modes](playbooks/ci-failure-modes.md)
- [Autonomous Repository Upgrade](playbooks/autonomous-repo-upgrade.md)

## Reusable prompts
- [Repository execution](prompts/repository.md)
- [Code review](prompts/code-review.md)
- [Architecture review](prompts/architecture.md)
- [Testing](prompts/testing.md)
- [DevOps / SRE](prompts/devops.md)

## Validation surfaces
- `catalog/re-skills.json` — machine-readable skill/version/risk index.
- `benchmarks/re/scenarios.json` — synthetic reference scenarios.
- `fixtures/re/` — metadata-only safe fixture corpus.
- `schemas/re-evidence-report.schema.json` — evidence-report contract.

Use only the layers relevant to the task. Repository-local instructions remain authoritative within higher-priority safety/security/legal/authorization boundaries.
