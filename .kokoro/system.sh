#!/bin/bash
# Copyright 2020 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License"); ...
set -eo pipefail

export PYTHONUNBUFFERED=1
export FIRESTORE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/firebase-credentials.json
export PROJECT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}")/..)

cd "$PROJECT_ROOT"
git config --global --add safe.directory $(realpath .)

# HOISTED: Install uv exactly once globally before we fan out
echo "Installing uv globally..."
python3 -m pip install uv

# --- NEW: Set maximum concurrent jobs ---
MAX_CONCURRENT=4
# --------------------------------------

RETVAL=0
pwd

run_package_test() {
  local package_name=$1
  local package_path="packages/${package_name}"
  
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

  export PROJECT_ID GOOGLE_APPLICATION_CREDENTIALS NOX_FILE NOX_SESSION
  export GOOGLE_CLOUD_PROJECT="${PROJECT_ID}"
  
  # NEW: Subshell-isolated GCP auth. Never modify the global gcloud config!
  export CLOUDSDK_CORE_PROJECT="${PROJECT_ID}"
  export CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE="${GOOGLE_APPLICATION_CREDENTIALS}"

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

system_test_script="${PROJECT_ROOT}/.kokoro/system-single.sh"
packages_with_system_tests_pattern=$(printf "|*%s*" "${packages_with_system_tests[@]}")
packages_with_system_tests_pattern="${packages_with_system_tests_pattern:1}"

declare -A pids

for path in `find 'packages' \
  \( -type d -wholename 'packages/*/tests/system' \) -o \
  \( -type d -wholename 'packages/*/system_tests' \) -o \
  \( -type f -wholename 'packages/*/tests/system.py' \)`; do

  package_name=${path#packages/}
  package_name=${package_name%%/*}
  package_path="packages/${package_name}"

  files_to_check="${package_path}/CHANGELOG.md"
  if [[ $package_name == @($packages_with_system_tests_pattern) ]]; then
    files_to_check="${package_path}"
  fi

  echo "checking changes with 'git diff ${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT} -- ${files_to_check}'"
  set +e
  package_modified=$(git diff "${KOKORO_GITHUB_PULL_REQUEST_TARGET_BRANCH}...${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" -- ${files_to_check} | wc -l)
  set -e

  if [[ "${package_modified}" -gt 0 || "$KOKORO_BUILD_ARTIFACTS_SUBDIR" == *"continuous"* ]]; then
      
      # --- NEW: Bounded Concurrency Throttle ---
      # Check how many background jobs are currently running.
      # If we hit our limit, pause for 5 seconds and check again.
      while (( $(jobs -pr | wc -l) >= MAX_CONCURRENT )); do
          sleep 5
      done
      # -----------------------------------------

      echo ">>> Dispatching ${package_name} in the background <<<"
      
      # Execute inside an isolated subshell ( ) to prevent GCP credential collisions
      (
        run_package_test "$package_name"
      ) &
      
      # Capture the PID of the subshell
      pids["$package_name"]=$!
  else
      echo "No changes in ${package_name} and not a continuous build, skipping."
  fi
done

echo "============================================================"
echo "All affected packages dispatched. Waiting for completion..."
echo "============================================================"

for package in "${!pids[@]}"; do
  wait ${pids[$package]} || {
    echo "============================================================"
    echo "ERROR: System tests failed for $package"
    echo "============================================================"
    RETVAL=1
  }
done

echo "All concurrent tests completed."
exit ${RETVAL}