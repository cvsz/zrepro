---
name: zeaz-re-static
title: ZEAZ Static Reverse Engineering
description: Evidence-driven static analysis for native binaries, bytecode and packaged artifacts.
version: "0.1.0"
license: MIT
tags: [reverse-engineering, disassembly, decompilation, binary-formats]
supported_harnesses: [codex, claude, opencode]
risk_level: medium
requires_network: false
requires_credentials: false
evidence_required: true
---

# ZEAZ Static Reverse Engineering

## Purpose
Understand executable structure and likely behavior without launching the artifact.

## Analysis order
1. File format and architecture: PE, ELF, Mach-O, DEX/bytecode or other container.
2. Headers, sections/segments, entropy and resources.
3. Signatures, symbols, imports/exports and linked libraries.
4. Strings and embedded configuration, ranked by relevance.
5. Entry points, initialization paths and high-value functions.
6. Cross-references, call graph, data flow and serialization/protocol clues.
7. Decompiler output, always cross-checked against lower-level evidence.
8. Obfuscation/packing indicators and resulting confidence limitations.

## Tool selection
Choose maintained tooling appropriate to the artifact, such as Ghidra, Binary Ninja, radare2/Cutter, objdump/readelf/nm, Capstone, JADX/apktool, or equivalent approved tooling. Record exact tool/version; do not require a specific commercial tool.

## Evidence rules
- A string is evidence of embedded text, not proof that a behavior executes.
- An imported API is capability evidence, not proof of invocation.
- Decompiler output is a reconstruction, not original source.
- Mark dead/unreachable or conditionally reachable code when distinguishable.

## Output
Provide structure map, important functions, suspected interfaces, confirmed facts, hypotheses, unresolved questions and exact next validation step.
