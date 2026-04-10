# Project Manifest

---

## Project Context

| File | Description |
|------|-------------|
| [CLAUDE.md](../CLAUDE.md) | Project rules and guidelines for Claude and file management |
| [project_management/manifest.md](manifest.md) | This file — full project file listing with descriptions |
| [project_management/status.md](status.md) | Active work, open items, and closed items tracking |
| [project_management/cdoc.md](cdoc.md) | Template instructions for generating context documents |
| [project_management/prompting.md](prompting.md) | Prompt composition rules injected by floor.py into the prompting session |
| [project_management/standards/style.md](standards/style.md) | Coding conventions: universal rules, naming, formatting, error handling, and build gate |
| [project_management/standards/architecture.md](standards/architecture.md) | Architecture conventions: universal rules, module hierarchy, forbidden patterns, state mutation rules |
| [project_management/prompts/architecture-check.md](prompts/architecture-check.md) | Periodic health check prompt: map current architecture, run forbidden pattern checks, compare to baseline, produce verdict |
| [project_management/artifacts/architecture-baseline.md](artifacts/architecture-baseline.md) | Architecture module summary and diagram index; updated on each health check pass |
| [project_management/artifacts/01-module-dependency.mermaid](artifacts/01-module-dependency.mermaid) | Module dependency graph: file-to-file read/write/ref edges |
| [project_management/artifacts/02-layer-hierarchy.mermaid](artifacts/02-layer-hierarchy.mermaid) | Layer hierarchy diagram: permitted reference directions by layer |
| [project_management/artifacts/03-state-mutation.mermaid](artifacts/03-state-mutation.mermaid) | State mutation flow: which agents are authorized to mutate each shared state file |
| [project_management/artifacts/04-user-task-flow.mermaid](artifacts/04-user-task-flow.mermaid) | User task flow sequence: end-to-end developer workflow |
| [project_management/cdoc_hashes.json](cdoc_hashes.json) | Generated hash store for check_cdocs.py; tracks per-cdoc source file hashes |
| [project_management/task_counter.txt](task_counter.txt) | Generated counter file; stores the current Task Counter value as a plain integer |
| [.gitignore](../.gitignore) | Git ignore rules for the repository |

---

## Context Documents

| File | Description |
|------|-------------|
| [project_management/cdocs/floor-system.md](cdocs/floor-system.md) | Context document: what Floor is, its structure, key design decisions, and boundaries |
| [project_management/cdocs/agents-and-roles.md](cdocs/agents-and-roles.md) | Context document: the agent types, user responsibilities, workflow break points, and correction mechanisms |
| [project_management/cdocs/scripts-orchestration.md](cdocs/scripts-orchestration.md) | Context document: floor.py and shutdown.py — orchestration scripts that launch sessions and run post-task cleanup |
| [project_management/cdocs/scripts-and-checks.md](cdocs/scripts-and-checks.md) | Context document: check scripts (cdocs, manifest, coverage) and utility modules (hash_util, task_counter) |
| [project_management/cdocs/template-scaffolding.md](cdocs/template-scaffolding.md) | Context document: template scaffolding files (cdoc.md, project-overview.md, status.md) |
| [project_management/cdocs/01-task-lifecycle.mermaid](cdocs/01-task-lifecycle.mermaid) | Mermaid diagram: full task lifecycle from user request to git commit - stale snapshot|
| [project_management/cdocs/02-pre-prompt-decision-tree.mermaid](cdocs/02-pre-prompt-decision-tree.mermaid) | Mermaid diagram: pre-prompt decision tree for the prompting agent session - stale snapshot|
| [project_management/cdocs/03-post-task-cleanup.mermaid](cdocs/03-post-task-cleanup.mermaid) | Mermaid diagram: post-task cleanup checklist steps run by the task agent - stale snapshot|
| [project_management/cdocs/04-architecture-health-check.mermaid](cdocs/04-architecture-health-check.mermaid) | Mermaid diagram: architecture health check 8-step process - stale snapshot|
| [project_management/cdocs/05-error-mitigation-map.mermaid](cdocs/05-error-mitigation-map.mermaid) | Mermaid diagram: error and mitigation map for the Floor workflow - stale snapshot|

---

## Template Files

| File | Description |
|------|-------------|
| [floor/CLAUDE.md](../floor/CLAUDE.md) | Template CLAUDE.md distributed to new projects |
| [floor/setup.md](../floor/setup.md) | Setup checklist for new projects using this template |
| [floor/project_management/manifest.md](../floor/project_management/manifest.md) | Template manifest file |
| [floor/project_management/status.md](../floor/project_management/status.md) | Template status tracking file |
| [floor/project_management/cdoc.md](../floor/project_management/cdoc.md) | Template instructions for context documents |
| [floor/project_management/prompting.md](../floor/project_management/prompting.md) | Template prompt composition rules for floor.py |
| [floor/project_management/standards/style.md](../floor/project_management/standards/style.md) | Template style guide |
| [floor/project_management/standards/architecture.md](../floor/project_management/standards/architecture.md) | Template architecture conventions |
| [floor/project_management/prompts/architecture-check.md](../floor/project_management/prompts/architecture-check.md) | Template architecture health check prompt |
| [floor/project_management/cdocs/project-overview.md](../floor/project_management/cdocs/project-overview.md) | Template starter cdoc with placeholder project name and description |

---

## Scripts

| File | Description |
|------|-------------|
| [floor/scripts/floor.py](../floor/scripts/floor.py) | CLI entry point: gathers context, checks arch gate, assembles prompt, launches interactive Claude session |
| [floor/scripts/shutdown.py](../floor/scripts/shutdown.py) | Post-task cleanup: runs all checks, increments task counter, outputs structured results for Claude Code |
| [floor/scripts/hash_util.py](../floor/scripts/hash_util.py) | Shared utility module: SHA-256 hashing, frontmatter parsing, and source hash aggregation for Floor scripts |
| [floor/scripts/check_cdocs.py](../floor/scripts/check_cdocs.py) | Detects stale cdocs by hashing declared source files and comparing against a stored baseline |
| [floor/scripts/check_manifest.py](../floor/scripts/check_manifest.py) | Audits manifest.md for file coverage: reports files missing from the manifest and dead manifest entries |
| [floor/scripts/check_cdoc_coverage.py](../floor/scripts/check_cdoc_coverage.py) | Reports repo files not declared as a source in any cdoc; wired into shutdown.py |
| [floor/scripts/task_counter.py](../floor/scripts/task_counter.py) | Manages the Task Counter: read, increment, and reset operations; stores value in project_management/task_counter.txt |
