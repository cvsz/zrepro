# Reverse-Engineering Evidence Report Schema

The machine-readable contract is [`schemas/re-evidence-report.schema.json`](../../../schemas/re-evidence-report.schema.json).

The schema standardizes:
- artifact identity and optional SHA-256;
- authorized objective and analysis environment;
- finding confidence: confirmed / probable / hypothesis;
- evidence kind and source;
- tool/version/method metadata;
- canonical ZEAZ evidence state;
- limitations and next evidence step.

The schema intentionally does not turn tool output into a verified claim. A report remains only as strong as the evidence referenced by it.

The repository validator evaluates the schema keywords used by this contract with the Python standard library. It fails closed on unsupported schema keywords; schema extensions must update the validator and include regression coverage.
