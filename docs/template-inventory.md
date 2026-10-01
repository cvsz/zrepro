# Repository Template Inventory

zRepro provides a secure reusable baseline for new GitHub projects and a reference baseline for hardening existing repositories.

## Governance and community
- `AGENTS.md`, `README.md`, `ABOUT.md`
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `GOVERNANCE.md`, `SECURITY.md`
- issue/PR templates and CODEOWNERS

## Repository automation and security
- baseline CI
- CodeQL
- Dependency Review
- Dependabot
- OpenSSF Scorecard advisory workflow
- immutable SHA pins for baseline Actions
- least-privilege workflow permissions
- `scripts/validate_repo.py`
- `scripts/github_admin.py`
- protected-branch/security-setting read-back verification
- [Scorecard configuration and supply-chain note](security/openssf-scorecard.md)

## AI/agent and reverse-engineering layer
- `ZEAZ-INTRODUCTION.md`
- `docs/ai/`
- `skills/`
- `components.d/`
- `catalog/re-skills.json`
- `benchmarks/re/`
- `fixtures/re/`
- `schemas/re-evidence-report.schema.json`
- `.agents/skills/scrutinize/SKILL.md`

## Starter packs
- `starter-packs/python/`
- `starter-packs/node/`
- `starter-packs/go/`
- `starter-packs/rust/`
- `starter-packs/kubernetes-helm/`

Starter packs are adoption guidance, not production-ready applications.

## Engineering lifecycle
- `CHANGELOG.md`
- `ROADMAP.md`
- `IMPLEMENTATION-CHECKLIST.md`
- architecture/development/release/ADR documentation
- Cloudflare/Terraform ownership contract
- repository rollout guide
- Dockerfile / Makefile / environment example

## Project initialization
- `scripts/bootstrap.py`
- `tests/test_bootstrap.py`
- `templates/project-readme.md`
- `templates/project-about.md`
- `docs/startup.md`
- `docs/profiles.md`

Application Makefile targets intentionally fail until customized instead of reporting false success.

## Adoption principle
For a new project, inherit the baseline then customize it. For an existing project, audit first and port only compatible missing controls. Never copy production credentials into a generated or migrated repository.
