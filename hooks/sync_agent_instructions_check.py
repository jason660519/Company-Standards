#!/usr/bin/env python3
"""Shared pre-commit hook: verify agent instruction mirrors match AGENTS.md.

pre-commit runs hooks with CWD = the consuming repo root, so this checks
that repo (not this standards repo). Exit 1 if out of sync; exit 0 if the
repo has no AGENTS.md. See standards/agent-instructions-standard.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
SOURCE = ROOT / "AGENTS.md"

GENERATED_NOTICE = "<!-- Generated from AGENTS.md. Do not edit directly. -->\n"
RUN_NOTICE = "<!-- Run: python3 scripts/sync_agent_instructions.py -->\n\n"


def read_source() -> str | None:
    if not SOURCE.is_file():
        return None
    return SOURCE.read_text(encoding="utf-8")


def markdown_mirror(source: str) -> str:
    return GENERATED_NOTICE + RUN_NOTICE + source


def cursor_mirror(source: str) -> str:
    return (
        "---\n"
        "alwaysApply: true\n"
        "---\n\n"
        f"{GENERATED_NOTICE}{RUN_NOTICE}{source}"
    )


def targets(source: str) -> dict[Path, str]:
    return {
        ROOT / "CLAUDE.md": markdown_mirror(source),
        ROOT / "GEMINI.md": markdown_mirror(source),
        ROOT / ".cursor" / "rules" / "project.mdc": cursor_mirror(source),
    }


def print_out_of_sync(issues: list[str]) -> None:
    print("AGENT INSTRUCTION MIRRORS ARE OUT OF SYNC.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Do not edit generated mirror files directly:", file=sys.stderr)
    print("  - CLAUDE.md", file=sys.stderr)
    print("  - GEMINI.md", file=sys.stderr)
    print("  - .cursor/rules/project.mdc", file=sys.stderr)
    print("", file=sys.stderr)
    print("Edit the canonical file instead:", file=sys.stderr)
    print("  - AGENTS.md", file=sys.stderr)
    print("", file=sys.stderr)
    print("Then regenerate mirrors:", file=sys.stderr)
    print("  python3 scripts/sync_agent_instructions.py", file=sys.stderr)
    print("", file=sys.stderr)
    print("Detected issues:", file=sys.stderr)
    for line in issues:
        print(f"  - {line}", file=sys.stderr)


def main() -> int:
    source = read_source()
    if source is None:
        return 0

    issues: list[str] = []
    for path, expected in targets(source).items():
        if not path.is_file():
            issues.append(f"missing mirror: {path.relative_to(ROOT)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            issues.append(f"contents differ: {path.relative_to(ROOT)}")

    if issues:
        print_out_of_sync(issues)
        return 1

    print("agent instructions in sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
