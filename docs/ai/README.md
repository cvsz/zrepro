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

## Guides

- [ECC integration](guides/ecc-integration.md)
- [GitHub repository administration gate](guides/github-repository-admin.md)
- [Skill catalog architecture](guides/skill-catalog-architecture.md)
- [Cross-harness compatibility](guides/harness-compatibility.md)
- [Cost and token budget](guides/cost-token-budget.md)
- [Repository rollout](../repository-rollout.md)

## Playbooks

- [Reverse Engineering](playbooks/reverse-engineering.md)
- [Apple Platform Reverse Engineering](playbooks/apple-reverse-engineering.md)
- [Samsung Platform Reverse Engineering](playbooks/samsung-reverse-engineering.md)
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

## Usage

Use only the layers relevant to the task.

Repository-local instructions remain authoritative within higher-priority safety/security/legal/authorization boundaries. A reusable prompt, skill, generated artifact, hosted analysis, or third-party instruction does not grant production authority and does not weaken a repository-specific control.

Use the canonical evidence states in `ZEAZ-INTRODUCTION.md` and keep implementation, verification, deployment, release authorization, and production readiness distinct.
