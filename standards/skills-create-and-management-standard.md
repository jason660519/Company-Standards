# Skills Create-and-Management Standard

Status: Company baseline v0.3.0
Applies to: 任何 repo 內含 agent「skills」（`SKILL.md` 資料夾），且會被**一種以上**工具消費時。

涵蓋兩件事：**怎麼建立一個新 skill**（create）與**怎麼跨工具維持單一真相來源**（manage）。

---

## Part A — 建立一個新 skill（create）

### 放哪

新 skill 一律建立在 **canonical 目錄** `.agents/skills/<skill-name>/`，**不要**直接建在 `.claude/skills/`（那是產生物）。

### 命名

- 資料夾名：kebab-case、動詞/用途導向、夠具體可被觸發判斷，如 `nesa-pdf-to-md`、`md-to-pdf`。
- 避免過於籠統（`helper`、`utils`）導致觸發條件模糊。

### 結構

```
.agents/skills/<skill-name>/
  SKILL.md            # 必要：frontmatter + 指示
  scripts/            # 選用：此 skill 自己的執行用腳本
  references/         # 選用：補充文件、範例
```

### SKILL.md frontmatter

```markdown
---
name: <skill-name>
description: <一句話講「做什麼 + 何時用」，觸發判斷靠它，要具體、含關鍵字>
---

# <Skill 標題>

（指示本體：步驟、輸入輸出、邊界條件、範例）
```

- `description` 是觸發命中率的關鍵：寫清楚「**做什麼**」與「**什麼情況該用**」，並放進使用者可能說的關鍵字。
- 指示本體寫**穩定、可重複**的流程；把可變的專案細節留給專案 `CLAUDE.md`。

### 每個 skill 自己的 scripts

放在該 skill 內 `<skill>/scripts/`，屬於該 skill 的執行邏輯。**這與下面 repo 層級的 sync script 是不同層級，別混。**

---

## Part B — 跨工具單一真相來源（manage）

### 問題

不同 agent 工具掃描的 skill 目錄不同：Claude Code 只自動掃 `.claude/skills/`（與 `~/.claude/skills/`、plugin），其他工具可能掃 `.agents/skills/`。同一 skill 各放一份會漂移；「叫大家統一看某目錄」也沒用——工具不會掃它沒被設定的路徑。

### 標準

1. **canonical**：`.agents/skills/<skill>/` 為唯一真相來源，工具中立，**只在這裡編輯**。
2. **mirror**：`.claude/skills/<skill>/` 是給 Claude Code 掃描的**產生物**，**不要手改**。
3. **用 sync script 產生鏡像**：無第三方依賴、可直接 `python` 執行、跨 OS；提供 `sync`（鏡像）與 `--check`（驗證一致、不一致 exit 1）兩模式。參考實作見本 repo [`shared/scripts/sync_skills.py`](../shared/scripts/sync_skills.py)。
4. **用實體 copy，不要 symlink**：symlink 在 Windows clone 需 `core.symlinks=true` + Developer Mode 才還原，否則壞成純文字檔；copy 跨 OS 都穩。
5. **明確決定 git 策略**（二選一，寫進專案 `CLAUDE.md`）：
   - **兩份都 commit**：clone 即可用；代價是重複內容，靠 pre-commit `--check` 保證一致。
   - **只 commit canonical、gitignore 鏡像**：git 乾淨；代價是 clone / pull 後需自行 sync。
6. **掛 pre-commit `--check` hook**：防止改了 canonical 忘了 sync 就 commit 進不一致鏡像。團隊共用版用 `.pre-commit-config.yaml`（進 git），每位工程師 clone 後 `pre-commit install` 一次。

### 名詞

| 名詞 | 意思 |
|------|------|
| canonical | 真相來源／正本，你實際編輯的那份（`.agents/skills/`） |
| mirror | 從 canonical 複製、給特定工具掃描的副本（`.claude/skills/`） |
| sync | 把 canonical 複製成 mirror 的動作 |

### pre-commit 參考設定

```yaml
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

---

## 採用檢查清單

- [ ] 新 skill 建在 `.agents/skills/<skill>/`，含 `SKILL.md` + frontmatter（`name` / `description`）
- [ ] `scripts/sync_skills.py` 存在且 `--check` 可跑
- [ ] git 策略已決定並寫進專案 `CLAUDE.md`
- [ ] `.pre-commit-config.yaml` 含 `sync-skills-check`，工程師已 `pre-commit install`
- [ ] 專案 `CLAUDE.md` 註明「只改 canonical、改完跑 sync」
