# Architecture Health Check Prompt

Read `project_management/manifest.md` and the CACT summary tree before proceeding.

## Task

Perform a full architectural health check on the Floor codebase. Present all findings before making any changes.

### Step 1 — Read Standards

Read `project_management/standards/architecture.md` (conventions and forbidden patterns) and `project_management/artifacts/architecture-baseline.md` (previous baseline overview and diagram index).

If no baseline exists yet, note that this run will produce the initial baseline and skip the comparison in Step 6.

### Step 2 — Map Current Architecture

Read every file in `project_management/scripts/` and every file in `floor/` (the product templates). For each file, record:
- All explicit references to other files (Python `import` statements, `subprocess` invocations of another script, and Markdown links between template files)
- Whether it accesses a shared resource (calls to the `claude` CLI, writes to `project_management/cact_tree.json`, writes to `project_management/task_counter.txt`, writes to `.floor_session.json`)
- Whether it changes shared state (any of: `cact_tree.json`, `task_counter.txt`, `.floor_session.json`, `project_management/prompts/implement-this.md`, or files under `floor/`)
- Its approximate line count

### Step 3 — Generate Current Diagram

Produce one Mermaid diagram per graph type in `project_management/artifacts/` (create the directory if it does not exist). If the current state reveals structure not captured by these types, add additional diagram files as needed — do not omit structure that the listed types cannot express.

Graph types for this project (one file each):
- Module Dependency Graph — `01-module-dependency.mermaid` (Python imports + subprocess invocations between scripts)
- Layered Architecture — `02-layer-hierarchy.mermaid` (Entry → Orchestration → Tools → Utility, plus the Content layer for `floor/`)
- State Mutation Flow — `03-state-mutation.mermaid` (which modules write to `cact_tree.json`, `task_counter.txt`, `.floor_session.json`, and `implement-this.md`)

Update the Module Summary table for `project_management/artifacts/architecture-baseline.md`.

### Step 4 — Run Forbidden Pattern Checks

Execute each check below. Report pass/fail for each.

- **F1** (subprocess calls confined to Entry and Orchestration): `rg -l "subprocess\.|os\.execvp" project_management/scripts/` — must return only `floor.py`, `shutdown.py`, `cact_build.py`, `cact_update.py`.
- **F2** (writes to `cact_tree.json` confined to Orchestration): `rg -n "cact_tree\.json" project_management/scripts/` — inspect results; write operations must appear only in `cact_build.py` and `cact_update.py`.
- **F3** (writes to `task_counter.txt` confined to owner): `rg -n "task_counter\.txt" project_management/scripts/` — write operations must appear only in `task_counter.py`; read-only path references elsewhere are acceptable.
- **F4** (Claude CLI calls confined to designated callers): `rg -n '"claude"' project_management/scripts/` — hits must appear only in `cact_build.py`, `cact_update.py`, and `floor.py`.
- **F5**: Review the dependency graph in `01-module-dependency.mermaid` for cycles.

### Step 5 — Run Build & Lint

Floor has no compiler or linter. Instead, smoke-test the scripts:
- `python3 project_management/scripts/cact_build.py --no-api` — must exit 0
- `python3 project_management/scripts/check_manifest.py` — must exit 0
- `python3 project_management/scripts/check_cact_coverage.py` — must exit 0
- `python3 project_management/scripts/task_counter.py read` — must exit 0

Report any non-zero exits.

### Step 6 — Compare to Baseline

If a baseline exists, diff the current diagram against it. Flag:
- New dependencies (imports or subprocess calls that didn't exist in the baseline)
- Removed dependencies
- New modules or removed modules
- Any dependency that violates the layer hierarchy (upward import or upward subprocess call)
- Any module whose responsibility has shifted (e.g., a read-only module now mutating state)

If no baseline exists, note that this is the initial run and skip this step.

### Step 7 — Verdict

Produce a verdict:

**PASS** — No violations found. Architecture matches conventions. Update the baseline date.

**PASS WITH NOTES** — No violations, but there are new dependencies or structural changes that are intentional and conform to conventions. List the changes. Update the baseline to reflect them.

**FAIL** — One or more violations found. List each violation with:
- Which rule was broken (reference the F-number or convention)
- Which file and line
- Suggested fix

Do not update the baseline when the verdict is FAIL.

### Step 8 — Update Baseline (if PASS or PASS WITH NOTES)

Overwrite `project_management/artifacts/architecture-baseline.md` with the updated Module Summary table and the "Generated" date set to today.

Overwrite each diagram file in `project_management/artifacts/` with the newly generated diagram. Each file must begin with a `%%` comment line stating its title and noting it is generated by the architecture health check.

If the verdict is PASS WITH NOTES, add a "Ratified Changes" section to `architecture-baseline.md` listing what changed and why.

Run `python3 project_management/scripts/task_counter.py reset`
