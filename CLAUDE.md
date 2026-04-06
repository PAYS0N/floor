## Project Summary

Read project_management/manifest.md.

Floor is a project management template system for AI-assisted software development, providing structured conventions, standards, and prompts that give Claude consistent context across sessions.


## Project Rules

- Challenge requests that are logically or structurally wrong, or where a clearly better approach exists (e.g. using markdown as a database). Briefly explain the concern and suggest an alternative before proceeding.

- Remember: If tracing code execution manually to understand a bug requires more than 2-3 reasoning steps without certainty, add targeted logging statements, ask the user to run them, and use the output to diagnose rather than guessing.

- All non-code files should be markdown unless specifically mentioned otherwise.

- Remember: When asked to create or edit a context document, read project_management/cdoc.md.

- When asked to create project management files, create them in the project_management directory in root.

- When asked to create a prompt, read project_management/prompting.md. Do not rely on memory, re-read it every time.

- Before creating new source files, adding cross-module imports, or moving responsibilities between modules, read `project_management/standards/architecture.md`.

- When the user requests a feature/task implementation that requires more than one clear step, read prompting.md and enter the Q&A phase before doing anything else.