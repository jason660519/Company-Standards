#!/usr/bin/env python3
"""Mirror AGENTS.md into tool-specific agent instruction files.

Single source of truth: AGENTS.md
Mirror targets:
  - CLAUDE.md
  - GEMINI.md
  - .cursor/rules/project.mdc

Run it whenever AGENTS.md changes:

    python3 scripts/sync_agent_instructions.py
    python3 scripts/sync_agent_instructions.py --check

Pure standard library, no dependencies, runs on macOS / Linux / Windows.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "AGENTS.md"

GENERATED_NOTICE = "<!-- Generated from AGENTS.md. Do not edit directly. -->\n"
RUN_NOTICE = "<!-- Run: python3 scripts/sync_agent_instructions.py -->\n\n"


def read_source() -> str:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"canonical source not found: {SOURCE}")
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
        REPO_ROOT / "CLAUDE.md": markdown_mirror(source),
        REPO_ROOT / "GEMINI.md": markdown_mirror(source),
        REPO_ROOT / ".cursor" / "rules" / "project.mdc": cursor_mirror(source),
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


def check() -> int:
    try:
        source = read_source()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    out_of_sync: list[str] = []
    for path, expected in targets(source).items():
        if not path.is_file():
            out_of_sync.append(f"missing mirror: {path.relative_to(REPO_ROOT)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            out_of_sync.append(f"contents differ: {path.relative_to(REPO_ROOT)}")

    if out_of_sync:
        print_out_of_sync(out_of_sync)
        return 1

    print("agent instructions in sync")
    return 0


def sync() -> int:
    try:
        source = read_source()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for path, content in targets(source).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"synced: {path.relative_to(REPO_ROOT)}")

    print("\ndone. mirrored AGENTS.md into tool-specific instruction files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify mirrors are in sync without writing; exit 1 if not",
    )
    args = parser.parse_args()
    return check() if args.check else sync()


if __name__ == "__main__":
    raise SystemExit(main())
