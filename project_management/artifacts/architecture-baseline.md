# Architecture Baseline — Floor

Generated: 2026-04-10

---

## Script Modules

| File | Layer | Lines | Imports From | Subprocess Calls | State Writes |
|------|-------|-------|-------------|-----------------|-------------|
| `project_management/scripts/floor.py` | 0 — Entry | 212 | (none) | check_cdocs.py, task_counter.py | .floor_session.json |
| `project_management/scripts/shutdown.py` | 1 — Orchestrator | 138 | (none) | check_manifest.py, check_cdocs.py, check_cdoc_coverage.py, task_counter.py | (deletes .floor_session.json) |
| `project_management/scripts/check_manifest.py` | 2 — Check | 143 | (none) | (none) | (none) |
| `project_management/scripts/check_cdocs.py` | 2 — Check | 204 | hash_util | (none) | cdoc_hashes.json |
| `project_management/scripts/check_cdoc_coverage.py` | 2 — Check | 160 | hash_util | (none) | (none) |
| `project_management/scripts/task_counter.py` | 3 — Domain | 118 | (none) | (none) | task_counter.txt |
| `project_management/scripts/hash_util.py` | 4 — Utility | 102 | (none) | (none) | (none) |

## Project Management Files

These files are read/written by scripts and Claude as part of the workflow. They are not code modules but are integral to the system.

| File | Read By | Written By | Role |
|------|---------|-----------|------|
| `project_management/prompting.md` | floor.py, Claude (prompting) | Claude (impl, when adding cdoc routing rows) | Prompt composition instructions and cdoc routing table |
| `project_management/status.md` | floor.py | Claude (impl, marking tasks complete) | Project task tracking (delegates to external CLI) |
| `project_management/manifest.md` | check_manifest.py, Claude (impl) | Claude (impl, adding/removing rows) | File index for the project |
| `project_management/cdoc.md` | Claude (impl) | (read-only) | Instructions for creating/updating context documents |
| `project_management/cdocs/*.md` | check_cdocs.py, check_cdoc_coverage.py, Claude (impl) | Claude (impl, updating stale docs) | Context documents describing system domains |
| `project_management/standards/*.md` | Claude (impl) | (read-only during tasks) | Style and architecture conventions |
| `project_management/prompts/implement-this.md` | Claude Code (impl, via CLAUDE.md) | Claude (prompting session) | The task prompt produced by floor.py's Claude session |
| `project_management/task_counter.txt` | task_counter.py | task_counter.py | Task count; triggers arch check at threshold |
| `project_management/cdoc_hashes.json` | check_cdocs.py | check_cdocs.py | Source file hash store for staleness detection |
| `.floor_session.json` | shutdown.py, Claude (prompting) | floor.py (create), Claude (update), shutdown.py (delete) | Ephemeral session state linking prompt and implementation phases |

---

## Diagrams

See `project_management/artifacts/`:

- `01-module-dependency.mermaid` — Module dependency graph (imports, subprocess calls, and file access)
- `02-layer-hierarchy.mermaid` — Layered architecture with project management files
- `03-state-mutation.mermaid` — State mutation flow (scripts and Claude agents)
- `04-user-task-flow.mermaid` — Full user workflow: prompt composition → implementation → shutdown
