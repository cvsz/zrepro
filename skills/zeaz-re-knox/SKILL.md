---
name: zeaz-re-knox
title: ZEAZ Samsung Knox Reverse Engineering
description: Evidence-driven analysis of authorized Samsung Knox SDK, enterprise policy, attestation and managed-device integrations.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, samsung, knox, enterprise, mdm, emm, attestation, one-ui]
supported_harnesses: [codex, claude, opencode]
risk_level: high
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Samsung Knox Reverse Engineering

## Purpose
Analyze authorized Knox-enabled applications and enterprise-management integrations while preserving the distinction between declared capability, assigned policy, effective policy and observed enforcement.

## Analysis targets
- Knox SDK / Knox Platform for Enterprise
- Knox Manage / EMM integrations
- device-admin / device-policy interactions
- Knox Workspace/container-related metadata
- enterprise enrollment configuration
- attestation flows
- kiosk / application-control / VPN / certificate / restriction policy references
- Samsung enterprise Binder/service integrations

## Static workflow

### 1. Identity
Record:
- SHA-256;
- package name/version;
- signing certificate metadata;
- min/target SDK;
- Samsung/One UI/Knox context when known.

### 2. Knox capability surface
Inspect:
- Knox-specific package/class namespaces;
- declared Knox/Samsung permissions;
- enterprise service references;
- device-policy/admin receivers and metadata;
- SDK initialization/configuration;
- policy method references;
- attestation request/verification code;
- error/return-code handling.

### 3. Policy model
For each relevant capability, record four states separately:
1. declared;
2. granted/assigned;
3. effective;
4. observed.

Do not collapse these into a single “enabled” state.

### 4. Attestation analysis
Document:
- nonce/challenge handling;
- request construction;
- response parsing;
- certificate/token verification path;
- freshness/replay protections when visible;
- trust decision location.

Do not generate forged attestation, bypass verification, or weaken trust decisions.

## Dynamic workflow
Use only on an explicitly authorized Samsung test device enrolled in a test management environment.

Record:
- exact model;
- Android version;
- One UI version;
- Knox version where available;
- security patch;
- management mode;
- policy assignment;
- observed policy result;
- logs/errors returned by Knox APIs.

Use test-only accounts, certificates and policies.

## Security boundaries
This skill does not authorize:
- Knox/MDM/EMM enrollment bypass;
- policy removal on unauthorized devices;
- attestation forgery or trust bypass;
- FRP/Samsung Account bypass;
- bootloader/Verified Boot bypass;
- enterprise secret or key extraction.

## Output
Report:
1. artifact/package identity;
2. Knox SDK/service dependency map;
3. declared permissions/capabilities;
4. policy-state matrix: declared / assigned / effective / observed;
5. attestation flow map when applicable;
6. authorized runtime evidence;
7. exact device/build/management context;
8. confidence and unresolved questions.
