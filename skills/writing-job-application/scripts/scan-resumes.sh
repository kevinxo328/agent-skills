#!/bin/bash

# Define paths to search
LOCAL_PATH="./resumes"
GLOBAL_PATH="$HOME/.agents/resumes"

# Function to list resumes in a directory
list_resumes() {
    local dir=$1
    if [ -d "$dir" ]; then
        # Find .pdf and .md files
        find "$dir" -maxdepth 1 \( -name "*.pdf" -o -name "*.md" \) 2>/dev/null | while read -r file; do
            # Using stat for macOS (Darwin)
            # %m: modification time, %z: size
            stat -f "%m|%z|%N" "$file"
        done
    fi
}

# Collect all resumes
resumes=$( (list_resumes "$LOCAL_PATH"; list_resumes "$GLOBAL_PATH") | sort -rn )

if [ -z "$resumes" ]; then
    echo "No resumes found in $LOCAL_PATH or $GLOBAL_PATH"
    exit 0
fi

echo "Found the following resumes (sorted by most recent):"
echo "--------------------------------------------------"
printf "%-25s | %-10s | %s\n" "Modified Date" "Size" "Path"

while IFS='|' read -r timestamp size path; do
    date_str=$(date -r "$timestamp" "+%Y-%m-%d %H:%M:%S")
    
    # Simple human readable size since numfmt might not be on all macOS
    if [ "$size" -ge 1048576 ]; then
        size_h="$(echo "scale=1; $size/1048576" | bc) MiB"
    elif [ "$size" -ge 1024 ]; then
        size_h="$(echo "scale=1; $size/1024" | bc) KiB"
    else
        size_h="$size B"
    fi
    
    printf "%-25s | %-10s | %s\n" "$date_str" "$size_h" "$path"
done <<< "$resumes"
