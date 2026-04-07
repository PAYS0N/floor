---
sources:
  - floor/CLAUDE.md
  - floor/project_management/prompting.md
  - floor/project_management/prompts/architecture-check.md
---

# Agents and Roles

## Workflow

All Claude sessions start fresh. The three agent types below are distinct sessions with no shared state.

**Prompting agent** — The Claude session in the user's active project session. CLAUDE.md's response rule triggers it unconditionally when the user requests a task.

1. Checks Task Counter in status.md. If ≥ 10, generates the architecture check prompt from architecture-check.md and stops; no task prompt is produced.
2. Runs `check_cdocs.py`. If relevant cdocs are stale, inserts a warning into the generated prompt.
3. Interviews the user if management decisions are needed before the prompt can be composed.
4. Selects cdocs from the routing table in prompting.md; outputs a complete prompt text (not a file) to the user.

**Task agent** — A fresh Claude session. The user pastes the generated prompt to start it.

1. Reads manifest.md and all specified cdocs.
2. Presents an implementation plan and waits before touching any files.
3. Implements following style.md; reads architecture.md before creating files or adding imports.
4. Writes a summary and test steps, then explicitly pauses for user confirmation.
5. After confirmation: increments Task Counter in status.md, updates manifest.md, runs `check_cdoc_coverage.py`, updates affected cdocs, reminds user to commit.

**Architecture check agent** — A fresh Claude session. The prompting agent generates this prompt from architecture-check.md when the Task Counter reaches 10; the user pastes it.

1. Reads architecture.md and architecture-baseline.md.
2. Reads every file in `floor/`, mapping all inter-file references and state mutations.
3. Generates a Mermaid dependency graph (four sections).
4. Compares to the baseline; flags new/removed references, layer violations, shifted responsibilities.
5. Issues verdict: PASS, PASS WITH NOTES, or FAIL.
6. On PASS or PASS WITH NOTES: overwrites the baseline, resets Task Counter to 0.
7. On FAIL: presents violations to the user; user initiates a new task agent to fix them.

**User**

- Requests tasks; answers prompting agent interviews.
- Opens a fresh session and pastes the generated prompt.
- Reviews the task agent's plan before implementation proceeds.
- Runs verification steps listed by the task agent; confirms task completion.
- Makes git commits.

## Break Points

| Stage | What goes wrong | Downstream effect |
|-------|-----------------|-------------------|
| Prompting agent — cdoc selection | Wrong cdocs included or omitted | Task agent has missing or irrelevant context |
| Prompting agent — interview skipped | Agent decides management questions | Unreviewed assumptions baked into the task |
| Prompting agent — stale check skipped | Stale warning omitted from prompt | Task agent works from outdated cdoc descriptions |
| Task agent — plan skipped | Implementation without review | Design and architecture errors proceed unchecked |
| Task agent — architecture.md skipped | Files/imports added without checking layers | Layer violations introduced silently |
| Task agent — confirmation skipped | Checklist runs before user reviews | Correction window lost; errors locked in |
| Task agent — checklist skipped | Management files not updated | Drift in status.md, manifest.md, cdocs; stale context for future sessions |
| Arch check — files missed in mapping | Incomplete dependency graph | False PASS; violations go undetected |
| Arch check — baseline updated on FAIL | Violations ratified in baseline | Architecture rules become unenforceable |
| User — plan not reviewed | No human review gate | Design errors proceed without check |
| User — tests skipped before confirming | Confirmation without verification | Regressions treated as passing |
| User — commit not made | Work not in version control | Changes at risk |

## Correction Mechanisms

- **Stale cdoc detection** (`check_cdocs.py`) — Fired by prompting agent pre-prompt. Catches cdocs whose source files changed since the cdoc was last updated; inserts a staleness warning into the generated prompt. Signal persists until the cdoc content is updated.
- **Cdoc coverage** (`check_cdoc_coverage.py`) — Fired by task agent post-task. Catches repo files not declared as a source in any cdoc.
- **Manifest audit** (`check_manifest.py`) — Reports MISSING and DEAD manifest entries. Run ad-hoc by the user.
- **Task Counter** — Incremented after each completed task; resets to 0 on a clean arch check. Forces a structural review every 10 tasks.
- **Plan-first gate** — Task agent presents plan and waits; primary mechanism for catching design errors before code is written.
- **User confirmation gate** — Task agent pauses after implementation; gives the user a window to catch errors before management files are updated.
