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
ROUNDS="${ROUNDS:-2}"                        # Run benchmark 2 rounds by default
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
OUT_JSON="${OUT_JSON:-${HOME:-/tmp}/bench_result.json}"
UPLOAD_GCS_PREFIX="${UPLOAD_GCS_PREFIX:-}"

echo "========================================================================"
echo " GCS Read Microbenchmark Runner (gRPC BidiReadObject / REST)"
echo " Processes:       ${PROCESSES}"
echo " Coroutines/proc: ${COROS}"
echo " File Size:       ${FILE_SIZE_MIB} MiB"
echo " Chunk Size:      ${CHUNK_SIZE_KIB} KiB"
echo " Rounds:          ${ROUNDS}"
echo " Bucket Type:     ${BUCKET_TYPE}"
echo " Zonal Bucket:    gs://${ZONAL_BUCKET}"
echo " Regional Bucket: gs://${REGIONAL_BUCKET}"
echo "========================================================================"

# Ensure HOME is exported for gRPC / ALTS Application Default Credentials
export HOME="${HOME:-/root}"
export DEFAULT_RAPID_ZONAL_BUCKET="${ZONAL_BUCKET}"
export DEFAULT_STANDARD_BUCKET="${REGIONAL_BUCKET}"
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
    defaults = d.get('defaults')
    if isinstance(defaults, dict):
        defaults['DEFAULT_RAPID_ZONAL_BUCKET'] = '${ZONAL_BUCKET}'
        defaults['DEFAULT_STANDARD_BUCKET'] = '${REGIONAL_BUCKET}'
    common = d.get('common')
    if isinstance(common, dict):
        common['file_sizes_mib'] = [${FILE_SIZE_MIB}]
        common['chunk_sizes_kib'] = [${CHUNK_SIZE_KIB}]
        b_types = [b.strip() for b in '${BUCKET_TYPE}'.split(',') if b.strip()]
        common['bucket_types'] = b_types if b_types else ['zonal']
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
        target = 'files_names = _create_files(\n            params.num_files,\n            params.bucket_name,\n            params.bucket_type,\n            params.file_size_bytes,\n)'
        replacement = 'files_names = [f\"fio-go_storage_fio.0.{i}\" for i in range(params.num_files)]'
        if target not in s:
            raise ValueError('Exact _create_files call signature not found in conftest.py')
        s = s.replace(target, replacement)
        with open(path, 'w') as f:
            f.write(s)
except Exception as e:
    print(f'Warning patching conftest.py: {e}')
"

echo "--- 3. Executing pytest benchmark suite (${ROUNDS} rounds) ---"
rm -f "${OUT_JSON}" 2>/dev/null || true
python3 -m pytest --benchmark-json="${OUT_JSON}" \
  -rA \
  tests/perf/microbenchmarks/time_based/reads/test_reads.py

if [ -s "${OUT_JSON}" ]; then
  python3 -c "
import json, sys
with open('${OUT_JSON}') as f:
    d = json.load(f)
if not isinstance(d, dict):
    print('ERROR: Invalid JSON structure in benchmark result file.', file=sys.stderr)
    sys.exit(1)
benchmarks = d.get('benchmarks', [])
if not isinstance(benchmarks, list) or not benchmarks:
    print('No benchmarks found in result file.')
    sys.exit(0)
print('\n' + '='*85)
print('              GCS DIRECTPATH READ BENCHMARK PERFORMANCE RESULTS')
print('='*85)
header = f'| {\"Workload Pattern\":<36} | {\"Avg Throughput\":<17} | {\"Network Bandwidth\":<22} | {\"CPU Usage\":<9} |'
print(header)
print('|' + '-'*38 + '|' + '-'*19 + '|' + '-'*24 + '|' + '-'*11 + '|')
for b in benchmarks:
    if not isinstance(b, dict):
        continue
    name = b.get('name', '').replace('test_downloads_multi_proc_multi_coro[', '').replace(']', '')
    extra = b.get('extra_info', {})
    if not isinstance(extra, dict):
        extra = {}
    avg_mib = extra.get('avg_throughput_mib_s', 'N/A')
    net_mb = extra.get('net_throughput_mb_s')
    if net_mb:
        try:
            net_str = f'{float(net_mb):,.1f} MB/s ({float(net_mb)*0.008:.1f} Gbps)'
        except Exception:
            net_str = str(net_mb)
    else:
        net_str = 'N/A'
    cpu = extra.get('cpu_max_global', 'N/A')
    row = f'| {name:<36} | {str(avg_mib) + \" MiB/s\":<17} | {net_str:<22} | {str(cpu):<9} |'
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
