---
name: zeaz-re-dynamic
title: ZEAZ Dynamic Reverse Engineering
description: Contained runtime observation and debugging for authorized artifacts.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, dynamic-analysis, debugging, sandbox]
supported_harnesses: [codex, claude, opencode]
risk_level: high
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Dynamic Reverse Engineering

## Preconditions
Use only for authorized analysis in a disposable/restorable lab. Never execute an untrusted artifact directly on production systems or with real credentials.

## Preparation
1. Snapshot the lab and record OS/build/tool versions.
2. Establish baseline process, filesystem, configuration/registry and network state.
3. Decide network mode: disabled, simulated, or tightly controlled.
4. Prepare logging before execution.
5. Preserve the artifact hash and a copy of the original sample.

## Observation
Capture:
- process tree and module loads;
- file/configuration/registry changes;
- IPC and persistence-related changes;
- network destinations and protocol metadata;
- debugger breakpoints/traces relevant to the stated question;
- exceptions, crashes and anti-analysis divergence.

## Correlation
Map runtime events back to static functions/imports/strings where possible. Treat behavior not reproducible across runs as provisional until explained.

## Stop conditions
Stop if isolation fails, destructive impact exceeds the lab, or the environment can no longer produce trustworthy evidence.

## Output
Timeline, reproducible observations, static↔dynamic correlation, environment limitations and sanitized evidence references.
