---
name: zeaz-re-detection
title: ZEAZ Reverse Engineering Detection Engineering
description: Convert verified reverse-engineering observations into defensive indicators and detections.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, yara, detection, incident-response]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Reverse Engineering Detection Engineering

## Purpose
Produce defensive detection material only from verified artifact characteristics and observed behavior.

## Inputs
Use evidence from triage/static/dynamic analysis. Require artifact hashes and provenance of each indicator when available.

## Workflow
1. Separate stable identifiers from environment-specific noise.
2. Prefer multi-feature detections over fragile single strings.
3. Avoid secrets, personal data and customer-specific identifiers.
4. For YARA-like detections, select distinctive static features and document expected false positives.
5. For behavioral detections, describe observable events and required telemetry rather than assuming sensor coverage.
6. Validate against known-good samples when available.
7. Version the rule and evidence set.

## Output
- detection intent;
- rule/indicator;
- evidence mapping;
- expected false positives / negatives;
- validation status;
- maintenance trigger.

Do not label an artifact malicious solely because it matches one weak indicator.
