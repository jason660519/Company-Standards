# Releasing Company-Standards

如何發布新版本。消費端（submodule / pre-commit `rev:`）都釘 tag，所以**變更只有在你打 tag 後才會傳到各專案**。

## 版本怎麼選（SemVer）

| Bump | 什麼情況 |
|------|---------|
| **PATCH** `x.y.Z` | 錯字、措辭澄清、不改變規則語意的編輯 |
| **MINOR** `x.Y.0` | 新增標準 / 模板 / hook，或對既有標準做**向後相容**的擴充 |
| **MAJOR** `X.0.0` | **破壞性**：移除 / 重命名標準、改變既有規則導致既有專案需要改動 |

> `0.x` 階段：MINOR 可含破壞性變更，但 **CHANGELOG 必須明確標示**。

## 發版步驟

1. 改內容（只改該改的；遵守本 repo 自己的標準）。
2. 把變更記到 `CHANGELOG.md` 的 `## [Unreleased]`（分 Added / Changed / Removed）。
3. 決定版本號，更新：
   - `VERSION` → `X.Y.Z`
   - `CHANGELOG.md`：把 `## [Unreleased]` 改成 `## [X.Y.Z] - YYYY-MM-DD`
   - 若新增 / 改 hook：確認 `.pre-commit-hooks.yaml` 與 `hooks/` 腳本正確
4. commit（Conventional Commits）。
5. 打 annotated tag 並 push：
   ```bash
   git tag -a vX.Y.Z -m "Company-Standards vX.Y.Z"
   git push origin main vX.Y.Z
   ```
6. （選用）開 GitHub Release，貼上 CHANGELOG 對應段落。

## 消費端怎麼跟上

- 釘 tag 的專案不會自動變。
- **Renovate** 偵測到新 tag → 自動開 bump PR → 各專案 review + merge 才升級。

## 注意

- **main 可以領先最後一個 tag**（未發布的變更先放 `## [Unreleased]`）——這是正常狀態；只有「要發布」時才打 tag。
- **不要動已發布的 tag**（immutable）。要修就發新版。
