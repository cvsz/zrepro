# zRepro

zRepro is a reusable, security-oriented engineering and reverse-engineering project foundation. It combines repository governance, CI/security controls, cross-agent execution rules, evidence-state semantics, reusable reverse-engineering agents/skills, validation fixtures, starter packs, and supply-chain checks.

This repository is a **template and analysis framework**, not a deployable application and not evidence that a generated project is production ready.

## Core capabilities

### Engineering foundation
- repository governance and CODEOWNERS
- CI baseline validation
- CodeQL, Dependency Review and Dependabot
- advisory OpenSSF Scorecard workflow
- release/rollback/recovery guidance
- GitHub administration apply/verify tooling
- ZEAZ cross-agent execution framework
- reusable skill/component/plugin catalog structure
- Python, Node.js/TypeScript, Go and Rust adoption starter packs
- Kubernetes/Helm adoption starter pack

### Reverse-engineering layer
- artifact triage and cryptographic identity
- static and contained dynamic analysis
- Windows PE/COFF and Linux ELF
- Android/mobile
- Apple macOS/iOS/iPadOS/Mach-O
- Samsung Galaxy/One UI
- Samsung Knox/KPE/EMM/MDM/attestation
- firmware/update images
- PDF/Office/document artifacts
- memory forensics
- protocol/interface reconstruction
- safe bounded fuzzing
- defensive detection engineering
- machine-readable skill catalog, evidence schema, synthetic fixtures/reports and reference scenarios

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
5. Configure and verify repository administration controls:

   ```bash
   python3 scripts/github_admin.py --repo my-org/my-service --apply
   ```

6. Add stack-specific CI, security, release, deployment, backup/restore, rollback, monitoring, and operational evidence.

See the [startup guide](docs/startup.md).

## Starter packs

- [Python](starter-packs/python/README.md)
- [Node.js / TypeScript](starter-packs/node/README.md)
- [Go](starter-packs/go/README.md)
- [Rust](starter-packs/rust/README.md)
- [Kubernetes / Helm](starter-packs/kubernetes-helm/README.md)

Starter packs are adoption guidance, not production-ready applications.

## Reverse-engineering routing

```text
artifact
  -> zeaz-re-triage
      -> zeaz-re-static
      -> zeaz-re-dynamic
      -> zeaz-re-windows
      -> zeaz-re-linux
      -> zeaz-re-mobile
      -> zeaz-re-apple
      -> zeaz-re-samsung
      -> zeaz-re-knox
      -> zeaz-re-firmware
      -> zeaz-re-document
      -> zeaz-re-memory
      -> zeaz-re-protocol
      -> zeaz-re-fuzzing
      -> zeaz-re-detection
```

Material findings should identify artifact hash, tool/version, evidence source, confidence, and environment. Strings, imports, permissions, entitlements, API references, or decompiler output alone are not proof of runtime behavior.

## Validation surfaces

- `schemas/re-evidence-report.schema.json`
- `catalog/re-skills.json`
- `fixtures/re/`
- `benchmarks/re/scenarios.json`
- `scripts/validate_re_catalog.py`

`make validate-template` validates repository links/structure, the RE catalog, fixtures/reports/reference scenarios, and repository tests.

## OpenSSF Scorecard

zRepro includes an advisory Scorecard workflow. Results are not published to the Scorecard service and SARIF is uploaded to GitHub Code Scanning.

See [OpenSSF Scorecard configuration](docs/security/openssf-scorecard.md). The upstream v2.4.4 action currently references its runtime container using a mutable tag, so the action commit pin does not independently digest-pin the runtime image.

## Authorization and safety boundaries

Reverse-engineering artifacts and runtime samples are untrusted input. Dynamic execution requires an explicitly authorized disposable/restorable lab. Do not use production credentials, signing identities, enterprise secrets, or unrelated personal data.

The framework does not authorize bypassing account/device ownership, DRM, enrollment/MDM, attestation, Verified Boot or equivalent protections; destructive flashing; unauthorized credential extraction; third-party production fuzzing; or uncontrolled propagation.

## Repository administration gate

`scripts/github_admin.py` is dry-run by default.

```bash
python3 scripts/github_admin.py --repo OWNER/REPO --verify
```

Presence of the script is not evidence provider-side controls are active. Effective settings must be read back successfully.

## Principles

- secure by default
- least privilege
- explicit authorization
- static-first analysis
- contained runtime execution
- evidence-backed findings
- reproducible tooling
- immutable automation references where practical
- small, reviewable changes
- no weakening security controls merely to make CI green
- explicit rollback/recovery
- no production-readiness claim without environment-appropriate evidence

## Template limitations

- Green baseline CI proves only the checks that ran.
- Generated applications require stack-specific test/security/deployment evidence.
- Starter packs and skills are guidance, not readiness evidence.
- Platform behavior may vary by OS/device/model/build/region/management state.
- Artifact signing/attestation and container scanning become applicable only when the generated project produces those artifact types.

## License

MIT. See [LICENSE](LICENSE).
