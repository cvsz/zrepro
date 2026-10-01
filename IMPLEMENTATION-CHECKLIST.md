# Implementation Checklist

Use this checklist after creating a repository from zRepro, when porting the baseline into an existing repository, or when enabling reverse-engineering capabilities.

## Bootstrap

- [ ] Create the new repository with **Use this template** when independent history is desired.
- [ ] Preview and apply `scripts/bootstrap.py` with the actual name, owner, code owner, and description.
- [ ] Review identity/ownership changes and commit `.ztemplate-initialized.json` as nonsecret setup evidence.
- [ ] Run `make validate-template`.
- [ ] Choose a project profile in `docs/profiles.md` and record non-goals.
- [ ] Confirm README and ABOUT describe the real project.

## Repository identity

- [ ] Replace template identity/placeholders with the real project.
- [ ] Confirm license choice and preserve required attribution.
- [ ] Configure repository description, topics, homepage, visibility, and template status as applicable.

## Ownership and governance

- [ ] Update `.github/CODEOWNERS`.
- [ ] Review `CONTRIBUTING.md`, `GOVERNANCE.md`, and `CODE_OF_CONDUCT.md`.
- [ ] Apply repository administration controls with an authenticated admin identity.
- [ ] Verify effective controls:

  ```bash
  python3 scripts/github_admin.py --repo OWNER/REPO --verify
  ```

- [ ] Require pull-request review and CODEOWNERS approval.
- [ ] Require passing checks and conversation resolution.
- [ ] Block force pushes and protected-branch deletion.
- [ ] Document break-glass process.

## Reverse-engineering authorization and evidence

- [ ] Record the exact authorized objective and non-goals.
- [ ] Confirm the operator is authorized to inspect each artifact/device/environment.
- [ ] Treat samples, firmware, packages, logs and generated output as untrusted.
- [ ] Record SHA-256 for artifacts when bytes are available.
- [ ] Record provenance/source when known.
- [ ] Record tool and version for material findings.
- [ ] Classify findings as confirmed / probable / hypothesis.
- [ ] Separate static evidence from runtime evidence.
- [ ] Do not treat strings, imports, permissions, entitlements, API references or decompiler output as runtime proof.
- [ ] Preserve reproduction commands/steps without exposing secrets.

## Dynamic-analysis lab

- [ ] Use a disposable/restorable VM, emulator, test device or isolated environment.
- [ ] Capture a baseline/snapshot before executing untrusted artifacts.
- [ ] Decide network mode before launch: disabled, simulated or tightly controlled.
- [ ] Use test-only credentials, certificates and data.
- [ ] Do not attach production secrets or signing identities.
- [ ] Record OS/device/build/tooling state.
- [ ] Define stop conditions for containment failure or destructive behavior.
- [ ] Correlate runtime observations back to static evidence where possible.

## Apple platform analysis

- [ ] Record Mach-O architecture(s) and hashes.
- [ ] Inspect load commands, segments/sections, linked dylibs/frameworks and rpaths.
- [ ] Record bundle identifier, version and build.
- [ ] Inspect `Info.plist`.
- [ ] Inspect signing state, entitlements and provisioning metadata as applicable.
- [ ] Inspect Objective-C runtime metadata/selectors where present.
- [ ] Inspect Swift symbols/metadata and demangle where useful.
- [ ] Distinguish entitlement presence from observed capability use.
- [ ] Do not bypass Activation Lock, Apple ID, FairPlay/DRM or device ownership protections.

## Samsung platform analysis

- [ ] Record package/version/signing metadata.
- [ ] Record exact Galaxy model, region/carrier where relevant, Android version, One UI version and security patch for runtime evidence.
- [ ] Inspect manifest permissions/components and exported surfaces.
- [ ] Separate standard Android behavior from Samsung/One UI-specific behavior.
- [ ] Identify Samsung frameworks/services and Binder/IPC integration.
- [ ] Inspect ARM/ARM64 native libraries where present.
- [ ] Do not bypass FRP, Samsung Account, bootloader or Verified Boot protections.

## Samsung Knox analysis

- [ ] Identify Knox SDK/KPE/enterprise service dependencies.
- [ ] Record Knox-related permissions and policy APIs.
- [ ] Identify management mode/environment.
- [ ] Maintain separate policy states: declared / assigned / effective / observed.
- [ ] Record exact Knox/Android/One UI/device context for runtime evidence.
- [ ] For attestation, document challenge/nonce, parsing and verification flow without weakening trust decisions.
- [ ] Do not bypass Knox enrollment, EMM/MDM policy, attestation or enterprise controls.
- [ ] Do not extract enterprise credentials, certificates or private keys.

## Detection engineering

- [ ] Build detections only from verified evidence.
- [ ] Prefer multiple stable features over one weak string/indicator.
- [ ] Document expected false positives and false negatives.
- [ ] Avoid customer-specific secrets or personal data.
- [ ] Validate against known-good/synthetic fixtures when available.
- [ ] Version rule and evidence set.

## Security

- [ ] Configure private vulnerability reporting.
- [ ] Enable Dependabot alerts/security updates.
- [ ] Review CodeQL language support.
- [ ] Keep dependency review enabled where supported.
- [ ] Enable secret scanning/push protection where available.
- [ ] Add applicable SAST/container/IaC/SBOM/provenance/signing checks.
- [ ] Confirm Actions permissions follow least privilege.
- [ ] Confirm fork PRs cannot access unsafe secrets/write tokens.

## Development and validation

- [ ] Add formatter/linter/type-checker configuration as appropriate.
- [ ] Add unit/integration/E2E tests for executable helper code.
- [ ] Add machine-readable validation for skill metadata.
- [ ] Validate that skill catalog/component registration is synchronized.
- [ ] Validate all local Markdown links.
- [ ] Use safe synthetic/non-malicious fixture artifacts for automated tests.
- [ ] Avoid checking real sensitive samples into the public repository.

## CI/CD

- [ ] Customize CI for the selected stack.
- [ ] Pin runtime versions.
- [ ] Add real lint/test/build/security validation.
- [ ] Configure artifact retention/provenance where needed.
- [ ] Validate CI from pull requests and protected default branch.

## Release and operations

- [ ] Maintain `CHANGELOG.md`.
- [ ] Publish from trusted workflows only.
- [ ] Add artifact signing/attestation where appropriate.
- [ ] Document known-good rollback.
- [ ] Define health/readiness checks for executable services.
- [ ] Configure logs/metrics/traces where applicable.
- [ ] Perform backup/restore and DR verification for stateful services.
- [ ] Define incident-response ownership.

## Documentation

- [ ] Keep `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `skills/README.md`, `docs/ai/README.md`, playbooks and component manifests synchronized.
- [ ] Add ADRs for material architecture/security decisions.
- [ ] Document supported platforms and known evidence limitations.
- [ ] Document operational ownership/support expectations.

## Final verification

- [ ] Fresh clone works with documented setup.
- [ ] Repository validator passes.
- [ ] Required CI/security checks pass on the exact release head.
- [ ] Protected-branch/admin verification succeeds.
- [ ] No secrets/private data or sensitive real-world samples are committed.
- [ ] Every applicable readiness/evidence gate uses the canonical ZEAZ evidence state.
- [ ] No production-ready/security claim is made solely from documentation or green template CI.

A green template CI run alone is never sufficient to claim application or analysis production readiness.
