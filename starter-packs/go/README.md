# Go Service Starter Pack

Adoption guide for Go services/libraries generated from zRepro.

Recommended baseline:
- pin supported Go version;
- maintain `go.mod` / `go.sum`;
- `gofmt`/format verification;
- `go vet` and project-selected static analysis;
- unit/integration tests and race testing where relevant;
- reproducible binary/container build;
- SBOM/provenance for distributed binaries;
- health/readiness, structured logging and metrics for services.

Do not claim cross-platform compatibility until each target is built and tested.
