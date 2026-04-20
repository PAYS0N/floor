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
| Framework structure, conventions, project management | `cdocs/floor-system.md` |
| Scripts, automation, task lifecycle | `cdocs/scripts-orchestration.md`, `cdocs/scripts-and-checks.md` |
| Agent roles, responsibilities, workflow | `cdocs/agents-and-roles.md` |
| Template scaffolding, onboarding | `cdocs/template-scaffolding.md` |

# Shutdown
- When implementation is complete (task description fully implemented), before waiting for user confirmation:

    1. Write a brief summary of what was done.
    2. List suggested test steps for the user to verify the work — make clear that running tests is the user's responsibility, not the agent's.
    3. Explicitly pause and wait for the user to confirm the task is done.

- Only after the user has confirmed the task is done, run scripts/shutdown.py.

## Model recommendation

After composing the prompt, indicate the Claude model best suited for the task. This is guidance for the user, not part of the prompt itself. Do not include in .md file; output to user.
