# Project Manifest

---

## Project Context

| File | Description |
|------|-------------|
| [CLAUDE.md](../CLAUDE.md) | Project rules and guidelines for Claude and file management |
| [.gitignore](../.gitignore) | Git ignore patterns — excludes `__pycache__/` and `.floor_session.json` |
| [project_management/manifest.md](manifest.md) | This file — full project file listing with descriptions |
| [project_management/status.md](status.md) | Active work, open items, and closed items tracking |
| [project_management/prompting.md](prompting.md) | Template instructions for generating task prompts |
| [project_management/standards/style.md](standards/style.md) | Coding conventions: universal rules, naming, formatting, error handling, and build gate |
| [project_management/standards/architecture.md](standards/architecture.md) | Architecture conventions: universal rules, module hierarchy, forbidden patterns, state mutation rules |
| [project_management/prompts/architecture-check.md](prompts/architecture-check.md) | Periodic health check prompt: map current architecture, run forbidden pattern checks, compare to baseline, produce verdict |

---

## Management Scripts

These run the Floor workflow on this repo itself. They live under `project_management/scripts/` and must stay in sync with the matching templates under `floor/project_management/scripts/`.

| File | Description |
|------|-------------|
| [project_management/scripts/floor.py](scripts/floor.py) | Entry CLI: gathers CACT context + status, assembles base prompt, execs Claude CLI for the interactive prompting session |
| [project_management/scripts/shutdown.py](scripts/shutdown.py) | Entry CLI: runs manifest / CACT coverage / CACT update / task counter checks post-task and prints a structured report |
| [project_management/scripts/cact_build.py](scripts/cact_build.py) | Builds or fully rebuilds the CACT tree from source files, computing hashes and generating directory summaries via Claude CLI |
| [project_management/scripts/cact_walk.py](scripts/cact_walk.py) | Outputs accumulated context from root to specified target nodes in the CACT tree |
| [project_management/scripts/cact_update.py](scripts/cact_update.py) | Post-task: detects changed files, regenerates stale directory summaries, reports uncovered files |
| [project_management/scripts/check_cact_coverage.py](scripts/check_cact_coverage.py) | Reports repo files not represented as a leaf node in the CACT tree |
| [project_management/scripts/check_manifest.py](scripts/check_manifest.py) | Audits `manifest.md` for MISSING (on-disk, not listed) and DEAD (listed, not on-disk) entries |
| [project_management/scripts/task_counter.py](scripts/task_counter.py) | Sole owner of `task_counter.txt`; read/increment/reset operations that gate the architecture health check |
| [project_management/scripts/hash_util.py](scripts/hash_util.py) | Pure utility helpers: SHA-256 hashing, YAML frontmatter parsing, gitignore pattern reading |
| [project_management/cact_tree.json](cact_tree.json) | Generated CACT tree containing node hashes, directory summaries, and cross-references. Written by `cact_build.py` / `cact_update.py` |

---

## Floor Product Templates (the deliverable)

These files under `floor/` are the pristine template distribution shipped to end users. They are content, not executed code, and must not be imported or mutated by any script in `project_management/scripts/`. Any change under `floor/` should be mirrored (when appropriate) to the live working copy under `project_management/`.

| File | Description |
|------|-------------|
| [floor/CLAUDE.md](../floor/CLAUDE.md) | Template top-level Claude instructions for end-user projects |
| [floor/setup.md](../floor/setup.md) | Template setup checklist that end users complete on first use |
| [floor/project_management/manifest.md](../floor/project_management/manifest.md) | Template manifest with the placeholder Project Files table |
| [floor/project_management/prompting.md](../floor/project_management/prompting.md) | Template prompt-composition instructions (no customization expected) |
| [floor/project_management/status.md](../floor/project_management/status.md) | Template status file placeholder |
| [floor/project_management/prompts/architecture-check.md](../floor/project_management/prompts/architecture-check.md) | Template architecture health check prompt with placeholders |
| [floor/project_management/standards/architecture.md](../floor/project_management/standards/architecture.md) | Template architecture standards with placeholder layer/module/check sections |
| [floor/project_management/standards/style.md](../floor/project_management/standards/style.md) | Template style standards with placeholder language/tooling/naming sections |
| [floor/project_management/scripts/floor.py](../floor/project_management/scripts/floor.py) | Template copy of the floor entry script |
| [floor/project_management/scripts/shutdown.py](../floor/project_management/scripts/shutdown.py) | Template copy of the shutdown script |
| [floor/project_management/scripts/cact_build.py](../floor/project_management/scripts/cact_build.py) | Template copy of the CACT build script |
| [floor/project_management/scripts/cact_update.py](../floor/project_management/scripts/cact_update.py) | Template copy of the CACT update script |
| [floor/project_management/scripts/cact_walk.py](../floor/project_management/scripts/cact_walk.py) | Template copy of the CACT walk script |
| [floor/project_management/scripts/check_cact_coverage.py](../floor/project_management/scripts/check_cact_coverage.py) | Template copy of the CACT coverage check script |
| [floor/project_management/scripts/check_manifest.py](../floor/project_management/scripts/check_manifest.py) | Template copy of the manifest audit script |
| [floor/project_management/scripts/task_counter.py](../floor/project_management/scripts/task_counter.py) | Template copy of the task counter script |
| [floor/project_management/scripts/hash_util.py](../floor/project_management/scripts/hash_util.py) | Template copy of the hash utility module |
