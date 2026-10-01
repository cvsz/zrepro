---
name: zeaz-re-firmware
title: ZEAZ Firmware Reverse Engineering
description: Evidence-driven analysis of authorized firmware images, embedded filesystems, boot metadata and update packages.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, firmware, embedded, boot, filesystem]
supported_harnesses: [codex, claude, opencode]
risk_level: high
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Firmware Reverse Engineering

## Purpose
Analyze authorized firmware/update images without modifying or flashing real devices unless separately approved.

## Workflow
1. Hash the original image and preserve a read-only copy.
2. Identify container/update format, architecture, partition/filesystem boundaries and compression.
3. Inventory bootloaders, kernels, root filesystems, services, configs, certificates and update metadata.
4. Trace trust/update verification paths and externally exposed interfaces.
5. Prefer offline extraction/emulation; device execution requires an isolated owned test device and recovery path.

## Evidence rules
- Extracted config does not prove active runtime state.
- Embedded credentials/certificates must be handled as secrets and not published.
- A boot/update verification path must be distinguished from an actual bypass.

## Boundaries
Do not provide unauthorized secure-boot bypass, device-lock bypass, credential extraction, or destructive flashing procedures.
