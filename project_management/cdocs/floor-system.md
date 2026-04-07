---
sources:
  - floor/scripts/hash_util.py
  - floor/scripts/check_cdocs.py
  - floor/scripts/check_manifest.py
  - floor/CLAUDE.md
  - floor/setup.md
  - floor/project_management/cdoc.md
  - floor/project_management/manifest.md
  - floor/project_management/prompting.md
  - floor/project_management/status.md
  - floor/project_management/standards/architecture.md
  - floor/project_management/standards/style.md
  - floor/project_management/cdocs/project-overview.md
  - floor/project_management/prompts/architecture-check.md
---

# Floor — System Context

## What Floor Is

Floor is a project management template system for AI-assisted development. It provides a set of markdown files that give Claude structured, consistent context across sessions. The template is copied into a new project and customized via a setup checklist.

## Structure

The template lives in `floor/`. Everything at the repo root is the management system for developing Floor itself — Floor managing its own development.

The template ships these file groups:
- **CLAUDE.md** — Session entry point. Points Claude to the manifest and defines behavioral rules.
- **project_management/** — Manifest (file index), status (work tracking), cdoc/prompting templates (meta-templates for generating context docs and task prompts).
- **project_management/standards/** — Style guide and architecture conventions. These are the enforceable rules.
- **project_management/prompts/** — Reusable prompts (e.g. architecture health check). Consume standards, never define them.
- **scripts/** — Python tooling scripts. `hash_util.py` is a shared utility module (no shebang, declares `__all__`); `check_cdocs.py` detects stale cdocs by hashing source files declared in cdoc frontmatter; `check_manifest.py` audits `manifest.md` for file coverage (MISSING and DEAD entries).

## System Flow

1. **Copy template** — User copies `floor/` into a new project repo.
2. **Run setup** — User works through `setup.md`, filling in project-specific placeholders in CLAUDE.md, prompting.md, style.md, architecture.md, and architecture-check.md. When done, setup.md is deleted.
3. **User requests a task** — User describes a feature or change to Claude in the project session.
4. **Claude reads prompting.md** — CLAUDE.md's response rule triggers this unconditionally before any other action. Claude runs `scripts/check_cdocs.py` to detect stale cdocs, then checks the Task Counter in status.md: if ≥ 10, it generates an architecture health check prompt from architecture-check.md instead of a task prompt and stops.
5. **Claude interviews user if needed** — If management decisions must be made before the prompt can be composed, Claude asks rather than deciding.
6. **Claude selects context** — Using the cdoc routing table in prompting.md, Claude selects only the context documents relevant to the task domain.
7. **Prompt is output to user** — Claude produces a complete prompt text (not a file) containing: the manifest.md read instruction, selected cdocs, the task description, a plan-first requirement, applicable standards references, and the close-prompt workflow checklist. Claude also indicates the recommended Claude model.
8. **User pastes prompt into a new agent session** — The user manually opens a fresh Claude session and pastes the generated prompt.
9. **Agent reads context** — The agent reads manifest.md and all specified cdocs to build its working context.
10. **Agent presents plan** — Before touching any files, the agent lays out its implementation approach and waits for implicit or explicit approval.
11. **Agent implements** — Agent makes changes, following style.md conventions and checking architecture.md before creating files, adding imports, or shifting module responsibilities.
12. **Agent pauses for user confirmation** — Agent writes a brief summary of what was done, lists test steps for the user to run (making clear testing is the user's responsibility), and explicitly waits.
13. **User verifies and confirms** — User runs the suggested tests and tells the agent the task is complete.
14. **Agent updates management files** — Agent removes the item from Open in status.md (adds any newly discovered items, increments Task Counter), updates manifest.md rows for created or deleted files, and updates the relevant cdocs to reflect current system state.
15. **Agent reminds user to commit** — Final output is a reminder to make a git commit.

## Key Design Decisions

- **Python tooling** Floor ships Python scripts in `floor/scripts/` for tasks that require computation (e.g. hashing). Python was chosen for cross-platform compatibility and zero OS-specific deps.
- **Templates are the product.** Changes to files in `floor/` are what ship. The root-level management files describe and support them.
- **Minimum viable context.** Prompts should give agents only what they need. This is both a design principle and a documented style rule.
- **Setup-then-delete.** New projects run `setup.md` to customize placeholders, then delete it. Setup is considered complete — not partially deferred — when the checklist is done.
