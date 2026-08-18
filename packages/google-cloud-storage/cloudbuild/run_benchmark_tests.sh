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
BUCKET_TYPE="${BUCKET_TYPE:-zonal}"          # "zonal" uses BidiReadObject gRPC DirectPath
TARGET_BUCKET="${DEFAULT_RAPID_ZONAL_BUCKET:-shradhakatyal-read-bench-zb}"
OUT_JSON="${OUT_JSON:-/tmp/bench_result.json}"
UPLOAD_GCS_PREFIX="${UPLOAD_GCS_PREFIX:-}"

echo "========================================================================"
echo " GCS Read Microbenchmark Runner (gRPC BidiReadObject / REST)"
echo " Processes:       ${PROCESSES}"
echo " Coroutines/proc: ${COROS}"
echo " File Size:       ${FILE_SIZE_MIB} MiB"
echo " Chunk Size:      ${CHUNK_SIZE_KIB} KiB"
echo " Bucket Type:     ${BUCKET_TYPE} (zonal = BidiReadObject gRPC DirectPath)"
echo " Target Bucket:   gs://${TARGET_BUCKET}"
echo "========================================================================"

# Ensure HOME is exported for gRPC / ALTS Application Default Credentials
export HOME="${HOME:-/root}"
export DEFAULT_RAPID_ZONAL_BUCKET="${TARGET_BUCKET}"
export DEFAULT_STANDARD_BUCKET="${TARGET_BUCKET}"

# Determine repository root
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "${REPO_ROOT}/packages/google-cloud-storage" 2>/dev/null || cd "$(pwd)"

echo "--- 1. Checking Python dependencies ---"
if ! python3 -c "import pytest, psutil, yaml" 2>/dev/null; then
  echo "Installing test dependencies..."
  pip install --upgrade pip
  pip install -e .
  pip install pytest pytest-benchmark psutil pyyaml google-cloud-testutils google-cloud-kms
fi

CONFIG_PATH="tests/perf/microbenchmarks/time_based/reads/config.yaml"
if [ ! -f "${CONFIG_PATH}" ]; then
  echo "ERROR: Could not find ${CONFIG_PATH}. Please run from google-cloud-storage root."
  exit 1
fi

echo "--- 2. Updating ${CONFIG_PATH} parameters ---"
python3 -c "
import yaml
path = '${CONFIG_PATH}'
with open(path) as f:
    d = yaml.safe_load(f)
d['common']['file_sizes_mib'] = [${FILE_SIZE_MIB}]
d['common']['chunk_sizes_kib'] = [${CHUNK_SIZE_KIB}]
d['common']['bucket_types'] = ['${BUCKET_TYPE}']
for w in d['workload']:
    w['processes'] = [${PROCESSES}]
    w['coros'] = [${COROS}]
with open(path, 'w') as f:
    yaml.dump(d, f)
"

# Patch config.py so 1-to-1 process-to-file indexing prevents 404 on multi-coroutine runs
sed -i 's/num_files = num_processes \* num_coros/num_files = num_processes/g' tests/perf/microbenchmarks/time_based/reads/config.py || true
sed -i 's/num_files = num_processes \* num_coros/num_files = num_processes/g' tests/perf/microbenchmarks/reads/config.py || true

echo "--- 3. Pre-seeding & verifying ${PROCESSES} test objects (${FILE_SIZE_MIB} MiB each) in gs://${TARGET_BUCKET} ---"
python3 -c "
import multiprocessing, os, time
from google.cloud import storage

bucket_name = '${TARGET_BUCKET}'
client = storage.Client()
bucket = client.bucket(bucket_name)

local_file = '/tmp/benchmark_test_payload'
expected_size = ${FILE_SIZE_MIB} * 1024 * 1024

def ensure_object(idx):
    obj_name = f'fio-go_storage_fio.0.{idx}'
    blob = bucket.get_blob(obj_name)
    if not blob or blob.size != expected_size:
        if not os.path.exists(local_file):
            print(f'Generating {expected_size} bytes payload locally...')
            os.system(f'dd if=/dev/urandom of={local_file} bs=1M count=${FILE_SIZE_MIB} status=none')
        t0 = time.time()
        print(f'Uploading {obj_name} ({FILE_SIZE_MIB} MiB)...')
        blob_new = bucket.blob(obj_name)
        blob_new.upload_from_filename(local_file)
        print(f'Uploaded {obj_name} in {time.time()-t0:.1f}s')

print(f'Verifying {${PROCESSES}} objects in bucket {bucket_name}...')
with multiprocessing.Pool(min(16, ${PROCESSES})) as pool:
    pool.map(ensure_object, range(${PROCESSES}))
"

echo "--- 4. Executing pytest benchmark suite ---"
pytest --benchmark-json="${OUT_JSON}" \
  -vv -s \
  --log-format='%(asctime)s %(levelname)s %(message)s' --log-date-format='%H:%M:%S' \
  tests/perf/microbenchmarks/time_based/reads/test_reads.py || true

if [ -s "${OUT_JSON}" ]; then
  echo "========================================================================"
  echo " BENCHMARK STATS SUMMARY"
  echo "========================================================================"
  grep -E '"name":|"avg_throughput_mib_s":|"net_throughput_mb_s":|"cpu_max_global":' "${OUT_JSON}" -B 1 -A 2 || true

  if [ -n "${UPLOAD_GCS_PREFIX}" ]; then
    GCS_DEST="${UPLOAD_GCS_PREFIX}/test_result_$(hostname)_$(date +%s).json"
    echo "Uploading JSON report to ${GCS_DEST}..."
    gcloud storage cp "${OUT_JSON}" "${GCS_DEST}"
  fi
fi

echo "--- Benchmark Run Complete ---"
