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

"""Benchmark comparing:
1. Python Protobuf Object Deserialization + Pure-Python Arrow
2. Python Protobuf Object Deserialization + C-Extension Arrow (rows_to_c_batch)
3. Direct Protobuf Wire Decoding in C -> Arrow (wire_prs_to_c_batch)
   (Measuring pure parsing/decoding throughput and multi-threaded scaling).
"""

import concurrent.futures
import gc
import statistics
import time
from typing import List

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


def fetch_wire_chunks(database, num_rows: int):
    """Fetch raw protobuf wire byte chunks and assembled rows from Spanner."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        results._lazy_decode = True
        chunks = []
        python_rows = []

        raw_iter = results._response_iterator

        class InterceptingIterator:
            def __init__(self, it):
                self.it = it
            def __iter__(self):
                return self
            def __next__(self):
                resp = next(self.it)
                chunks.append(resp._pb.SerializeToString())
                return resp

        results._response_iterator = InterceptingIterator(raw_iter)

        while True:
            try:
                results._consume_next()
            except StopIteration:
                break
            if results._rows:
                python_rows.extend(results._rows)
                results._rows = []
            if results._done:
                break

        fields = results.fields
        return fields, chunks, python_rows


# -------------------------------------------------------------
# Parsing Benchmarks (Pure parsing CPU speed excluding network)
# -------------------------------------------------------------

def bench_pure_python_parsing(fields, python_rows: List[List]):
    start = time.perf_counter()
    batch = spanner_arrow_python.rows_to_arrow_batch(fields, python_rows)
    elapsed = time.perf_counter() - start
    return elapsed, batch.num_rows


def bench_c_object_parsing(fields, python_rows: List[List]):
    start = time.perf_counter()
    batch = spanner_arrow_cext.rows_to_arrow_batch(fields, python_rows)
    elapsed = time.perf_counter() - start
    return elapsed, batch.num_rows


def bench_c_direct_wire_parsing(fields, wire_chunks: List[bytes]):
    start = time.perf_counter()
    batch = spanner_arrow_cext.wire_prs_to_arrow_batch(fields, wire_chunks)
    elapsed = time.perf_counter() - start
    return elapsed, batch.num_rows


def run_benchmark():
    print(f"Connecting to Cloud Spanner: {PROJECT_ID} / {INSTANCE_ID} / {DATABASE_ID}")
    client = spanner.Client(project=PROJECT_ID)
    instance = client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)

    test_sizes = [10000, 50000, 100000]
    iterations = 5

    print("\n" + "=" * 84)
    print(" 1. PARSING & CONVERSION CPU THROUGHPUT (Single-Threaded)")
    print("    Measuring pure decoding & Arrow construction time")
    print("=" * 84)

    for num_rows in test_sizes:
        print(f"\nFetching test dataset of {num_rows:,} rows from Spanner...")
        fields, wire_chunks, python_rows = fetch_wire_chunks(database, num_rows)
        total_wire_bytes = sum(len(c) for c in wire_chunks)
        print(f"Dataset: {len(python_rows):,} rows | 12 cols | {total_wire_bytes / (1024*1024):.2f} MB wire protobuf")

        actual_rows = len(python_rows)
        times_py = []
        times_c_obj = []
        times_c_wire = []

        for _ in range(iterations):
            gc.collect()
            t, r = bench_pure_python_parsing(fields, python_rows)
            times_py.append(t)

            gc.collect()
            t, r = bench_c_object_parsing(fields, python_rows)
            times_c_obj.append(t)

            gc.collect()
            t, r = bench_c_direct_wire_parsing(fields, wire_chunks)
            times_c_wire.append(t)

        avg_py = statistics.mean(times_py)
        avg_c_obj = statistics.mean(times_c_obj)
        avg_c_wire = statistics.mean(times_c_wire)

        rps_py = actual_rows / avg_py
        rps_c_obj = actual_rows / avg_c_obj
        rps_c_wire = actual_rows / avg_c_wire

        print(f"  A. Pure-Python (Values -> Arrow):         {avg_py*1000:7.2f} ms  |  {rps_py:10,.0f} rows/s")
        print(f"  B. C-Ext Objects (Values -> Arrow):       {avg_c_obj*1000:7.2f} ms  |  {rps_c_obj:10,.0f} rows/s")
        print(f"  C. Direct Wire C-Ext (Raw Proto -> Arrow):{avg_c_wire*1000:7.2f} ms  |  {rps_c_wire:10,.0f} rows/s")
        print(f"     ==> Direct Wire vs Pure-Python:  {avg_py/avg_c_wire:6.1f}x FASTER!")
        print(f"     ==> Direct Wire vs C-Ext Object: {avg_c_obj/avg_c_wire:6.1f}x FASTER!")

    print("\n" + "=" * 84)
    print(" 2. MULTI-THREADED CONCURRENT SCALING (8 Threads Parallel Parsing)")
    print("=" * 84)

    num_rows = 100000
    num_threads = 8
    print(f"\nBenchmarking 8 parallel threads decoding 100k rows each (800,000 rows total)...")
    fields, wire_chunks, python_rows = fetch_wire_chunks(database, num_rows)
    actual_rows = len(python_rows)

    def run_multi(fn, data):
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(fn, fields, data) for _ in range(num_threads)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        return time.perf_counter() - start, sum(r[1] for r in results)

    times_mt_py = []
    times_mt_c_obj = []
    times_mt_c_wire = []

    for _ in range(iterations):
        gc.collect()
        t, r = run_multi(bench_pure_python_parsing, python_rows)
        times_mt_py.append(t)

        gc.collect()
        t, r = run_multi(bench_c_object_parsing, python_rows)
        times_mt_c_obj.append(t)

        gc.collect()
        t, r = run_multi(bench_c_direct_wire_parsing, wire_chunks)
        times_mt_c_wire.append(t)

    avg_mt_py = statistics.mean(times_mt_py)
    avg_mt_obj = statistics.mean(times_mt_c_obj)
    avg_mt_wire = statistics.mean(times_mt_c_wire)

    total_rows = actual_rows * num_threads
    rps_mt_py = total_rows / avg_mt_py
    rps_mt_obj = total_rows / avg_mt_obj
    rps_mt_wire = total_rows / avg_mt_wire

    print(f"  A. Pure-Python (8 threads):              {avg_mt_py*1000:7.2f} ms  |  {rps_mt_py:10,.0f} rows/s (total)")
    print(f"  B. C-Ext Objects (8 threads):            {avg_mt_obj*1000:7.2f} ms  |  {rps_mt_obj:10,.0f} rows/s (total)")
    print(f"  C. Direct Wire C-Ext (8 threads):        {avg_mt_wire*1000:7.2f} ms  |  {rps_mt_wire:10,.0f} rows/s (total)")
    print(f"     ==> Multi-Threaded Speedup over Pure-Python:  {avg_mt_py/avg_mt_wire:6.1f}x FASTER!")
    print(f"     ==> Multi-Threaded Speedup over C-Ext Object: {avg_mt_obj/avg_mt_wire:6.1f}x FASTER!")


if __name__ == "__main__":
    run_benchmark()
