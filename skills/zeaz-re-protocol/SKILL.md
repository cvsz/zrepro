---
name: zeaz-re-protocol
title: ZEAZ Protocol Interface Reconstruction
description: Evidence-driven reconstruction of authorized protocols and interfaces for interoperability, debugging and compatibility.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, protocol, interoperability, network, ipc]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Protocol Interface Reconstruction

## Purpose
Reconstruct authorized network/IPC/file interfaces for interoperability and debugging without bypassing authentication or access controls.

## Workflow
1. Define endpoint/interface scope and authorization.
2. Capture or inspect message framing, fields, state transitions, serialization and error behavior.
3. Correlate static implementation clues with controlled traces.
4. Separate observed protocol facts from inferred field semantics.
5. Produce a versioned interface model with examples using synthetic/test data.

## Evidence rules
- One capture may represent one path/version only.
- Field meaning is hypothesis until corroborated.
- Authentication/authorization behavior must be documented, not bypassed.
