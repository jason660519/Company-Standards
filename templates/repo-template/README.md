# Repo Template（起手式）

新專案的最小骨架。複製本資料夾內容到新 repo，再依下方清單調整。

## 內含

```
CLAUDE.md                     # agent / 工程師專案規約骨架（引用 Company-Standards）
.gitignore
.editorconfig                 # 從 Company-Standards 根 .editorconfig 複製而來
.pre-commit-config.yaml       # 含 skills sync 檢查
.github/pull_request_template.md
docs/architecture/decisions/  # ADR 放這（含 .gitkeep）
.agents/skills/               # canonical skills（含 .gitkeep）
scripts/                      # repo 層級工具（如 sync_skills.py）
```

## 起手步驟

1. 複製本資料夾內容到新 repo 根目錄。
2. 把 Company-Standards 掛成 submodule：
   ```bash
   git submodule add https://github.com/jason660519/Company-Standards.git standards
   git -C standards checkout v0.3.0
   ```
3. 從 `standards/.editorconfig` 複製一份 `.editorconfig` 到根目錄。
4. 從 `standards/shared/scripts/sync_skills.py` 複製到 `scripts/`（若會用 skills）。
5. 填好 `CLAUDE.md` 的專案專屬段落。
6. `uv tool install pre-commit && pre-commit install`。
7. 刪掉本說明檔，換成真正的專案 README。
