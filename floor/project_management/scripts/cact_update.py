#!/usr/bin/env python3
"""
cact_update.py -- Incremental CACT tree update.

Detects changed files, regenerates stale directory summaries, checks file
coverage, and saves the updated tree.

Usage:
  python project_management/scripts/cact_update.py [--repo-root PATH]
  python project_management/scripts/cact_update.py --check-only [--repo-root PATH]
  python project_management/scripts/cact_update.py --no-api [--repo-root PATH]

Modes:
  (default)      Full update: recompute hashes, regenerate summaries, save.
  --check-only   Report staleness only. Exit 0 if fresh, 1 if stale.
  --no-api       Recompute hashes, mark stale summaries, skip regeneration.

Exit codes:
  0 -- success (or fresh, in --check-only mode)
  1 -- stale nodes found (--check-only), or tree definition error
  2 -- I/O or subprocess error
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from hash_util import (
  DEFAULT_COVERAGE_EXCLUDES,
  file_sha256,
  read_gitignore_patterns,
  text_sha256,
)

CACT_TREE_PATH = "project_management/cact_tree.json"
MAX_LEAF_LINES = 200


# ── Logic layer ──────────────────────────────────────────────────────────────


def is_excluded(rel_path, excludes):
  """Return True if rel_path matches or is under any excluded prefix."""
  for excl in excludes:
    if rel_path == excl or rel_path.startswith(excl + "/"):
      return True
  return False


def compute_directory_hash(node, nodes):
  """Compute content_hash for a directory from sorted children hashes."""
  child_hashes = []
  for child_key in sorted(node["children"]):
    child = nodes[child_key]
    child_hashes.append(child["content_hash"])
  return text_sha256("".join(child_hashes))


def find_stale_leaves(nodes, repo_root):
  """Recompute leaf hashes, return dict of {key: new_hash} for changed leaves."""
  changed = {}
  for key, node in nodes.items():
    if node["node_type"] not in ("source", "explanation"):
      continue
    path = repo_root / node["file_path"]
    try:
      new_hash = file_sha256(path)
    except FileNotFoundError:
      print(f"warning: file not found for node {key}: {node['file_path']}",
            file=sys.stderr)
      continue
    if new_hash != node.get("content_hash"):
      changed[key] = new_hash
  return changed


def find_stale_directories(nodes, root_key):
  """Return set of directory keys whose content_hash changed.

  Must be called after leaf hashes are updated in nodes.
  Processes bottom-up.
  """
  stale = set()

  def walk(key):
    node = nodes[key]
    if node["node_type"] != "directory":
      return
    for ck in node["children"]:
      walk(ck)
    new_hash = compute_directory_hash(node, nodes)
    if new_hash != node.get("content_hash"):
      stale.add(key)
      node["content_hash"] = new_hash

  walk(root_key)
  return stale


def get_processing_order(nodes, root_key):
  """Return directory keys in bottom-up order."""
  order = []

  def walk(key):
    node = nodes[key]
    if node["node_type"] != "directory":
      return
    for ck in node["children"]:
      walk(ck)
    order.append(key)

  walk(root_key)
  return order


def collect_leaf_file_paths(nodes):
  """Return set of file_path values from all leaf nodes."""
  return {
    node["file_path"]
    for node in nodes.values()
    if "file_path" in node
  }


def find_uncovered_files(repo_root, covered_paths, excludes):
  """Return sorted list of repo files not in the CACT tree."""
  uncovered = []
  for path in sorted(repo_root.rglob("*")):
    if not path.is_file():
      continue
    rel = str(path.relative_to(repo_root))
    if any(part in {".git", "__pycache__"} for part in path.relative_to(repo_root).parts):
      continue
    if is_excluded(rel, excludes):
      continue
    if rel not in covered_paths:
      uncovered.append(rel)
  return uncovered


# ── I/O layer ────────────────────────────────────────────────────────────────


def load_tree(repo_root):
  """Load cact_tree.json. Returns the parsed dict or raises."""
  path = repo_root / CACT_TREE_PATH
  if not path.exists():
    raise FileNotFoundError(
      f"{CACT_TREE_PATH} not found. Run cact_build.py first."
    )
  return json.loads(path.read_text(encoding="utf-8"))


def save_tree(repo_root, tree_data):
  """Write cact_tree.json to disk."""
  path = repo_root / CACT_TREE_PATH
  path.write_text(
    json.dumps(tree_data, indent=2) + "\n",
    encoding="utf-8",
  )


def read_file_head(path, max_lines=MAX_LEAF_LINES):
  """Read up to max_lines from a file."""
  lines = path.read_text(encoding="utf-8").splitlines()
  if len(lines) > max_lines:
    lines = lines[:max_lines]
    lines.append(f"\n... (truncated at {max_lines} lines)")
  return "\n".join(lines)


def call_claude(prompt):
  """Call claude CLI in non-interactive mode. Returns stdout text."""
  try:
    result = subprocess.run(
      ["claude", "-p", prompt, "--model", "claude-sonnet-4-6"],
      capture_output=True,
      text=True,
      timeout=120,
    )
  except FileNotFoundError:
    raise RuntimeError("claude CLI not found on PATH")
  except subprocess.TimeoutExpired:
    raise RuntimeError("claude CLI call timed out")
  if result.returncode != 0:
    raise RuntimeError(
      f"claude CLI returned exit code {result.returncode}: "
      f"{result.stderr.strip()}"
    )
  return result.stdout.strip()


def regenerate_summary(key, node, nodes, repo_root):
  """Regenerate a directory node's summary via the Claude CLI."""
  children = node["children"]
  has_dir_children = any(
    nodes[ck]["node_type"] == "directory" for ck in children
  )

  if has_dir_children:
    parts = ["Write a higher-level 2-4 sentence summary of what this group "
             "does, based on the child summaries below.\n"]
    for ck in children:
      child = nodes[ck]
      if child["node_type"] == "directory":
        parts.append(f"### {ck}\n{child.get('summary', '(no summary)')}\n")
      else:
        content = read_file_head(repo_root / child["file_path"])
        parts.append(f"### {ck}\n{content}\n")
    prompt = "\n".join(parts)
  else:
    parts = ["Summarize what this group of files does, their dependencies, "
             "and any constraints they enforce. Write 3-5 dense sentences.\n"]
    for ck in children:
      child = nodes[ck]
      content = read_file_head(repo_root / child["file_path"])
      parts.append(f"### {ck}\n```\n{content}\n```\n")
    prompt = "\n".join(parts)

  return call_claude(prompt)


