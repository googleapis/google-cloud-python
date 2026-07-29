#!/bin/bash
set -eo pipefail

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Assume we are running from the repo root or we need to find it.
# If this script is in packages/bigframes/scripts/run_doctest.sh,
# then repo root is 3 levels up.
export PROJECT_ROOT=$(realpath "$(dirname "${BASH_SOURCE[0]}")/../../..")
cd "$PROJECT_ROOT"

git config --global --add safe.directory "$(realpath .)"

package_name="bigframes"
package_path="packages/${package_name}"
files_to_check="${package_path}"

# Use the IF block to handle the case where KOKORO vars are missing
# (e.g. local testing)
if [[ -n "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}" && -n "${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" ]]; then
    echo "checking changes with 'git diff ${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT} -- ${files_to_check}'"

    package_modified=$(git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- "${files_to_check}" | wc -l)
else
    # If not a PR (like a local run or a different CI trigger), 
    # we treat it as 0 so it falls through to the "continuous" check.
    package_modified=0
fi

# Check if modified OR if it's a continuous build
if [[ "${package_modified}" -gt 0 || "$KOKORO_BUILD_ARTIFACTS_SUBDIR" == *"continuous"* ]]; then
    echo "------------------------------------------------------------"
    echo "Running doctest for: ${package_name}"
    echo "------------------------------------------------------------"
    
    # Ensure credentials are set for system tests in Kokoro
    if [[ -z "${GOOGLE_APPLICATION_CREDENTIALS}" && -f "${KOKORO_GFILE_DIR}/service-account.json" ]]; then
        export GOOGLE_APPLICATION_CREDENTIALS="${KOKORO_GFILE_DIR}/service-account.json"
    fi

    export GOOGLE_CLOUD_PROJECT="bigframes-testing"
    NOX_SESSION=("cleanup" "doctest")

    cd "${package_path}"
    python3 -m nox -s "${NOX_SESSION[@]}"
else
    echo "No changes in ${package_name} and not a continuous build, skipping."
fi