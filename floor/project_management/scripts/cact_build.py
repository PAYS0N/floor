#!/usr/bin/env python3
"""
cact_build.py -- Build or fully rebuild the CACT tree from scratch.

Reads a hardcoded tree structure definition, computes content hashes for all
leaf nodes, generates directory summaries via the Claude CLI, and writes the
result to project_management/cact_tree.json.

Usage: python project_management/scripts/cact_build.py [--repo-root PATH]
       python project_management/scripts/cact_build.py --no-api [--repo-root PATH]

Exit codes:
  0 -- success
  1 -- tree definition error (missing files, etc.)
  2 -- I/O or subprocess error (claude CLI not found, etc.)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from hash_util import file_sha256, text_sha256

CACT_TREE_PATH = "project_management/cact_tree.json"
MAX_LEAF_LINES = 200


# ── Tree structure definition ────────────────────────────────────────────────
# This is the canonical mapping of the project's semantic tree.
# CUSTOMIZE THIS during project setup (see setup.md):
#   - Add your project's source files and directories under the "project" node.
#   - Update cross-references to reflect lateral dependencies in your project.
#
# The "project_management" subtree covers the Floor scaffolding and should
# require little or no changes. "project" is initially empty — it is the
# placeholder for your project's own source files.
#
# UPDATE THIS FILE whenever the project structure changes.
#
# Node types:
#   "source"      — a source file; content_hash tracks changes
#   "explanation" — a prescriptive doc (standards, rules) never auto-regenerated
#   "directory"   — interior node; summary is LLM-generated from children
#
# Cross-references track lateral dependencies not captured by the tree hierarchy.
# Declare them manually — they are not auto-detected.

TREE_DEFINITION = [
  {
    "key": "root",
    "node_type": "directory",
    "children": [
      # ── Your project files go here ─────────────────────────────────────────
      # Replace this empty "project" node with your actual source structure.
      # Example:
      #   {
      #     "key": "project/src",
      #     "node_type": "directory",
      #     "children": [
      #       {"key": "project/src/main.py", "node_type": "source",
      #        "file_path": "src/main.py"},
      #     ],
      #   },
      {
        "key": "project",
        "node_type": "directory",
        "children": [],
      },
      # ── Floor project management scaffolding ───────────────────────────────
      {
        "key": "project_management",
        "node_type": "directory",
        "children": [
          {
            "key": "project_management/scripts",
            "node_type": "directory",
            "children": [
              {"key": "project_management/scripts/floor.py", "node_type": "source",
               "file_path": "project_management/scripts/floor.py"},
              {"key": "project_management/scripts/shutdown.py", "node_type": "source",
               "file_path": "project_management/scripts/shutdown.py"},
              {"key": "project_management/scripts/check_manifest.py", "node_type": "source",
               "file_path": "project_management/scripts/check_manifest.py"},
              {"key": "project_management/scripts/check_cact_coverage.py", "node_type": "source",
               "file_path": "project_management/scripts/check_cact_coverage.py"},
              {"key": "project_management/scripts/task_counter.py", "node_type": "source",
               "file_path": "project_management/scripts/task_counter.py"},
              {"key": "project_management/scripts/hash_util.py", "node_type": "source",
               "file_path": "project_management/scripts/hash_util.py"},
              {"key": "project_management/scripts/cact_build.py", "node_type": "source",
               "file_path": "project_management/scripts/cact_build.py"},
              {"key": "project_management/scripts/cact_walk.py", "node_type": "source",
               "file_path": "project_management/scripts/cact_walk.py"},
              {"key": "project_management/scripts/cact_update.py", "node_type": "source",
               "file_path": "project_management/scripts/cact_update.py"},
            ],
          },
          {
            "key": "project_management/standards",
            "node_type": "directory",
            "children": [
              {"key": "project_management/standards/architecture.md",
               "node_type": "explanation",
               "file_path": "project_management/standards/architecture.md"},
              {"key": "project_management/standards/style.md",
               "node_type": "explanation",
               "file_path": "project_management/standards/style.md"},
            ],
          },
          {
            "key": "project_management/governance",
            "node_type": "directory",
            "children": [
              {"key": "project_management/governance/CLAUDE.md",
               "node_type": "explanation",
               "file_path": "CLAUDE.md"},
              {"key": "project_management/governance/manifest.md",
               "node_type": "explanation",
               "file_path": "project_management/manifest.md"},
              {"key": "project_management/governance/prompting.md",
               "node_type": "explanation",
               "file_path": "project_management/prompting.md"},
            ],
          },
          {
            "key": "project_management/prompts",
            "node_type": "directory",
            "children": [
              {"key": "project_management/prompts/architecture-check.md",
               "node_type": "source",
               "file_path": "project_management/prompts/architecture-check.md"},
              {"key": "project_management/prompts/implement-this.md",
               "node_type": "source",
               "file_path": "project_management/prompts/implement-this.md"},
            ],
          },
          {
            "key": "project_management/status",
            "node_type": "directory",
            "children": [
              {"key": "project_management/status/status.md", "node_type": "source",
               "file_path": "project_management/status.md"},
            ],
          },
        ],
      },
    ],
  },
]

CROSS_REFERENCES = [
  {
    "source": "project_management/scripts/floor.py",
    "target": "project_management/standards/architecture.md",
    "relation": "enforced_by",
    "note": "Checks arch gate via task counter threshold",
  },
  {
    "source": "project_management/scripts/shutdown.py",
    "target": "project_management/governance/manifest.md",
    "relation": "enforced_by",
    "note": "Runs manifest audit post-task",
  },
  {
    "source": "project_management/scripts/floor.py",
    "target": "project_management/governance/prompting.md",
    "relation": "reads",
    "note": "Injects prompting instructions into the assembled prompt",
  },
  # Add cross-references for your project files here.
]


# ── Logic layer ──────────────────────────────────────────────────────────────


def flatten_definition(tree_def, parent=None):
  """Walk the tree definition and return a flat dict of {key: node_info}.

  Also returns a processing order list (leaves first, then directories
  bottom-up) suitable for hash computation and summary generation.
  """
  nodes = {}
  order = []

  for item in tree_def:
    key = item["key"]
    node_type = item["node_type"]

    if node_type == "directory":
      child_defs = item.get("children", [])
      child_keys = [c["key"] for c in child_defs]
      nodes[key] = {
        "node_type": "directory",
        "children": child_keys,
      }
      # Recurse into children first (bottom-up order)
      child_nodes, child_order = flatten_definition(child_defs, key)
      nodes.update(child_nodes)
      order.extend(child_order)
      order.append(key)
    else:
      nodes[key] = {
        "node_type": node_type,
        "file_path": item["file_path"],
      }
      order.append(key)

  return nodes, order


MISSING_FILE_HASH = "0" * 64


def compute_leaf_hash(node, repo_root):
  """Compute content_hash for a source or explanation leaf node.

  Returns a zeroed hash if the file does not exist yet (e.g. implement-this.md
  before the first floor session).
  """
  try:
    return file_sha256(repo_root / node["file_path"])
  except FileNotFoundError:
    return MISSING_FILE_HASH


def compute_directory_hash(node, nodes):
  """Compute content_hash for a directory node from its children's hashes."""
  child_hashes = []
  for child_key in sorted(node["children"]):
    child = nodes[child_key]
    if "content_hash" not in child:
      raise ValueError(f"child {child_key} has no content_hash yet")
    child_hashes.append(child["content_hash"])
  combined = "".join(child_hashes)
  return text_sha256(combined)


