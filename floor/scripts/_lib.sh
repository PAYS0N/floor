#!/usr/bin/env bash
# Internal helpers for task counter operations on project_management/status.md.
# Not intended to be called directly — sourced by prompt.sh and done.sh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
STATUS_FILE="$PROJECT_ROOT/project_management/status.md"

_get_counter() {
    awk '/^## Task Counter$/{found=1; next} found && /^[0-9]+$/{print; exit}' "$STATUS_FILE"
}

_set_counter() {
    local current new="$1"
    current=$(_get_counter)
    awk -v old="$current" -v new="$new" '
        /^## Task Counter$/{found=1}
        found && $0 == old {print new; found=0; next}
        {print}
    ' "$STATUS_FILE" > "$STATUS_FILE.tmp" && mv "$STATUS_FILE.tmp" "$STATUS_FILE"
}

case "$1" in
    get)       _get_counter ;;
    increment) _set_counter "$(( $(_get_counter) + 1 ))" ;;
    reset)     _set_counter 0 ;;
    *)         echo "Usage: _lib.sh [get|increment|reset]" >&2; exit 1 ;;
esac
