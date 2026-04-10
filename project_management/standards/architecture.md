# Architecture Conventions: Floor

## Universal Rules

- **Single responsibility per module** — Every file/module owns one concern. If you can't describe what it does in one sentence without "and", split it.
- **Dependency direction is inward/downward** — High-level modules do not reference low-level modules. The project-specific layer table below defines what "inward/downward" means for this project.
- **No circular dependencies** — No module may reference a module that (directly or transitively) references it.
- **Explicit references, no implicit coupling** — When a module needs something from another module, it references it explicitly. No shared mutable singletons, no coupling through side channels. No global mutable state, explicit imports only.
- **Public interfaces have at least one test** — Every public function, method, or API endpoint has at least one test exercising it. Internal helpers may be tested indirectly through their callers.
- **No side effects at import time** — Importing a module does not trigger behavior. Initialization happens explicitly.
- **Separate I/O from logic** — Pure computation should be separable from I/O (file, network, user input).

---

## Module Hierarchy

Files and components are organized in layers. A module may only reference its own layer or lower layers — never upward.

| Layer | Modules | Responsibility |
|-------|---------|----------------|
| 0 — Entry | `project_management/scripts/floor.py` | CLI entry point; gathers context, assembles prompt, launches Claude session |
| 1 — Orchestrator | `project_management/scripts/shutdown.py` | Post-task cleanup; invokes checks, increments counter, outputs results |
| 2 — Check | `project_management/scripts/check_manifest.py`, `project_management/scripts/check_cdocs.py`, `project_management/scripts/check_cdoc_coverage.py` | Diagnostic tools; each owns one check concern |
| 3 — Domain | `project_management/scripts/task_counter.py` | Core state management with no orchestration logic |
| 4 — Utility | `project_management/scripts/hash_util.py` | Shared helpers with no domain knowledge |

**Rule: no upward references.** A Layer 3 module must never reference Layer 2 or above. A Layer 2 module must never reference Layer 1 or above. This keeps the dependency graph acyclic.

Note: Layer 0–1 invoke Layer 2–3 scripts via subprocess, not import. This is intentional — it provides process isolation and allows users to run check scripts independently for debugging.

## Module Responsibilities

Each module owns a single concern. Do not spread a concern across modules or merge concerns into one module.

- **project_management/scripts/floor.py** — CLI entry point. Gathers context (cdoc staleness, status, prompting instructions), assembles a base prompt, checks the architecture gate, and launches an interactive Claude session. No domain logic.
- **project_management/scripts/shutdown.py** — Post-task orchestrator. Invokes all check scripts and the task counter via subprocess, collects results, and outputs structured markdown for Claude to act on.
- **project_management/scripts/check_manifest.py** — Audits manifest.md for coverage. Reports MISSING (file on disk, no entry) and DEAD (entry, no file). Read-only.
- **project_management/scripts/check_cdocs.py** — Detects stale context documents by comparing source file hashes against stored values. Writes updated hashes to `cdoc_hashes.json`.
- **project_management/scripts/check_cdoc_coverage.py** — Reports repo files not declared as a source in any cdoc. Read-only.
- **project_management/scripts/task_counter.py** — Manages the task counter in `task_counter.txt`. Supports read, increment, and reset operations.
- **project_management/scripts/hash_util.py** — Generic hashing utilities: SHA-256 file/text hashing, YAML frontmatter parsing, source hash aggregation. No domain knowledge, no project imports.

## Forbidden Patterns

These are patterns that must not appear in the project. Each includes a check to verify compliance.

**F1 — Only entry and orchestrator scripts may spawn subprocesses.**
Layer 2+ scripts must not invoke other scripts via subprocess. Orchestration belongs in floor.py and shutdown.py.

Check: `rg "import subprocess" project_management/scripts/ | grep -v -E "(floor|shutdown)\.py"` — should return nothing.

**F2 — No upward imports.**
A module must not import from a higher layer. Check scripts must not import from floor.py or shutdown.py. Domain and utility scripts must not import from any higher layer.

Check: `rg "^from (floor|shutdown|check_)" project_management/scripts/task_counter.py project_management/scripts/hash_util.py` — should return nothing.

**F3 — Utility layer has no project imports.**
hash_util.py must only import from the standard library. This keeps it reusable and free of domain coupling.

Check: `rg "^(from|import) " project_management/scripts/hash_util.py | grep -v -E "^(import hashlib|from pathlib)"` — should return nothing.

**F4 — No circular dependencies.**
Every reference must point downward or sideways within the same layer. No module may reference a module that (directly or transitively) references it.

Check: Review the dependency graph manually or via the architecture health check prompt.

## State / Data Mutation Rules

- **project_management/task_counter.txt**: written by `project_management/scripts/task_counter.py`. Incremented/reset by shutdown.py (via subprocess); read by floor.py (via subprocess) for the architecture gate.
- **project_management/cdoc_hashes.json**: written by `project_management/scripts/check_cdocs.py` on every run to track source file hashes.
- **.floor_session.json**: written by floor.py at session start; read and deleted by shutdown.py at session end.
- **project_management/*.md files**: modified only by Claude, not by scripts.

## Adding New Modules

When creating a new file or component:
1. Determine its layer in the hierarchy above. If it doesn't fit an existing layer, that's a signal to reconsider the design.
2. Ensure it references only its layer or below.
3. Give it a single clear responsibility that doesn't overlap with existing modules.
4. Update the module hierarchy table in this document.
5. Update `project_management/artifacts/architecture-baseline.md` with the new dependency.
