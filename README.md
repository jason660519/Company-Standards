# Company Standards

跨專案的公司工程基線（single source of truth）。所有專案**引用**這個 repo，而不是各自複製，避免標準漂移。

目前版本見 [`VERSION`](VERSION)，變更見 [`CHANGELOG.md`](CHANGELOG.md)。

## 標準清單

| 標準 | 說明 |
|------|------|
| [standards/file-naming-standards.md](standards/file-naming-standards.md) | 檔名與目錄命名規約 |
| [standards/skills-management-standard.md](standards/skills-management-standard.md) | Agent skills 的單一真相來源 + sync 機制 |

## 怎麼在專案裡使用（reference, not copy）

核心原則：**這個 repo 是 SSoT，專案用引用的方式取得，不要複製貼上。**

### 方式 A — git submodule（推薦，文件/規約類）

把本 repo 掛進專案的固定路徑、pin 在某個版本：

```bash
git submodule add https://github.com/jason660519/Company-Standards.git standards
git -C standards checkout v0.2.0     # pin 版本
git commit -m "chore: vendor Company-Standards v0.2.0 as submodule"
```

升級到新版本時：

```bash
git -C standards fetch --tags
git -C standards checkout v0.3.0
git commit -am "chore: bump Company-Standards -> v0.3.0"
```

clone 專案的人要記得 `git clone --recursive`，或 clone 後 `git submodule update --init`。

專案的 `CLAUDE.md` 保持薄，只寫「本專案如何套用」並指向 submodule 內的標準，例如：

```markdown
本專案遵循 Company-Standards（見 ./standards），
skills 結構依 standards/skills-management-standard.md 實作。
```

### 方式 B — 共用 pre-commit hooks（可執行規則）

可執行的檢查（如 skills sync 檢查）之後會以 pre-commit 遠端 repo 形式提供，專案只需在 `.pre-commit-config.yaml` 引用：

```yaml
repos:
  - repo: https://github.com/jason660519/Company-Standards
    rev: v0.2.0
    hooks:
      - id: <hook-id>
```

（目前 hook 仍以各專案 `repo: local` 實作，後續版本會搬上來統一。）

## 版本與相容性

- 採語意化版本（SemVer）。標準有破壞性變更 → bump major。
- 專案 pin 在某個 tag，主動決定何時升級；不會被動受影響。
- 每次變更都要更新 `CHANGELOG.md` 與 `VERSION`，並打 git tag（`vX.Y.Z`）。

## 三層規約怎麼分（避免混淆）

| 層級 | 放哪 | 例子 |
|------|------|------|
| 個人偏好（跨專案、私人） | `~/.claude/CLAUDE.md` | 語氣、工具偏好 |
| **公司標準（跨專案、共用）** | **本 repo** | 命名規約、skills 機制 |
| 專案實作（單一 repo） | 該 repo 的 `CLAUDE.md` / ADR | 實際路徑、專案特例 |
