# AGENTS.md

專案層級規約，給 coding agent 與所有工程師遵守。

## 遵循的公司標準

本專案遵循 Company-Standards（掛在 `./Company-Standards`，pin v0.5.0）。除非下方「專案特例」另有說明，一律以標準為準：

- Agent instructions：`Company-Standards/standards/agent-instructions-standard.md`
- 命名：`Company-Standards/standards/file-naming-standards.md`
- Git / commit / PR / 版本：`Company-Standards/standards/git-workflow-standard.md`
- ADR 流程：`Company-Standards/standards/adr-standard.md`
- API 設計：`Company-Standards/standards/api-design-standard.md`
- EditorConfig：`Company-Standards/standards/editorconfig-standard.md`
- Skills：`Company-Standards/standards/skills-create-and-management-standard.md`

## Agent Instructions

- canonical：`AGENTS.md`（只改這裡）。
- mirrors：`CLAUDE.md`、`GEMINI.md`、`.cursor/rules/project.mdc`（產生物，勿手改）。
- 改完跑 `python3 scripts/sync_agent_instructions.py`；commit 由 pre-commit `--check` 把關。
- git 策略：<全部 commit | 只 commit canonical>（在此明確寫死本專案採哪種）。

## Skills（若本專案有 skills）

- canonical：`.agents/skills/`（只改這裡）；mirror：`.claude/skills/`（產生物，勿手改）。
- 改完跑 `python3 scripts/sync_skills.py`；commit 由 pre-commit `--check` 把關。
- git 策略：<兩份都 commit | 只 commit canonical>（在此明確寫死本專案採哪種）。

## 專案特例

<與公司標準有出入之處寫在這，並連到對應的 repo-local ADR>
