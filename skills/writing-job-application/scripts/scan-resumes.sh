#!/usr/bin/env bash

set -euo pipefail

LOCAL_PATH=${1:-"$PWD/resumes"}
GLOBAL_PATH=${2:-"$HOME/.agents/resumes"}
entries=()

file_metadata() {
    local file=$1
    if stat -f "%m|%z|%N" "$file" >/dev/null 2>&1; then
        stat -f "%m|%z|%N" "$file"
    else
        stat -c "%Y|%s|%n" "$file"
    fi
}

collect_resumes() {
    local dir=$1
    local file
    if [ ! -d "$dir" ]; then
        return
    fi

    while IFS= read -r -d '' file; do
        entries+=("$(file_metadata "$file")")
    done < <(find "$dir" -maxdepth 1 -type f \( -name "*.pdf" -o -name "*.md" \) -print0)
}

format_date() {
    local timestamp=$1
    if date -r "$timestamp" "+%Y-%m-%d %H:%M:%S" >/dev/null 2>&1; then
        date -r "$timestamp" "+%Y-%m-%d %H:%M:%S"
    else
        date -d "@$timestamp" "+%Y-%m-%d %H:%M:%S"
    fi
}

collect_resumes "$LOCAL_PATH"
collect_resumes "$GLOBAL_PATH"

printf 'RESUME_COUNT=%s\n' "${#entries[@]}"
if [ "${#entries[@]}" -eq 0 ]; then
    exit 0
fi

printf 'MODIFIED_AT\tSIZE_BYTES\tPATH\n'
printf '%s\n' "${entries[@]}" | sort -t '|' -k1,1nr | while IFS='|' read -r timestamp size path; do
    printf '%s\t%s\t%s\n' "$(format_date "$timestamp")" "$size" "$path"
done
