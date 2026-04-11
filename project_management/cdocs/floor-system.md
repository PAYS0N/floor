---
sources:
  - floor/CLAUDE.md
  - floor/setup.md
  - floor/project_management/prompting.md
  - floor/project_management/manifest.md
  - floor/project_management/standards/architecture.md
  - floor/project_management/standards/style.md
---

# Floor — System Context

## What Floor Is

Floor is a project management template system for AI-assisted development. It provides markdown files and Python scripts that give Claude structured, consistent context across sessions. The template is copied into a new project and customized via a setup checklist.

## Structure

The template lives in `floor/`. Everything at the repo root manages Floor's own development.

The template ships these file groups:
- **CLAUDE.md** — Session entry point. Defines the "implement" response rule.
- **project_management/** — Manifest, status, cdoc/prompting templates, standards, prompts, artifacts, and scripts.
- **project_management/scripts/** — Python tooling. `floor.py` (CLI entry), `shutdown.py` (post-task), check scripts, utilities.

## Core Flow

Scripts orchestrate agents, not the other way around.

1. **`floor.py "<task>"`** — Checks arch gate, gathers context, launches interactive Claude CLI session for prompt iteration.
2. **Prompting session** — User iterates with Claude. Final prompt written to `prompts/implement-this.md`.
3. **User says "implement"** — CLAUDE.md response rule fires. Plan-first implementation.
4. **User confirms** — Claude runs `shutdown.py`. Structured results guide doc updates.

## Key Design Decisions

- **Scripts orchestrate agents.** `floor.py` and `shutdown.py` set boundaries; agents execute within them.
- **Templates are the product.** Files in `floor/` are what ship.
- **Minimum viable context.** Prompts give agents only what they need.
- **Setup-then-delete.** `setup.md` customizes placeholders, then is deleted.
