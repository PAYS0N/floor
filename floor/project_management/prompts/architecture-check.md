<!-- Template file. Customize: replace [your source dir], [your modules], and [your check command] with your project's actual paths and commands. Steps 1-8 and the verdict format are universal and should be kept as-is. -->

# Architecture Health Check Prompt

Read `project_management/manifest.md` before proceeding.

## Task

Perform a full architectural health check on the [PROJECT NAME] codebase. Present all findings before making any changes.

### Step 1 — Read Standards

Read `project_management/standards/architecture.md` (conventions and forbidden patterns) and `project_management/architecture-baseline.md` (previous baseline diagram).

If no baseline exists yet, note that this run will produce the initial baseline and skip the comparison in Step 6.

### Step 2 — Map Current Architecture

Read every file in `[your source dir]`. For each file, record:
- All explicit references to other files (imports, inclusions, links, or declared dependencies)
- Whether it accesses `[shared resource]` (calls to [relevant APIs or patterns])
- Whether it changes shared state (writes to [key state fields])
- Its approximate line count

### Step 3 — Generate Current Diagram

Produce Mermaid diagrams in the same format as the baseline in `architecture-baseline.md` (if it exists). Use the graph types listed below as the baseline. If the current state reveals structure not captured by these types, add additional diagrams as needed — do not omit structure that the listed types cannot express.

Graph types for this project:
- [your graph type 1]
- [your graph type 2]

Update the Module Summary table.

### Step 4 — Run Forbidden Pattern Checks

Execute each check below. Report pass/fail for each. For manual review steps, describe what was checked and what was found.

- **F1**: `[your check command]` — should return nothing
- **F2**: `[your check command]` — should return nothing
- **F3**: `[your check command]` — should return nothing
- **F4**: `[your check command]` — should return results only in `[allowed module]`
- **F5**: Review dependency graph for cycles

### Step 5 — Run Build & Lint

If this project has a build or lint step, run `[your lint command]` and `[your build command]`. Report any errors or warnings. If not applicable, skip this step.

### Step 6 — Compare to Baseline

If a baseline exists, diff the current diagram against it. Flag:
- New dependencies (imports that didn't exist in the baseline)
- Removed dependencies
- New modules or removed modules
- Any dependency that violates the layer hierarchy (upward import)
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

Overwrite `project_management/architecture-baseline.md` with the newly generated diagram and updated Module Summary table. Set the "Generated" date to today.

If the verdict is PASS WITH NOTES, add a "Ratified Changes" section to the baseline listing what changed and why.

Reset the Task Counter in `project_management/status.md` to 0.
