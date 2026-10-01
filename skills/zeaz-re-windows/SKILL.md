---
name: zeaz-re-windows
title: ZEAZ Windows PE Reverse Engineering
description: Evidence-driven analysis of authorized Windows PE/COFF executables, DLLs, services and application artifacts.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, windows, pe, coff, dll]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Windows PE Reverse Engineering

## Purpose
Analyze authorized Windows PE/COFF artifacts using static-first evidence and contained runtime validation when necessary.

## Workflow
1. Record SHA-256, PE type, architecture, signer/version metadata and provenance.
2. Inspect PE headers, sections, imports/exports, resources, TLS callbacks, relocations and debug metadata.
3. Identify services, COM/registry/configuration references, IPC and persistence-related code paths without assuming execution.
4. Correlate strings/imports/symbols with xrefs and control flow.
5. Use contained Windows VM/runtime tracing only when the scoped question requires it.

## Evidence rules
- Imports do not prove invocation.
- Service/registry strings do not prove installation or persistence.
- Signature presence and signature validity are separate claims.
- Decompiled code is reconstructed logic.

## Boundaries
Do not use this skill to obtain unauthorized access, credential theft, persistence on third-party systems, evasion, destructive payload execution, or uncontrolled propagation.
