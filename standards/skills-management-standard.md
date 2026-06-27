# Skills Management Standard

Status: Company baseline v0.2.0
Applies to: 任何 repo 內含 agent「skills」（`SKILL.md` 資料夾），且會被**一種以上**工具消費時。

## 問題（為什麼需要這個標準）

不同的 agent 工具掃描的 skill 目錄不一樣：

- Claude Code 只自動掃 `.claude/skills/`（與 `~/.claude/skills/`、plugin 內的 skills）。
- 其他走 Agent Skills open format 的工具可能掃 `.agents/skills/` 或別的路徑。

若把同一個 skill 在兩個目錄各放一份，會變成兩份各自漂移的副本，改了一邊忘了另一邊就出包。「叫大家統一看某個目錄」也行不通——工具不會去掃它沒被設定的路徑。

## 標準

1. **單一真相來源（canonical）**：`.agents/skills/<skill>/` 為唯一真相來源，工具中立。**只在這裡編輯。**
2. **鏡像（mirror）**：`.claude/skills/<skill>/` 是給 Claude Code 掃描用的**產生物**。**不要手改**，它會被覆蓋。
3. **用 sync script 產生鏡像**：一支無第三方依賴、可直接 `python` 執行、跨 OS 的腳本，提供兩個模式：
   - 預設：把 canonical 整包鏡像到目標目錄（覆蓋 + prune 掉 canonical 已移除的）。
   - `--check`：只比對是否一致、不寫入；不一致則 exit 1，供 CI / pre-commit gate 使用。
4. **用實體 copy，不要用 symlink**：symlink 在 Windows clone 需要 `core.symlinks=true` + Developer Mode 才會還原，否則壞成純文字檔；實體 copy 不依賴檔案系統特性，跨 OS 都穩。
5. **明確決定 git 策略**（二選一，寫進專案文件）：
   - **兩份都 commit**：clone 下來即可用、不必先 sync；代價是 git 內有重複內容，且要靠 pre-commit `--check` 保證兩份一致。
   - **只 commit canonical、gitignore 鏡像**：git 乾淨無重複；代價是 clone / pull 後需自行跑一次 sync 才有鏡像。
6. **掛 pre-commit `--check` hook**：避免有人改了 canonical 忘了 sync 就 commit 進不一致的鏡像。團隊共用版用 `.pre-commit-config.yaml`（進 git），每位工程師 clone 後各自 `pre-commit install` 一次。
7. **分清兩種 scripts**：每個 skill 自己的執行用腳本放該 skill 內 `<skill>/scripts/`（屬於該 skill）；repo 層級的 sync script 放 `scripts/`（屬於 repo 基礎設施）。兩者不同層級，不要混。

## 名詞

| 名詞 | 意思 |
|------|------|
| canonical | 真相來源／正本，你實際編輯的那一份（`.agents/skills/`） |
| mirror | 從 canonical 複製產生、給特定工具掃描的副本（`.claude/skills/`） |
| sync | 把 canonical 複製成 mirror 的動作（跑 sync script） |

## sync script 參考實作

純標準函式庫、無依賴，macOS / Linux / Windows 皆可跑。要點：

- 來源 `.agents/skills/`、目標 `.claude/skills/`，路徑相對 script 自身位置推導，不寫死絕對路徑。
- sync：逐一 `rmtree` 既有目標再 `copytree` 重建（乾淨鏡像）；canonical 已移除的 skill 從鏡像 prune 掉。
- `--check`：用 `filecmp` 遞迴比對兩邊樹是否一致，供自動化 gate。

```python
#!/usr/bin/env python3
"""Mirror canonical skills (.agents/skills) into .claude/skills.

  python scripts/sync_skills.py            # 鏡像 canonical -> mirror
  python scripts/sync_skills.py --check    # 驗證是否一致，不一致 exit 1
"""
from __future__ import annotations
import argparse, filecmp, shutil, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / ".agents" / "skills"
DEST = REPO_ROOT / ".claude" / "skills"


def skill_dirs(base: Path) -> set[str]:
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith(".")}


def dirs_in_sync(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(dirs_in_sync(a / sub, b / sub) for sub in cmp.common_dirs)


def check() -> int:
    if not SOURCE.is_dir():
        print(f"ERROR: canonical source not found: {SOURCE}", file=sys.stderr)
        return 1
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
    print(f"in sync: {sorted(src)}")
    return 0


def sync() -> int:
    if not SOURCE.is_dir():
        print(f"ERROR: canonical source not found: {SOURCE}", file=sys.stderr)
        return 1
    DEST.mkdir(parents=True, exist_ok=True)
    src, dst = skill_dirs(SOURCE), skill_dirs(DEST)
    for stale in dst - src:
        shutil.rmtree(DEST / stale)
        print(f"removed (stale): {stale}")
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
    parser.add_argument("--check", action="store_true",
                        help="verify mirror is in sync without writing; exit 1 if not")
    args = parser.parse_args()
    return check() if args.check else sync()


if __name__ == "__main__":
    raise SystemExit(main())
```

## pre-commit 參考設定

```yaml
# .pre-commit-config.yaml — 團隊共用；clone 後各自 `pre-commit install` 一次。
repos:
  - repo: local
    hooks:
      - id: sync-skills-check
        name: skills mirror in sync (.agents/skills -> .claude/skills)
        entry: python3 scripts/sync_skills.py --check
        language: system
        pass_filenames: false
        files: ^\.(agents|claude)/skills/
```

## 採用檢查清單

- [ ] skill 真實檔案只放在 `.agents/skills/<skill>/`
- [ ] `scripts/sync_skills.py` 存在且 `--check` 可跑
- [ ] git 策略已決定並寫進專案 `CLAUDE.md`
- [ ] `.pre-commit-config.yaml` 含 `sync-skills-check`，且工程師已 `pre-commit install`
- [ ] 專案 `CLAUDE.md` 註明「只改 canonical、改完跑 sync」
