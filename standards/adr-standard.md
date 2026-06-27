# Architecture Decision Record (ADR) Standard

Status: Company baseline v0.3.0

## 是什麼 / 為什麼

ADR 是一篇短文，記錄一個**重要架構決策**的背景、決定與後果。它是**不可變的歷史紀錄**：決策會被取代，但不被竄改。目的是讓「為什麼當初這樣決定」可追溯，避免後人重踩或盲改。

## 什麼時候要寫

決策若**難以反轉**或**影響結構**，就寫一篇：

- 技術 / 框架 / 資料庫選型
- 資料模型、API contract、跨切面模式（auth、錯誤處理、快取策略）
- **偏離某條公司標準**（在這裡記錄理由，對應 file-naming / git-workflow 等標準的「per-project 例外」）

瑣碎、可輕易反轉的決定不需要 ADR。

## 位置與命名

```
docs/architecture/decisions/ADR-NNN-kebab-title.md
```

- `NNN` 為補零流水號（`001`, `002`…）。
- 例：`ADR-001-initial-architecture.md`、`ADR-007-use-cursor-pagination.md`。

## 狀態與生命週期

`Proposed → Accepted → (Superseded by ADR-XXX | Deprecated)`

- **不要編輯已 Accepted 的 ADR 的決策內容**；要改決定就寫一篇新的去 supersede 它，並在舊的標 `Superseded by ADR-XXX`。

## 流程

1. 開 PR 附上 ADR 草稿（狀態 `Proposed`）。
2. 討論、收斂 → 合併時改成 `Accepted`。
3. 實作該決策的後續 PR 連回這篇 ADR。

模板見 [`templates/adr/ADR-template.md`](../templates/adr/ADR-template.md)。
