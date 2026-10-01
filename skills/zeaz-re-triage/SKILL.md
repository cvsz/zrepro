---
name: zeaz-re-triage
title: ZEAZ Reverse Engineering Triage
description: Safely identify an artifact, define authorization and choose the smallest reverse-engineering workflow.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, triage, binary-analysis, evidence]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Reverse Engineering Triage

## Purpose
Establish scope, artifact identity, evidence handling and the least-risk analysis path before deeper analysis.

## Workflow
1. Record the authorized objective and non-goals.
2. Compute/record cryptographic hashes when artifact bytes are available.
3. Identify file/container type, architecture, platform and packaging.
4. Record provenance if known; do not treat filenames as identity.
5. Inspect metadata, signatures and obvious dependencies.
6. Decide whether static analysis is sufficient.
7. Permit dynamic analysis only when contained execution is justified and available.
8. Create an evidence ledger with confirmed / probable / hypothesis states.

## Routing
- native executable/library -> `zeaz-re-static`
- APK/AAB/DEX/mobile package -> `zeaz-re-mobile`
- runtime-only question -> `zeaz-re-dynamic` after static triage
- defensive signature/indicator request -> `zeaz-re-detection` after evidence verification

## Output
Artifact identity, authorization assumptions, risk notes, selected skills, evidence plan and stop conditions.
