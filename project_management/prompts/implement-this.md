# Task: Extract CACT summary prompts into prompt files

## Setup

1. Read `project_management/manifest.md` before proceeding.
2. Run the following CACT walk to load context on the relevant code:
   ```
   python3 project_management/scripts/cact_walk.py \
     project_management/scripts/cact_build.py \
     project_management/scripts/cact_update.py \
     project_management/prompts \
     project/project_management/scripts \
     project/project_management/prompts
   ```
3. Read `project_management/standards/architecture.md` before planning, as this task creates new files and registers them in the CACT tree definition.

## Task

Both `project_management/scripts/cact_build.py` and `project_management/scripts/cact_update.py` contain hardcoded LLM instruction text used when generating CACT directory summaries. Extract those instruction strings into standalone prompt files and update both scripts to load them from disk.

### Prompt files to create

Create these two files, each containing only the instruction text (no dynamic content):

**`project_management/prompts/cact-leaf-summary.md`**
Content: the instruction header currently in `build_leaf_prompt` in `cact_build.py` (and its equivalent inline in `cact_update.py`).

**`project_management/prompts/cact-dir-summary.md`**
Content: the instruction header currently in `build_directory_prompt` in `cact_build.py` (and its equivalent inline in `cact_update.py`).

Mirror both files identically into `floor/project_management/prompts/`.

### Script changes

In both `cact_build.py` and `cact_update.py`:
- Add a loader that reads the prompt file from disk (relative to `repo_root`) and returns its text stripped of leading/trailing whitespace.
- Replace each hardcoded instruction string with a call to the loader.
- The dynamic content (file snippets or child summaries appended after the instruction) remains assembled by code exactly as before — only the instruction header is extracted.

### CACT tree registration

In `cact_build.py`'s `TREE_DEFINITION`:
- Add `cact-leaf-summary.md` and `cact-dir-summary.md` as `"source"` leaf nodes under the existing `project_management/prompts` directory node.
- Add the same two files as `"source"` leaf nodes under the existing `project/project_management/prompts` directory node (pointing to the `floor/` copies).

Do the same mirroring for `floor/project_management/scripts/cact_build.py` if that file also contains `TREE_DEFINITION`.

## Plan first

Present a step-by-step plan and wait for approval before making any changes.

## Style

Follow `project_management/standards/style.md` for all files created or modified.
