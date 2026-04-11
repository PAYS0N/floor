Read `project_management/manifest.md` before proceeding.

Then read these context documents:
- `project_management/cdocs/scripts-and-checks.md`
- `project_management/cdocs/scripts-orchestration.md`

## Task

Fix a false-positive stale report in `check_cdocs.py`.

**Bug:** When source files change AND the cdoc is updated in the same pass (content_changed=True), `check_cdocs.py` still reports STALE on the first run after the update, then reports fresh on the second run. This is a false positive — if the cdoc content changed, the developer has already refreshed it.

**Root cause:** In `run_check`, the stale branch only updates the store when `content_changed=True`, but it always prints STALE and sets `any_stale = True` regardless. The store update correctly happens, but the report is wrong.

**Expected behavior:** When `status == "stale"` AND `content_changed == True`, the cdoc should be reported as refreshed (not stale) and should not contribute to a non-zero exit code. The store should be updated as it already is. The stale-persists behavior (no store update, exit 1) should only apply when `content_changed == False`.

**Scope:**
- Edit `project_management/scripts/check_cdocs.py` (logic layer and/or orchestration)
- Edit `floor/scripts/check_cdocs.py` (template copy — must be kept identical)
- Do not change the public interface, exit codes for true-stale cases, or the hash store format
