# Copyright 2026 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""End-to-End concurrency benchmark measuring full query lifecycle:
- snapshot.execute_sql() RPC dispatch
- gRPC streaming network transport
- Stream ingestion and decoding
Across 1, 4, 8, 16, and 32 concurrent threads.
"""

import concurrent.futures
import gc
import statistics
import time
from typing import Tuple

import pyarrow as pa
from google.cloud import spanner
from google_cloud_spanner_arrow import cext as spanner_arrow_cext
from google_cloud_spanner_arrow import python as spanner_arrow_python

PROJECT_ID = "appdev-soda-spanner-staging"
INSTANCE_ID = "knut-test-ycsb"
DATABASE_ID = "spring-data-jpa"

SQL = """SELECT
  MOD(FARM_FINGERPRINT(GENERATE_UUID()), 2) = 0 AS random_bool,
  CAST(GENERATE_UUID() AS BYTES) AS random_bytes,
  DATE_FROM_UNIX_DATE(ABS(MOD(FARM_FINGERPRINT(GENERATE_UUID()), 2932896))) AS random_date,
  CAST(FARM_FINGERPRINT(GENERATE_UUID()) / FARM_FINGERPRINT(GENERATE_UUID()) AS FLOAT32) AS random_float32,
  CAST(FARM_FINGERPRINT(GENERATE_UUID()) / FARM_FINGERPRINT(GENERATE_UUID()) AS FLOAT64) AS random_float64,
  MAKE_INTERVAL(ABS(MOD(FARM_FINGERPRINT(GENERATE_UUID()), 10)), ABS(MOD(FARM_FINGERPRINT(GENERATE_UUID()), 12)), ABS(MOD(FARM_FINGERPRINT(GENERATE_UUID()), 28)), ABS(MOD(FARM_FINGERPRINT(GENERATE_UUID()), 24)), ABS(MOD(FARM_FINGERPRINT(GENERATE_UUID()), 60)), ABS(MOD(FARM_FINGERPRINT(GENERATE_UUID()), 60))) AS random_interval,
  TO_JSON('{"key": "' || GENERATE_UUID() || '"}') AS random_json,
  FARM_FINGERPRINT(GENERATE_UUID()) AS random_int64,
  CAST(FARM_FINGERPRINT(GENERATE_UUID()) / FARM_FINGERPRINT(GENERATE_UUID()) AS NUMERIC) AS random_numeric,
  GENERATE_UUID() AS random_string,
  TIMESTAMP_MICROS(ABS(MOD(FARM_FINGERPRINT(GENERATE_UUID()), 1230219000000000))) AS random_timestamp,
  NEW_UUID() AS random_uuid
