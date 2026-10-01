# Samsung Platform Reverse Engineering Playbook

Use this playbook for authorized Samsung Galaxy / One UI application, APK/AAB/DEX, native ARM/ARM64 library, Samsung-framework or Knox-integration analysis.

## Route
1. Start with [ZEAZ Reverse Engineering Triage](../../../skills/zeaz-re-triage/SKILL.md).
2. Load [ZEAZ Samsung Platform Reverse Engineering](../../../skills/zeaz-re-samsung/SKILL.md).
3. Use [ZEAZ Mobile Reverse Engineering](../../../skills/zeaz-re-mobile/SKILL.md) for generic Android component analysis.
4. Use [ZEAZ Static Reverse Engineering](../../../skills/zeaz-re-static/SKILL.md) for deeper native/bytecode analysis.
5. Use [ZEAZ Dynamic Reverse Engineering](../../../skills/zeaz-re-dynamic/SKILL.md) only in an authorized contained lab.
6. Use [ZEAZ Reverse Engineering Detection Engineering](../../../skills/zeaz-re-detection/SKILL.md) for defensive detections from verified evidence.

## Samsung evidence checklist
- SHA-256
- package/version/signing metadata
- Android min/target SDK
- ABI/native libraries
- manifest permissions/components
- exported activities/services/receivers/providers
- Samsung/One UI namespaces and dependencies
- Knox-related metadata/interfaces when present
- exact Galaxy model/region/build when runtime evidence is device-specific
- Android / One UI / security patch versions

## Completion criteria
Do not generalize a finding across Samsung devices unless model/build variability is addressed. Device-specific runtime claims must include exact environment evidence.
