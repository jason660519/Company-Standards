#!/usr/bin/env python3
"""Mirror canonical skills into the Claude Code skill directory.

Single source of truth: .agents/skills/  (tool-neutral, edit here)
Mirror target:         .claude/skills/   (what Claude Code scans; do NOT edit)

Claude Code only auto-discovers skills under .claude/skills/, so this script
copies every skill from the canonical location into it. We use real copies
instead of symlinks because symlinks are fragile across operating systems
(Windows checkouts need core.symlinks + Developer Mode).

Run it whenever a skill under .agents/skills/ changes:

    python3 scripts/sync_skills.py            # mirror canonical -> .claude/skills
    python3 scripts/sync_skills.py --check    # verify in sync, exit 1 if not (for CI / pre-commit)

Pure standard library, no dependencies, runs on macOS / Linux / Windows.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / ".agents" / "skills"
DEST = REPO_ROOT / ".claude" / "skills"


def skill_dirs(base: Path) -> set[str]:
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith(".")}


def dirs_in_sync(a: Path, b: Path) -> bool:
    """True if directory trees a and b have identical contents."""
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(
        dirs_in_sync(a / sub, b / sub) for sub in cmp.common_dirs
    )


def print_out_of_sync(issues: list[str]) -> None:
    print("SKILL MIRRORS ARE OUT OF SYNC.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Do not edit generated mirror skills directly:", file=sys.stderr)
    print("  - .claude/skills/<skill>/", file=sys.stderr)
    print("", file=sys.stderr)
    print("Edit the canonical skill instead:", file=sys.stderr)
    print("  - .agents/skills/<skill>/", file=sys.stderr)
    print("", file=sys.stderr)
    print("Then regenerate mirrors:", file=sys.stderr)
    print("  python3 scripts/sync_skills.py", file=sys.stderr)
    print("", file=sys.stderr)
    print("Detected issues:", file=sys.stderr)
    for line in issues:
        print(f"  - {line}", file=sys.stderr)


def check() -> int:
    if not SOURCE.is_dir():
        print(f"ERROR: canonical source not found: {SOURCE}", file=sys.stderr)
        return 1
    src, dst = skill_dirs(SOURCE), skill_dirs(DEST)
    out_of_sync = []
    if src != dst:
        out_of_sync.append(f"skill set differs: canonical={sorted(src)} mirror={sorted(dst)}")
    for name in src & dst:
        if not dirs_in_sync(SOURCE / name, DEST / name):
            out_of_sync.append(f"contents differ: {name}")
    if out_of_sync:
        print_out_of_sync(out_of_sync)
        return 1
    print(f"in sync: {sorted(src)}")
    return 0


def sync() -> int:
    if not SOURCE.is_dir():
        print(f"ERROR: canonical source not found: {SOURCE}", file=sys.stderr)
        return 1
    DEST.mkdir(parents=True, exist_ok=True)
    src, dst = skill_dirs(SOURCE), skill_dirs(DEST)

    # Prune mirror entries that no longer exist in canonical.
    for stale in dst - src:
        shutil.rmtree(DEST / stale)
        print(f"removed (stale): {stale}")

    # Copy / refresh each canonical skill.
    for name in sorted(src):
        target = DEST / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(SOURCE / name, target)
        print(f"synced: {name}")

    print(f"\ndone. mirrored {len(src)} skill(s) into {DEST.relative_to(REPO_ROOT)}/")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify mirror is in sync without writing; exit 1 if not",
    )
    args = parser.parse_args()
    return check() if args.check else sync()


if __name__ == "__main__":
    raise SystemExit(main())
