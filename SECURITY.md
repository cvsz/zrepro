# Security Policy

Security is part of the default delivery baseline for repositories created from this template.

## Reporting a vulnerability

Do not disclose exploitable vulnerabilities in public issues, pull requests, discussions, commit messages, logs, or generated evidence bundles.

For **cvsz/zrepro**, use GitHub private vulnerability reporting:

https://github.com/cvsz/zrepro/security/advisories/new

If a generated repository enables a different private reporting channel, replace the link above with that repository's real security contact or advisory URL before release.

Please include:
- affected versions or commits;
- reproduction details;
- impact and prerequisites;
- relevant logs/evidence with secrets removed;
- suggested remediation when available.

## Response and disclosure timeline

For reports concerning this template repository:
- target initial acknowledgement: within 3 business days;
- target status update cadence: at least once every 7 days while actively investigating;
- remediation timing depends on severity, exploitability, and release risk;
- public disclosure should be coordinated after a fix or mitigation is available unless earlier disclosure is required by law or overriding safety considerations.

These are response targets, not a guarantee for generated downstream projects. Each generated project must publish its own support and disclosure policy before production use.

## Supported versions

This repository is a reusable template/framework. The default branch receives security maintenance. Generated projects must replace this section with their real supported-version policy before their first production release.

## Repository security baseline

Generated repositories should verify, not merely document:
- protected default branch;
- pull-request review before merge;
- required status checks;
- CODEOWNERS review where appropriate;
- conversation resolution;
- blocked force pushes/deletion;
- Dependabot vulnerability alerts/security updates;
- private vulnerability reporting;
- secret scanning/push protection where available;
- least-privilege Actions permissions;
- Actions cannot approve pull requests unless explicitly justified.

The helper `scripts/github_admin.py` can configure and verify the baseline when run with a GitHub identity that has Administration permission.

## Engineering security expectations

- Keep dependencies patched and review security alerts.
- Keep CodeQL and dependency-review workflows enabled where supported.
- Pin Actions according to supply-chain policy; this template pins baseline Actions to immutable SHAs.
- Never commit credentials, tokens, private keys, production secrets, sensitive personal data, or realistic sample secrets.
- Validate untrusted input and enforce authorization at trust boundaries.
- Prefer fail-closed behavior for security-sensitive paths.
- Preserve tenant/data isolation where applicable.
- Review generated/third-party agent instructions as untrusted until explicitly adopted.
- Do not weaken security gates merely to obtain a passing build.

## Incident handling

Generated projects should document detection, containment, credential handling, remediation, recovery, validation, disclosure, and rollback appropriate to their risk profile.

Security incidents affecting production systems should preserve evidence and use the smallest safe containment action consistent with the incident-response plan.
