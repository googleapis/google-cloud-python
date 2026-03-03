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

export PROJECT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}")/..)

cd "$PROJECT_ROOT"

# This is needed in order for `git diff` to succeed
git config --global --add safe.directory $(realpath .)

RETVAL=0

pwd

run_package_test() {
  local package_name=$1
  local package_path="packages/${package_name}"
  
  # Declare local overrides to prevent bleeding into the next loop iteration
  local PROJECT_ID
  local GOOGLE_APPLICATION_CREDENTIALS
  local NOX_FILE
  local NOX_SESSION

  echo "------------------------------------------------------------"
  echo "Configuring environment for: ${package_name}"
  echo "------------------------------------------------------------"

  case "${package_name}" in
    "google-auth")
      PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/google-auth-project-id.json")
      GOOGLE_APPLICATION_CREDENTIALS="${KOKORO_GFILE_DIR}/google-auth-service-account.json"
      NOX_FILE="system_tests/noxfile.py"
      NOX_SESSION=""

      # Activate gcloud for this specific package
      gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
      gcloud config set project "$PROJECT_ID"

      # Decrypt secrets
      gcloud kms decrypt \
        --location=global --keyring=ci --key=kokoro-secrets \
        --ciphertext-file="${package_path}/system_tests/secrets.tar.enc" \
        --plaintext-file="${package_path}/system_tests/secrets.tar"
      # Extract files directly into the package directory.
      # --strip-components=2 removes 'system_tests/data/' from the archived paths.
      mkdir -p "${package_path}/system_tests/data"
      tar xvf "${package_path}/system_tests/secrets.tar" -C "${package_path}/system_tests/data/" --strip-components=2

      rm "${package_path}/system_tests/secrets.tar"
      ;;
    *)
      PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")
      GOOGLE_APPLICATION_CREDENTIALS="${KOKORO_GFILE_DIR}/service-account.json"
      NOX_FILE="noxfile.py"
      NOX_SESSION="system-3.12"

      # Activate gcloud for this specific package
      gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
      gcloud config set project "$PROJECT_ID"
      ;;
  esac

  # Export variables for the duration of this function's sub-processes
  export PROJECT_ID GOOGLE_APPLICATION_CREDENTIALS NOX_FILE NOX_SESSION

  # Run the actual test
  pushd "${package_path}" > /dev/null
  set +e
  "${system_test_script}"
  local res=$?
  set -e
  popd > /dev/null
  
  return $res
}

packages_with_system_tests=(
  "google-auth"
  "google-cloud-bigquery-storage"
  "google-cloud-bigtable"
  "google-cloud-datastore"
  "google-cloud-dns"
  "google-cloud-error-reporting"
  "google-cloud-firestore"
  "google-cloud-logging"
  "google-cloud-testutils"
)

# Join array elements with | for the pattern match
packages_with_system_tests_pattern=$(printf "|*%s*" "${packages_with_system_tests[@]}")
packages_with_system_tests_pattern="${packages_with_system_tests_pattern:1}" # Remove the leading pipe


# A file for running system tests
system_test_script="${PROJECT_ROOT}/.kokoro/system-single.sh"


# Run system tests for each package with directory `packages/*/tests/system` or directory `packages/*/system_tests`
for dir in `find 'packages' -type d -wholename 'packages/*/tests/system' -o -wholename 'packages/*/system_tests'`; do
  # Extract the package name and define the relative package path
  # 1. Remove the 'packages/' prefix from the start
  # 2. Remove everything after the first '/' remaining
  package_name=${dir#packages/}
  package_name=${package_name%%/*}
  package_path="packages/${package_name}"

  # Determine if we should skip based on git diff
  files_to_check="${package_path}/CHANGELOG.md"
  if [[ $package_name == @($pattern) ]]; then
    files_to_check="${package_path}"
  fi

  echo "checking changes with 'git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- ${files_to_check}'"
  set +e
  package_modified=$(git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- ${files_to_check} | wc -l)
  set -e

  if [[ "${package_modified}" -gt 0 ]]; then
      # Call the function - its internal exports won't affect the next loop
      run_package_test "$package_name" || RETVAL=$?
  else
      echo "No changes in ${package_name}, skipping."
  fi
done
exit ${RETVAL}