def build_leaf_prompt(children_content):
  """Build a prompt for summarizing a directory whose children are all leaves."""
  parts = ["Summarize what this group of files does, their dependencies, and "
           "any constraints they enforce. Write 3-5 dense sentences.\n"]
  for name, content in children_content:
    parts.append(f"### {name}\n```\n{content}\n```\n")
  return "\n".join(parts)


def build_directory_prompt(children_summaries):
  """Build a prompt for summarizing a directory with directory children."""
  parts = ["Write a higher-level 2-4 sentence summary of what this group does, "
           "based on the child summaries below.\n"]
  for name, summary in children_summaries:
    parts.append(f"### {name}\n{summary}\n")
  return "\n".join(parts)


# ── I/O layer ────────────────────────────────────────────────────────────────


def read_file_head(path, max_lines=MAX_LEAF_LINES):
  """Read up to max_lines from a file. Returns the text, or a placeholder
  if the file does not exist."""
  if not path.exists():
    return "(file not yet created)"
  lines = path.read_text(encoding="utf-8").splitlines()
  if len(lines) > max_lines:
    lines = lines[:max_lines]
    lines.append(f"\n... (truncated at {max_lines} lines)")
  return "\n".join(lines)


def call_claude(prompt):
  """Call claude CLI in non-interactive mode. Returns stdout text.

  Raises RuntimeError if the CLI is not found or returns an error.
  """
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


