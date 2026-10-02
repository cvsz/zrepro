#!/usr/bin/env python3
"""Reject tracked credential filenames without inspecting or printing file contents."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import PurePosixPath


def secret_file_paths(paths: list[str]) -> list[str]:
    rejected = []
    for path in paths:
        name = PurePosixPath(path).name.casefold()
        if name == ".env.example":
            continue
        if (
            name == ".env"
            or name.startswith(".env.")
            or name in {"id_rsa", "id_ed25519", "id_dsa", "id_ecdsa"}
            or name.endswith((".pem", ".key"))
        ):
            rejected.append(path)
    return sorted(rejected)


def main() -> int:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], capture_output=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        print("Unable to enumerate tracked files; run inside a Git repository.", file=sys.stderr)
        return 1
    paths = [os.fsdecode(path) for path in result.stdout.split(b"\0") if path]
    rejected = secret_file_paths(paths)
    if rejected:
        for path in rejected:
            print(f"Potential credential file is tracked: {path!r}", file=sys.stderr)
        return 1
    print("Tracked credential filename check passed; contents were not scanned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
