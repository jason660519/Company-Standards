# Changelog

採語意化版本（SemVer）。每次發布請更新本檔與 [`VERSION`](VERSION)，並打對應 git tag `vX.Y.Z`。

## [0.2.0] - 2026-06-28

### Added
- 初始化獨立的 Company-Standards repo 作為跨專案 single source of truth。
- `standards/file-naming-standards.md`：檔名與目錄命名規約（沿用既有 company baseline v0.2）。
- `standards/skills-management-standard.md`：Agent skills 的單一真相來源 + sync 機制（含 canonical/mirror 區分、sync script、為何用 copy 而非 symlink、pre-commit 把關、git 策略）。
- `README.md`：使用方式（submodule / 共用 pre-commit）、三層規約分層說明。

### Notes
- 共用 pre-commit hooks 目前仍由各專案以 `repo: local` 實作，後續版本計畫搬上本 repo 統一提供。
