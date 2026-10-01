# Reverse-Engineering Reference Scenarios

This benchmark layer validates routing/evidence semantics using safe metadata-only fixtures. It is not a malware benchmark and contains no executable samples.

Each scenario declares:
- source fixture;
- expected skill route;
- required evidence concept;
- forbidden inference.

CI validates scenario references and skill names through `scripts/validate_re_catalog.py`.
