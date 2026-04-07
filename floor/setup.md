# Template Setup Checklist

Complete all items below before using this template. When a setup task is complete, delete all setup-related comments in that file.

---

### CLAUDE.md

- [ ] **Project summary block** — Replace `[PROJECT NAME] is a [brief description].` with one sentence describing your project.

### project_management/cdocs/project-overview.md

- [ ] **Project name** — Replace `[Project Name]` in the heading and the Name field.
- [ ] **Description** — Replace the two placeholder sentences with at least two real sentences. For example: what the project does, and who it's for or what problem it solves.

### project_management/prompting.md

- [ ] **cdoc routing table** — Replace `[Replace with your top-level domain — e.g. core system / data model]` with the actual domain name from your project overview cdoc. Add more rows as you create additional cdocs.

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

Before filling in the placeholders, identify your project type. This determines which universal rules apply and what your layer scheme should look like.

**Identify your project type:**

| Type | Examples | Rules to evaluate for disabling |
|---|---|---|
| Software application | web app, CLI tool, library | Review all — most rules apply |
| Scripts-only | automation scripts, build tools | "Public interfaces have at least one test" may not apply |
| Documentation system | wikis, knowledge bases, template systems | "No side effects at import time", "Separate I/O from logic", and "Public interfaces have at least one test" likely don't apply |
| Static site | generated sites, landing pages | Same as documentation system |
| Data pipeline | ETL, data transforms, analytics | "Public interfaces have at least one test" may not apply; evaluate others |

**Choose your layer scheme.** The placeholder layers (Entry/Orchestration/Primary/Secondary/Utility) are an example for software applications. Replace them with names that describe your project's actual structure. Suggested schemes:

- Software application: Entry → Orchestrator → Domain → Data → Utility
- Documentation system: Entry → Index → Content → Templates → Tools
- Scripts-only: Runner → Coordinator → Core → Utility
- Data pipeline: Trigger → Pipeline → Transform → Source → Utility

**Choose your graph types.** During the architecture health check, the agent will produce Mermaid diagrams of your project's structure. Decide which diagram types are appropriate now, and you'll fill them in to architecture-check.md below. Common options:

- *Module Dependency Graph* — what references what (applies to most projects)
- *Layered Architecture* — files grouped by layer (applies to most projects)
- *Resource Access Boundary* — which modules access external resources (code projects, data pipelines)
- *State Mutation Flow* — which modules write to shared state (code projects)
- *Document Reference Graph* — which docs link to or depend on other docs (documentation systems)
- *Data Flow Diagram* — how data moves through the system (data pipelines)

Choose at least two. You can always add more during a health check if the project warrants it.

**Now fill in the placeholders:**

- [ ] **Project name** — Replace `[PROJECT NAME]` in the heading.
- [ ] **Universal rules** — For any rule that does not apply to your project type, move it to the "Disabled Universal Rules" section at the bottom of the file with a written rationale.
- [ ] **Module Hierarchy table** — Replace placeholder layer names and module names with your actual structure. Use the scheme you chose above.
- [ ] **Module Responsibilities** — Replace each bullet with a real description of each module's single concern.
- [ ] **Forbidden Patterns (F1–F4)** — Replace each placeholder with your project's actual forbidden patterns. For code projects, include shell check commands. For non-code projects, describe the manual inspection step. Keep F5 (no circular dependencies) as-is.
- [ ] **State / Data Mutation Rules** — Replace placeholders with your actual shared state and the modules that own change rights.

### project_management/prompts/architecture-check.md

- [ ] **Project name** — Replace `[PROJECT NAME]` in the Task section.
- [ ] **`[your source dir]`** — Replace with your actual source directory. For documentation-only projects, this may be the full repo root.
- [ ] **`[shared resource]`** and relevant patterns (Step 2) — Describe what counts as "accessing a shared resource" in your project.
- [ ] **`[key state fields]`** (Step 2) — List the shared state or documents that count as mutations/changes.
- [ ] **Graph types** (Step 3) — Replace `[your graph types]` with the list you chose in the architecture.md setup above.
- [ ] **F1–F4 check commands** (Step 4) — Replace with the actual commands from your architecture.md Forbidden Patterns section. For non-code projects, replace with manual review descriptions.
- [ ] **`[your lint command]` and `[your build command]`** (Step 5) — Replace with your actual commands, or remove this step if your project has no build or lint step.

### project_management/manifest.md

- [ ] **Project Files section** — Replace the empty table with rows for your actual project files. Add section headers (## headings) to group files as the project grows.
---

## Done

Once all items above are complete, delete this file.
