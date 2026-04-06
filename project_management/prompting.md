# Pre-prompt
Before composing the prompt: check the Task Counter in `project_management/status.md`. If the counter is 10 or greater, generate the architecture check prompt from `project_management/prompts/architecture-check.md` instead of a task prompt. Do not proceed with the steps below.

# Prompt instructions
Indicate the Claude model best suited for the task, not as part of the prompt.
The created prompt should be output to the user, not a markdown doc.

# Compose task prompt
Compose a prompt for a new session task to do the indicated work item.
The prompt should indicate that the plan must be presented first, before code changes.

# Interview user if neccessary - Q&A
If there are management decisions that need to be made before the prompt can be created, ask the user, don't decide yourself.

# Include context
Include all the context someone would need, both code files and cdocs.
The prompt should always include an instruction to read project_management/manifest.md.
The prompt should include only the cdocs relevant to the task — do not by  default load all cdocs. Use the table below to decide which to include:

| Task involves... | Load these cdocs |
|-----------------|-----------------|
| Template structure, design decisions, what Floor is/isn't | `cdocs/floor-system.md` |

Where applicable, the prompt should indicate that project_management/standards/style.md should be followed when coding.
Where the task involves creating new files, adding imports, or changing module responsibilities, the prompt should indicate that project_management/standards/architecture.md should be read before planning.

# Close prompt
The prompt should indicate the following workflow item in addition to the task definition:

- When implementation is complete (task description fully implemented), before waiting for user confirmation:
    1. Write a brief summary of what was done.
    2. List suggested test steps for the user to verify the work — make clear that running tests is the user's responsibility, not the agent's.
    3. Explicitly pause and wait for the user to confirm the task is done.

- Only after the user has confirmed the task is done, run this checklist:

    1. **status.md** — remove the item from Open; add any newly discovered open items; increment the Task Counter by 1.
    2. **manifest.md** — add a row for every new file created; remove rows for deleted files.
    3. **context docs** — Read cdoc.md. Update appropriate context documents.
    4. **response to user** - Remind the user to make a git commit

