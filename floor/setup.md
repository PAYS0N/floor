# Template Setup Checklist

Complete the **Setup Now** items before using this template. **Setup When Needed** items can wait until your project reaches the complexity that demands them.

When a setup task is complete, delete all setup related comments in that file.

---

## Setup Now

### CLAUDE.md

- [ ] **Project summary block** — Replace `[PROJECT NAME] is a [brief description].` with one sentence describing your project.

### project_management/manifest.md

- [ ] **Project Files section** — Replace the empty table with rows for your actual project files. Add section headers (## headings) to group files as the project grows.

### project_management/standards/style.md

- [ ] **Project name** — Replace `[PROJECT NAME]` in the heading.
- [ ] **Language & Tooling** — Fill in your language, build command, lint/format command, source directory, and output directory.
- [ ] **Naming Conventions** — Replace each placeholder with your actual casing rules.
- [ ] **Formatting** — Replace placeholder rules with your indentation style, brace conventions, etc.
- [ ] **Type Safety** — Fill in how your project uses types, annotations, and guards.
- [ ] **Error Handling** — Document your error propagation strategy and validation boundaries.
- [ ] **Serialization** — Describe your save/load format, or remove this section if not applicable.
- [ ] **Build & Lint Gate** — Replace `[lint command]` and `[build command]` with your actual commands.
- [ ] **Universal rules** — Review the Universal Rules section. For any rule that does not apply to this project, move it to the "Disabled Universal Rules" section at the bottom of the file with a written rationale.

### project_management/standards/architecture.md

- [ ] **Project name** — Replace `[PROJECT NAME]` in the heading.
- [ ] **Module Hierarchy table** — Replace placeholder layer names and module names with your actual modules. Add or remove layers as needed.
- [ ] **Module Responsibilities** — Replace each bullet with a real description of each module's single concern.
- [ ] **Forbidden Patterns (F1–F4)** — Replace each placeholder with your project's actual forbidden patterns and check commands. Keep F5 (no circular dependencies) as-is.
- [ ] **State / Data Mutation Rules** — Replace placeholders with your actual shared state and the modules that own mutation rights.
- [ ] **Universal rules** — Review the Universal Rules section. For any rule that does not apply to this project, move it to the "Disabled Universal Rules" section at the bottom of the file with a written rationale.

### scripts/forbidden-patterns.sh

- [ ] **F1–F4 check commands** — Replace each `[your check command]` and `[Pattern name]` with the actual values from your `project_management/standards/architecture.md` Forbidden Patterns section. If you have a tool for circular dependency detection, replace the F5 line with a `run_check` call.

---

## Setup When Needed

These items become relevant as the project grows. Don't create them speculatively.

### Context documents (cdocs)

Create your first cdoc when a module or domain becomes complex enough that a new Claude session would need background to work on it effectively. Follow `project_management/cdoc.md` — it handles adding the routing table row in `prompting.md` automatically.

### project_management/prompting.md

- [ ] **cdoc routing table** — Populated automatically as you create cdocs. No upfront setup needed. If you want to pre-plan your domains, replace the placeholder rows with your expected areas, but this is optional.

### project_management/prompts/architecture-check.md

Customize when you're ready to run your first architecture health check (typically after 10+ tasks or when the codebase has enough modules to warrant it).

- [ ] **Project name** — Replace `[PROJECT NAME]` in the Task section.
- [ ] **`[your source dir]`** — Replace with your actual source directory.
- [ ] **`[shared resource]`** and relevant API patterns (Step 2) — Describe what counts as "accessing a shared resource" in your codebase.
- [ ] **`[key state fields]`** (Step 2) — List the shared state fields that count as mutations.
- [ ] **F1–F4 check commands** (Step 4) — Replace with the actual commands from your architecture.md Forbidden Patterns section.
- [ ] **`[your lint command]` and `[your build command]`** (Step 5) — Replace with your actual commands.

---

## Done

Once all **Setup Now** items are complete, delete this file. (The **Setup When Needed** items are self-documenting in their respective files.)
