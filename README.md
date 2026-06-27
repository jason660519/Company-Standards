# Company Standards

跨專案的公司工程基線（single source of truth）。所有專案**引用**這個 repo，而不是各自複製，避免標準漂移。

目前版本見 [`VERSION`](VERSION)，變更見 [`CHANGELOG.md`](CHANGELOG.md)。

## 標準清單

| 標準 | 說明 |
|------|------|
| [standards/agent-instructions-standard.md](standards/agent-instructions-standard.md) | Agent instructions 的 `AGENTS.md` canonical + tool-specific mirror 機制 |
| [standards/file-naming-standards.md](standards/file-naming-standards.md) | 檔名與目錄命名規約 |
| [standards/git-workflow-standard.md](standards/git-workflow-standard.md) | branch / commit / push / PR 規範 + SemVer / release 政策 |
| [standards/adr-standard.md](standards/adr-standard.md) | Architecture Decision Record 流程 |
| [standards/api-design-standard.md](standards/api-design-standard.md) | HTTP / REST API 設計準則 |
| [standards/editorconfig-standard.md](standards/editorconfig-standard.md) | EditorConfig 共用設定（canonical：根 [`.editorconfig`](.editorconfig)） |
| [standards/skills-create-and-management-standard.md](standards/skills-create-and-management-standard.md) | Agent skills 的建立規範 + 單一真相來源 + sync 機制 |

## 共用資產（consumable）

| 路徑 | 內容 |
|------|------|
| [`.editorconfig`](.editorconfig) | canonical EditorConfig，複製到專案根 |
| [`shared/scripts/sync_agent_instructions.py`](shared/scripts/sync_agent_instructions.py) | 通用 agent instructions sync script（無依賴、跨 OS） |
| [`shared/scripts/sync_skills.py`](shared/scripts/sync_skills.py) | 通用 skills sync script（無依賴、跨 OS） |
| [`templates/repo-template/`](templates/repo-template/) | 新專案起手骨架 |
| [`templates/adr/ADR-template.md`](templates/adr/ADR-template.md) | ADR 模板 |

## 怎麼在專案裡使用（reference, not copy）

核心原則：**這個 repo 是 SSoT，專案用引用的方式取得，不要複製貼上。**

### 方式 A — git submodule（推薦，文件/規約類）

把本 repo 掛進專案的固定路徑、pin 在某個版本：

```bash
git submodule add https://github.com/jason660519/Company-Standards.git Company-Standards
git -C Company-Standards checkout v0.5.0     # pin 版本
git commit -m "chore: vendor Company-Standards v0.5.0 as submodule"
```

升級到新版本時：

```bash
git -C Company-Standards fetch --tags
git -C Company-Standards checkout vX.Y.Z
git commit -am "chore: bump Company-Standards -> vX.Y.Z"
```

clone 專案的人要記得 `git clone --recursive`，或 clone 後 `git submodule update --init`。

專案的 `AGENTS.md` 保持薄，只寫「本專案如何套用」並指向 submodule 內的標準，例如：

```markdown
本專案遵循 Company-Standards（見 ./Company-Standards），
agent instructions 結構依 Company-Standards/standards/agent-instructions-standard.md 實作。
```

### 方式 B — 共用 pre-commit hooks（可執行規則）

本 repo 是 pre-commit hook repo（根有 `.pre-commit-hooks.yaml`）。專案只需在 `.pre-commit-config.yaml` 引用，不必各自複製 hook 腳本：

```yaml
repos:
  - repo: https://github.com/jason660519/Company-Standards
    rev: v0.5.0
    hooks:
      - id: sync-agent-instructions-check
      - id: sync-skills-check   # .claude/skills 是否與 .agents/skills 一致
```

裝法：`uv tool install pre-commit && pre-commit install`。hook 以使用方 repo 為工作目錄執行，repo 沒有 `.agents/skills/` 時自動跳過。

可用 hooks 見根目錄 [`.pre-commit-hooks.yaml`](.pre-commit-hooks.yaml)。

## 版本與相容性

- 採語意化版本（SemVer）。標準有破壞性變更 → bump major。
- 專案 pin 在某個 tag，主動決定何時升級；不會被動受影響。
- 每次變更都要更新 `CHANGELOG.md` 與 `VERSION`，並打 git tag（`vX.Y.Z`）。

## 三層規約怎麼分（避免混淆）

| 層級 | 放哪 | 例子 |
|------|------|------|
| 個人偏好（跨專案、私人） | `~/.claude/CLAUDE.md` | 語氣、工具偏好 |
| **公司標準（跨專案、共用）** | **本 repo** | 命名規約、agent instructions、skills 機制 |
| 專案實作（單一 repo） | 該 repo 的 `AGENTS.md` / ADR | 實際路徑、專案特例 |
