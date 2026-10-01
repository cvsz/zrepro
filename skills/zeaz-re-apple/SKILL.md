---
name: zeaz-re-apple
title: ZEAZ Apple Platform Reverse Engineering
description: Evidence-driven reverse engineering for authorized macOS, iOS and iPadOS binaries, bundles and application packages.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, apple, macos, ios, ipados, macho, swift, objective-c]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Apple Platform Reverse Engineering

## Purpose
Analyze authorized Apple-platform software and application packages while preserving artifact identity, code-signing evidence and platform-specific metadata.

## Artifact types
- Mach-O executable / dylib
- macOS `.app`
- iOS/iPadOS `.ipa`
- `.framework` / `.xcframework`
- app extensions
- provisioning profiles
- plist/resource bundles

## Static workflow

### 1. Identity
Record:
- SHA-256;
- file type;
- CPU architecture(s);
- minimum OS/platform when discoverable;
- bundle identifier/version/build;
- source/provenance if known.

### 2. Mach-O structure
Inspect:
- Mach header;
- load commands;
- segments/sections;
- dylib dependencies;
- rpaths;
- symbols;
- exports/imports;
- code signature load command;
- Objective-C / Swift metadata sections where present.

Common platform-native tooling may include:
- `file`
- `otool`
- `nm`
- `codesign`
- `plutil`
- `security`
- `xcrun`
- `swift-demangle`

Use equivalent maintained tooling where appropriate and record tool/version.

### 3. Bundle and signing metadata
Inspect:
- `Info.plist`;
- embedded provisioning profile where present;
- application identifier/team identifier;
- code-signing identity metadata;
- hardened runtime/notarization indicators when relevant;
- entitlements;
- app extensions;
- URL schemes and declared document/content types.

### 4. Objective-C / Swift surface
Identify:
- Objective-C classes, categories, protocols and selectors;
- Swift mangled/demangled symbols;
- framework boundaries;
- likely entry points and initialization code;
- IPC/XPC/service interfaces where visible;
- serialization/networking/storage clues.

### 5. Correlation
Do not treat one signal as proof. Correlate symbols, selectors, imports, strings, call references, bundle metadata and runtime observations.

## Dynamic workflow
Use only with explicit authorization and a disposable/restorable test environment.

Possible observation areas:
- process launch/child processes;
- dylib/framework loading;
- filesystem changes;
- preferences/keychain access using test-only data;
- XPC/IPC;
- network destinations;
- crashes/exceptions;
- sandbox-related failures.

Never use real Apple IDs, production signing identities, real keychain secrets or personal device data in analysis.

## Security boundaries
This skill does not authorize:
- bypassing Activation Lock;
- unauthorized Apple ID/account access;
- circumventing DRM/FairPlay protections;
- defeating device ownership controls;
- modifying entitlements/signatures to gain unauthorized privileges.

## Output
Report:
1. artifact identity;
2. bundle/package structure;
3. signing and entitlement evidence;
4. Mach-O architecture and dependencies;
5. Objective-C/Swift surface;
6. static behavior hypotheses;
7. runtime evidence if authorized;
8. confidence and unresolved questions.
