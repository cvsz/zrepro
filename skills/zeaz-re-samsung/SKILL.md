---
name: zeaz-re-samsung
title: ZEAZ Samsung Platform Reverse Engineering
description: Evidence-driven analysis for authorized Samsung Galaxy / One UI applications, packages, native libraries and platform integrations.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, samsung, galaxy, one-ui, android, knox, apk, dex, arm64]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Samsung Platform Reverse Engineering

## Purpose
Analyze authorized Samsung/One UI software artifacts while distinguishing standard Android behavior from Samsung-specific frameworks and services.

## Artifact types
- APK / AAB / DEX
- Samsung/One UI application packages
- native `.so` libraries
- resources and configuration bundles
- firmware/package metadata supplied for analysis
- logs/traces from authorized Samsung test devices or emulators

## Static workflow

### 1. Identity
Record:
- SHA-256;
- package name;
- versionName/versionCode;
- signing certificate metadata;
- min/target SDK;
- CPU ABI(s);
- Samsung/Android/One UI provenance when known.

### 2. Android application surface
Inspect:
- `AndroidManifest.xml`;
- permissions;
- exported activities/services/receivers/providers;
- intent filters and deep links;
- content providers;
- network security configuration;
- resources/assets;
- DEX/classes;
- JNI/native libraries.

### 3. Samsung-specific surface
Identify and classify:
- Samsung-specific package/class namespaces;
- Samsung SDK/framework dependencies;
- One UI-specific APIs;
- Knox-related declarations/interfaces;
- Samsung account/service integrations;
- Samsung system-service or Binder interactions;
- device/model/build-specific feature gates.

Do not assume a namespace/API is active solely because it exists in the artifact.

### 4. Native analysis
For ARM/ARM64 native libraries:
- inspect ELF headers/segments;
- imports/exports/symbols;
- JNI registration;
- strings/resources;
- call paths around Samsung/platform integration points;
- compiler/obfuscation indicators.

### 5. Runtime workflow
Use only on an authorized disposable test device/emulator or isolated lab.

Record:
- exact model;
- Android version;
- One UI version;
- build number/security patch level;
- package version;
- observed process/service/component behavior;
- Binder/IPC, filesystem and network evidence relevant to the scoped question.

## Security boundaries
This skill does not authorize:
- FRP bypass;
- Samsung Account bypass;
- Knox enrollment/policy bypass;
- unauthorized bootloader/verified-boot bypass;
- extraction of user secrets or personal device data.

## Output
Report:
1. artifact/package identity;
2. standard Android component map;
3. Samsung/One UI-specific dependencies;
4. Knox-related metadata/interfaces when present;
5. native ARM/ARM64 findings;
6. runtime evidence with exact device/build context when authorized;
7. confidence and unresolved questions.
