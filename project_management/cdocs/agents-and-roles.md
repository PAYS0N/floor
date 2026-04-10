---
sources:
  - floor/CLAUDE.md
  - floor/scripts/floor.py
  - floor/scripts/shutdown.py
  - floor/project_management/prompting.md
  - floor/project_management/prompts/architecture-check.md
---

# Agents and Roles

## Workflow

The CLI script `floor.py` initiates all workflows. Agents operate within sessions launched or triggered by scripts.

**floor.py (CLI entry point)** — Run by the user from the command line with a task description.

1. Reads the task counter. If >= 10, prints a message that an architecture check is required and exits — no session is launched.
2. Runs `check_cdocs.py` and captures staleness output.
3. Reads `prompting.md` (prompt composition rules) and `status.md` (open items).
4. Assembles a base prompt combining: composition rules, cdoc staleness warnings, status items, and the task description. Instructs the session to act as a prompting assistant, iterate with the user, and write the final prompt to `project_management/prompts/implement-this.md`.
5. Writes `.floor_session.json` to the repo root.
6. Launches `claude --model claude-sonnet-4-6` with the assembled prompt via `os.execvp`.

**Task agent (Claude Code session)** — The user says "implement" in Claude Code.

1. CLAUDE.md response rule fires. Reads the prompt file (`implement-this.md` by default).
2. Reads `manifest.md` and all specified cdocs.
3. Presents an implementation plan and waits before touching any files.
4. Implements following `style.md`; reads `architecture.md` before creating files or adding imports.
5. Writes a summary and test steps, then explicitly pauses for user confirmation.
6. After confirmation: runs `shutdown.py`, which handles all post-task checks and outputs structured results. The agent follows the output to update documentation and reminds the user to commit.

**Architecture check agent** — A fresh Claude Code session. The user runs the arch-check prompt (from `prompts/architecture-check.md`) when `floor.py` reports the counter has reached the threshold.

1. Reads `architecture.md` and `artifacts/architecture-baseline.md`.
2. Reads every file in `floor/`, mapping all inter-file references and state mutations.
3. Generates four Mermaid diagrams.
4. Compares to the baseline; flags violations.
5. Issues verdict: PASS, PASS WITH NOTES, or FAIL.
6. On PASS/PASS WITH NOTES: overwrites baseline and diagram files; resets task counter to 0.
7. On FAIL: presents violations to the user for a new task to fix.

**User**

- Runs `floor.py "<task>"` to start the workflow.
- Iterates on the prompt in the Claude CLI session.
- Optionally edits the prompt file before implementing.
- Says "implement" in Claude Code to trigger the task agent.
- Reviews the plan before implementation proceeds.
- Runs verification steps; confirms task completion.
- Makes git commits.

## Break Points

| Stage | What goes wrong | Downstream effect |
|-------|-----------------|-------------------|
| floor.py — cdoc check | Stale warning not surfaced | Prompt built on outdated cdoc descriptions |
| Prompting session — cdoc selection | Wrong cdocs included or omitted | Task agent has missing or irrelevant context |
| Prompting session — interview skipped | Agent decides management questions | Unreviewed assumptions baked into the task |
| Task agent — plan skipped | Implementation without review | Design and architecture errors proceed unchecked |
| Task agent — architecture.md skipped | Files/imports added without checking layers | Layer violations introduced silently |
| Task agent — confirmation skipped | shutdown.py runs before user reviews | Correction window lost; errors locked in |
| shutdown.py — checks skipped | Management files not updated | Drift in manifest, cdocs; stale context for future sessions |
| Arch check — files missed in mapping | Incomplete dependency graph | False PASS; violations go undetected |
| User — plan not reviewed | No human review gate | Design errors proceed without check |
| User — tests skipped before confirming | Confirmation without verification | Regressions treated as passing |

## Correction Mechanisms

- **Stale cdoc detection** (`check_cdocs.py`) — Run by `floor.py` pre-session and by `shutdown.py` post-task. Catches cdocs whose source files changed.
- **Cdoc coverage** (`check_cdoc_coverage.py`) — Run by `shutdown.py` post-task. Catches repo files not declared as a source in any cdoc.
- **Manifest audit** (`check_manifest.py`) — Run by `shutdown.py` post-task. Reports MISSING and DEAD manifest entries.
- **Task Counter** — Incremented by `shutdown.py` after each task; resets to 0 on a clean arch check. `floor.py` gates new tasks when the counter reaches 10.
- **Plan-first gate** — Task agent presents plan and waits; primary mechanism for catching design errors.
- **User confirmation gate** — Task agent pauses after implementation; gives the user a window to catch errors before shutdown runs.
