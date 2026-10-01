---
name: zeaz-re-fuzzing
title: ZEAZ Safe Fuzzing Guidance
description: Safe bounded fuzzing workflow for authorized parsers, libraries and services in isolated test environments.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, fuzzing, testing, robustness]
supported_harnesses: [codex, claude, opencode]
risk_level: high
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Safe Fuzzing Guidance

## Purpose
Use fuzzing for robustness and vulnerability discovery only on explicitly authorized targets and isolated test environments.

## Preconditions
- target/source/binary is authorized;
- execution is isolated and disposable;
- resource/time limits are defined;
- production endpoints/data are excluded;
- crash artifacts are treated as potentially sensitive.

## Workflow
1. Select the smallest input boundary and deterministic harness.
2. Seed with synthetic/minimal valid inputs.
3. Set CPU/memory/time/process/network limits.
4. Record tool/version, corpus hash/state and exact target build.
5. Deduplicate crashes and reproduce deterministically.
6. Minimize failing inputs and report root cause/evidence.
7. Add regression tests before considering a fix verified.

## Boundaries
Do not fuzz public/third-party production services without explicit authorization, do not amplify traffic, and do not weaponize discovered crashes.
