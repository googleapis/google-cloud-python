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

# Setup firestore account credentials
export FIRESTORE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/firebase-credentials.json

# Setup service account credentials.
export GOOGLE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/service-account.json

# Setup project id.
export PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")

RETVAL=0

export PROJECT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}")/..)

cd "$PROJECT_ROOT"

pwd

# A file for running system tests
system_test_script="${PROJECT_ROOT}/.kokoro/system-single.sh"

# This is needed in order for `git diff` to succeed
git config --global --add safe.directory $(realpath .)

# Run system tests for each package with directory packages/*/tests/system
for dir in `find 'packages' -type d -wholename 'packages/*/tests/system'`; do
  # Get the path to the package by removing the suffix /tests/system
  package=$(echo $dir | cut -f -2 -d '/')

  # Run system tests on every change to these libraries
  if [[ $package = @(*google-cloud-bigquery-storage*|*google-cloud-dns*|*google-cloud-testutils*) ]]; then
    files_to_check=${package}
  else
    files_to_check=${package}/CHANGELOG.md
  fi

  echo "checking changes with 'git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- ${files_to_check}'"
  set +e
  package_modified=$(git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- ${files_to_check} | wc -l)
  set -e
  if [[ "${package_modified}" -eq 0 ]]; then
      echo "no change detected in ${files_to_check}, skipping"
  else
      echo "change detected in ${files_to_check}"
      echo "Running system tests for ${package}"
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
  fi
done
exit ${RETVAL}
