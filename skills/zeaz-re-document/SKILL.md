---
name: zeaz-re-document
title: ZEAZ Document Artifact Analysis
description: Safe evidence-driven analysis of authorized PDF, Office, archive and document-like artifacts.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, document, pdf, office, archive]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Document Artifact Analysis

## Purpose
Analyze authorized document/container artifacts statically first and avoid opening untrusted active content in normal desktop applications.

## Workflow
1. Hash the artifact and identify container/file format.
2. Inventory metadata, embedded objects, scripts/macros, links, forms, attachments and compression layers.
3. Extract or decode suspicious components without executing them.
4. Correlate indicators across container structure and embedded content.
5. If runtime observation is necessary, use a disposable isolated document-analysis VM.

## Evidence rules
- Embedded script does not prove it executed.
- A URL does not prove a network connection occurred.
- Document metadata can be spoofed and should not be treated as identity proof.
