# Rust Starter Pack

Adoption guide for Rust applications/libraries generated from zRepro.

Recommended baseline:
- pin supported stable toolchain;
- commit `Cargo.lock` for applications;
- `cargo fmt --check`;
- `cargo clippy` with project policy;
- unit/integration tests;
- dependency/advisory review;
- reproducible release builds;
- SBOM/provenance for distributed artifacts.

Unsafe code, FFI and privileged platform integrations require explicit review and targeted tests.
