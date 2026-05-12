# Task: Implement CACT (Content-Addressed Context Tree)

## Goal

Replace Floor's cdoc system with CACT: a tree of file/directory nodes where directory nodes hold LLM-generated summaries of their contents. Content hashing detects when summaries are stale.

CACT fully replaces cdocs. After this task, the cdoc system (scripts, hash store, cdocs/, cdoc.md) is gone.

## Tree model

Two node types:

- **leaf** — a file. `content_hash` = SHA-256 of file bytes. No summary.
- **directory** — a directory. `content_hash` = SHA-256 of children's content_hashes concatenated in sorted order. `summary` = LLM-generated text describing the directory's contents.

Node keys are filesystem paths relative to the repo root (e.g. `project_management/scripts/floor.py`). No synthetic key space, no `file_path` field. The tree's shape comes from the filesystem.

When a directory's `content_hash` differs from stored, its summary is stale and must be regenerated.

## Tree file: `project_management/cact_tree.json`

```json
{
  "version": 1,
  "root": "project_management",
  "nodes": {
    "project_management": {
      "node_type": "directory",
      "summary": "...",
      "content_hash": "...",
      "children": ["project_management/scripts", "project_management/standards", "..."]
    },
    "project_management/scripts": {
      "node_type": "directory",
      "summary": "...",
      "content_hash": "...",
      "children": ["project_management/scripts/floor.py", "..."]
    },
    "project_management/scripts/floor.py": {
      "node_type": "leaf",
      "content_hash": "..."
    }
  }
}
```

Generated, not hand-edited. Do not commit a stub; first run of `cact build` produces it.

## Excludes

Files/dirs not included in the tree:
- `.git/`
- `project_management/artifacts/`
- `project_management/cact_tree.json` (the tree file itself)
- `.floor_session.json`
- `project_management/task_counter.txt`
- `__pycache__/`, `*.pyc`
- Everything matched by `.gitignore`

Define as a constant `DEFAULT_EXCLUDES` plus `.gitignore` parsing. Mirror the pattern in the existing `check_cdoc_coverage.py` so the two implementations look familiar.

## Prompts (markdown, not hardcoded)

Create two separate prompt files — `project_management/prompts/cact-summarize-leaf.md` and `project_management/prompts/cact-summarize-dir.md`. Each is a plain prompt that is prepended as context before the children content when the script calls `claude -p`.

- `cact-summarize-leaf.md`: primes the model to produce 3–5 dense sentences on what a set of leaf files do.
- `cact-summarize-dir.md`: primes the model to produce 2–4 sentences at a higher level from child directory summaries.

## Single script: `project_management/scripts/cact.py`

One file, three subcommands. Shared helpers (load/save tree, walk filesystem, hash, summarize) are module-level functions used by all subcommands.

```
python3 project_management/scripts/cact.py build [--no-api]
python3 project_management/scripts/cact.py check
python3 project_management/scripts/cact.py walk <path> [<path> ...] [--full]
```

### `cact build`

Idempotent full build. First run creates the tree; later runs only call the LLM for directories whose `content_hash` actually changed.

1. Walk filesystem from repo root, applying excludes. Every directory becomes a directory node; every file becomes a leaf node.
2. Compute hashes bottom-up (file SHA-256 for leaves; sorted concat-hash of children for directories).
3. Load existing tree if present. For each directory node whose `content_hash` differs from the stored value (or has no stored value), regenerate its summary via `claude -p` using the appropriate prompt section. Reuse the existing summary otherwise.
4. Save tree. Print: nodes total, summaries regenerated, LLM calls made.

`--no-api`: skip LLM calls. Mark directories with new/changed hashes as `"stale": true` in the node dict. Useful when `claude` isn't available.

If `claude` errors or isn't on PATH (and `--no-api` wasn't passed), print the error and exit 2.

### `cact check`

Read-only for files. Only writes are for hashes, no LLM calls.

1. Walk filesystem; recompute hashes.
2. Compare against stored tree. Report:
   - Leaves whose file hash changed
   - Directories whose content_hash changed (i.e., have stale summaries)
   - Files on disk not in the tree (uncovered) — should be empty since the tree is filesystem-derived, but coverage check guards against excludes drift
   - Files in the tree not on disk (deleted)
