---
sources:
  - floor/project_management/scripts/hash_util.py
  - floor/project_management/scripts/check_cdocs.py
  - floor/project_management/scripts/check_manifest.py
  - floor/project_management/scripts/check_cdoc_coverage.py
  - floor/project_management/scripts/task_counter.py
---

# Scripts — Checks and Utilities

All scripts live in `floor/project_management/scripts/`. Two categories: utility modules (no shebang, declare `__all__`) and runnable scripts (shebang + `main()`). Scripts may import from utility modules in the same directory; scripts must not import from other scripts.

## hash_util.py

Utility module. Provides SHA-256 hashing (`text_sha256`), YAML frontmatter parsing (`parse_frontmatter`), and source hash aggregation (`compute_source_hash`, `find_changed_sources`). Imported by `check_cdocs.py` and `check_cdoc_coverage.py`. Not invoked directly.

## check_cdocs.py

Run by `floor.py` before prompt assembly and by `shutdown.py` post-task. Reads the `sources:` list from each cdoc's YAML frontmatter, computes an aggregate SHA-256 hash, and compares against stored hashes in `project_management/cdoc_hashes.json`. Reports per cdoc: STALE, fresh, or new. A stale cdoc whose own content is unchanged retains its old source hash — the stale signal persists until the cdoc content is also updated. Also validates cdoc size limits: warns on > 6 sources or > 70 lines.

## check_manifest.py

Run by `shutdown.py` post-task. Audits `project_management/manifest.md` for file coverage. MISSING: file exists on disk but has no manifest entry. DEAD: manifest entry references a nonexistent file.

## check_cdoc_coverage.py

Run by `shutdown.py` post-task. Reports UNCOVERED: repo files not declared as a source in any cdoc's `sources:` list.

## task_counter.py

Manages the Task Counter: a plain integer in `project_management/task_counter.txt`. A missing file is treated as 0. Operations: `read`, `increment`, `reset`. Called by `floor.py` (arch gate check) and `shutdown.py` (increment). The architecture check agent calls `reset` after a PASS verdict.