def write_tree(repo_root, tree_data):
  """Write cact_tree.json to disk."""
  path = repo_root / CACT_TREE_PATH
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(
    json.dumps(tree_data, indent=2) + "\n",
    encoding="utf-8",
  )


# ── Orchestration ────────────────────────────────────────────────────────────


def generate_summary(key, node, nodes, repo_root):
  """Generate a summary for a directory node by calling the Claude CLI."""
  children = node["children"]
  has_dir_children = any(
    nodes[ck]["node_type"] == "directory" for ck in children
  )

  if has_dir_children:
    # Mix of directories and leaves — use child summaries
    child_summaries = []
    for ck in children:
      child = nodes[ck]
      if child["node_type"] == "directory":
        child_summaries.append((ck, child.get("summary", "(no summary)")))
      else:
        content = read_file_head(repo_root / child["file_path"])
        child_summaries.append((ck, content))
    prompt = build_directory_prompt(child_summaries)
  else:
    # All children are leaves
    children_content = []
    for ck in children:
      child = nodes[ck]
      content = read_file_head(repo_root / child["file_path"])
      children_content.append((ck, content))
    prompt = build_leaf_prompt(children_content)

  return call_claude(prompt)


def build_tree(repo_root, no_api=False):
  """Build the full CACT tree. Returns (tree_data, stats).

  If no_api is True, directory summaries are set to a placeholder
  and marked stale instead of calling the Claude CLI.
  """
  nodes, order = flatten_definition(TREE_DEFINITION)
  stats = {"nodes": len(nodes), "summaries_generated": 0, "cli_calls": 0}

  # Compute leaf hashes
  for key in order:
    node = nodes[key]
    if node["node_type"] in ("source", "explanation"):
      node["content_hash"] = compute_leaf_hash(node, repo_root)

  # Compute directory hashes and summaries (bottom-up via order)
  for key in order:
    node = nodes[key]
    if node["node_type"] != "directory":
      continue
    node["content_hash"] = compute_directory_hash(node, nodes)
    if no_api:
      node["summary"] = "(summary pending — run without --no-api to generate)"
      node["stale"] = True
    else:
      node["summary"] = generate_summary(key, node, nodes, repo_root)
      stats["summaries_generated"] += 1
      stats["cli_calls"] += 1

  tree_data = {
    "version": 1,
    "root": "root",
    "nodes": nodes,
    "cross_references": CROSS_REFERENCES,
  }
  return tree_data, stats


def main():
  parser = argparse.ArgumentParser(
    description="Build or fully rebuild the CACT tree."
  )
  parser.add_argument(
    "--repo-root",
    default=".",
    help="path to repo root (default: current directory)",
  )
  parser.add_argument(
    "--no-api",
    action="store_true",
    help="skip Claude CLI calls; mark directory summaries as stale",
  )
  args = parser.parse_args()
  repo_root = Path(args.repo_root).resolve()

  try:
    tree_data, stats = build_tree(repo_root, no_api=args.no_api)
  except FileNotFoundError as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 1
  except RuntimeError as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 2

  write_tree(repo_root, tree_data)

  print(f"CACT tree built: {stats['nodes']} nodes, "
        f"{stats['summaries_generated']} summaries generated, "
        f"{stats['cli_calls']} CLI calls.")
  print(f"Written to {CACT_TREE_PATH}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