# ── Orchestration ────────────────────────────────────────────────────────────


def run_update(repo_root, check_only=False, no_api=False):
  """Main update logic. Returns exit code."""
  try:
    tree_data = load_tree(repo_root)
  except (FileNotFoundError, json.JSONDecodeError) as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 1

  nodes = tree_data["nodes"]
  root_key = tree_data["root"]

  # Step 1: find changed leaves
  changed_leaves = find_stale_leaves(nodes, repo_root)

  # Update leaf hashes in the tree
  explanation_updates = []
  for key, new_hash in changed_leaves.items():
    node = nodes[key]
    node["content_hash"] = new_hash
    if node["node_type"] == "explanation":
      explanation_updates.append(key)

  # Step 2: find stale directories (bottom-up recompute)
  stale_dirs = find_stale_directories(nodes, root_key)

  # Step 3: check-only mode — report and exit
  if check_only:
    if not changed_leaves and not stale_dirs:
      print("CACT tree is fresh.")
      return 0
    if changed_leaves:
      print("Stale leaves:")
      for key in sorted(changed_leaves):
        node = nodes[key]
        print(f"  {key} -> {node.get('file_path', '?')}")
    if stale_dirs:
      print("Stale directory summaries:")
      for key in sorted(stale_dirs):
        print(f"  {key}")
    return 1

  # Step 4: report explanation updates
  for key in explanation_updates:
    node = nodes[key]
    print(f"explanation node updated: {key} "
          f"— parent summaries will be regenerated")

  # Step 5: regenerate stale directory summaries
  summaries_regenerated = []
  if stale_dirs:
    order = get_processing_order(nodes, root_key)
    for key in order:
      if key not in stale_dirs:
        continue
      node = nodes[key]
      if no_api:
        node["stale"] = True
        summaries_regenerated.append((key, False))
      else:
        try:
          node["summary"] = regenerate_summary(key, node, nodes, repo_root)
          node.pop("stale", None)
          summaries_regenerated.append((key, True))
        except RuntimeError as exc:
          print(f"warning: could not regenerate {key}: {exc}",
                file=sys.stderr)
          node["stale"] = True
          summaries_regenerated.append((key, False))

  # Step 6: coverage check
  gitignore_patterns = read_gitignore_patterns(repo_root)
  all_excludes = DEFAULT_COVERAGE_EXCLUDES + gitignore_patterns
  covered = collect_leaf_file_paths(nodes)
  uncovered = find_uncovered_files(repo_root, covered, all_excludes)

  # Step 7: save
  save_tree(repo_root, tree_data)

  # Step 8: structured report
  print("# CACT Update Report\n")

  if changed_leaves:
    print("## Changed leaves")
    for key in sorted(changed_leaves):
      node = nodes[key]
      print(f"  {key} -> {node.get('file_path', '?')}")
    print()

  if summaries_regenerated:
    print("## Summaries")
    for key, was_regenerated in summaries_regenerated:
      status = "regenerated" if was_regenerated else "marked stale"
      print(f"  {key}: {status}")
    print()

  if uncovered:
    print("## Uncovered files")
    for path in uncovered:
      print(f"  UNCOVERED: {path}")
    print()

  root_changed = root_key in stale_dirs
  print(f"Root hash changed: {root_changed}")

  return 0


def main():
  parser = argparse.ArgumentParser(
    description="Incremental CACT tree update."
  )
  parser.add_argument(
    "--repo-root",
    default=".",
    help="path to repo root (default: current directory)",
  )
  parser.add_argument(
    "--check-only",
    action="store_true",
    help="report staleness without updating; exit 0=fresh, 1=stale",
  )
  parser.add_argument(
    "--no-api",
    action="store_true",
    help="update hashes but skip summary regeneration (mark stale)",
  )
  args = parser.parse_args()

  if args.check_only and args.no_api:
    parser.error("--check-only and --no-api are mutually exclusive")

  repo_root = Path(args.repo_root).resolve()

  try:
    sys.exit(run_update(repo_root, args.check_only, args.no_api))
  except RuntimeError as exc:
    print(f"error: {exc}", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
  main()
