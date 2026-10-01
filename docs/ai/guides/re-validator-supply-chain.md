# Reverse-Engineering Validator Supply-Chain Note

`scripts/validate_re_catalog.py` uses only the Python standard library and is executed from repository source in CI.

Current supply-chain state:
- no third-party Python packages;
- no separately published executable artifact;
- no runtime service/container;
- no embedded sample binaries;
- fixtures are JSON metadata only.

Therefore a separate package SBOM for the validator is currently **NOT APPLICABLE**. If the validator gains third-party dependencies or is packaged/distributed, add dependency lockfiles, SBOM generation, provenance and release integrity verification before treating that distribution as trusted.
