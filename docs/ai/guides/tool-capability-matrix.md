# Reverse-Engineering Tool Capability Matrix

Use the smallest maintained toolset that can answer the scoped question. Tool availability is not authorization.

| Domain | Typical tools | Evidence produced | Important limitation |
| --- | --- | --- | --- |
| PE/COFF | Ghidra, Binary Ninja, radare2/Cutter, dumpbin/llvm tools | headers, imports, symbols, disassembly/decompilation | imports and decompiler output do not prove runtime execution |
| ELF | readelf, objdump, nm, Ghidra, Binary Ninja, radare2/Cutter | ELF metadata, symbols, relocations, dependencies, code views | stripped/optimized binaries reduce semantic certainty |
| Mach-O / Apple | file, otool, nm, codesign, plutil, security, xcrun, Ghidra/Binary Ninja | load commands, dylibs, symbols, signing, entitlements, bundle metadata | entitlement/signature presence does not prove runtime use |
| Android | JADX, apktool, apksigner, bundletool, Ghidra for JNI/native | manifest, DEX/resources, signing, native libraries | decompiled Java/Kotlin is reconstructed logic |
| Samsung / One UI | Android tools plus Samsung SDK/framework references | package/component map, Samsung dependencies, device/build observations | behavior can vary by model/region/One UI build |
| Samsung Knox | Android/Samsung tooling plus test EMM/MDM evidence | Knox API surface, policy state, attestation flow, managed-device observations | declared/assigned policy is not proof of effective enforcement |
| Dynamic native | gdb/lldb/WinDbg/x64dbg and platform observability tools | traces, exceptions, process/module/file/network observations | requires authorized contained lab |
| Defensive detection | YARA-compatible engines and telemetry query tooling | rules, matches, false-positive/negative validation | a single weak indicator is insufficient attribution |

## Version discipline

For material findings record the exact tool and version used. Re-run evidence when a tool upgrade, platform build change, or parser/decompiler change could materially alter interpretation.
