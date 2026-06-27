# Git Workflow Standard

Status: Company baseline v0.3.0

涵蓋 branch / commit / push / PR / 版本與 release 政策。專案特例寫進 repo-local ADR。

## Branching

- **`main` 永遠可發布**，是預設分支。
- 採 **trunk-based**：開短命分支、儘快合回，不要長命 `develop` 分支。
- 分支命名：`<type>/<kebab-short-desc>`，type 用 commit 同一套：
  - `feat/auth-token-refresh`、`fix/null-pointer-on-login`、`chore/bump-deps`、`docs/api-guide`、`refactor/…`、`test/…`、`ci/…`
- 經常 `git pull --rebase` 跟上 `main`，保持線性歷史。

## Commits（Conventional Commits）

- 格式：`type(scope)?: subject`
- type：`feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`
- subject：祈使句、≤72 字、結尾不加句點。
- **Breaking change**：type/scope 後加 `!`（如 `feat!:`）或在 footer 寫 `BREAKING CHANGE:`。
- body 重點寫 **WHY**（可中英混雜）；配對開發加 `Co-Authored-By:` footer。

```
feat(auth): refresh access token before expiry

避免長工作階段中途 401；改在到期前 60s 主動換 token。

BREAKING CHANGE: TokenProvider.get() 現在回傳 Promise。
```

## Push 規則

- **不要 push 直接進 `main`** —— 一律走 PR（repo owner 初始化骨架例外）。
- **絕不 force-push 共享分支**（`main` 或別人的分支）。只在自己的 feature 分支用 `--force-with-lease`。
- `git pull --rebase` 為預設，避免無意義 merge commit。

## Pull Requests

- 一個 PR 一個邏輯變更，**保持小**。
- 標題遵循 Conventional Commits。
- 描述：what / why、UI 改動附截圖、測試說明、連到 issue / ADR。
- 合併門檻：CI 綠燈、≥1 review、無未解決討論串。
- **合併策略：squash merge**（`main` 上一個變更一個 Conventional Commit），合併後刪分支。
- 用 `CODEOWNERS` 自動指派 reviewer。

## Versioning & Release（SemVer）

- `MAJOR.MINOR.PATCH`：breaking→major、feature→minor、fix→patch。
- `0.x` 階段：minor 可含 breaking，但**務必在 CHANGELOG 標明**。
- 每次發布：更新 `CHANGELOG.md`（Keep a Changelog 風格）+ `VERSION`，打 **annotated tag `vX.Y.Z`**。
- 從 `main` 發布；pre-release 用 `vX.Y.Z-rc.N`。
