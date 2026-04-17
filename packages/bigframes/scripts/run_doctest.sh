#!/bin/bash
# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to non-zero if any command fails,
# or zero if all commands in the pipeline exit successfully.
set -eo pipefail

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Assume we are running from the repo root or we need to find it.
# If this script is in packages/bigframes/scripts/run_doctest.sh,
# then repo root is 3 levels up.
export PROJECT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}")/../../..)
cd "$PROJECT_ROOT"

# This is needed in order for `git diff` to succeed
git config --global --add safe.directory $(realpath .)

package_name="bigframes"
package_path="packages/${package_name}"

# Determine if we should skip based on git diff
files_to_check="${package_path}"

echo "checking changes with 'git diff ${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT} -- ${files_to_check}'"
set +e
package_modified=$(git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- ${files_to_check} | wc -l)
set -e

if [[ "${package_modified}" -gt 0 || "$KOKORO_BUILD_ARTIFACTS_SUBDIR" == *"continuous"* ]]; then
    echo "------------------------------------------------------------"
    echo "Running doctest for: ${package_name}"
    echo "------------------------------------------------------------"
    
    export GOOGLE_CLOUD_PROJECT="bigframes-testing"
    export NOX_SESSION="cleanup doctest"
    
    cd "${package_path}"
    python3 -m nox -s "${NOX_SESSION}"
else
    echo "No changes in ${package_name} and not a continuous build, skipping."
fi
