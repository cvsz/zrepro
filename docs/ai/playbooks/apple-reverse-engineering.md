# Apple Platform Reverse Engineering Playbook

Use this playbook for authorized macOS, iOS, iPadOS, Mach-O, app bundle, IPA, framework, code-signing, entitlement, Objective-C or Swift analysis.

## Route
1. Start with [ZEAZ Reverse Engineering Triage](../../../skills/zeaz-re-triage/SKILL.md).
2. Load [ZEAZ Apple Platform Reverse Engineering](../../../skills/zeaz-re-apple/SKILL.md).
3. Use [ZEAZ Static Reverse Engineering](../../../skills/zeaz-re-static/SKILL.md) for deeper native-binary control/data-flow analysis.
4. Use [ZEAZ Dynamic Reverse Engineering](../../../skills/zeaz-re-dynamic/SKILL.md) only when runtime evidence is required and the lab is isolated.
5. Use [ZEAZ Reverse Engineering Detection Engineering](../../../skills/zeaz-re-detection/SKILL.md) for defensive rules from verified evidence.

## Platform evidence checklist
- artifact SHA-256
- CPU architecture
- Mach-O load commands
- linked dylibs/frameworks
- bundle identifier/version/build
- Info.plist
- code-signing metadata
- entitlements
- provisioning profile where applicable
- Objective-C runtime metadata
- Swift symbols/metadata
- app extensions / XPC services / URL schemes

## Completion criteria
Do not declare analysis complete until platform identity, signing/entitlement state, binary structure and the scoped behavioral question are backed by reproducible evidence.
