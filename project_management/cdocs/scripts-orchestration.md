---
sources:
  - floor/scripts/floor.py
  - floor/scripts/shutdown.py
---

# Scripts — Orchestration

## floor.py

CLI entry point. Accepts one positional argument: the task description string. Checks the task counter — if >= 10, prints an arch-check-required message and exits. Otherwise, runs `check_cdocs.py`, reads `prompting.md` and `status.md`, assembles a base prompt, writes `.floor_session.json`, and launches `claude --model claude-sonnet-4-6` via `os.execvp`.

If `status.md` references `project_tasks_cli.py`, floor.py runs the list command and injects the results instead of the raw file contents.

The assembled prompt instructs the Claude session to act as a prompting assistant, iterate with the user, write the final prompt to `project_management/prompts/implement-this.md`, and record any matching status item ID in `.floor_session.json`. Stdlib only; no external dependencies.

## shutdown.py

Post-task cleanup script. Reads `.floor_session.json` for a matched status item ID. Runs four scripts in sequence: `check_cdoc_coverage.py`, `check_manifest.py`, `check_cdocs.py`, and `task_counter.py increment`. If a status item ID is present, includes it in the output for the agent to mark complete. Outputs all results as structured markdown. Ends with an "Actions Required" section. Cleans up `.floor_session.json` on exit.
