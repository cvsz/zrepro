# zRepro

zRepro is a reusable, security-oriented engineering and reverse-engineering project foundation. It combines repository governance, CI/security controls, cross-agent execution rules, evidence-state semantics, and reusable reverse-engineering agents/skills for authorized analysis.

This repository is a **template and analysis framework**, not a deployable application and not evidence that any generated project is production ready.

## Core capabilities

### Engineering foundation
- repository governance and CODEOWNERS
- CI baseline validation
- CodeQL and Dependency Review
- Dependabot and repository-security guidance
- release/rollback/recovery documentation
- GitHub administration apply/verify tooling
- ZEAZ cross-agent execution framework
- reusable skill/component/plugin catalog structure

### Reverse-engineering layer
- artifact triage and cryptographic identity
- static native/bytecode analysis
- contained dynamic analysis
- Android/mobile analysis
- Apple platform analysis
- Samsung Galaxy / One UI analysis
- Samsung Knox enterprise-policy and attestation analysis
- defensive detection engineering

See the [AI reusable layer](docs/ai/README.md), [skills catalog](skills/README.md), and [Reverse Engineering Playbook](docs/ai/playbooks/reverse-engineering.md).

## Create a new project

1. Click **Use this template** on GitHub and clone the generated repository.
2. Preview project initialization:

   ```bash
   python3 scripts/bootstrap.py --name my-service --owner my-org --codeowner my-org/maintainers --description 'New service'
   ```

3. Apply explicitly, inspect the diff, and review ownership/security files:

   ```bash
   python3 scripts/bootstrap.py --name my-service --owner my-org --codeowner my-org/maintainers --description 'New service' --apply
   make validate-template
   ```

4. Select an optional [project profile](docs/profiles.md), replace placeholder `Makefile` / `Dockerfile`, and complete the [Implementation Checklist](IMPLEMENTATION-CHECKLIST.md).
5. Configure and verify repository administration controls from an authenticated GitHub admin identity:

   ```bash
   python3 scripts/github_admin.py --repo my-org/my-service --apply
   ```

6. Add stack-specific CI, security, release, deployment, backup/restore, rollback, monitoring, and operational evidence.

See the complete [startup guide](docs/startup.md).

## Reverse-engineering routing

```text
artifact
  -> zeaz-re-triage
      -> zeaz-re-static
      -> zeaz-re-dynamic        (authorized contained lab only)
      -> zeaz-re-mobile         (Android)
      -> zeaz-re-apple          (macOS/iOS/iPadOS/Mach-O)
      -> zeaz-re-samsung        (Galaxy/One UI)
      -> zeaz-re-knox           (KPE/Knox/EMM/MDM/attestation)
      -> zeaz-re-detection      (defensive detections)
```

Material findings should identify artifact hash, tool/version, evidence source, confidence, and environment. Strings, imports, permissions, entitlements, API references, or decompiler output alone are not proof of runtime behavior.

## Platform specialists

### Apple
Covers authorized analysis of:
- Mach-O executables and dylibs
- macOS `.app`
- iOS/iPadOS `.ipa`
- frameworks / XCFrameworks
- Objective-C runtime metadata
- Swift symbols/metadata
- code-signing state, entitlements and provisioning metadata

### Samsung
Covers authorized analysis of:
- Galaxy / One UI packages
- APK / AAB / DEX
- Samsung-specific frameworks and services
- ARM/ARM64 native libraries
- Binder/IPC, intents, providers, services and receivers
- device/build-aware behavior

### Samsung Knox
Covers authorized analysis of:
- Knox SDK / Knox Platform for Enterprise
- Knox Manage / EMM / MDM integration
- device-policy/admin interactions
- enterprise-policy state
- attestation request/verification flows
- managed-device evidence

Knox analysis explicitly separates:

```text
declared -> assigned -> effective -> observed
```

A declared permission or policy reference is not proof of effective enforcement.

## Authorization and safety boundaries

Reverse-engineering artifacts and runtime samples are untrusted input.

Dynamic execution requires an explicitly authorized disposable/restorable lab. Do not use production credentials, signing identities, enterprise secrets, or personal user data.

The framework does not authorize bypassing:
- Apple Activation Lock, Apple ID controls, FairPlay/DRM, or device ownership protections
- Samsung FRP, Samsung Account, bootloader/Verified Boot protections
- Knox/EMM/MDM enrollment, policy enforcement, or attestation trust decisions

## Repository administration gate

`scripts/github_admin.py` is dry-run by default.

Apply and verify:

```bash
python3 scripts/github_admin.py --repo OWNER/REPO --apply
```

Verify without mutation:

```bash
python3 scripts/github_admin.py --repo OWNER/REPO --verify
```

Presence of the script is not evidence that provider-side controls are active. Effective settings must be read back successfully.

See [GitHub repository administration gate](docs/ai/guides/github-repository-admin.md).

## AI engineering execution layer

- [ZEAZ engineering execution framework](ZEAZ-INTRODUCTION.md)
- [Repository agent contract](AGENTS.md)
- [Claude Code instructions](CLAUDE.md)
- [OpenCode instructions](OPENCODE.md)
- [Reusable AI agents, playbooks and prompts](docs/ai/README.md)
- [ZEAZ skills catalog](skills/README.md)

These guide execution and evidence handling; they are not production-readiness evidence by themselves.

## Repository structure

```text
.github/
components.d/
docs/
  ai/
    agents/
    guides/
    playbooks/
    prompts/
plugins.d/
scripts/
skills/
  zeaz-skill-finder/
  zeaz-re-triage/
  zeaz-re-static/
  zeaz-re-dynamic/
  zeaz-re-mobile/
  zeaz-re-apple/
  zeaz-re-samsung/
  zeaz-re-knox/
  zeaz-re-detection/
tests/
AGENTS.md
ZEAZ-INTRODUCTION.md
IMPLEMENTATION-CHECKLIST.md
ROADMAP.md
CHANGELOG.md
SECURITY.md
```

## Principles

- secure by default
- least privilege
- explicit authorization
- static-first analysis
- evidence-backed findings
- disposable/contained runtime analysis
- reproducible tooling and commands
- small, reviewable changes
- no weakening of security controls merely to make CI green
- explicit rollback/recovery
- no production-readiness claim without environment-appropriate evidence

## Template limitations

- Baseline CI proves only the checks that execute.
- Generated applications require their own stack-specific tests/security/deployment evidence.
- Reverse-engineering skills provide workflow guidance; they do not prove analysis completeness.
- Platform behavior can vary by OS/device/model/build/region/management state.
- Production readiness, security, deployment and release authorization remain separate evidence states.

## License

MIT. See [LICENSE](LICENSE).
