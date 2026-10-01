# OpenSSF Scorecard Workflow

zRepro runs an advisory OpenSSF Scorecard scan on the default branch and on a weekly schedule.

## Configuration
- Scorecard Action: `ossf/scorecard-action` v2.4.4 commit `2d1146689b8cda280b9bc96326124645441f03bc`.
- `publish_results: false` — zRepro does not publish results to the Scorecard service from this workflow.
- SARIF is uploaded to GitHub Code Scanning.
- Workflow permissions are limited to repository read access plus `security-events: write` for SARIF upload.
- Checkout does not persist credentials.

## Supply-chain limitation

The upstream v2.4.4 `action.yaml` is a Docker action whose runtime image is referenced as:

```text
ghcr.io/ossf/scorecard-action:v2.4.4
```

Therefore pinning the GitHub Action to a commit SHA does **not** independently pin the underlying container image digest. Treat this as a known upstream supply-chain limitation and re-evaluate when upstream changes its runtime reference or provides a digest-pinned consumption path.

Scorecard findings are advisory evidence. A score is not a production-readiness verdict.
