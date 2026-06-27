# CLAUDE.md

專案層級規約，給 coding agent 與所有工程師遵守。

## 遵循的公司標準

本專案遵循 Company-Standards（掛在 `./standards`，pin v0.3.0）。除非下方「專案特例」另有說明，一律以標準為準：

- 命名：`standards/standards/file-naming-standards.md`
- Git / commit / PR / 版本：`standards/standards/git-workflow-standard.md`
- ADR 流程：`standards/standards/adr-standard.md`
- API 設計：`standards/standards/api-design-standard.md`
- EditorConfig：`standards/standards/editorconfig-standard.md`
- Skills：`standards/standards/skills-create-and-management-standard.md`

## Skills（若本專案有 skills）

- canonical：`.agents/skills/`（只改這裡）；mirror：`.claude/skills/`（產生物，勿手改）。
- 改完跑 `python scripts/sync_skills.py`；commit 由 pre-commit `--check` 把關。
- git 策略：<兩份都 commit | 只 commit canonical>（在此明確寫死本專案採哪種）。

## 專案特例

<與公司標準有出入之處寫在這，並連到對應的 repo-local ADR>
