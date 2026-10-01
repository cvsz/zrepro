#!/usr/bin/env python3
"""Validate zRepro structure and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = (
    "README.md", "ABOUT.md", "AGENTS.md", "CLAUDE.md", "OPENCODE.md",
    "ZEAZ-INTRODUCTION.md", "CONTRIBUTING.md", "SECURITY.md",
    "CODE_OF_CONDUCT.md", "CHANGELOG.md", "ROADMAP.md",
    "IMPLEMENTATION-CHECKLIST.md", ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml", ".github/workflows/scorecard.yml",
    "docs/ai/README.md", "docs/ai/agents", "docs/ai/guides",
    "docs/ai/playbooks", "docs/ai/prompts", "docs/security/openssf-scorecard.md",
    "docs/architecture/mcp-server.md",
    "skills/zeaz-skill-finder/SKILL.md", "skills/zeaz-re-triage/SKILL.md",
    "skills/zeaz-re-static/SKILL.md", "skills/zeaz-re-dynamic/SKILL.md",
    "skills/zeaz-re-mobile/SKILL.md", "skills/zeaz-re-apple/SKILL.md",
    "skills/zeaz-re-samsung/SKILL.md", "skills/zeaz-re-knox/SKILL.md",
    "skills/zeaz-re-windows/SKILL.md", "skills/zeaz-re-linux/SKILL.md",
    "skills/zeaz-re-firmware/SKILL.md", "skills/zeaz-re-document/SKILL.md",
    "skills/zeaz-re-memory/SKILL.md", "skills/zeaz-re-protocol/SKILL.md",
    "skills/zeaz-re-fuzzing/SKILL.md", "skills/zeaz-re-detection/SKILL.md",
    "components.d/zeaz-engineering.yml", "components.d/zeaz-reverse-engineering.yml",
    "plugins.d/zeaz-skills.yml", "scripts/github_admin.py",
    "scripts/validate_re_catalog.py", "schemas/re-evidence-report.schema.json",
    "fixtures/re/README.md", "catalog/re-skills.json",
    "benchmarks/re/README.md", "benchmarks/re/scenarios.json",
    "sbom/re-validator.spdx.json", "provenance/re-validator.md",
    "docs/ai/guides/github-repository-admin.md",
    "docs/ai/guides/tool-capability-matrix.md",
    "docs/ai/guides/evidence-report-schema.md",
    "starter-packs/python/README.md", "starter-packs/node/README.md",
    "starter-packs/go/README.md", "starter-packs/rust/README.md",
    "starter-packs/kubernetes-helm/README.md",
    "services/mcp/pyproject.toml", "services/mcp/Dockerfile",
    "services/mcp/.env.example", "services/mcp/src/zrepro_mcp/server.py",
    "services/mcp/src/zrepro_mcp/config.py", "services/mcp/src/zrepro_mcp/auth.py",
    "services/mcp/src/zrepro_mcp/core.py", "services/mcp/tests",
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "data:")


def validate_required_paths() -> list[str]:
    return [f"missing required path: {rel}" for rel in REQUIRED_PATHS if not (ROOT / rel).exists()]


def normalize_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target)


def validate_markdown_links() -> list[str]:
    errors: list[str] = []
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip()
            if not raw or raw.startswith(SKIP_PREFIXES):
                continue
            target = normalize_link_target(raw)
            if not target:
                continue
            link_base = ROOT if md.relative_to(ROOT).as_posix() == "templates/project-readme.md" else md.parent
            resolved = (link_base / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{md.relative_to(ROOT)}: link escapes repository: {raw}")
                continue
            if not resolved.exists():
                errors.append(f"{md.relative_to(ROOT)}: broken local link: {raw}")
    return errors


def main() -> int:
    errors = validate_required_paths() + validate_markdown_links()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("zRepro structure and local Markdown links are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
