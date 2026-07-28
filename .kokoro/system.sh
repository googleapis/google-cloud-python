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
      # Note: system.sh is also reused for monorepo-wide continuous unit test jobs
      # like `core_deps_from_source` and `prerelease_deps`. For google-auth, we only
      # want to override NOX_FILE to system_tests/noxfile.py when running actual system tests.
      if [[ -z "${NOX_SESSION}" || "${NOX_SESSION}" == "system-"* ]]; then
        NOX_FILE="system_tests/noxfile.py"
        NOX_SESSION=""
      else
        NOX_FILE="noxfile.py"
      fi
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

  # Isolate PIP cache to prevent concurrent pip file lock deadlocks
  export PIP_CACHE_DIR="/tmpfs/.pip_cache_$(basename ${package_name})"
  mkdir -p "$PIP_CACHE_DIR"

  # Isolate gcloud state to prevent SQLite lock deadlocks and project race conditions
  export CLOUDSDK_CONFIG="/tmpfs/.gcloud_config_$(basename ${package_name})"
  mkdir -p "$CLOUDSDK_CONFIG"
  
  # Isolate boto config (used by storage/bigquery) to prevent lock contention
  export BOTO_CONFIG="/tmpfs/.boto_$(basename ${package_name})"
  touch "$BOTO_CONFIG"

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

# A file for running system tests
system_test_script="${PROJECT_ROOT}/.kokoro/system-single.sh"

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
      PACKAGES_TO_TEST="${PACKAGES_TO_TEST} ${package_name}"
  else
      echo "No changes in ${package_name} and not a continuous build, skipping."
  fi
done

if [ -n "$PACKAGES_TO_TEST" ]; then
  export -f run_package_test
  export system_test_script PROJECT_ROOT KOKORO_GFILE_DIR

  # 1. DYNAMIC ROUTING: Automatically detect which packages are CPU hogs by checking if they install pytest-xdist or hardcode workers
  LIGHT_TO_TEST=""
  HEAVY_TO_TEST=""
  for pkg in $PACKAGES_TO_TEST; do
    if grep -qE "pytest-xdist|-n=auto|-n=[0-9]+" "packages/$pkg/noxfile.py" "packages/$pkg/setup.py" 2>/dev/null; then
      HEAVY_TO_TEST="$HEAVY_TO_TEST $pkg"
    else
      LIGHT_TO_TEST="$LIGHT_TO_TEST $pkg"
    fi
  done

  # 2. PARALLEL LANE (Live Streaming): Run light packages with a parallel job queue. 
  # We prefix every line with the package name so output streams LIVE and remains readable.
  if [ -n "$LIGHT_TO_TEST" ]; then
    echo "============================================================"
    echo "Running Lightweight Packages in Parallel (4 workers max)"
    echo "============================================================"
    for pkg in $LIGHT_TO_TEST; do
      (
        timeout 15m bash -c "run_package_test \"$pkg\" < /dev/null" 2>&1 | awk -v prefix="[$pkg]" '{print prefix, $0}'
        if [ ${PIPESTATUS[0]} -ne 0 ]; then touch ".failed_$pkg"; fi
      ) &
      # Limit parallel background jobs to 4
      while [ $(jobs -r | wc -l) -ge 4 ]; do sleep 1; done
    done
    wait # Wait for all parallel jobs to finish
  fi

  # 3. SEQUENTIAL VIP LANE: Run heavy packages one-by-one so they have 100% of the VM resources.
  if [ -n "$HEAVY_TO_TEST" ]; then
    echo "============================================================"
    echo "Running CPU-Intensive Packages Sequentially"
    echo "============================================================"
    for pkg in $HEAVY_TO_TEST; do
      if [ -n "$pkg" ]; then
        echo "[$pkg] Starting sequential execution..."
        timeout 25m bash -c "run_package_test \"$pkg\" < /dev/null" 2>&1 | awk -v prefix="[$pkg]" '{print prefix, $0}'
        if [ ${PIPESTATUS[0]} -ne 0 ]; then touch ".failed_$pkg"; fi
      fi
    done
  fi

  # 4. FAIL STATE EVALUATION
  for failed_marker in .failed_*; do
    if [ -f "$failed_marker" ]; then
      failed_pkg="${failed_marker#.failed_}"
      echo "--- FAILED: $failed_pkg ---"
      RETVAL=1
    fi
  done
fi

exit ${RETVAL}
