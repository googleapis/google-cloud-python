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

  # Create a dedicated directory for this package's artifacts
  local artifact_dir="${KOKORO_ARTIFACTS_DIR}/${package_name}"
  mkdir -p "${artifact_dir}"

  # Define standard output paths for logs and XML results
  export XML_OUTPUT_FILE="${artifact_dir}/sponge_log.xml"
  local log_file="${artifact_dir}/sponge_log.log"

  # Isolate gcloud config for parallel execution
  export CLOUDSDK_CONFIG=$(mktemp -d)

  # Declare local overrides to prevent bleeding into the next loop iteration
  local PROJECT_ID
  local GOOGLE_APPLICATION_CREDENTIALS
  local NOX_FILE
  # Inherit NOX_SESSION from environment to allow configs (like prerelease.cfg) to pass it in
  local NOX_SESSION="${NOX_SESSION}"

  echo "------------------------------------------------------------"
  echo "Configuring environment for: ${package_name}"
  echo "Log file: ${log_file}"
  echo "XML results: ${XML_OUTPUT_FILE}"
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
  # *** CRITICAL: system-single.sh MUST use XML_OUTPUT_FILE to generate the JUnit XML ***
  "${system_test_script}" > "${log_file}" 2>&1
  local res=$?
  set -e
  popd > /dev/null

  # Clean up isolated gcloud config
  rm -rf "${CLOUDSDK_CONFIG}"

  return $res
}

# A file for running system tests
system_test_script="${PROJECT_ROOT}/.kokoro/system-single.sh"
# Ensure KOKORO_ARTIFACTS_DIR is set, fallback to a local directory
export KOKORO_ARTIFACTS_DIR="${KOKORO_ARTIFACTS_DIR:-${PROJECT_ROOT}/.artifacts}"

# Parallel execution settings
MAX_PARALLEL=4
running_pids=()
declare -A pid_to_pkg
declare -A pid_to_resfile

# Array to keep track of results for the final summary
results=()
handle_finished_job() {
  local pid=$1
  local pkg=${pid_to_pkg[$pid]}
  local resfile=${pid_to_resfile[$pid]}
  local pkg_log="${KOKORO_ARTIFACTS_DIR}/${pkg}/sponge_log.log"

  # wait $pid might fail if it was already reaped by wait -n, 
  # so we ignore its exit code and use the resfile.
  wait "$pid" 2>/dev/null || true

  local res=1
  if [ -s "$resfile" ]; then
    res=$(cat "$resfile")
    rm "$resfile"
  else
    # If the file is empty or missing, the subshell crashed early
    res=1
  fi

  echo "============================================================"
  echo "System tests for ${pkg} finished (Exit code: ${res})"
  echo "Artifacts in: ${KOKORO_ARTIFACTS_DIR}/${pkg}"
  echo "============================================================"

  if [ -f "${pkg_log}" ]; then
    echo "--- Start of Logs for ${pkg} ---"
    cat "${pkg_log}"
    echo "--- End of Logs for ${pkg} ---"
  else
    echo "Console Fallback Warning: Log file not found at ${pkg_log}"
  fi
  echo ""

  if [ -z "${res}" ] || [ "${res}" -ne 0 ]; then
    RETVAL=1
    results+=("${pkg}: FAILED")
  else
    results+=("${pkg}: PASSED")
  fi
}
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
  # We always check for changes in these specific versioning/config files
  files_to_check=(
    "${package_path}/CHANGELOG.md"
    "${package_path}/setup.py"
    "${package_path}/pyproject.toml"
    "${package_path}/**/gapic_version.py"
    "${package_path}/**/version.py"
  )

  # Hand-written (non-GAPIC_AUTO) packages or google-cloud-compute should check
  # the whole directory for changes.
  metadata="${package_path}/.repo-metadata.json"
  library_type="UNKNOWN"
  if [ -f "$metadata" ]; then
    library_type=$(sed -n 's/.*"library_type":[[:space:]]*"\([^"]*\)".*/\1/p' "$metadata")
    library_type="${library_type:-UNKNOWN}"
  fi

  # System tests always run in release PRs, regardless of library type.
  # Automated GAPIC libraries bypass system tests in non-release PRs because their generation is deterministic.
  # However, google-cloud-compute is included because its Discovery-based nature requires additional
  # verification.
  if [[ "${library_type}" != "GAPIC_AUTO" || "${package_name}" == "google-cloud-compute"* ]]; then
    files_to_check=("${package_path}")
  fi

  echo "checking changes with 'git diff ${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT} -- ${files_to_check[*]}'"
  set +e
  # Passing the array expanded as arguments to git diff
  package_modified=$(git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- "${files_to_check[@]}" | wc -l)
  set -e

  if [[ "${package_modified}" -gt 0 || "$KOKORO_BUILD_ARTIFACTS_SUBDIR" == *"continuous"* ]]; then
      # Wait if we have reached MAX_PARALLEL
      while [[ ${#running_pids[@]} -ge $MAX_PARALLEL ]]; do
        set +e
        wait -n
        set -e
        # Find which job finished
        new_pids=()
        for pid in "${running_pids[@]}"; do
          if kill -0 "$pid" 2>/dev/null; then
            new_pids+=("$pid")
          else
            handle_finished_job "$pid"
          fi
        done
        running_pids=("${new_pids[@]}")
      done

      # Start the next test in the background
      res_file=$(mktemp)
      (
        if run_package_test "$package_name"; then
          echo 0 > "$res_file"
        else
          res=$?
          echo $res > "$res_file"
        fi
      ) &
      pid=$!
      running_pids+=($pid)
      pid_to_pkg[$pid]=$package_name
      pid_to_resfile[$pid]=$res_file
      echo "Started system tests for ${package_name} (PID: ${pid})"
  else
      echo "No changes in ${package_name} and not a continuous build, skipping."
  fi
done

# Wait for all remaining jobs
for pid in "${running_pids[@]}"; do
  handle_finished_job "$pid"
done

echo "------------------------------------------------------------"
echo "System Test Summary"
echo "------------------------------------------------------------"
for res in "${results[@]}"; do
  echo "$res"
done
echo "------------------------------------------------------------"

exit ${RETVAL}

