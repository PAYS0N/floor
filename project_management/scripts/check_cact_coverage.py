#!/usr/bin/env python3
"""
check_cact_coverage.py -- Reports repo files not represented as a leaf node in
the CACT tree.

Loads cact_tree.json, collects all leaf node file_path values, walks the repo,
and reports any file not declared as a leaf.

Usage: python project_management/scripts/check_cact_coverage.py [--repo-root PATH]
       python project_management/scripts/check_cact_coverage.py [--repo-root PATH] [--exclude PATH ...]

Exit codes:
  0 -- all files covered
  1 -- any uncovered files found
  2 -- cact_tree.json not found or unreadable
"""

import argparse
import json
import sys
from pathlib import Path

from hash_util import DEFAULT_COVERAGE_EXCLUDES, read_gitignore_patterns

CACT_TREE_PATH = "project_management/cact_tree.json"


# ── Logic layer ──────────────────────────────────────────────────────────────


def collect_leaf_paths(nodes):
  """Return the set of file_path values declared across all leaf nodes."""
  return {node["file_path"] for node in nodes.values() if "file_path" in node}


def is_excluded(rel_path, excludes):
  """Return True if rel_path matches or is under any excluded path."""
  for excl in excludes:
    excl = excl.rstrip("/")
    if rel_path == excl or rel_path.startswith(excl + "/"):
      return True
  return False


# ── I/O layer ────────────────────────────────────────────────────────────────


def load_tree(repo_root):
  """Load cact_tree.json. Raises FileNotFoundError or json.JSONDecodeError."""
  path = repo_root / CACT_TREE_PATH
  if not path.exists():
    raise FileNotFoundError(
      f"{CACT_TREE_PATH} not found. Run cact_build.py first."
    )
  return json.loads(path.read_text(encoding="utf-8"))


def walk_repo_files(repo_root, excludes):
  """Yield relative path strings for all files under repo_root.

  Skips .git/ and __pycache__/ subtrees, and any path in excludes.
  """
  for path in sorted(repo_root.rglob("*")):
    if not path.is_file():
      continue
    rel = str(path.relative_to(repo_root))
    parts = path.relative_to(repo_root).parts
    if any(part in {".git", "__pycache__"} for part in parts):
      continue
    if is_excluded(rel, excludes):
      continue
    yield rel


# ── Orchestration ────────────────────────────────────────────────────────────


def normalize_excludes(excludes, repo_root):
  """Return excludes as paths relative to repo_root.

  Accepts paths relative to CWD or already relative to repo_root.
  Paths that cannot be made relative are kept as-is.
  """
  normalized = []
  for excl in excludes:
    try:
      abs_excl = (Path.cwd() / excl).resolve()
      normalized.append(str(abs_excl.relative_to(repo_root)))
    except ValueError:
      normalized.append(excl)
  return normalized


def run_check(repo_root, extra_excludes):
  """Walk repo files and report any not declared as a CACT leaf node.

  Returns exit code: 0 if all covered, 1 if any uncovered, 2 on error.
  """
  try:
    tree_data = load_tree(repo_root)
  except FileNotFoundError as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 2
  except json.JSONDecodeError as exc:
    print(f"error: could not parse {CACT_TREE_PATH}: {exc}", file=sys.stderr)
    return 2

  covered = collect_leaf_paths(tree_data["nodes"])
  gitignore = read_gitignore_patterns(repo_root)
  all_excludes = (
    DEFAULT_COVERAGE_EXCLUDES
    + gitignore
    + normalize_excludes(extra_excludes, repo_root)
  )
  disk_files = list(walk_repo_files(repo_root, all_excludes))

  uncovered = sorted(f for f in disk_files if f not in covered)
  for path in uncovered:
    print(f"UNCOVERED: {path}")

  return 1 if uncovered else 0


def main():
  parser = argparse.ArgumentParser(
    description="Report repo files not represented as a leaf node in the CACT tree."
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
