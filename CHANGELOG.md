# Changelog

採語意化版本（SemVer）。每次發布請更新本檔與 [`VERSION`](VERSION)，並打對應 git tag `vX.Y.Z`。

## [0.3.0] - 2026-06-28

### Added
- `standards/git-workflow-standard.md`：branch / commit（Conventional Commits）/ push / PR 規範與 SemVer / release 政策。
- `standards/adr-standard.md`：ADR 流程與生命週期；`templates/adr/ADR-template.md` 模板。
- `standards/api-design-standard.md`：HTTP / REST API 設計準則。
- `standards/editorconfig-standard.md` + 根 `.editorconfig`（canonical 共用設定）。
- `shared/scripts/sync_skills.py`：通用 skills sync script（從各專案 local 提升為共用資產）。
- `templates/repo-template/`：新專案起手骨架（CLAUDE.md / .gitignore / .pre-commit / PR template / ADR 與 skills 目錄結構）。

### Changed
- `skills-management-standard.md` → `skills-create-and-management-standard.md`，新增「建立新 skill」（命名、SKILL.md frontmatter、結構）一節。

## [0.2.0] - 2026-06-28

### Added
- 初始化獨立的 Company-Standards repo 作為跨專案 single source of truth。
- `standards/file-naming-standards.md`：檔名與目錄命名規約（沿用既有 company baseline v0.2）。
- `standards/skills-management-standard.md`：Agent skills 的單一真相來源 + sync 機制（含 canonical/mirror 區分、sync script、為何用 copy 而非 symlink、pre-commit 把關、git 策略）。
- `README.md`：使用方式（submodule / 共用 pre-commit）、三層規約分層說明。

### Notes
- 共用 pre-commit hooks 目前仍由各專案以 `repo: local` 實作，後續版本計畫搬上本 repo 統一提供。
