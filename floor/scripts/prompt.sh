#!/usr/bin/env bash
# Entry point for starting a new task or architecture health check.
# Checks the task counter and routes to the appropriate agent.
# Usage: ./scripts/prompt.sh "<task description>"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT" || exit 1

if [ -z "$1" ]; then
    echo "Usage: scripts/prompt.sh \"<task description>\"" >&2
    exit 1
fi

counter=$("$SCRIPT_DIR/_lib.sh" get)

if [ "$counter" -ge 10 ]; then
    claude -p "$(cat project_management/prompts/architecture-check.md)"
    "$SCRIPT_DIR/_lib.sh" reset
else
    claude -p "$(cat project_management/prompting.md)

Task: $1"
fi
