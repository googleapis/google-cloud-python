#!/bin/bash
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script requires the following environment variables to be set:
# `BUILD_TYPE` should be one of ["presubmit", "continuous"]
# `TEST_TYPE` should be one of ["docs", "docfx", "prerelease", "unit"]
# or match the name of the nox session that you want to run.
# `PY_VERSION` should be one of ["3.10", "3.11", "3.12"]

# `TEST_TYPE` and `PY_VERSION` are required by the script `ci/run_single_test.sh`

# This script will determine which directories have changed
# under the `packages` folder. For `BUILD_TYPE=="presubmit"`,
# we'll compare against the `packages` folder in HEAD,
# whereas for `BUILD_TYPE=="continuous"` we'll compare changes
# with HEAD~1. For all directories that have changed files, we will
# run the script located at `${PROJECT_ROOT}/ci/run_single_test.sh`.

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to non-zero if any command fails,
# or zero if all commands in the pipeline exit successfully.
set -eo pipefail

export PROJECT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}")/..)
TARGET_BRANCH="${TARGET_BRANCH:-main}"

# Redirect git clones for core dependencies to the local repository.
# This serves two purposes:
# 1. Performance: Avoids repeated 100MB+ downloads of the monorepo for each dependency.
# 2. Correctness: Ensures that changes in core packages (like google-api-core) are
#    tested against downstream packages in the same Pull Request.
git config --global url."${PROJECT_ROOT}".insteadOf "https://github.com/googleapis/google-cloud-python"
git config --global url."${PROJECT_ROOT}".insteadOf "https://github.com/googleapis/google-cloud-python.git"

# A script file for running the test in a sub project.
test_script="${PROJECT_ROOT}/ci/run_single_test.sh"

# Global exit code tracker
RETVAL=0

# Shared test execution logic
run_test_in_dir() {
    local d=$1
    echo "running test in ${d}"
    pushd ${d} > /dev/null
    
    # Temporarily allow failure.
    set +e
    
    # Ensure unique coverage file per package to avoid DataError
    # when combining statement and branch coverage.
    # Strip trailing slash from directory name for the filename.
    local pkg_name_clean=$(echo ${d} | sed 's|/$||' | sed 's|/|_|g')
    export COVERAGE_FILE="${PROJECT_ROOT}/.coverage.${PY_VERSION}.${pkg_name_clean}"
    
    ${test_script}
    local ret=$?
    set -e
    
    if [ ${ret} -ne 0 ]; then
        RETVAL=${ret}
    fi
    popd > /dev/null
}

if [ -n "${PACKAGE_LIST}" ]; then
    echo "Using provided PACKAGE_LIST"
    for d in ${PACKAGE_LIST}; do
        run_test_in_dir "${d}"
    done
    exit ${RETVAL}
fi

if [[ ${BUILD_TYPE} == "presubmit" ]]; then
    # For presubmit build, we want to know the difference from the
    # common commit in the target branch.
    GIT_DIFF_ARG="origin/$TARGET_BRANCH..."

    # Then fetch enough history for finding the common commit.
    git fetch origin "$TARGET_BRANCH" --deepen=200 || true

elif [[ ${BUILD_TYPE} == "continuous" ]]; then
    # For continuous build, we want to know the difference in the last
    # commit. This assumes we use squash commit when merging PRs.
    GIT_DIFF_ARG="HEAD~.."

    # Then fetch one last commit for getting the diff.
    git fetch origin "$TARGET_BRANCH" --deepen=1 || true

else
    # Run everything.
    GIT_DIFF_ARG=""
fi

# Sharding logic (fallback for manual runs)
subdirs=(
    packages
)
TOTAL_SHARDS="${TOTAL_SHARDS:-1}"
SHARD_INDEX="${SHARD_INDEX:-1}"
count=0

for subdir in ${subdirs[@]}; do
    # Sort the directories to ensure consistent sharding across jobs
    for d in `ls -d ${subdir}/*/ | sort`; do
        # Sharding logic: only process directories that belong to this shard
        if (( count % TOTAL_SHARDS != SHARD_INDEX - 1 )); then
            ((++count))
            continue
        fi
        ((++count))

        should_test=false
        if [ -n "${GIT_DIFF_ARG}" ]; then
            echo "checking changes with 'git diff --quiet ${GIT_DIFF_ARG} ${d}'"
            set +e
            git diff --quiet ${GIT_DIFF_ARG} ${d}
            changed=$?
            set -e
            if [[ "${changed}" -eq 0 ]]; then
                echo "no change detected in ${d}, skipping"
            else
                echo "change detected in ${d}"
                should_test=true
            fi
        else
            # If GIT_DIFF_ARG is empty, run all the tests.
            should_test=true
        fi
        if [ "${should_test}" = true ]; then
            run_test_in_dir "${d}"
        fi
    done
done

exit ${RETVAL}
