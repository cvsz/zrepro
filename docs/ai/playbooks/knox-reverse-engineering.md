# Samsung Knox Reverse Engineering Playbook

Use this playbook for authorized Samsung Knox SDK, Knox Platform for Enterprise, Knox Manage/EMM integration, enterprise policy, managed-device behavior or attestation analysis.

## Route
1. Start with [ZEAZ Reverse Engineering Triage](../../../skills/zeaz-re-triage/SKILL.md).
2. Load [ZEAZ Samsung Knox Reverse Engineering](../../../skills/zeaz-re-knox/SKILL.md).
3. Load [ZEAZ Samsung Platform Reverse Engineering](../../../skills/zeaz-re-samsung/SKILL.md) for Samsung/One UI context.
4. Use [ZEAZ Mobile Reverse Engineering](../../../skills/zeaz-re-mobile/SKILL.md) for generic Android application/component analysis.
5. Use [ZEAZ Dynamic Reverse Engineering](../../../skills/zeaz-re-dynamic/SKILL.md) only on an authorized managed-device lab.

## Knox evidence checklist
- package SHA-256
- package/version/signing metadata
- Knox SDK/service dependencies
- declared Samsung/Knox permissions
- device-admin / policy receivers
- enterprise service/Binder interactions
- management mode
- assigned policy
- effective policy
- observed enforcement
- attestation request/verification path when relevant
- exact model / Android / One UI / Knox / security patch context

## Completion criteria
A Knox finding must distinguish declaration, policy assignment, effective state and observed behavior. Do not call a control active or bypassed based on static metadata alone.
