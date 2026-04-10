# Architecture Conventions: Floor

## Universal Rules

These apply to all projects by default. To disable one, move it to the "Disabled Universal Rules" section at the bottom of this file with a written rationale.

- **Single responsibility per module** — Every file/module owns one concern. If you can't describe what it does in one sentence without "and", split it.
- **Dependency direction is inward/downward** — High-level modules do not import from low-level modules. The project-specific layer table below defines what "inward/downward" means for this codebase.
- **No circular dependencies** — No module may import from a module that (directly or transitively) imports it.
- **Explicit imports, no implicit coupling** — When a module needs something from another module, it imports it explicitly. No global mutable state, no shared mutable singletons, no coupling through side channels.
- **Public interfaces have at least one test** — Every public function, method, or API endpoint has at least one test exercising it. Internal helpers may be tested indirectly through their callers.
- **No side effects at import time** — Importing a module does not trigger behavior. Initialization happens explicitly.
- **Separate I/O from logic** — Pure computation should be separable from I/O (file, network, user input). If the agent needs to violate this (e.g. embedded ISR handlers, performance-critical paths), it must note the exception and get confirmation.

---

## Module Hierarchy

Floor is a documentation/template project, not a runtime application. "Modules" here are groups of files organized by concern. References between files (e.g. "read X before proceeding") flow downward — never upward.

| Layer | Modules | Responsibility |
|-------|---------|----------------|
| 0 — Entry | `CLAUDE.md` | Entry point for Claude sessions; points to manifest, defines rules |
| 1 — Orchestration | `project_management/manifest.md`, `project_management/status.md` | File index and work tracking; no conventions or templates |
| 1 — Artifacts | `project_management/artifacts/` | Structured reference data produced by the architecture health check: module summary and Mermaid diagrams. Not narrative; not cdocs. |
| 2 — Standards | `project_management/standards/style.md`, `project_management/standards/architecture.md` | Define project conventions; referenced by prompts and CLAUDE.md |
| 3 — Prompts & Templates | `project_management/prompts/`, `project_management/cdoc.md`, `project_management/prompting.md` | Task prompts and template generators; consume standards, never define them |
| 4 — Scripts | `floor/scripts/` | Standalone tooling scripts; no imports from layers above; no domain logic |

**Rule: no upward references.** A prompt may reference a standard, but a standard must never depend on a specific prompt. CLAUDE.md may reference any file, but no file should require reading CLAUDE.md to function.

## Module Responsibilities

- **CLAUDE.md** — Session entry point. Directs Claude to the manifest and defines behavioral rules. No conventions or domain logic.
- **manifest.md** — Complete file index with descriptions. Updated whenever files are added or removed.
- **status.md** — Tracks active work, open items, and completed items. No conventions.
- **standards/** — Defines coding and architecture conventions. Self-contained; does not reference prompts or status.
- **prompts/** — Task-specific prompts for Claude. May direct the agent to read standards or other files.
- **cdoc.md, prompting.md** — Meta-templates that define how to create context documents and prompts respectively.
- **artifacts/** — Structured reference data written by the architecture check agent. Contains `architecture-baseline.md` (module summary + diagram index) and four `.mermaid` files (one per diagram type). These are generated outputs — not narrative, not cdocs. Do not edit manually; the arch agent overwrites them on PASS.
- **floor/scripts/** — Python tooling shipped with the template. Two kinds of files live here: runnable scripts (shebang + `main()`) and utility modules (no shebang, declare `__all__`). Scripts may import from utility modules in the same directory; scripts must not import from other scripts. `floor.py`: CLI entry point that assembles prompts and launches Claude sessions. `shutdown.py`: post-task cleanup that runs all checks and outputs structured results. `hash_util.py`: shared hashing and frontmatter utilities. `check_cdocs.py`: detects stale cdocs by comparing source file hashes. `check_manifest.py`: audits manifest.md for file coverage (MISSING/DEAD entries). `check_cdoc_coverage.py`: reports repo files not declared in any cdoc. `task_counter.py`: manages the architecture check counter.

## Forbidden Patterns

No project-specific forbidden patterns defined yet. Patterns should be added here as the project grows and anti-patterns are identified. F5 (no circular dependencies) applies universally.

## State / Data Mutation Rules

- **status.md**: Updated only when work items change state (new, in-progress, completed, or removed).
- **manifest.md**: Updated only when files are added, removed, or renamed.
- **Template files (floor/)**: The canonical source. Changes here are the "product" — all other project management files describe or support the templates.

## Adding New Modules

When creating a new file:
1. Determine its layer in the hierarchy above. If it doesn't fit an existing layer, that's a signal to reconsider the design.
2. Ensure it only references files from its layer or below.
3. Give it a single clear responsibility that doesn't overlap with existing files.
4. Update the module hierarchy table in this document.
5. Add a row to `project_management/manifest.md`.
