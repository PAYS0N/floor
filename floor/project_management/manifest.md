<!-- Template file. Customize: replace the placeholder rows below the Project Context section with your actual project files. Keep the Project Context section intact — those files exist in every project using this template. Add section headers (## headings) to group files as your project grows. -->

# Project Manifest

---

## Project Context

| File | Description |
|------|-------------|
| [CLAUDE.md](../CLAUDE.md) | Project rules and guidelines for Claude and file management |
| [project_management/manifest.md](manifest.md) | This file — full project file listing with descriptions |
| [project_management/status.md](status.md) | Active work, open items, and closed items tracking |
| [project_management/prompting.md](prompting.md) | Template instructions for generating task prompts |
| [project_management/standards/style.md](standards/style.md) | Coding conventions: universal rules, naming, formatting, error handling, and build gate |
| [project_management/standards/architecture.md](standards/architecture.md) | Architecture conventions: universal rules, module hierarchy, forbidden patterns, state mutation rules |
| [project_management/prompts/architecture-check.md](prompts/architecture-check.md) | Periodic health check prompt: map current architecture, run forbidden pattern checks, compare to baseline, produce verdict |

---

## Project Files

<!-- Add rows for every source file, config file, test file, etc. in your project. Group into sections (## headings) when the table gets long — e.g. "## Source", "## Tests", "## Config". -->

| File | Description |
|------|-------------|
| [project_management/scripts/cact_build.py](scripts/cact_build.py) | Builds or fully rebuilds the CACT tree from source files, computing hashes and generating directory summaries |
| [project_management/scripts/cact_walk.py](scripts/cact_walk.py) | Outputs accumulated context from root to specified target nodes in the CACT tree |
| [project_management/scripts/cact_update.py](scripts/cact_update.py) | Post-task: detects changed files, regenerates stale directory summaries, reports uncovered files |
| [project_management/scripts/check_cact_coverage.py](scripts/check_cact_coverage.py) | Reports repo files not represented as a leaf node in the CACT tree |
| [project_management/cact_tree.json](cact_tree.json) | Generated CACT tree file containing node hashes, directory summaries, and cross-references |
