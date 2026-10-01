# Python Service Starter Pack

Adoption guide for a generated zRepro repository using Python.

Recommended baseline:
- Python 3.12+ pinned in CI/runtime;
- `pyproject.toml` as the project metadata/configuration source;
- deterministic dependency locking;
- formatter/linter/type checking;
- unit + integration tests;
- dependency/security scanning;
- application-specific Dockerfile/Makefile targets;
- health/readiness and observability for services.

Suggested CI gates:

```text
format-check -> lint -> typecheck -> unit -> integration -> build -> security
```

Do not copy credentials into configuration. Generated projects must choose their actual package manager/framework and validate deployment/recovery separately.
