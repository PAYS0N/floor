# Architecture Health Check Prompt

Read `project_management/manifest.md` before proceeding.

## Task

Perform a full architectural health check on the Floor project. Present all findings before making any changes.

### Step 1 — Read Standards

Read `project_management/standards/architecture.md` (conventions and forbidden patterns) and `project_management/architecture-baseline.md` (previous baseline diagram).

If no baseline exists yet, note that this run will produce the initial baseline and skip the comparison in Step 6.

### Step 2 — Map Current Architecture

Read every file in `floor/`. For each file, record:
- All references to other files (e.g. "read X", links, directives)
- Whether it modifies shared state (`status.md`, `manifest.md`, template files in `floor/`)
- Its approximate line count

### Step 3 — Generate Current Diagram

From the reference map, produce a Mermaid dependency graph in the same format as the baseline in `architecture-baseline.md`, if it exists. Include all four diagram sections: Module Dependency Graph, Layered Architecture, Reference Boundary, State Mutation Flow. Update the Module Summary table.

### Step 4 — Run Forbidden Pattern Checks

No forbidden patterns yet. Skip this step.

### Step 5 — Run Build & Lint

No automated build or lint commands yet. Skip this step until tooling is added.

### Step 6 — Compare to Baseline

If a baseline exists, diff the current diagram against it. Flag:
- New references (file-to-file links that didn't exist in the baseline)
- Removed references
- New files or removed files
- Any reference that violates the layer hierarchy (upward reference)
- Any file whose responsibility has shifted

If no baseline exists, note that this is the initial run and skip this step.

### Step 7 — Verdict

Produce a verdict:

**PASS** — No violations found. Architecture matches conventions. Update the baseline date.

**PASS WITH NOTES** — No violations, but there are new references or structural changes that are intentional and conform to conventions. List the changes. Update the baseline to reflect them.

**FAIL** — One or more violations found. List each violation with:
- Which rule was broken (reference the F-number or convention)
- Which file
- Suggested fix

Do not update the baseline when the verdict is FAIL.

### Step 8 — Update Baseline (if PASS or PASS WITH NOTES)

Overwrite `project_management/architecture-baseline.md` with the newly generated diagram and updated Module Summary table. Set the "Generated" date to today.

If the verdict is PASS WITH NOTES, add a "Ratified Changes" section to the baseline listing what changed and why.

Reset the Task Counter in `project_management/status.md` to 0.
