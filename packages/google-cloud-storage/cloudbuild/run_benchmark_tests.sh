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
ROUNDS="${ROUNDS:-1}"                        # Run benchmark 1 round by default
BUCKET_TYPE="${BUCKET_TYPE:-zonal}"          # "zonal" uses BidiReadObject gRPC DirectPath
TARGET_BUCKET="${DEFAULT_RAPID_ZONAL_BUCKET:-gcs-read-bench-zb-us-west4-a}"
OUT_JSON="${OUT_JSON:-${HOME:-/tmp}/bench_result.json}"
UPLOAD_GCS_PREFIX="${UPLOAD_GCS_PREFIX:-}"

echo "========================================================================"
echo " GCS Read Microbenchmark Runner (gRPC BidiReadObject / REST)"
echo " Processes:       ${PROCESSES}"
echo " Coroutines/proc: ${COROS}"
echo " File Size:       ${FILE_SIZE_MIB} MiB"
echo " Chunk Size:      ${CHUNK_SIZE_KIB} KiB"
echo " Rounds:          ${ROUNDS}"
echo " Bucket Type:     ${BUCKET_TYPE} (zonal = BidiReadObject gRPC DirectPath)"
echo " Target Bucket:   gs://${TARGET_BUCKET}"
echo "========================================================================"

# Ensure HOME is exported for gRPC / ALTS Application Default Credentials
export HOME="${HOME:-/root}"
export DEFAULT_RAPID_ZONAL_BUCKET="${TARGET_BUCKET}"
export DEFAULT_STANDARD_BUCKET="${TARGET_BUCKET}"
export USE_PRESEEDED_BENCHMARK_OBJECTS="1"

# Determine repository root
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
  pip install google-cloud-kms
fi

# Ensure latest source code is linked
pip install --no-deps -e .

CONFIG_PATH="tests/perf/microbenchmarks/time_based/reads/config.yaml"
if [ ! -f "${CONFIG_PATH}" ]; then
  echo "ERROR: Could not find ${CONFIG_PATH}. Please run from google-cloud-storage root."
  exit 1
fi

echo "--- 2. Updating ${CONFIG_PATH} parameters (rounds=${ROUNDS}) ---"
python3 -c "
import yaml
path = '${CONFIG_PATH}'
with open(path) as f:
    d = yaml.safe_load(f)
if isinstance(d, dict):
    common = d.get('common')
    if isinstance(common, dict):
        common['file_sizes_mib'] = [${FILE_SIZE_MIB}]
        common['chunk_sizes_kib'] = [${CHUNK_SIZE_KIB}]
        common['bucket_types'] = ['${BUCKET_TYPE}']
        common['rounds'] = int('${ROUNDS}')
    workloads = d.get('workload')
    if isinstance(workloads, list):
        for w in workloads:
            if isinstance(w, dict):
                w['processes'] = [${PROCESSES}]
                w['coros'] = [${COROS}]
with open(path, 'w') as f:
    yaml.dump(d, f)
"

# Patch config.py so 1-to-1 process-to-file indexing prevents 404 on multi-coroutine runs
sed -i 's/num_files = num_processes \* num_coros/num_files = num_processes/g' tests/perf/microbenchmarks/time_based/reads/config.py || true
sed -i 's/num_files = num_processes \* num_coros/num_files = num_processes/g' tests/perf/microbenchmarks/reads/config.py || true

# Patch conftest.py at runtime on VM to use pre-seeded test objects and bypass 480GB re-upload
python3 -c "
path = 'tests/perf/microbenchmarks/conftest.py'
try:
    with open(path) as f:
        s = f.read()
    if '_create_files(' in s:
        s = s.replace('files_names = _create_files(\n            params.num_files,\n            params.bucket_name,\n            params.bucket_type,\n            params.file_size_bytes,\n        )', 'files_names = [f\"fio-go_storage_fio.0.{i}\" for i in range(params.num_files)]')
        with open(path, 'w') as f:
            f.write(s)
except Exception as e:
    print(f'Warning patching conftest.py: {e}')
"

echo "--- 3. Pre-seeding & verifying ${PROCESSES} test objects (${FILE_SIZE_MIB} MiB each) in gs://${TARGET_BUCKET} ---"
SEED_SCRIPT="cloudbuild/seed_benchmark_objects.py"
if [ ! -f "${SEED_SCRIPT}" ]; then
  SEED_SCRIPT="${HOME}/seed_benchmark_objects.py"
fi
if [ ! -f "${SEED_SCRIPT}" ]; then
  SEED_SCRIPT="packages/google-cloud-storage/cloudbuild/seed_benchmark_objects.py"
fi

python3 "${SEED_SCRIPT}" \
  --bucket="${TARGET_BUCKET}" \
  --file-size-mib="${FILE_SIZE_MIB}" \
  --num-objects="${PROCESSES}" \
  --concurrency=16

echo "--- 4. Executing pytest benchmark suite (${ROUNDS} rounds) ---"
rm -f "${OUT_JSON}" 2>/dev/null || true
python3 -m pytest --benchmark-json="${OUT_JSON}" \
  -rA \
  tests/perf/microbenchmarks/time_based/reads/test_reads.py

if [ -s "${OUT_JSON}" ]; then
  python3 -c "
import json
with open('${OUT_JSON}') as f:
    d = json.load(f)
benchmarks = d.get('benchmarks', [])
print('\n' + '='*85)
print('              GCS DIRECTPATH READ BENCHMARK PERFORMANCE RESULTS')
print('='*85)
header = f'| {\"Workload Pattern\":<36} | {\"Avg Throughput\":<17} | {\"Network Bandwidth\":<22} | {\"CPU Usage\":<9} |'
print(header)
print('|' + '-'*38 + '|' + '-'*19 + '|' + '-'*24 + '|' + '-'*11 + '|')
for b in benchmarks:
    name = b.get('name', '').replace('test_downloads_multi_proc_multi_coro[', '').replace(']', '')
    extra = b.get('extra_info', {})
    avg_mib = extra.get('avg_throughput_mib_s', 'N/A')
    net_mb = extra.get('net_throughput_mb_s')
    if net_mb:
        net_str = f'{float(net_mb):,.1f} MB/s ({float(net_mb)*0.008:.1f} Gbps)'
    else:
        net_str = 'N/A'
    cpu = extra.get('cpu_max_global', 'N/A')
    row = f'| {name:<36} | {avg_mib + \" MiB/s\":<17} | {net_str:<22} | {str(cpu):<9} |'
    print(row)
print('='*85 + '\n')
"

  if [ -n "${UPLOAD_GCS_PREFIX}" ]; then
    GCS_DEST="${UPLOAD_GCS_PREFIX}/test_result_$(hostname)_$(date +%s).json"
    echo "Uploading JSON report to ${GCS_DEST}..."
    gcloud storage cp "${OUT_JSON}" "${GCS_DEST}"
  fi
fi

echo "--- Benchmark Run Complete ---"
