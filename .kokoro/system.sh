#!/bin/bash
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to non-zero if any command fails,
# or zero if all commands in the pipeline exit successfully.
set -eo pipefail

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Setup service account credentials.
export GOOGLE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/service-account.json

# Setup project id.
export PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")

# If this is a continuous build, send the test log to the FlakyBot.
# See https://github.com/googleapis/repo-automation-bots/tree/main/packages/flakybot.
if [[ $KOKORO_BUILD_ARTIFACTS_SUBDIR = *"continuous"* ]]; then
  cleanup() {
    chmod +x $KOKORO_GFILE_DIR/linux_amd64/flakybot
    $KOKORO_GFILE_DIR/linux_amd64/flakybot
  }
  trap cleanup EXIT HUP
fi

RETVAL=0

export PROJECT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}")/..)

cd "$PROJECT_ROOT"

pwd

# A file for running system tests
system_test_script="${PROJECT_ROOT}/.kokoro/system-single.sh"

subdirs=(
    ${PROJECT_ROOT}/packages
)
for subdir in ${subdirs[@]}; do
  # Run system tests for each package with a directory packages/*/tests/system
  for d in `find 'packages' -type d -wholename 'packages/*/tests/system'`; do
      # Get the path to the package by removing the suffix /tests/system
      package=$(echo $d | cut -f -2 -d '/')
      echo "Running system tests in package in ${package}"
      pushd ${package}
      # Temporarily allow failure.
      set +e
      ${system_test_script}
      ret=$?
      set -e
      if [ ${ret} -ne 0 ]; then
          RETVAL=${ret}
      fi
      popd
    done
done

exit ${RETVAL}
