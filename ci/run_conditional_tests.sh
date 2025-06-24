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
# `PY_VERSION` should be one of ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]

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

# A script file for running the test in a sub project.
test_script="${PROJECT_ROOT}/ci/run_single_test.sh"

if [ ${BUILD_TYPE} == "presubmit" ]; then
    # For presubmit build, we want to know the difference from the
    # common commit in origin/main.
    GIT_DIFF_ARG="origin/main..."

    # Then fetch enough history for finding the common commit.
    git fetch origin main --deepen=200

elif [ ${BUILD_TYPE} == "continuous" ]; then
    # For continuous build, we want to know the difference in the last
    # commit. This assumes we use squash commit when merging PRs.
    GIT_DIFF_ARG="HEAD~.."

    # Then fetch one last commit for getting the diff.
    git fetch origin main --deepen=1

else
    # Run everything.
    GIT_DIFF_ARG=""
fi

# Then detect changes in the test scripts.

set +e
git diff --quiet ${GIT_DIFF_ARG} ci
changed=$?
set -e

# Now we have a fixed list, but we can change it to autodetect if
# necessary.

subdirs=(
    packages
)

RETVAL=0

for subdir in ${subdirs[@]}; do
    for d in `ls -d ${subdir}/*/`; do
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
            echo "running test in ${d}"
            pushd ${d}
            # Temporarily allow failure.
            set +e
            ${test_script}
            ret=$?
            set -e
            if [ ${ret} -ne 0 ]; then
                RETVAL=${ret}
            fi
            popd
        fi
    done
done

exit ${RETVAL}
