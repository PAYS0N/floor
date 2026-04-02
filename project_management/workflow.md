# Session Workflow

## Standard Task Session

1. **Open a new session.** Tell Claude to create a prompt for the task you want to do (e.g. "Create a prompt for adding X feature").
2. **Claude generates the prompt.** Review it. Modify any details that need adjusting — scope, referenced files, constraints.
3. **Open a new session.** Paste the modified prompt. Complete the task with Claude.
4. **Confirm done.** Once you are satisfied with the work, tell Claude the task is complete. Claude will run the post-task checklist (status.md, manifest.md, context docs, commit reminder).
5. **Commit.** Make a git commit.

## Architecture Health Check

After approximately every 10 task sessions, run the architecture health check:

1. Open a new session.
2. Paste the contents of `project_management/prompts/architecture-check.md` as the prompt.
3. Claude will map the current architecture, run forbidden pattern checks, compare to the stored baseline, and produce a verdict.
4. If the verdict is PASS or PASS WITH NOTES, Claude updates the baseline. If FAIL, fix the violations before the next session.