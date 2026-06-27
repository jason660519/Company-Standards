# API Design Standard

Status: Company baseline v0.3.0
Scope: HTTP / REST（GraphQL、gRPC 之 addendum 後續版本補）。

## 原則

- **Resource-oriented**：用名詞不用動詞；集合用複數。`/users`、`/users/{id}`。
- 一致性優先於聰明。團隊內慣例統一，勝過每個 endpoint 各自最佳化。

## URL 與方法

- `GET`（讀、safe）、`POST`（建立）、`PUT`（整體取代）、`PATCH`（部分更新）、`DELETE`。
- 路徑 kebab-case、無結尾斜線、無副檔名。
- 巢狀**最多一層**：`/users/{id}/orders`，更深就改用 query 或頂層資源。

## 版本

- 版本放路徑：`/v1/…`。Breaking change → bump major。**不要默默破壞 `v1`**。

## Request / Response

- 一律 JSON。欄位命名 snake_case 或 camelCase **全公司擇一**（baseline：`snake_case`）並貫徹。
- 時間用 ISO-8601 UTC（`2026-06-28T00:00:00Z`）。金額用最小單位整數 + currency 欄位，不用 float。
- 分頁：優先 **cursor-based**（`limit` + `cursor`），回傳 `next_cursor`。
- 過濾 / 排序走 query params：`?status=active&sort=-created_at`。

## 狀態碼

- 成功：`200` / `201`（建立）/ `204`（無內容）。
- 用戶端：`400` 格式錯、`401` 未認證、`403` 無權限、`404` 不存在、`409` 衝突、`422` 語意驗證失敗、`429` 限流。
- 伺服器：`5xx`。

## 錯誤格式

統一信封，含**穩定的機器可讀 code**：

```json
{ "error": { "code": "user_not_found", "message": "User 42 does not exist", "details": {} } }
```

## 其他

- 不安全且會重試的操作支援 **idempotency key**。
- 回傳限流標頭（`RateLimit-*`）。
- **URL 不放 secrets / token**。
- 以 **OpenAPI** 文件化，與實作同 repo、同步維護。
