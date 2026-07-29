#!/bin/bash

# Script to determine ad-hoc packages to test.
# This script is intended to be sourced from main test scripts.

# Ensure we are in the project root if called directly,
# but usually this is sourced and CWD is already project root.
# For safety, we can use script location but if sourced $0 might be the parent script.
# Let's assume CWD is project root as per system.sh behavior.

ADHOC_DIR="ci/adhoc"
STANDALONE_LIST="${ADHOC_DIR}/.standalone_package_list.txt"
GROUPS_FILE="${ADHOC_DIR}/.package_groups.txt"

if [[ ! -f "$STANDALONE_LIST" ]]; then
    echo "Warning: $STANDALONE_LIST not found."
    return 0 2>/dev/null || exit 0
fi

if [[ ! -f "$GROUPS_FILE" ]]; then
    echo "Warning: $GROUPS_FILE not found."
    return 0 2>/dev/null || exit 0
fi

# Grab individual packages
adhoc_packages=$(grep "^package:" "$STANDALONE_LIST" | cut -d':' -f2 | xargs || true)

# Grab requested groups
requested_groups=$(grep "^group:" "$STANDALONE_LIST" | cut -d':' -f2 | xargs || true)

# Expand groups
for group in $requested_groups; do
    group_pkgs=$(grep "^$group:" "$GROUPS_FILE" | cut -d':' -f2 | xargs || true)
    adhoc_packages="$adhoc_packages $group_pkgs"
done

# Convert to unique list (deduplicate our adhoc packages)
ADHOC_PACKAGES=$(echo "$adhoc_packages" | tr ' ' '\n' | sort -u | xargs)

export ADHOC_PACKAGES