FROM UNNEST(GENERATE_ARRAY(1, @num_rows)) AS n"""


# -------------------------------------------------------------
# Full End-to-End Query Functions (Measuring execute_sql -> done)
# -------------------------------------------------------------

def e2e_traditional_rows(database, num_rows: int) -> Tuple[float, int]:
    """Full end-to-end traditional Python row iteration."""
    start = time.perf_counter()
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        count = 0
        for row in results:
            for _ in row:
                pass
            count += 1
    elapsed = time.perf_counter() - start
    return elapsed, count


def e2e_pure_python_arrow(database, num_rows: int) -> Tuple[float, int]:
    """Full end-to-end pure-Python PyArrow streaming table."""
    start = time.perf_counter()
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        results._lazy_decode = True
        batches = []
        accumulated = []
        fields = None
        pa_schema = None
        max_chunk_size = 65536

        while True:
            try:
                results._consume_next()
            except StopIteration:
                break
            if fields is None and results._metadata:
                fields = results.fields
                pa_schema = spanner_arrow_python.fields_to_arrow_schema(fields)
            if results._rows:
                accumulated.extend(results._rows)
                results._rows = []
            while len(accumulated) >= max_chunk_size:
                chunk = accumulated[:max_chunk_size]
                accumulated = accumulated[max_chunk_size:]
                batches.append(spanner_arrow_python.rows_to_arrow_batch(fields, chunk, schema=pa_schema))
            if results._done:
                break
        if accumulated:
            batches.append(spanner_arrow_python.rows_to_arrow_batch(fields, accumulated, schema=pa_schema))
        table = pa.Table.from_batches(batches, schema=pa_schema)
        count = table.num_rows
    elapsed = time.perf_counter() - start
    return elapsed, count


def e2e_direct_wire_c_arrow(database, num_rows: int) -> Tuple[float, int]:
    """Full end-to-end Direct Wire C-extension Arrow streaming."""
    start = time.perf_counter()
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        chunks = []
        fields = None
        pa_schema = None
        for resp in results._response_iterator:
            if fields is None and resp.metadata:
                fields = resp.metadata.row_type.fields
                pa_schema = spanner_arrow_python.fields_to_arrow_schema(fields)
            chunks.append(resp._pb.SerializeToString())
        batch = spanner_arrow_cext.wire_prs_to_arrow_batch(fields, chunks, schema=pa_schema)
        count = batch.num_rows
    elapsed = time.perf_counter() - start
    return elapsed, count


def run_concurrent_workload(database, num_rows_per_query: int, num_threads: int, fn):
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(fn, database, num_rows_per_query) for _ in range(num_threads)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    total_time = time.perf_counter() - start
    total_rows = sum(r[1] for r in results)
    return total_time, total_rows


def run_e2e_benchmarks():
    print(f"Connecting to Cloud Spanner: {PROJECT_ID} / {INSTANCE_ID} / {DATABASE_ID}")
    client = spanner.Client(project=PROJECT_ID)
    instance = client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)

    # Warmup
    print("Warming up gRPC channels and Spanner query caches...")
    e2e_traditional_rows(database, 1000)
    e2e_direct_wire_c_arrow(database, 1000)

    thread_counts = [1, 4, 8, 16, 32]
    num_rows_per_query = 30000  # 30,000 rows x 12 cols per concurrent query
    iterations = 3

    print("\n" + "=" * 86)
    print(" END-TO-END CONCURRENCY BENCHMARK (1, 4, 8, 16, 32 Concurrent Queries)")
    print(f" Each thread runs ExecuteStreamingSql() for {num_rows_per_query:,} rows (12 diverse columns)")
    print(" Measures full wall-clock time from execute_sql() RPC dispatch to final Table/Batch")
    print("=" * 86)

    for num_threads in thread_counts:
        total_rows = num_threads * num_rows_per_query
        print(f"\n--- {num_threads} Concurrent Threads ({total_rows:,} total rows across {num_threads} queries) ---")

        times_trad = []
        times_py_arrow = []
        times_wire_c = []

        for _ in range(iterations):
            gc.collect()
            t, r = run_concurrent_workload(database, num_rows_per_query, num_threads, e2e_traditional_rows)
            times_trad.append(t)

            gc.collect()
            t, r = run_concurrent_workload(database, num_rows_per_query, num_threads, e2e_pure_python_arrow)
            times_py_arrow.append(t)

            gc.collect()
            t, r = run_concurrent_workload(database, num_rows_per_query, num_threads, e2e_direct_wire_c_arrow)
            times_wire_c.append(t)

        avg_trad = statistics.mean(times_trad)
        avg_py = statistics.mean(times_py_arrow)
        avg_wire = statistics.mean(times_wire_c)

        rps_trad = total_rows / avg_trad
        rps_py = total_rows / avg_py
        rps_wire = total_rows / avg_wire

        print(f"  1. Traditional Python Rows:        {avg_trad*1000:7.1f} ms  |  {rps_trad:9,.0f} rows/s (total throughput)")
        print(f"  2. Pure-Python PyArrow:            {avg_py*1000:7.1f} ms  |  {rps_py:9,.0f} rows/s (total throughput)")
        print(f"  3. Direct Wire C-Ext PyArrow:      {avg_wire*1000:7.1f} ms  |  {rps_wire:9,.0f} rows/s (total throughput)")
        print(f"     ==> Wire C Speedup vs Traditional: {avg_trad/avg_wire:5.2f}x faster")
        print(f"     ==> Wire C Speedup vs Pure-Python: {avg_py/avg_wire:5.2f}x faster")


if __name__ == "__main__":
    run_e2e_benchmarks()
