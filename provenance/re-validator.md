# RE Validator Provenance

Component: `scripts/validate_re_catalog.py`

Version: repository source at the exact Git commit under validation.

Build/distribution model:
- executed directly from checked-out repository source;
- not compiled or published as a standalone binary/package;
- Python standard library only;
- no third-party runtime dependencies;
- CI invocation is defined in `.github/workflows/ci.yml`;
- local invocation is defined in `Makefile` through `make validate-template`.

Integrity boundary:
- Git commit identity is the source provenance reference;
- GitHub Actions checkout is pinned to an immutable action SHA;
- the validator must run on the exact PR/release head used for a readiness claim.

If packaging or third-party dependencies are added later, replace this source-only provenance model with generated artifact provenance and dependency-resolved SBOM evidence.
