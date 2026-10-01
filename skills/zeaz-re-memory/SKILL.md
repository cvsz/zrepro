---
name: zeaz-re-memory
title: ZEAZ Memory Forensics
description: Evidence-driven analysis of authorized memory captures for incident response, debugging and provenance investigation.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, memory, forensics, incident-response]
supported_harnesses: [codex, claude, opencode]
risk_level: high
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Memory Forensics

## Purpose
Analyze authorized volatile-memory captures while protecting secrets and personal data that may be present.

## Workflow
1. Record capture hash, acquisition method, source OS/build and acquisition time.
2. Preserve original capture read-only.
3. Inventory processes, modules, handles, sockets, mappings and relevant kernel/user artifacts.
4. Correlate suspicious memory observations with filesystem/log/network evidence when available.
5. Minimize extraction and redact secrets/private data from reports.

## Evidence rules
- Memory residue may be stale or incomplete.
- Process/module presence does not prove maliciousness.
- Attribution requires corroborating evidence.

## Boundaries
Do not extract or disclose credentials, session tokens, private keys or unrelated personal data beyond the authorized investigation need.
