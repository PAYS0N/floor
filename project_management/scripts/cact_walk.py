#!/usr/bin/env python3
"""
cact_walk.py -- Walk the CACT tree and output accumulated context.

Given one or more node keys (or file paths), outputs the context path from
root to each target as structured markdown. No API/CLI calls — pure I/O.

Usage:
  python project_management/scripts/cact_walk.py <key> [<key> ...]
  python project_management/scripts/cact_walk.py --all
  python project_management/scripts/cact_walk.py --full <key> [<key> ...]

Exit codes:
  0 -- success
  1 -- node not found or tree file missing
  2 -- I/O error
"""

import argparse
import json
import sys
from pathlib import Path

CACT_TREE_PATH = "project_management/cact_tree.json"


# ── Logic layer ──────────────────────────────────────────────────────────────


def resolve_key(nodes, arg):
  """Resolve an argument to a node key.

  Accepts either a node key directly or a file_path, searching leaf nodes
  for a match. Returns the key or None.
  """
  if arg in nodes:
    return arg
  for key, node in nodes.items():
    if node.get("file_path") == arg:
      return key
  return None


def find_ancestors(nodes, root_key, target_key):
  """Return the path from root to target as a list of keys (inclusive).

  Uses BFS from root. Returns [] if target is not reachable.
  """
  # Build parent map
  parent = {root_key: None}
  queue = [root_key]
  while queue:
    current = queue.pop(0)
    node = nodes[current]
    for child_key in node.get("children", []):
      if child_key not in parent:
        parent[child_key] = current
        queue.append(child_key)

  if target_key not in parent:
    return []

  path = []
  cursor = target_key
  while cursor is not None:
    path.append(cursor)
    cursor = parent[cursor]
  path.reverse()
  return path


def merge_paths(paths):
  """Merge multiple root-to-target paths, deduplicating shared ancestors.

  Returns a list of (key, is_target) pairs in tree order.
  """
  seen = set()
  result = []
  targets = {p[-1] for p in paths}

  for path in paths:
    for key in path:
      if key not in seen:
        seen.add(key)
        result.append((key, key in targets))
  return result


def collect_cross_refs(cross_references, path_keys):
  """Return cross-references where source is in path but target is not."""
  path_set = set(path_keys)
  refs = []
  for xref in cross_references:
    if xref["source"] in path_set and xref["target"] not in path_set:
      refs.append(xref)
  return refs


def format_all_tree(nodes, root_key, cross_references):
  """Format the full summary tree: all directory summaries + leaf listing."""
  lines = ["# CACT Summary Tree\n"]

  def walk(key, depth):
    node = nodes[key]
    prefix = "#" * min(depth + 1, 6)
    if node["node_type"] == "directory":
      stale_mark = " (STALE)" if node.get("stale") else ""
      lines.append(f"{prefix} {key}{stale_mark}")
      lines.append(f"{node.get('summary', '(no summary)')}\n")
      # List leaf children
      leaves = [ck for ck in node["children"]
                if nodes[ck]["node_type"] != "directory"]
      if leaves:
        lines.append("Files:")
        for lk in leaves:
          leaf = nodes[lk]
          type_tag = f"[{leaf['node_type']}]"
          lines.append(f"- {lk} {type_tag} -> {leaf['file_path']}")
        lines.append("")
      # Recurse into directory children
      for ck in node["children"]:
        if nodes[ck]["node_type"] == "directory":
          walk(ck, depth + 1)

  walk(root_key, 1)

  if cross_references:
    lines.append("---\n")
    lines.append("## Cross-References\n")
    for xref in cross_references:
      target_node = nodes.get(xref["target"], {})
      file_info = f"  File: {target_node['file_path']}" if "file_path" in target_node else ""
      lines.append(
        f"- {xref['source']} -> {xref['target']} "
        f"({xref['relation']}): {xref['note']}"
      )
      if file_info:
        lines.append(file_info)

  return "\n".join(lines)


def format_context_path(merged, nodes, cross_refs, full_content, repo_root):
  """Format the merged context path as markdown."""
  lines = ["# Context Path\n"]

  for key, is_target in merged:
    node = nodes[key]
    if node["node_type"] == "directory":
      stale_mark = " (STALE)" if node.get("stale") else ""
      lines.append(f"## {key}{stale_mark}")
      lines.append(f"{node.get('summary', '(no summary)')}\n")
    elif is_target:
      lines.append(f"### Target: {key}")
      lines.append(f"File: {node['file_path']}")
      if full_content:
        file_path = repo_root / node["file_path"]
        if file_path.exists():
          content = file_path.read_text(encoding="utf-8")
          lines.append(f"\n```\n{content}\n```")
        else:
          lines.append(f"\n(file not found: {node['file_path']})")
      lines.append("")

  if cross_refs:
    lines.append("---\n")
    lines.append("## See Also")
    for xref in cross_refs:
      target_node = nodes.get(xref["target"], {})
      lines.append(
        f"- {xref['target']} ({xref['relation']}): {xref['note']}"
      )
      if "file_path" in target_node:
        lines.append(f"  File: {target_node['file_path']}")

  return "\n".join(lines)


# ── I/O layer ────────────────────────────────────────────────────────────────


def load_tree(repo_root):
  """Load cact_tree.json. Returns the parsed dict or raises."""
  path = repo_root / CACT_TREE_PATH
  if not path.exists():
    raise FileNotFoundError(
      f"{CACT_TREE_PATH} not found. Run cact_build.py first."
    )
  return json.loads(path.read_text(encoding="utf-8"))


# ── Orchestration ────────────────────────────────────────────────────────────


def run_walk(repo_root, targets, show_all, full_content):
  """Main walk logic. Returns exit code."""
  try:
    tree_data = load_tree(repo_root)
  except (FileNotFoundError, json.JSONDecodeError) as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 1

  nodes = tree_data["nodes"]
  root_key = tree_data["root"]
  cross_refs = tree_data.get("cross_references", [])

  if show_all:
    print(format_all_tree(nodes, root_key, cross_refs))
    return 0

  # Resolve targets to node keys
  resolved = []
  for arg in targets:
    key = resolve_key(nodes, arg)
    if key is None:
      print(f"error: node not found: {arg}", file=sys.stderr)
      return 1
    resolved.append(key)

  # Build ancestor paths
  paths = []
  for key in resolved:
    path = find_ancestors(nodes, root_key, key)
    if not path:
      print(f"error: {key} is not reachable from root", file=sys.stderr)
      return 1
    paths.append(path)

  merged = merge_paths(paths)
  path_keys = [k for k, _ in merged]
  see_also = collect_cross_refs(cross_refs, path_keys)

  print(format_context_path(merged, nodes, see_also, full_content, repo_root))
  return 0


def main():
  parser = argparse.ArgumentParser(
    description="Walk the CACT tree and output accumulated context."
  )
  parser.add_argument(
    "targets",
    nargs="*",
    help="node keys or file paths to walk to",
  )
  parser.add_argument(
    "--all",
    action="store_true",
    dest="show_all",
    help="output the full summary tree",
  )
  parser.add_argument(
    "--full",
    action="store_true",
    help="include file contents of target leaf nodes",
  )
  parser.add_argument(
    "--repo-root",
    default=".",
    help="path to repo root (default: current directory)",
  )
  args = parser.parse_args()
  repo_root = Path(args.repo_root).resolve()

  if not args.show_all and not args.targets:
    parser.error("provide node keys/file paths, or use --all")

  sys.exit(run_walk(repo_root, args.targets, args.show_all, args.full))


if __name__ == "__main__":
  main()
