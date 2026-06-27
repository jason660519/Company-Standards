# Agent Instructions Standard

Status: Company baseline v0.5.0-draft
Applies to: 任何 repo 需要被 Codex、Claude Code、Gemini CLI、Cursor 或其他 coding agent 讀取專案層級 instructions 時。

本標準規定 agent instruction files 的單一真相來源與跨工具 mirror 機制，避免 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、Cursor rules 各自漂移。

---

## 標準

1. **canonical**：`AGENTS.md` 是唯一真相來源，工具中立，**只在這裡編輯**。
2. **mirrors**：工具專用入口檔由 sync script 產生，**不要手改**：
   - `CLAUDE.md`：Claude Code mirror。
   - `GEMINI.md`：Gemini CLI mirror。
   - `.cursor/rules/project.mdc`：Cursor Project Rule mirror。
3. **用 sync script 產生 mirrors**：無第三方依賴、可直接 `python3` 執行、跨 OS；提供 `sync`（寫入 mirrors）與 `--check`（驗證一致、不一致 exit 1）兩模式。參考實作見本 repo [`shared/scripts/sync_agent_instructions.py`](../shared/scripts/sync_agent_instructions.py)。
4. **mirrors 要有 generated header**：明確提示工程師不要直接編輯 mirror，並告知 sync 指令。
5. **明確決定 git 策略**（二選一，寫進專案 `AGENTS.md`）：
   - **canonical 與 mirrors 都 commit**：clone 即可被各工具讀到；代價是重複內容，靠 pre-commit `--check` 保證一致。
   - **只 commit canonical、gitignore mirrors**：git 乾淨；代價是 clone / pull 後需自行 sync。
6. **掛 pre-commit `--check` hook**：防止改了 `AGENTS.md` 忘了 sync，或直接手改 generated mirror。hook 失敗時必須提示工程師改 `AGENTS.md` 並跑 `python3 scripts/sync_agent_instructions.py`。團隊共用版用 `.pre-commit-config.yaml`（進 git），每位工程師 clone 後 `pre-commit install` 一次。

---

## 保護機制

同步方向固定為：

```text
AGENTS.md -> CLAUDE.md / GEMINI.md / .cursor/rules/project.mdc
```

不要支援從 mirror 反向同步回 `AGENTS.md`，也不要支援「任一檔案改了就同步其他檔」。多向同步會讓權威來源變模糊，且可能把錯誤的 mirror 內容擴散到 canonical。

正確保護層級：

1. mirror 檔案頂部放 generated header。
2. `sync_agent_instructions.py --check` 比對 mirrors 是否完全由 `AGENTS.md` 產生。
3. pre-commit hook 擋下不同步內容，並提示：
   - 不要直接修改 generated mirror files。
   - 改 `AGENTS.md`。
   - 跑 `python3 scripts/sync_agent_instructions.py`。

---

## 檔案角色

| 路徑 | 角色 | 可不可以改 |
|------|------|-----------|
| `AGENTS.md` | canonical（唯一真相來源） | ✅ 只改這裡 |
| `CLAUDE.md` | Claude Code mirror | ❌ 不要手改 |
| `GEMINI.md` | Gemini CLI mirror | ❌ 不要手改 |
| `.cursor/rules/project.mdc` | Cursor Project Rule mirror | ❌ 不要手改 |

---

## 建議內容分層

`AGENTS.md` 應保持「薄而明確」：

- 引用 Company-Standards submodule。
- 寫本 repo 如何套用公司標準。
- 寫本 repo 的專案特例、路徑、scripts、驗證方式。
- 不要複製整份公司標準內容；跨專案共用規則留在 `standards/`。

---

## pre-commit 參考設定

```yaml
repos:
  - repo: https://github.com/jason660519/Company-Standards
    rev: v0.5.0
    hooks:
      - id: sync-agent-instructions-check
      - id: sync-skills-check
```

在本 standards hook 發布成 tag 前，專案也可以先用 local hook：

```yaml
repos:
  - repo: local
    hooks:
      - id: sync-agent-instructions-check
        name: agent instruction mirrors in sync (AGENTS.md -> tool-specific files)
        entry: python3 scripts/sync_agent_instructions.py --check
        language: system
        pass_filenames: false
        files: ^(AGENTS\.md|CLAUDE\.md|GEMINI\.md|\.cursor/rules/project\.mdc)$
```

---

## 採用檢查清單

- [ ] `AGENTS.md` 存在，並寫明它是唯一真相來源。
- [ ] `CLAUDE.md`、`GEMINI.md`、`.cursor/rules/project.mdc` 由 sync 產生且有 generated header。
- [ ] `scripts/sync_agent_instructions.py` 存在且 `--check` 可跑。
- [ ] git 策略已決定並寫進專案 `AGENTS.md`。
- [ ] `.pre-commit-config.yaml` 含 `sync-agent-instructions-check`，工程師已 `pre-commit install`。
