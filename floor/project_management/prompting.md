<!-- Template file. Customize: replace the cdoc routing table with rows matching your project's actual domains and context documents. The instructions above and below the table are universal and should be kept as-is. -->

Before composing the prompt: check the Task Counter in `project_management/status.md`. If the counter is 10 or greater, generate the architecture check prompt from `project_management/prompts/architecture-check.md` instead of a task prompt. Do not proceed with the steps below.

Compose a prompt for a new session task to do the indicated work item.
Include all the context someone would need, both practical code files and cdocs.
The prompt should always include an instruction to read project_management/manifest.md.
The prompt should include only the cdocs relevant to the task — do not load all cdocs. Use the table below to decide which to include:

| Task involves... | Load these cdocs |
|-----------------|-----------------|
| [Replace with your top-level domain — e.g. core system / data model] | `cdocs/project-overview.md` |

<!-- Add one row per domain in your project. Each row should name a coherent area of the codebase and point to the cdoc(s) that capture it. -->

Where applicable, the prompt should indicate that project_management/standards/style.md should be followed when coding.
Where the task involves creating new files, adding imports, or changing module responsibilities, the prompt should indicate that project_management/standards/architecture.md should be read before planning.
If there are management decisions that need to be made before the prompt can be created, ask the user, don't decide yourself.
The prompt should indicate that the plan must be presented first, before code changes.
The prompt should indicate the following workflow item in addition to the task definition:

- Run this checklist after the user has declared the task done (make it clear to run this after completion is externally confirmed, not when it thinks it's done.):

    1. **status.md** — remove the item from Open; add any newly discovered open items; increment the Task Counter by 1.
    2. **manifest.md** — add a row for every new file created; remove rows for deleted files.
    3. **context docs** — Read cdoc.md. Update appropriate context documents.
    4. **response to user** - Remind the user to make a git commit

Indicate the Claude model best suited for the task, not as part of the prompt.
The created prompt should be output to the user, not a markdown doc.
