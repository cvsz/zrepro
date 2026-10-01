# Reverse Engineering Playbook

Use this playbook for authorized compatibility research, debugging, incident response, provenance analysis, malware analysis, or defensive detection work.

## Route
1. Orchestrator: [Reverse Engineering Orchestrator](../agents/reverse-engineering-orchestrator.md)
2. Triage: [ZEAZ Reverse Engineering Triage](../../../skills/zeaz-re-triage/SKILL.md)
3. Static: [ZEAZ Static Reverse Engineering](../../../skills/zeaz-re-static/SKILL.md)
4. Dynamic, only when needed and contained: [ZEAZ Dynamic Reverse Engineering](../../../skills/zeaz-re-dynamic/SKILL.md)
5. Android/mobile: [ZEAZ Mobile Reverse Engineering](../../../skills/zeaz-re-mobile/SKILL.md)
6. Apple platforms: [ZEAZ Apple Platform Reverse Engineering](../../../skills/zeaz-re-apple/SKILL.md)
7. Samsung platforms: [ZEAZ Samsung Platform Reverse Engineering](../../../skills/zeaz-re-samsung/SKILL.md)
8. Defensive detections: [ZEAZ Reverse Engineering Detection Engineering](../../../skills/zeaz-re-detection/SKILL.md)

## Reference taxonomy
The workflow was informed by the public taxonomy in `wtsxDev/reverse-engineering`: binary formats, disassemblers/static analysis, bytecode, dynamic analysis/debugging, document analysis, scripting, Android and YARA. This repository adopts the taxonomy concept, not third-party content.

Apple support extends that taxonomy with explicit Mach-O, app-bundle, code-signing, entitlement, Objective-C and Swift analysis. Samsung support extends Android analysis with Galaxy/One UI-specific framework/service mapping, Knox-related metadata and device/build-aware evidence. Both preserve the same authorization, evidence and containment rules.

## Completion criteria
A reverse-engineering task is not complete because a tool produced output. Completion requires artifact identity, reproducible evidence, stated uncertainty, and a direct answer to the scoped question.
