<!-- Template file. Customize: replace the Project Summary block with your project's name and description. All rules below are universal and should be kept as-is. -->

## Project Summary

Read project_management/manifest.md.

[PROJECT NAME] is a [brief description].

## Response rules

- When the user requests a feature/task implementation or a prompt, read and follow prompting.md before doing anything else.

## Meta rules

- Challenge requests that are logically or structurally wrong, or where a clearly better approach exists (e.g. using markdown as a database). Briefly explain the concern and suggest an alternative before proceeding.

- Remember: If tracing code execution manually to understand a bug requires more than 2-3 reasoning steps without certainty, add targeted logging statements, ask the user to run them, and use the output to diagnose rather than guessing.

- Remember: All non-code files should be markdown unless specifically mentioned otherwise.

## Context Rules

- Remember: When asked to create or edit a context document, read project_management/cdoc.md.

- Remember: When asked to record an issue or summarize project status, read project_management/status.md.

- Remember: When asked to create project management files, create them in the project_management directory in root.

- Remember: Before creating new source files, adding cross-module imports, or moving responsibilities between modules, read `project_management/standards/architecture.md`.