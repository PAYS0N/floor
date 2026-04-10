<!-- Template file. Customize: replace the cdoc routing table with rows matching your project's actual domains and context documents. -->

Compose a prompt for a new Claude Code session to implement the task. The prompt must:

1. Include an instruction to read `project_management/manifest.md` before proceeding.
2. Require the plan to be presented first, before any code changes.
3. Include only the cdocs relevant to the task — use the routing table below.
4. Where applicable, direct the agent to follow `project_management/standards/style.md`.
5. Where the task involves creating new files, adding imports, or changing module responsibilities, direct the agent to read `project_management/standards/architecture.md` before planning.

## Interview the user if necessary

If management decisions must be made before the prompt can be composed, ask the user — do not decide yourself.

## Cdoc routing table

| Task involves... | Load these cdocs |
|-----------------|-----------------|
| [Replace with your top-level domain — e.g. core system / data model] | `cdocs/project-overview.md` |

<!-- Add one row per domain in your project. Each row should name a coherent area of the codebase and point to the cdoc(s) that capture it. -->

## Model recommendation

After composing the prompt, indicate the Claude model best suited for the task. This is guidance for the user, not part of the prompt itself.
