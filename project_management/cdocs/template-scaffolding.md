---
sources:
  - floor/project_management/cdoc.md
  - floor/project_management/cdocs/project-overview.md
  - floor/project_management/status.md
---

# Template Scaffolding

These are the template files that provide project management scaffolding when Floor is copied into a new project. They are not standards, scripts, or prompts — they are the structural starting points that users customize during setup.

## cdoc.md

Meta-template that defines how to create context documents. Specifies constraints: max 6 sources per cdoc, max 70 lines, one domain per file, dense factual prose. Read by agents before creating or editing any cdoc.

## project-overview.md

Starter cdoc shipped with the template. Contains placeholder project name and description. The user replaces these during setup. Serves as the first entry in the cdoc routing table.

## status.md

Work tracking file. In its template form, provides a structure for tracking active work, open items, and completed items. Projects using the external `project_tasks_cli.py` replace the contents with CLI instructions — `floor.py` detects this and runs the list command automatically.
