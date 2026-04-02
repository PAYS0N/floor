# Template Setup Checklist

Complete every item below before using this template. Items are ordered by file.

---

## CLAUDE.md

- [ ] **Project summary block** — Replace `[PROJECT NAME] is a [brief description].` with one sentence describing your project.

---

## project_management/manifest.md

- [ ] **Project title** — Replace the `# Project Manifest` title if you want the project name in the heading.
- [ ] **Entry Point section** — Replace `[src/entryPoint]` with your actual entry point file and a real description.
- [ ] **Source Modules section** — Replace the placeholder rows with your actual source files. Add one row per file; remove any rows that don't apply. Group files into sections that make sense for your project structure.
- [ ] **Project Context section** — Keep as-is. All listed files exist in every project using this template.

---

## project_management/prompting.md

- [ ] **cdoc routing table** — Replace the three placeholder rows (`[Domain A]`, `[Domain B]`, `[Domain C]`) with rows matching your project's actual domains and context documents. Add as many rows as you have distinct areas of the codebase. Each row should name a coherent topic and point to the cdoc(s) that cover it. (cdocs themselves are created later, as needed — don't create them speculatively at setup time.)

---

## project_management/standards/style.md

- [ ] **Language & Tooling** — Fill in your language, build command, lint/format command, source directory, and output directory.
- [ ] **Naming Conventions** — Replace each `[IdentifierType]: [convention]` placeholder with your actual casing rules.
- [ ] **Formatting** — Replace placeholder rules with your indentation style, brace conventions, etc.
- [ ] **Type Safety** — Fill in how your project uses types, annotations, and guards.
- [ ] **Error Handling** — Document your error propagation strategy and validation boundaries.
- [ ] **Serialization** — Describe your save/load or encode/decode format and conventions, or remove this section if not applicable.
- [ ] **Build & Lint Gate** — Replace `[lint command]` and `[build command]` with your actual commands.

---

## project_management/standards/architecture.md

- [ ] **Module Hierarchy table** — Replace placeholder layer names and module names (`[entryPoint]`, `[orchestrator]`, etc.) with your actual modules. Add or remove layers as needed.
- [ ] **Module Responsibilities** — Replace each bullet with a real description of each module's single concern.
- [ ] **Forbidden Patterns (F1–F4)** — Replace each `[Pattern name]`, description, and `[your check command]` with your project's actual forbidden patterns and the commands used to verify them. Keep F5 (no circular dependencies) as-is.
- [ ] **State / Data Mutation Rules** — Replace `[State A/B/C]` and module placeholders with your actual shared state and the modules that own mutation rights.

---

## project_management/prompts/architecture-check.md

- [ ] **Project name** — Replace `[PROJECT NAME]` in the Task section.
- [ ] **`[your source dir]`** — Replace with your actual source directory (e.g. `src/`).
- [ ] **`[shared resource]`** and relevant API patterns (Step 2) — Describe what counts as "accessing a shared resource" in your codebase (e.g. DOM access, database calls, file I/O).
- [ ] **`[key state fields]`** (Step 2) — List the shared state fields that count as mutations.
- [ ] **F1–F4 check commands** (Step 4) — Replace each `[your check command]` with the actual commands from your architecture.md Forbidden Patterns section.
- [ ] **`[your lint command]` and `[your build command]`** (Step 5) — Replace with your actual commands.

---

## Done

Once all items above are complete, delete this file.
