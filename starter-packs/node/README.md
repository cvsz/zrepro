# Node.js / TypeScript Starter Pack

Adoption guide for Node.js/TypeScript projects generated from zRepro.

Recommended baseline:
- pin supported Node LTS/runtime version;
- commit the package-manager lockfile;
- TypeScript strict mode where applicable;
- lint/format/typecheck/test/build gates;
- browser/E2E tests for user-facing web apps;
- dependency and supply-chain review;
- safe environment-variable schema;
- runtime health/readiness and observability for services.

Use `npm ci`, `pnpm --frozen-lockfile`, or the equivalent deterministic install mode selected by the project.
