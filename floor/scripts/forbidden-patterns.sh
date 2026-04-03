#!/usr/bin/env bash
# Runs F1-F5 forbidden pattern checks and reports PASS/FAIL for each.
# Called by the architecture health check agent during Step 4.
# Usage: ./scripts/forbidden-patterns.sh
#
# CUSTOMIZE: Replace each [your check command] below with the actual shell
# command from the corresponding entry in project_management/standards/architecture.md.
# A check passes when it produces no output. A check fails when it produces output.
# F5 (circular dependencies) is manual — update its description if you have a tool for it.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT" || exit 1

run_check() {
    local label="$1"
    local desc="$2"
    local result
    result=$(eval "$3" 2>&1)
    if [ -z "$result" ]; then
        echo "$label PASS — $desc"
    else
        echo "$label FAIL — $desc"
        echo "$result"
    fi
}

# CUSTOMIZE: Replace [your check command] with the actual command for each pattern.
run_check "F1" "[Pattern name]" "[your check command]"
run_check "F2" "[Pattern name]" "[your check command]"
run_check "F3" "[Pattern name]" "[your check command]"
run_check "F4" "[Pattern name]" "[your check command]"

# F5 — Circular dependencies (manual review; replace with a tool command if available)
echo "F5 — No circular dependencies: review import graph in architecture health check output"
