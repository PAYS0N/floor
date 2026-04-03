#!/usr/bin/env bash
# Increments the task counter in project_management/status.md.
# Called by the task agent as the final step of the completion checklist.
# Usage: ./scripts/done.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT" || exit 1

"$SCRIPT_DIR/_lib.sh" increment