3. Exit 0 if fully fresh, 1 if anything is stale or missing.

Used by `floor.py` pre-session to decide whether to run `cact build`.

### `cact walk <path> [<path> ...]`

Read-only. Emits markdown context for the given target paths.

1. Load tree.
2. For each target, collect the chain of ancestor directory nodes from root down.
3. Merge ancestor chains (shared ancestors appear once).
4. Output markdown:

```markdown
# Context

## project_management
[summary]

## project_management/scripts
[summary]

### Target: project_management/scripts/floor.py
```

5. `--full`: also inline the file contents of target leaves (read from disk).

No LLM calls.

## Integration changes

### `project_management/scripts/floor.py`

Replace the cdoc staleness check + routing-table injection with:

1. Run `cact check`. If it reports stale, run `cact build`.
2. Run `cact walk` against the entire `project_management/` root (or equivalently, dump all directory summaries) and inject the output into the assembled prompt. The prompting agent gets the full summary tree and uses it to pick which paths the acting agent should walk.

### `project_management/prompting.md`

Replace the cdoc routing table and instruction #3 with:

> The assembled prompt includes the full CACT summary tree. Identify which directories/files are relevant. In the implementation prompt, instruct the acting agent to run `python3 project_management/scripts/cact.py walk <paths>` to load context before proceeding. Do not paste summaries into the prompt — the agent walks the tree itself.

Update #4 and #5 to use path/node terminology where appropriate.

### `CLAUDE.md`

Replace the cdoc rule with:

> Remember: When starting a task, if the task prompt specifies CACT paths, run `python3 project_management/scripts/cact.py walk <paths>` and read the output before proceeding.

### `project_management/standards/architecture.md`

Add `cact.py` to the Module Hierarchy table. CACT layering:
- `cact.py` is a Layer 2 (Check) script for the read-only `check` and `walk` subcommands; the `build` subcommand mutates `cact_tree.json` and shells out to `claude` (analogous to existing scripts that update the cdoc hash store). Place it alongside the other check scripts and add a one-line note that `build` is the write path.

Add to State / Data Mutation Rules:
- **`project_management/cact_tree.json`** — written by `cact build`. Read by `cact walk`, `cact check`, and `floor.py`.

### `project_management/manifest.md`

- Add row: `project_management/scripts/cact.py` — CACT tooling: build/check/walk subcommands for the content-addressed context tree
- Add row: `project_management/prompts/cact-summarize.md` — Prompt templates used by `cact build` for directory summary generation
- Add row: `project_management/cact_tree.json` — Generated CACT tree (node hashes + directory summaries)
- Remove rows for the deleted cdoc files (see Removals).

### `project_management/scripts/shutdown.py`

Replace the `check_cdocs.py` and `check_cdoc_coverage.py` calls with a single `cact build` call. In "Actions Required," add:
- "Review regenerated summaries in `cact_tree.json` for accuracy."

## Removals (cdoc system)

Delete:
- `project_management/scripts/check_cdocs.py`
- `project_management/scripts/check_cdoc_coverage.py`
- `project_management/cdoc.md`
- `project_management/cdoc_hashes.json`
- `project_management/cdocs/` (entire directory and all cdocs in it)

Remove all references to the above from `manifest.md`, `CLAUDE.md`, `prompting.md`, `floor.py`, `shutdown.py`, and any other file that mentions them. Grep for `cdoc` to find stragglers.

## Implementation order

1. `project_management/prompts/cact-summarize.md`
2. `project_management/scripts/cact.py` (build, check, walk in one file)
3. `project_management/scripts/floor.py` and `shutdown.py` integration
4. `CLAUDE.md`, `prompting.md`, `manifest.md`, `standards/architecture.md` updates
5. Delete the cdoc system (scripts, cdoc.md, cdoc_hashes.json, cdocs/)
6. Run `cact build` once to generate the initial tree

## Shutdown

When implementation is complete, before waiting for confirmation:

1. Write a brief summary of what was done.
2. List suggested test steps for the user (running tests is the user's responsibility).
3. Pause and wait for the user to confirm.

Only after the user confirms, run `python3 project_management/scripts/shutdown.py`.
