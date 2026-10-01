---
name: zeaz-re-linux
title: ZEAZ Linux ELF Reverse Engineering
description: Evidence-driven analysis of authorized Linux ELF executables, shared objects and runtime interfaces.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, linux, elf, so, native]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Linux ELF Reverse Engineering

## Purpose
Analyze authorized ELF binaries and shared objects with reproducible static and contained runtime evidence.

## Workflow
1. Record SHA-256, ELF class, architecture, ABI, interpreter and provenance.
2. Inspect program/section headers, symbols, relocations, dynamic dependencies, RPATH/RUNPATH and notes.
3. Trace entry/init/fini routines and high-value exported/imported interfaces.
4. Correlate strings/configuration references with control/data flow.
5. Use a disposable Linux lab for runtime evidence only when static analysis is insufficient.

## Evidence rules
- Linked libraries do not prove called behavior.
- systemd/init/config references do not prove active deployment.
- Stripped/optimized binaries reduce semantic certainty.
- Runtime findings are environment/build-specific.
