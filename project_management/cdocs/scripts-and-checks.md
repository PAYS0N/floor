---
sources:
  - floor/scripts/hash_util.py
  - floor/scripts/check_cdocs.py
  - floor/scripts/check_manifest.py
  - floor/scripts/check_cdoc_coverage.py
---

# Scripts and Checks

All scripts live in `floor/scripts/`. Two categories: utility modules (no shebang, declare `__all__`) and runnable scripts (shebang + `main()`). Scripts may import from utility modules in the same directory; scripts must not import from other scripts.

## hash_util.py

Utility module. Provides SHA-256 hashing (`text_sha256`), YAML frontmatter parsing (`parse_frontmatter`), and source hash aggregation (`compute_source_hash`, `find_changed_sources`). Imported by `check_cdocs.py` and `check_cdoc_coverage.py`. Not invoked directly.

## check_cdocs.py

Invoked by the prompting agent before composing each task prompt. Reads the `sources:` list from each cdoc's YAML frontmatter, computes an aggregate SHA-256 hash of those files, and compares against stored hashes in `project_management/cdoc_hashes.json`. Reports per cdoc: STALE, fresh, or new. Updates the hash store on every run. A stale cdoc whose own content is unchanged retains its old source hash — the stale signal persists until the cdoc content is also updated.

## check_manifest.py

Audits `project_management/manifest.md` for file coverage. MISSING: a file exists on disk but has no manifest entry. DEAD: a manifest entry references a file that does not exist on disk. Run ad-hoc by the user from the repo root.

## check_cdoc_coverage.py

Run by the task agent as step 3 of the post-task checklist. Reports UNCOVERED: repo files not declared as a source in any cdoc's `sources:` list. The task agent adds uncovered files to the appropriate cdoc's source list, or creates a new cdoc if no suitable one exists.
