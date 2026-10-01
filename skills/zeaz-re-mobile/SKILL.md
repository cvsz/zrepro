---
name: zeaz-re-mobile
title: ZEAZ Mobile Reverse Engineering
description: Authorized static and contained runtime analysis of Android application packages.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, android, apk, dex, mobile]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Mobile Reverse Engineering

## Purpose
Analyze Android APK/AAB/DEX structure, application behavior and interfaces for compatibility, debugging, incident response or security review.

## Static workflow
- record package hash and signing metadata;
- inspect manifest, permissions, exported components and intent filters;
- inspect DEX/classes/resources/native libraries;
- identify endpoints, schemas, serialization and SDK dependencies;
- compare Java/Kotlin decompilation with bytecode/native evidence when claims matter.

## Dynamic workflow
Use an emulator/test device with disposable test data. Observe only what is necessary for the scoped question and correlate runtime events to components identified statically.

## Constraints
Do not bypass account controls, payment/access controls, device ownership protections, or third-party authorization boundaries. Do not use real user credentials in analysis labs.

## Output
Package/component map, permissions/exposure summary, relevant call paths, runtime evidence when authorized, and unresolved assumptions.
