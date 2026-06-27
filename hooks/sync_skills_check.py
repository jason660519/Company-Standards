#!/usr/bin/env python3
"""Shared pre-commit hook: verify the .claude/skills mirror matches the
.agents/skills canonical in the *consuming* repo.

pre-commit runs hooks with CWD = the consuming repo root, so this checks
that repo (not this standards repo). Exit 1 if out of sync; exit 0 if the
repo has no skills. See standards/skills-create-and-management-standard.md.
"""
from __future__ import annotations

import filecmp
import sys
from pathlib import Path

ROOT = Path.cwd()
SOURCE = ROOT / ".agents" / "skills"
DEST = ROOT / ".claude" / "skills"


def skill_dirs(base: Path) -> set[str]:
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith(".")}


def dirs_in_sync(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(dirs_in_sync(a / sub, b / sub) for sub in cmp.common_dirs)


def main() -> int:
    if not SOURCE.is_dir():
        return 0  # repo ships no skills; nothing to verify
    src, dst = skill_dirs(SOURCE), skill_dirs(DEST)
    issues = []
    if src != dst:
        issues.append(f"skill set differs: canonical={sorted(src)} mirror={sorted(dst)}")
    for name in src & dst:
        if not dirs_in_sync(SOURCE / name, DEST / name):
            issues.append(f"contents differ: {name}")
    if issues:
        print("OUT OF SYNC. Run: python scripts/sync_skills.py", file=sys.stderr)
        for line in issues:
            print(f"  - {line}", file=sys.stderr)
        return 1
    print(f"skills in sync: {sorted(src)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
