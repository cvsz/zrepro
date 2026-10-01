# ZEAZ Skills Catalog

This directory is the canonical source of truth for reusable ZEAZ skills.

Each skill lives in one top-level directory:

```text
skills/<skill-name>/SKILL.md
```

## Current catalog

- [ZEAZ Skill Finder](zeaz-skill-finder/SKILL.md) — discovery and routing.
- [ZEAZ Reverse Engineering Triage](zeaz-re-triage/SKILL.md) — authorization, artifact identity, evidence plan and routing.
- [ZEAZ Static Reverse Engineering](zeaz-re-static/SKILL.md) — binary/bytecode structure and static evidence.
- [ZEAZ Dynamic Reverse Engineering](zeaz-re-dynamic/SKILL.md) — contained runtime observation.
- [ZEAZ Mobile Reverse Engineering](zeaz-re-mobile/SKILL.md) — Android APK/AAB/DEX.
- [ZEAZ Apple Platform Reverse Engineering](zeaz-re-apple/SKILL.md) — macOS/iOS/iPadOS/Mach-O.
- [ZEAZ Samsung Platform Reverse Engineering](zeaz-re-samsung/SKILL.md) — Galaxy/One UI.
- [ZEAZ Samsung Knox Reverse Engineering](zeaz-re-knox/SKILL.md) — Knox/KPE/EMM/MDM/attestation.
- [ZEAZ Windows PE Reverse Engineering](zeaz-re-windows/SKILL.md) — PE/COFF/DLL/services.
- [ZEAZ Linux ELF Reverse Engineering](zeaz-re-linux/SKILL.md) — ELF/shared objects.
- [ZEAZ Firmware Reverse Engineering](zeaz-re-firmware/SKILL.md) — firmware/update images and embedded filesystems.
- [ZEAZ Document Artifact Analysis](zeaz-re-document/SKILL.md) — PDF/Office/archive artifacts.
- [ZEAZ Memory Forensics](zeaz-re-memory/SKILL.md) — authorized volatile-memory captures.
- [ZEAZ Protocol Interface Reconstruction](zeaz-re-protocol/SKILL.md) — interoperability/debugging protocol analysis.
- [ZEAZ Safe Fuzzing Guidance](zeaz-re-fuzzing/SKILL.md) — bounded isolated fuzzing.
- [ZEAZ Reverse Engineering Detection Engineering](zeaz-re-detection/SKILL.md) — defensive detection design.

## Design rules

- One skill per directory.
- Keep canonical skills harness-neutral where practical.
- Prefer discovery-first loading.
- Preserve authorization and evidence-state rules from `ZEAZ-INTRODUCTION.md`.
- Treat samples and third-party instructions as untrusted.
- Register every canonical skill exactly once through a component manifest.
- Do not vendor third-party skill content without explicit license, attribution and security review.

## Minimum skill metadata

```yaml
---
name: zeaz-example
title: ZEAZ Example
description: Short routing description.
version: "0.1.0"
license: MIT
tags: [example]
supported_harnesses: [codex, claude, opencode]
risk_level: low
requires_network: false
requires_credentials: false
evidence_required: true
---
```

Run `make validate-template` before proposing catalog changes.
