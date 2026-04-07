#!/usr/bin/env python3
"""
check_manifest.py — Audits project_management/manifest.md in two passes.

Part 1 — File coverage (no hashing):
  MISSING: file exists on disk but has no manifest entry
  DEAD:    manifest entry whose file path does not exist on disk

Part 2 — Cdoc staleness (hashing):
  STALE:   cdoc's declared source files changed since manifest was last updated
  fresh:   cdoc source hash matches stored baseline

Usage: python check_manifest.py [--repo-root PATH] [--exclude PATH ...]

Exit codes:
  0 — all fresh, no missing, no dead
  1 — any missing, dead, or stale
  2 — error (unreadable file, missing source, etc.)
"""

import argparse
import json
import re
import sys
from pathlib import Path

from hash_util import (
  compute_source_hash,
  find_changed_sources,
  parse_frontmatter,
  text_sha256,
)

MANIFEST_PATH = "project_management/manifest.md"
HASH_STORE_PATH = "project_management/manifest_hashes.json"
CDOCS_DIR = "project_management/cdocs"

MANIFEST_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")


# ── Logic layer (pure, no I/O) ────────────────────────────────────────────────


def parse_manifest_paths(manifest_text):
  """Extract file paths from manifest table rows.

  Parses [link text](href) — uses the text inside [...], not the href.
  Skips header and separator rows.
  Returns a set of path strings.
  """
  paths = set()
  for line in manifest_text.splitlines():
    stripped = line.strip()
    if not stripped.startswith("|"):
      continue
    if re.match(r"^\|[-| ]+\|$", stripped):
      continue
    match = MANIFEST_LINK_RE.search(stripped)
    if not match:
      continue
    link_text = match.group(1)
    if link_text.lower() == "file":
      continue
    paths.add(link_text)
  return paths


def is_excluded(rel_path, excludes):
  """Return True if rel_path matches or is under any excluded path."""
  for excl in excludes:
    excl = excl.rstrip("/")
    if rel_path == excl or rel_path.startswith(excl + "/"):
      return True
  return False


def assess_cdoc(cdoc_key, sources, store, repo_root):
  """Assess staleness of a single cdoc's sources against the store.

  Returns a result dict:
    status          — "fresh" | "stale" | "new"
    changed_sources — list of changed paths (stale only)
    current_source_hash  — str
    current_per_file     — dict
  """
  current_source_hash, current_per_file = compute_source_hash(sources, repo_root)

  stored = store.get("cdocs", {}).get(cdoc_key, {})
  stored_source_hash = stored.get("source_hash")
  stored_per_file = stored.get("source_file_hashes", {})

  if stored_source_hash is None:
    status = "new"
    changed = []
  elif current_source_hash != stored_source_hash:
    status = "stale"
    changed = find_changed_sources(current_per_file, stored_per_file)
  else:
    status = "fresh"
    changed = []

  return {
    "status": status,
    "changed_sources": changed,
    "current_source_hash": current_source_hash,
    "current_per_file": current_per_file,
  }


def build_cdoc_store_entry(result):
  """Build the cdocs store entry from an assessment result."""
  return {
    "source_hash": result["current_source_hash"],
    "source_file_hashes": result["current_per_file"],
  }


# ── I/O layer ─────────────────────────────────────────────────────────────────


def load_hash_store(store_path):
  """Load the JSON hash store. Returns {} if the file doesn't exist."""
  if not store_path.exists():
    return {}
  try:
    return json.loads(store_path.read_text(encoding="utf-8"))
  except (json.JSONDecodeError, OSError) as exc:
    print(f"error: could not read hash store at {store_path}: {exc}", file=sys.stderr)
    sys.exit(2)


