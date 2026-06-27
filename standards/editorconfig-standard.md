# EditorConfig Standard

Status: Company baseline v0.3.0

[EditorConfig](https://editorconfig.org/) 讓不同編輯器 / IDE 對縮排、換行、編碼有一致行為，是「跨工具的最低共識」，多數編輯器原生或一個外掛即支援。

## 規則

- 每個 repo **根目錄放一份 `.editorconfig`**，內容以本 repo 根的 [`.editorconfig`](../.editorconfig) 為 canonical。
- 採用方式：**複製** canonical 到專案根（這是少數適合直接 copy 的檔——它幾乎不變，且工具要求它實際存在於 repo 根；有更新時重新 copy 即可）。
- 基線重點：UTF-8、LF 換行、結尾換行、去尾端空白、預設 2 空格；Python 4 空格、Makefile/Go 用 tab、Markdown 保留尾端空白（換行語意）、Windows batch 用 CRLF。

## 與其他工具的關係

EditorConfig 管「編輯器層」的基本格式；語言專屬的 formatter（Prettier / Ruff / gofmt）管更細的風格，兩者並存、不衝突。語言 formatter 設定屬於「可執行共用設定」，後續版本以套件 / 引用方式提供。
