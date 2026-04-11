# Project Manifest

---

## Project Context

| File | Description |
|------|-------------|
| [CLAUDE.md](../CLAUDE.md) | Project rules and guidelines for Claude and file management |
| [project_management/manifest.md](manifest.md) | This file — full project file listing with descriptions |
| [project_management/status.md](status.md) | Active work, open items, and closed items tracking |
| [project_management/cdoc.md](cdoc.md) | Template instructions for generating context documents |
| [project_management/prompting.md](prompting.md) | Template instructions for generating task prompts |
| [project_management/standards/style.md](standards/style.md) | Coding conventions: universal rules, naming, formatting, error handling, and build gate |
| [project_management/standards/architecture.md](standards/architecture.md) | Architecture conventions: universal rules, module hierarchy, forbidden patterns, state mutation rules |
| [project_management/prompts/architecture-check.md](prompts/architecture-check.md) | Periodic health check prompt: map current architecture, run forbidden pattern checks, compare to baseline, produce verdict |
| [project_management/prompts/implement-this.md](prompts/implement-this.md) | Task prompt: written by prompting assistant during floor.py session, describes the work to be implemented |

---

## Scripts

| File | Description |
|------|-------------|
| [project_management/scripts/floor.py](scripts/floor.py) | CLI entry point: gathers context (cdoc staleness, status, prompting instructions), assembles a base prompt, and launches an interactive Claude session |
| [project_management/scripts/shutdown.py](scripts/shutdown.py) | Post-task cleanup: runs all check scripts, increments task counter, marks status item complete, and outputs structured results for documentation updates |
| [project_management/scripts/check_manifest.py](scripts/check_manifest.py) | Audits manifest.md for coverage — reports MISSING (file on disk with no entry) and DEAD (entry with no file on disk) |
| [project_management/scripts/check_cdocs.py](scripts/check_cdocs.py) | Detects stale context documents by comparing source file hashes against stored values; updates the hash store on fresh/new cdocs |
| [project_management/scripts/check_cdoc_coverage.py](scripts/check_cdoc_coverage.py) | Reports repo files not declared as a source in any cdoc, flagging gaps in context document coverage |
| [project_management/scripts/task_counter.py](scripts/task_counter.py) | Manages the task counter in task_counter.txt; supports read, increment, and reset operations |
| [project_management/scripts/hash_util.py](scripts/hash_util.py) | Shared hashing utilities: SHA-256 file/text hashing, YAML frontmatter parsing, and source hash aggregation used by check scripts |

---

## Context Documents

| File | Description |
|------|-------------|
| [project_management/cdocs/floor-system.md](cdocs/floor-system.md) | Context document covering the Floor system overview, setup, and prompting workflow |
| [project_management/cdocs/agents-and-roles.md](cdocs/agents-and-roles.md) | Context document covering the CLI agents (floor.py, shutdown.py) and their roles in the workflow |
| [project_management/cdocs/scripts-orchestration.md](cdocs/scripts-orchestration.md) | Context document covering how floor.py and shutdown.py orchestrate the full task lifecycle |
| [project_management/cdocs/scripts-and-checks.md](cdocs/scripts-and-checks.md) | Context document covering the check scripts (hash_util, check_cdocs, check_manifest) and their interfaces |
| [project_management/cdocs/template-scaffolding.md](cdocs/template-scaffolding.md) | Context document covering the template scaffolding files (cdoc.md, project-overview, status.md) |

---

## Artifacts

| File | Description |
|------|-------------|
| [project_management/artifacts/architecture-baseline.md](artifacts/architecture-baseline.md) | Snapshot of the architecture at a given point in time; used by the architecture health check for comparison |
| [project_management/artifacts/01-module-dependency.mermaid](artifacts/01-module-dependency.mermaid) | Mermaid diagram: module dependency graph for the Floor scripts |
| [project_management/artifacts/02-layer-hierarchy.mermaid](artifacts/02-layer-hierarchy.mermaid) | Mermaid diagram: layer hierarchy showing I/O, logic, and orchestration layers |
| [project_management/artifacts/03-state-mutation.mermaid](artifacts/03-state-mutation.mermaid) | Mermaid diagram: state mutation flow across the task lifecycle |
| [project_management/artifacts/04-user-task-flow.mermaid](artifacts/04-user-task-flow.mermaid) | Mermaid diagram: end-to-end user task flow from floor.py invocation to shutdown |

---

## Data & Config

| File | Description |
|------|-------------|
| [project_management/task_counter.txt](task_counter.txt) | Tracks the number of completed tasks; triggers architecture check gate when threshold is reached |
| [project_management/cdoc_hashes.json](cdoc_hashes.json) | Persisted hash store mapping cdoc paths to their last-known source and content hashes |
| [.floor_session.json](../.floor_session.json) | Ephemeral session file written by floor.py; holds task description and matched status item ID for shutdown.py |
| [.gitignore](../.gitignore) | Git ignore rules for the repository |

---

## Floor Template

| File | Description |
|------|-------------|
| [floor/CLAUDE.md](../floor/CLAUDE.md) | Template version of CLAUDE.md with placeholder project name and description |
| [floor/setup.md](../floor/setup.md) | Setup instructions for bootstrapping a new project using the Floor template |
| [floor/project_management/manifest.md](../floor/project_management/manifest.md) | Template manifest with placeholder rows for project files |
| [floor/project_management/status.md](../floor/project_management/status.md) | Template status document for tracking active and closed work items |
| [floor/project_management/cdoc.md](../floor/project_management/cdoc.md) | Template cdoc instructions (copied into new projects) |
| [floor/project_management/prompting.md](../floor/project_management/prompting.md) | Template prompting instructions (copied into new projects) |
| [floor/project_management/cdocs/project-overview.md](../floor/project_management/cdocs/project-overview.md) | Template project-overview context document (starter cdoc for new projects) |
| [floor/project_management/prompts/architecture-check.md](../floor/project_management/prompts/architecture-check.md) | Template architecture check prompt (copied into new projects) |
| [floor/project_management/standards/architecture.md](../floor/project_management/standards/architecture.md) | Template architecture standards (copied into new projects) |
| [floor/project_management/standards/style.md](../floor/project_management/standards/style.md) | Template style standards (copied into new projects) |
| [floor/project_management/scripts/floor.py](../floor/project_management/scripts/floor.py) | Template copy of floor.py (distributed with the template) |
| [floor/project_management/scripts/shutdown.py](../floor/project_management/scripts/shutdown.py) | Template copy of shutdown.py (distributed with the template) |
| [floor/project_management/scripts/check_manifest.py](../floor/project_management/scripts/check_manifest.py) | Template copy of check_manifest.py (distributed with the template) |
| [floor/project_management/scripts/check_cdocs.py](../floor/project_management/scripts/check_cdocs.py) | Template copy of check_cdocs.py (distributed with the template) |
| [floor/project_management/scripts/check_cdoc_coverage.py](../floor/project_management/scripts/check_cdoc_coverage.py) | Template copy of check_cdoc_coverage.py (distributed with the template) |
| [floor/project_management/scripts/task_counter.py](../floor/project_management/scripts/task_counter.py) | Template copy of task_counter.py (distributed with the template) |
| [floor/project_management/scripts/hash_util.py](../floor/project_management/scripts/hash_util.py) | Template copy of hash_util.py (distributed with the template) |