def save_hash_store(store_path, store):
  """Write the JSON hash store, creating parent directories if needed."""
  store_path.parent.mkdir(parents=True, exist_ok=True)
  store_path.write_text(
    json.dumps(store, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )


def walk_repo_files(repo_root, manifest_rel, excludes):
  """Yield relative path strings for all files under repo_root.

  Excludes:
    - .git/ subtree
    - the manifest file itself
    - any paths in excludes
  """
  for path in sorted(repo_root.rglob("*")):
    if not path.is_file():
      continue
    rel = str(path.relative_to(repo_root))
    rel_parts = path.relative_to(repo_root).parts
    if any(part in {".git", "__pycache__"} for part in rel_parts):
      continue
    if rel == manifest_rel:
      continue
    if is_excluded(rel, excludes):
      continue
    yield rel


def collect_cdoc_paths(cdocs_dir):
  """Return sorted list of .md files in cdocs_dir."""
  if not cdocs_dir.is_dir():
    return []
  return sorted(cdocs_dir.glob("*.md"))


# ── Orchestration ─────────────────────────────────────────────────────────────


def run_check(repo_root, excludes):
  """Run both audit passes, print results, update store.

  Returns exit code: 0 if all clear, 1 if any issues, 2 on error.
  """
  manifest_path = repo_root / MANIFEST_PATH
  store_path = repo_root / HASH_STORE_PATH
  cdocs_dir = repo_root / CDOCS_DIR

  if not manifest_path.exists():
    print(f"error: manifest not found at {manifest_path}", file=sys.stderr)
    return 2

  try:
    manifest_text = manifest_path.read_text(encoding="utf-8")
  except OSError as exc:
    print(f"error: could not read manifest: {exc}", file=sys.stderr)
    return 2

  # ── Part 1: file coverage ─────────────────────────────────────────────────

  manifest_paths = parse_manifest_paths(manifest_text)
  disk_paths = set(walk_repo_files(repo_root, MANIFEST_PATH, excludes))

  missing = sorted(disk_paths - manifest_paths)
  dead = sorted(p for p in manifest_paths if not (repo_root / p).exists())

  any_coverage_issues = bool(missing or dead)

  for path in missing:
    print(f"MISSING: {path}")
  for path in dead:
    print(f"DEAD: {path}")

  # ── Part 2: cdoc staleness ────────────────────────────────────────────────

  store = load_hash_store(store_path)
  current_manifest_hash = text_sha256(manifest_text)
  manifest_updated = current_manifest_hash != store.get("manifest_hash")

  cdoc_paths = collect_cdoc_paths(cdocs_dir)
  updated_cdocs = dict(store.get("cdocs", {}))
  any_stale = False

  for cdoc_path in cdoc_paths:
    cdoc_key = str(cdoc_path.relative_to(repo_root))
    try:
      text = cdoc_path.read_text(encoding="utf-8")
    except OSError as exc:
      print(f"error: could not read {cdoc_key}: {exc}", file=sys.stderr)
      return 2

    frontmatter = parse_frontmatter(text)
    if "sources" not in frontmatter:
      continue

    try:
      result = assess_cdoc(cdoc_key, frontmatter["sources"], store, repo_root)
    except FileNotFoundError as exc:
      print(f"error: {exc}", file=sys.stderr)
      return 2

    status = result["status"]

    if status == "stale":
      any_stale = True
      print(f"STALE: {cdoc_key}")
      for src in result["changed_sources"]:
        print(f"  changed: {src}")
      if manifest_updated:
        updated_cdocs[cdoc_key] = build_cdoc_store_entry(result)
    elif status == "new":
      print(f"new: {cdoc_key} (no prior hash recorded)")
      updated_cdocs[cdoc_key] = build_cdoc_store_entry(result)
    else:
      print(f"fresh: {cdoc_key}")
      updated_cdocs[cdoc_key] = build_cdoc_store_entry(result)

  save_hash_store(store_path, {
    "manifest_hash": current_manifest_hash,
    "cdocs": updated_cdocs,
  })

  if any_coverage_issues or any_stale:
    return 1
  return 0


def main():
  parser = argparse.ArgumentParser(
    description="Audit manifest.md for file coverage and cdoc staleness."
  )
  parser.add_argument(
    "--repo-root",
    default=".",
    help="path to repo root (default: current directory)",
  )
  parser.add_argument(
    "--exclude",
    metavar="PATH",
    action="append",
    default=[],
    help="path to exclude from the file walk (may be specified multiple times)",
  )
  args = parser.parse_args()
  repo_root = Path(args.repo_root).resolve()
  sys.exit(run_check(repo_root, args.exclude))


if __name__ == "__main__":
  main()
