# Architecture Conventions: Floor

## Universal Rules

- **Single responsibility per module** — Every file/module owns one concern. If you can't describe what it does in one sentence without "and", split it.
- **Dependency direction is inward/downward** — High-level modules do not reference low-level modules. The project-specific layer table below defines what "inward/downward" means for this project.
- **No circular dependencies** — No module may reference a module that (directly or transitively) references it.
- **Explicit references, no implicit coupling** — When a module needs something from another module, it references it explicitly. No shared mutable singletons, no coupling through side channels. For the Python scripts: no global mutable state, explicit imports only.
- **No side effects at import time** *(code)* — Importing a module does not trigger behavior. Initialization happens explicitly under `if __name__ == "__main__"` or via called functions.
- **Separate I/O from logic** *(code)* — Pure computation is separated from I/O. Scripts conventionally mark sections with `# ── Logic layer ──`, `# ── I/O layer ──`, `# ── Orchestration ──` banners.

---

## Disabled Universal Rules

- **Public interfaces have at least one test** — Floor has no automated test suite; correctness is verified by exercising the scripts against the repo's own `project_management/` tree. Revisit this rule once a test harness is added.

---

## Module Hierarchy

Files and components are organized in layers. A module may only reference its own layer or lower layers — never upward. "Reference" means both Python `import` statements and runtime `subprocess` invocations of another script.

| Layer | Modules | Responsibility |
|-------|---------|----------------|
| 0 — Entry | `floor.py`, `shutdown.py` | User-facing CLI entry points. Wire together tools via subprocess; no domain logic of their own. |
| 1 — Orchestration | `cact_build.py`, `cact_update.py` | CACT tree construction and refresh. Only layer allowed to invoke the Claude CLI for summary generation. |
| 2 — Tools | `cact_walk.py`, `check_manifest.py`, `check_cact_coverage.py`, `task_counter.py` | Pure read/audit/state operations over on-disk project artifacts. No external CLI calls. |
| 3 — Utility | `hash_util.py` | Shared pure helpers: hashing, frontmatter parsing, gitignore handling. No I/O beyond reading its argument paths. |
| C — Content (non-code) | `floor/**` | Pristine template files (the product being shipped). Not imported or executed by any script. |

**Rule: no upward references.** A Layer 3 module must never reference Layer 2 or above. A Layer 2 module must never reference Layer 1 or above. This keeps the dependency graph acyclic. The Content layer is orthogonal: scripts never read from `floor/`, and `floor/` files never execute.

## Module Responsibilities

- **floor.py** — CLI entry for starting a task. Gathers CACT staleness, CACT summary tree, status, and prompting instructions; assembles a base prompt; writes `.floor_session.json`; execs the Claude CLI for the interactive prompt-iteration session. No direct file mutations beyond the session file.
- **shutdown.py** — Post-task cleanup. Runs manifest/coverage/CACT audits and the task counter increment via subprocess, prints a structured report, deletes the session file. Does not itself mutate manifest, CACT, or counter state.
- **cact_build.py** — Full CACT tree rebuild from the hardcoded `TREE_DEFINITION`. Owns the structural definition of the tree; only place that invokes `claude` for initial summary generation; writes `cact_tree.json`.
- **cact_update.py** — Incremental CACT refresh. Detects changed leaves, regenerates affected ancestor summaries via the Claude CLI, rewrites `cact_tree.json`. Shares `TREE_DEFINITION` knowledge with `cact_build.py` by re-reading the existing tree.
- **cact_walk.py** — Read-only traversal that prints accumulated context from root to target nodes. No subprocess calls, no mutations.
- **check_manifest.py** — Read-only audit comparing `manifest.md` entries to files on disk. Reports MISSING and DEAD entries.
- **check_cact_coverage.py** — Read-only audit reporting repo files not present as a leaf in the CACT tree. Respects `.gitignore` and `DEFAULT_COVERAGE_EXCLUDES`.
- **task_counter.py** — Sole owner of `task_counter.txt`. Reads, increments, and resets the counter. No other module writes this file.
- **hash_util.py** — Pure helpers for SHA-256 hashing, YAML frontmatter parsing, gitignore parsing. No subprocess, no network, no module-level side effects.
- **floor/** — Pristine product templates (CLAUDE.md, project_management/ skeleton, setup.md). Mutated only by deliberate Floor-development tasks; never read or written by any script under `project_management/scripts/`.

## Forbidden Patterns

**F1 — Subprocess calls outside Entry and Orchestration layers.**
Only `floor.py`, `shutdown.py`, `cact_build.py`, and `cact_update.py` may call `subprocess.run` / `subprocess.Popen` / `os.execvp`. Tools (Layer 2) and Utility (Layer 3) must remain pure with respect to external processes.

Check: `rg -l "subprocess\.|os\.execvp" project_management/scripts/` — should return only the four allowed modules.

**F2 — Writes to `cact_tree.json` outside the Orchestration layer.**
Only `cact_build.py` and `cact_update.py` may write the CACT tree. All other scripts must treat it as read-only.

Check: `rg -n "cact_tree\.json" project_management/scripts/` — inspect results; write operations (`write_text`, `json.dump`) must appear only in `cact_build.py` and `cact_update.py`.

**F3 — Writes to `task_counter.txt` outside `task_counter.py`.**
The counter is a serialized state file with one owner. No other module mutates it.

Check: `rg -n "task_counter\.txt" project_management/scripts/` — write operations must appear only in `task_counter.py`; other mentions (e.g. paths in `TREE_DEFINITION`) are read-only references and acceptable.

**F4 — Claude CLI invocations outside the designated callers.**
Only `cact_build.py` and `cact_update.py` may call `claude -p …` for summary generation, and only `floor.py` may `execvp` the interactive `claude` session. No other script shells out to `claude`.

Check: `rg -n '"claude"' project_management/scripts/` — hits must appear only in `cact_build.py`, `cact_update.py`, and `floor.py`.

**F5 — No circular dependencies.**
Every reference must point downward or sideways within the same layer. No module may reference a module that (directly or transitively) references it.

Check: Review the dependency graph manually or via the architecture health check prompt.

## State / Data Mutation Rules

- **`project_management/cact_tree.json`**: written by `cact_build.py` (full rebuild) and `cact_update.py` (incremental). Read by `cact_walk.py` (which `floor.py` invokes via subprocess) and by `check_cact_coverage.py`.
- **`project_management/task_counter.txt`**: exclusively managed by `task_counter.py`. Incremented by `shutdown.py` via subprocess; read by `floor.py` via subprocess to gate the architecture check.
- **`.floor_session.json`**: created by `floor.py` at the start of a session; mutated during the session by the interactive Claude agent (which records the matched status item ID); deleted by `shutdown.py`.
- **`project_management/prompts/implement-this.md`**: written by the interactive Claude session launched from `floor.py`; read by implementation sessions. Not directly mutated by any script.
- **`floor/**`**: pristine template content. Mutated only by deliberate Floor-development tasks via normal editing. Never written by any script under `project_management/scripts/`.

## Adding New Modules

When creating a new file or component:
1. Determine its layer in the hierarchy above. If it doesn't fit an existing layer, that's a signal to reconsider the design.
2. Ensure it references only its layer or below.
3. Give it a single clear responsibility that doesn't overlap with existing modules.
4. Update the module hierarchy table in this document.
5. Update `project_management/artifacts/architecture-baseline.md` with the new dependency (the architecture health check will produce this file on the first run).
