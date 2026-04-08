<!-- Template file. Customize: replace the cdoc routing table with rows matching your project's actual domains and context documents. The instructions above and below the table are universal and should be kept as-is. -->

# Pre-prompt

Before composing the prompt: run `python scripts/task_counter.py read` from the repo root to get the current Task Counter value. If the counter is 10 or greater, generate the architecture check prompt from `project_management/prompts/architecture-check.md` instead of a task prompt. Do not proceed with the steps below.

Run `python scripts/check_cdocs.py` from the repo root. If any cdocs are reported as STALE that would be part of the prompt, include a note in the generated prompt alerting the agent that those cdocs may not reflect the current source files. Do not stop — continue composing the prompt normally.

# Prompt instructions
Indicate the Claude model best suited for the task, not as part of the prompt.
The created prompt should be output to the user, not a markdown doc.

# Compose task prompt
Compose a prompt for a new session task to do the indicated work item.
The prompt should indicate that the plan must be presented first, before code changes.

# Interview user if neccessary
If there are management decisions that need to be made before the prompt can be created, ask the user, don't decide yourself.

# Include context
Include all the context someone would need, both code files and cdocs.
The prompt should always include an instruction to read project_management/manifest.md.
The prompt should include only the cdocs relevant to the task — do not by  default load all cdocs. Use the table below to decide which to include:

| Task involves... | Load these cdocs |
|-----------------|-----------------|
| [Replace with your top-level domain — e.g. core system / data model] | `cdocs/project-overview.md` |

<!-- Add one row per domain in your project. Each row should name a coherent area of the codebase and point to the cdoc(s) that capture it. -->

Where applicable, the prompt should indicate that project_management/standards/style.md should be followed when coding.
Where the task involves creating new files, adding imports, or changing module responsibilities, the prompt should indicate that project_management/standards/architecture.md should be read before planning.

# Close prompt
The prompt should indicate the following workflow item in addition to the task definition:

- When implementation is complete (task description fully implemented), before waiting for user confirmation:
    1. Write a brief summary of what was done.
    2. List suggested test steps for the user to verify the work — make clear that running tests is the user's responsibility, not the agent's.
    3. Explicitly pause and wait for the user to confirm the task is done.

- Only after the user has confirmed the task is done, run this checklist:

    1. **status.md** — mark the item relating to the completed task as done; add any newly discovered open items; run `python scripts/task_counter.py increment` from the repo root
    2. **manifest.md** — add a row for every new file created; remove rows for deleted files.
    3. **cdoc coverage** — run `python scripts/check_cdoc_coverage.py` from the repo root. Add any `UNCOVERED` files to the appropriate cdoc's `sources` list, or create a new cdoc if no suitable one exists.
    4. **context docs** — Read cdoc.md. Update appropriate context documents.
    5. **response to user** - Remind the user to make a git commit

