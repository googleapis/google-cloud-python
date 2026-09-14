#!/bin/bash
# ==============================================================================
# Automated Google Cloud Storage Read Microbenchmark Runner
# Intended for GitHub CI/CD & GCE High-Bandwidth Tier-1 VMs (C4/N2/C3 series)
# Location: packages/google-cloud-storage/cloudbuild/run_benchmark_tests.sh
# ==============================================================================

set -eo pipefail

# Configurable defaults
PROCESSES="${PROCESSES:-48}"
COROS="${COROS:-1}"
FILE_SIZE_MIB="${FILE_SIZE_MIB:-10240}"      # 10 GiB files by default
CHUNK_SIZE_KIB="${CHUNK_SIZE_KIB:-102400}"   # ~100 MiB read chunks by default
ROUNDS="${ROUNDS:-3}"                        # Run benchmark 3 rounds by default
BUCKET_TYPE="${BUCKET_TYPE:-zonal}"          # "zonal" uses BidiReadObject gRPC DirectPath, "regional" uses REST/gRPC standard
ZONAL_BUCKET="${ZONAL_BUCKET:-${DEFAULT_RAPID_ZONAL_BUCKET:-gcs-read-bench-zb-us-west4-a}}"
REGIONAL_BUCKET="${REGIONAL_BUCKET:-${DEFAULT_STANDARD_BUCKET:-gcs-read-bench-rb-us-west4}}"
if [ -n "${TARGET_BUCKET:-}" ]; then
  if [ "${BUCKET_TYPE}" = "regional" ]; then
    REGIONAL_BUCKET="${TARGET_BUCKET}"
  else
    ZONAL_BUCKET="${TARGET_BUCKET}"
  fi
fi
OUTPUT_JSON_PATH="${OUTPUT_JSON_PATH:-${OUT_JSON:-${HOME:-/tmp}/bench_result.json}}"
UPLOAD_GCS_PREFIX="${UPLOAD_GCS_PREFIX:-}"

echo "========================================================================"
echo " GCS Read Microbenchmark Runner (gRPC BidiReadObject / REST)"
echo " Processes:        ${PROCESSES}"
echo " Coroutines/proc:  ${COROS}"
echo " File Size:        ${FILE_SIZE_MIB} MiB"
echo " Chunk Size:       ${CHUNK_SIZE_KIB} KiB"
echo " Rounds:           ${ROUNDS}"
echo " Bucket Type:      ${BUCKET_TYPE}"
echo " Zonal Bucket:     gs://${ZONAL_BUCKET}"
echo " Regional Bucket:  gs://${REGIONAL_BUCKET}"
echo " Output JSON Path: ${OUTPUT_JSON_PATH}"
echo " Upload GCS Path:  ${UPLOAD_GCS_PREFIX:-None}"
echo "========================================================================"

# Ensure HOME is exported for gRPC / ALTS Application Default Credentials
export HOME="${HOME:-/root}"
export DEFAULT_RAPID_ZONAL_BUCKET="${ZONAL_BUCKET}"
export DEFAULT_STANDARD_BUCKET="${REGIONAL_BUCKET}"
export PROCESSES="${PROCESSES}"
export COROS="${COROS}"
export FILE_SIZE_MIB="${FILE_SIZE_MIB}"
export CHUNK_SIZE_KIB="${CHUNK_SIZE_KIB}"
export ROUNDS="${ROUNDS}"
export BUCKET_TYPE="${BUCKET_TYPE}"
export USE_PRESEEDED_BENCHMARK_OBJECTS="1"

# Determine script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "${REPO_ROOT}/packages/google-cloud-storage" 2>/dev/null || cd "$(pwd)"

echo "--- 1. Setting up Python environment ---"
# Ensure python3-pip and python3-venv are present on the VM
if ! command -v pip3 &>/dev/null || ! python3 -c "import venv" 2>/dev/null; then
  echo "Installing python3-pip and python3-venv on VM..."
  sudo apt-get update && sudo apt-get install -y python3-pip python3-venv
fi

# Ensure persistent virtual environment exists and is activated
BENCH_VENV="${HOME}/bench_env"
if [ ! -d "${BENCH_VENV}" ]; then
  echo "Creating virtual environment at ${BENCH_VENV}..."
  python3 -m venv "${BENCH_VENV}"
fi
source "${BENCH_VENV}/bin/activate"

# Check and install all dependencies into virtual environment
if ! python3 -c "import pytest, psutil, yaml, google.cloud.storage" 2>/dev/null; then
  echo "Installing dependencies into virtual environment..."
  pip install --upgrade pip
  pip install -e ".[grpc,testing]"
fi

echo "--- 2. Executing pytest benchmark suite (${ROUNDS} rounds) ---"
rm -f "${OUTPUT_JSON_PATH}" 2>/dev/null || true
python3 -m pytest --benchmark-json="${OUTPUT_JSON_PATH}" \
  -rA \
  tests/perf/microbenchmarks/time_based/reads/test_reads.py

if [ -s "${OUTPUT_JSON_PATH}" ]; then
  DISPLAY_SCRIPT="${SCRIPT_DIR}/display_benchmark_results.py"
  if [ ! -f "${DISPLAY_SCRIPT}" ]; then
    DISPLAY_SCRIPT="cloudbuild/display_benchmark_results.py"
  fi
  python3 "${DISPLAY_SCRIPT}" "${OUTPUT_JSON_PATH}"

  if [ -n "${UPLOAD_GCS_PREFIX}" ]; then
    GCS_DEST="${UPLOAD_GCS_PREFIX}/test_result_$(hostname)_$(date +%s).json"
    echo "Uploading JSON report to ${GCS_DEST}..."
    gcloud storage cp "${OUTPUT_JSON_PATH}" "${GCS_DEST}"
  fi
fi

echo "--- Benchmark Run Complete ---"
