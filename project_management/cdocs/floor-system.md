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

## Key Design Decisions

- **No code yet.** Floor is currently pure markdown. Bash scripts are planned but not present.
- **Templates are the product.** Changes to files in `floor/` are what ship. The root-level management files describe and support them.
- **Minimum viable context.** Prompts should give agents only what they need. This is both a design principle and a documented style rule.
- **Forbidden patterns grow organically.** Only F5 (no circular references) is defined. F1–F4 will be added as anti-patterns emerge from real usage.
- **Setup-then-delete.** New projects run `setup.md` to customize placeholders, then delete it. The template files retain "Setup When Needed" comments for items that can wait.

## What Floor Does Not Do

Floor does not generate code, run builds, or enforce rules at runtime. It is a static context system — its value is in what it tells Claude, not what it executes.
