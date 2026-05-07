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
  # Inherit NOX_SESSION from environment to allow configs (like prerelease.cfg) to pass it in
  local NOX_SESSION="${NOX_SESSION}"

  echo "------------------------------------------------------------"
  echo "Configuring environment for: ${package_name}"
  echo "------------------------------------------------------------"

  case "${package_name}" in
    "google-auth")
      # Copy files needed for google-auth system tests
      mkdir -p "${package_path}/system_tests/data"
      cp "${KOKORO_GFILE_DIR}/google-auth-service-account.json" "${package_path}/system_tests/data/service_account.json"
      cp "${KOKORO_GFILE_DIR}/google-auth-authorized-user.json" "${package_path}/system_tests/data/authorized_user.json"
      cp "${KOKORO_GFILE_DIR}/google-auth-impersonated-service-account.json" "${package_path}/system_tests/data/impersonated_service_account.json"

      PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/google-auth-project-id.json")
      GOOGLE_APPLICATION_CREDENTIALS="${KOKORO_GFILE_DIR}/google-auth-service-account.json"
      NOX_FILE="system_tests/noxfile.py"
      NOX_SESSION=""
      ;;
    *)
      PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")
      GOOGLE_APPLICATION_CREDENTIALS="${KOKORO_GFILE_DIR}/service-account.json"
      NOX_FILE="noxfile.py"
      # Use inherited NOX_SESSION if set, otherwise fallback to system-3.12
      NOX_SESSION="${NOX_SESSION:-system-3.12}"
      ;;
  esac

  # Export variables for the duration of this function's sub-processes
  export PROJECT_ID GOOGLE_APPLICATION_CREDENTIALS NOX_FILE NOX_SESSION
  export GOOGLE_CLOUD_PROJECT="${PROJECT_ID}"

  gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
  gcloud config set project "$PROJECT_ID"

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
  "bigframes"
  "google-auth"
  "google-cloud-bigquery-storage"
  "google-cloud-bigtable"
  "google-cloud-compute"
  "google-cloud-compute-v1beta"
  "google-cloud-datastore"
  "google-cloud-dns"
  "google-cloud-error-reporting"
  "google-cloud-firestore"
  "google-cloud-logging"
  "google-cloud-ndb"
  "google-cloud-pubsub"
  "google-cloud-spanner"
  "google-cloud-storage"
  "google-cloud-testutils"
  "pandas-gbq"
  "sqlalchemy-bigquery"
  "sqlalchemy-spanner"
)

# A file for running system tests
system_test_script="${PROJECT_ROOT}/.kokoro/system-single.sh"

# Join array elements with | for the pattern match
packages_with_system_tests_pattern=$(printf "|*%s*" "${packages_with_system_tests[@]}")
packages_with_system_tests_pattern="${packages_with_system_tests_pattern:1}" # Remove the leading pipe

# Run system tests for each package with directory packages/*/tests/system
for path in `find 'packages' \
  \( -type d -wholename 'packages/*/tests/system' \) -o \
  \( -type d -wholename 'packages/*/system_tests' \) -o \
  \( -type f -wholename 'packages/*/tests/system.py' \)`; do

  # Extract the package name and define the relative package path
  # 1. Remove the 'packages/' prefix
  # 2. Remove everything after the first '/'
  package_name=${path#packages/}
  package_name=${package_name%%/*}
  package_path="packages/${package_name}"

  # Determine if we should skip based on git diff
  files_to_check="${package_path}/CHANGELOG.md"
  if [[ $package_name == @($packages_with_system_tests_pattern) ]]; then
    files_to_check="${package_path}"
  fi

  echo "checking changes with 'git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- ${files_to_check}'"
  set +e
  package_modified=$(git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- ${files_to_check} | wc -l)
  set -e

  if [[ "${package_modified}" -gt 0 || "$KOKORO_BUILD_ARTIFACTS_SUBDIR" == *"continuous"* ]]; then
      # Call the function - its internal exports won't affect the next loop
      run_package_test "$package_name" || RETVAL=$?
  else
      echo "No changes in ${package_name} and not a continuous build, skipping."
  fi
done
exit ${RETVAL}
