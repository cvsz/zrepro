# Safe Synthetic Reverse-Engineering Fixtures

This directory contains metadata-only synthetic fixtures for validating zRepro workflows.

Rules:
- no executable or malicious bytes;
- no real credentials, certificates, device identifiers, customer data, or proprietary samples;
- every JSON fixture must set `safe_synthetic: true`;
- every JSON fixture must set `contains_executable_bytes: false`;
- expected observations describe what a parser/agent should classify, not runtime behavior.

The fixtures exercise platform routing and evidence semantics without distributing binaries.
