Compose a prompt for a new Claude Code session to implement the task. The prompt must:

1. Include an instruction to read `project_management/manifest.md` before proceeding.
2. Require the plan to be presented first, before any code changes.
3. The assembled prompt includes the full CACT summary tree. Use it to identify which parts of the codebase are relevant to the task. In the implementation prompt, instruct the acting agent to run `python project_management/scripts/cact_walk.py <relevant node keys>` to load its own context before proceeding. Do not paste summaries into the prompt — the agent walks the tree itself and gets live, up-to-date context.
4. Where applicable, direct the agent to follow `project_management/standards/style.md`. If the style standards node is relevant, add it to the CACT walk keys.
5. Where the task involves creating new files, adding imports, or changing module responsibilities, direct the agent to read `project_management/standards/architecture.md` before planning. Add the architecture standards node to the CACT walk keys if reasonable.

## Interview the user if necessary

If management decisions must be made before the prompt can be composed, ask the user — do not decide yourself.

## Model recommendation

After composing the prompt, indicate the Claude model best suited for the task. This is guidance for the user, not part of the prompt itself. Do not include in .md file; output to user.
