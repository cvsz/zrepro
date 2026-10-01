# Reverse-Engineering Tool Capability Matrix

Use the smallest maintained toolset that can answer the authorized question. Tool availability is not authorization.

| Domain | Typical tools | Evidence produced | Important limitation |
| --- | --- | --- | --- |
| Windows PE/COFF | Ghidra, Binary Ninja, radare2/Cutter, dumpbin/LLVM tools | headers, imports, symbols, code views | imports/decompiler output do not prove execution |
| Linux ELF | readelf, objdump, nm, Ghidra, Binary Ninja, radare2/Cutter | ABI, symbols, relocations, dependencies | stripped/optimized binaries reduce certainty |
| Mach-O / Apple | file, otool, nm, codesign, plutil, security, xcrun | load commands, symbols, signing, entitlements | entitlement/signature presence does not prove use |
| Android | JADX, apktool, apksigner, bundletool, native analyzers | manifest, DEX/resources, signing, JNI/native | decompiled source is reconstructed |
| Samsung / One UI | Android tools + Samsung SDK/framework references | component/dependency/device context | behavior varies by model/build |
| Samsung Knox | Samsung/Android tools + test EMM/MDM evidence | policy/API/attestation observations | declared/assigned policy is not effective enforcement |
| Firmware | file/container parsers, filesystem extractors, Ghidra-class analyzers | image layout, rootfs, boot/update metadata | extracted image state is not device runtime state |
| Documents | format parsers, PDF/Office/archive extractors | metadata, objects, macros/scripts, links | embedded content does not prove execution |
| Memory forensics | maintained memory-analysis frameworks | processes/modules/sockets/mappings | residue can be stale; captures may contain secrets |
| Protocol reconstruction | packet/IPC capture and serialization inspection tools | framing, fields, state transitions | one trace may cover one version/path |
| Safe fuzzing | coverage-guided or grammar-based fuzzers in isolated labs | crashes, coverage, minimized inputs | crash does not automatically imply exploitability |
| Dynamic native | gdb/lldb/WinDbg/x64dbg and platform observability | traces, exceptions, process/file/network evidence | requires contained authorized lab |
| Defensive detection | YARA-compatible and telemetry query tooling | rules and validation results | weak indicators are insufficient attribution |

## Version discipline

Record exact tool/version for material findings. Re-run evidence when tool, parser, decompiler, OS, firmware, device build or management state changes could alter interpretation.
