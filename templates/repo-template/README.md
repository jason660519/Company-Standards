# Repo Template（起手式）

新專案的最小骨架。複製本資料夾內容到新 repo，再依下方清單調整。

## 內含

```
AGENTS.md                     # agent / 工程師專案規約 canonical（引用 Company-Standards）
CLAUDE.md                     # AGENTS.md mirror（產生物）
GEMINI.md                     # AGENTS.md mirror（產生物）
.cursor/rules/project.mdc     # AGENTS.md mirror（產生物）
.gitignore
.editorconfig                 # 從 Company-Standards 根 .editorconfig 複製而來
.pre-commit-config.yaml       # 含 agent instructions / skills sync 檢查
.github/pull_request_template.md
docs/architecture/decisions/  # ADR 放這（含 .gitkeep）
.agents/skills/               # canonical skills（含 .gitkeep）
scripts/                      # repo 層級工具（如 sync_agent_instructions.py / sync_skills.py）
```

## 起手步驟

1. 複製本資料夾內容到新 repo 根目錄。
2. 把 Company-Standards 掛成 submodule：
   ```bash
   git submodule add https://github.com/jason660519/Company-Standards.git Company-Standards
   git -C Company-Standards checkout v0.5.0
   ```
3. 從 `Company-Standards/.editorconfig` 複製一份 `.editorconfig` 到根目錄。
4. 從 `Company-Standards/shared/scripts/sync_agent_instructions.py` 複製到 `scripts/`。
5. 從 `Company-Standards/shared/scripts/sync_skills.py` 複製到 `scripts/`（若會用 skills）。
6. 填好 `AGENTS.md` 的專案專屬段落。
7. 跑 `python3 scripts/sync_agent_instructions.py` 產生工具 mirror。
8. `uv tool install pre-commit && pre-commit install`。
9. 刪掉本說明檔，換成真正的專案 README。
