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

"""Comprehensive benchmark comparing:
1. Traditional Python row decoding
2. Customer PyArrow conversion (Rows -> dicts -> pa.Table)
3. Pure-Python PyArrow (_arrow.py)
4. C-Accelerated PyArrow (google-cloud-spanner-arrow)

Measures Single-Threaded and Multi-Threaded setups for both Small and Large result sets.
"""

import concurrent.futures
import gc
import statistics
import time
from typing import Tuple

import pyarrow as pa
from google.cloud import spanner
from google.cloud.spanner_v1 import _arrow as pure_py_arrow
from google_cloud_spanner_arrow import cext as spanner_arrow_cext
from google_cloud_spanner_arrow import python as spanner_arrow_python

PROJECT_ID = "appdev-soda-spanner-staging"
INSTANCE_ID = "knut-test-ycsb"
DATABASE_ID = "spring-data-jpa"

# Query generating diverse column types dynamically
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
# Read Operations (measuring rows 2...N to isolate client parsing)
# -------------------------------------------------------------

def read_traditional_rows(database, num_rows: int) -> Tuple[float, int]:
    """Read rows using traditional Python client row decoding."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        row_iter = iter(results)
        try:
            first = next(row_iter)
            for _ in first:
                pass
        except StopIteration:
            return 0.0, 0

        start = time.perf_counter()
        count = 1
        for row in row_iter:
            for _ in row:
                pass
            count += 1
        elapsed = time.perf_counter() - start
        return elapsed, count


def read_customer_to_arrow(database, num_rows: int) -> Tuple[float, int]:
    """Customer approach: iterate rows into dicts, call pa.Table.from_pylist()."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        row_iter = iter(results)
        try:
            first = next(row_iter)
            for _ in first:
                pass
        except StopIteration:
            return 0.0, 0

        col_names = [col.name for col in results.fields]
        start = time.perf_counter()
        rows_list = []
        for row in row_iter:
            row_dict = {}
            for col_name, cell in zip(col_names, row):
                if hasattr(cell, "months"):
                    row_dict[col_name] = str(cell)
                else:
                    row_dict[col_name] = cell
            rows_list.append(row_dict)
        table = pa.Table.from_pylist(rows_list)
        elapsed = time.perf_counter() - start
        return elapsed, len(table) + 1


def read_pure_python_arrow(database, num_rows: int, max_chunk_size: int = 65536) -> Tuple[float, int]:
    """Pure-Python PyArrow stream ingestion."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        results._lazy_decode = True
        results._consume_next()

        fields = results.fields
        pa_schema = spanner_arrow_python.fields_to_arrow_schema(fields)

        start = time.perf_counter()
        batches = []
        accumulated = []
        while True:
            if results._rows:
                accumulated.extend(results._rows)
                results._rows = []
            while len(accumulated) >= max_chunk_size:
                chunk = accumulated[:max_chunk_size]
                accumulated = accumulated[max_chunk_size:]
                batches.append(spanner_arrow_python.rows_to_arrow_batch(fields, chunk, schema=pa_schema))
            if results._done:
                break
            try:
                results._consume_next()
            except StopIteration:
                break
        if accumulated:
            batches.append(spanner_arrow_python.rows_to_arrow_batch(fields, accumulated, schema=pa_schema))
        table = pa.Table.from_batches(batches, schema=pa_schema)
        elapsed = time.perf_counter() - start
        return elapsed, table.num_rows


def read_c_accelerated_arrow(database, num_rows: int, max_chunk_size: int = 65536) -> Tuple[float, int]:
    """Native C-accelerated PyArrow stream ingestion."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        results._lazy_decode = True
        results._consume_next()

        fields = results.fields
        pa_schema = spanner_arrow_python.fields_to_arrow_schema(fields)

        start = time.perf_counter()
        batches = []
        accumulated = []
        while True:
            if results._rows:
                accumulated.extend(results._rows)
                results._rows = []
            while len(accumulated) >= max_chunk_size:
                chunk = accumulated[:max_chunk_size]
                accumulated = accumulated[max_chunk_size:]
                batches.append(spanner_arrow_cext.rows_to_arrow_batch(fields, chunk, schema=pa_schema))
            if results._done:
                break
            try:
                results._consume_next()
            except StopIteration:
                break
        if accumulated:
            batches.append(spanner_arrow_cext.rows_to_arrow_batch(fields, accumulated, schema=pa_schema))
        table = pa.Table.from_batches(batches, schema=pa_schema)
        elapsed = time.perf_counter() - start
        return elapsed, table.num_rows


# -------------------------------------------------------------
# Multi-Threaded Concurrent Workloads
# -------------------------------------------------------------

def run_concurrent_workload(database, num_rows_per_query: int, num_threads: int, read_fn):
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(read_fn, database, num_rows_per_query) for _ in range(num_threads)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    total_time = time.perf_counter() - start
    total_rows = sum(r[1] for r in results)
    return total_time, total_rows


# -------------------------------------------------------------
# Benchmark Runner
# -------------------------------------------------------------

def run_all_benchmarks():
    print(f"Connecting to Cloud Spanner: {PROJECT_ID} / {INSTANCE_ID} / {DATABASE_ID}")

    client = spanner.Client(project=PROJECT_ID)
    instance = client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)

    # Warmup
    print("Warming up database connection and JIT/gRPC channels...")
    read_traditional_rows(database, 1000)
    read_pure_python_arrow(database, 1000)
    read_c_accelerated_arrow(database, 1000)

    # 1. Single-Threaded Benchmarks
    print("\n" + "=" * 80)
    print(" 1. SINGLE-THREADED BENCHMARKS (Small, Medium, Large Result Sets)")
    print("=" * 80)

    single_sizes = [
        ("Small", 2000),
        ("Medium", 10000),
        ("Large", 50000),
        ("Very Large", 100000),
    ]
    iterations = 3

    for label, num_rows in single_sizes:
        print(f"\n--- [{label}] Result Set: {num_rows:,} rows (12 diverse columns) ---")
        
        times_trad = []
        times_cust = []
        times_py_arrow = []
        times_c_arrow = []

        for it in range(iterations):
            gc.collect()
            t, _ = read_traditional_rows(database, num_rows)
            times_trad.append(t)

            gc.collect()
            t, _ = read_customer_to_arrow(database, num_rows)
            times_cust.append(t)

            gc.collect()
            t, _ = read_pure_python_arrow(database, num_rows)
            times_py_arrow.append(t)

            gc.collect()
            t, _ = read_c_accelerated_arrow(database, num_rows)
            times_c_arrow.append(t)

        avg_trad = statistics.mean(times_trad)
        avg_cust = statistics.mean(times_cust)
        avg_py_arrow = statistics.mean(times_py_arrow)
        avg_c_arrow = statistics.mean(times_c_arrow)

        rps_trad = num_rows / avg_trad
        rps_cust = num_rows / avg_cust
        rps_py = num_rows / avg_py_arrow
        rps_c = num_rows / avg_c_arrow

        print(f"  1. Traditional Rows:           {avg_trad*1000:7.1f} ms  |  {rps_trad:9,.0f} rows/s")
        print(f"  2. Customer (Rows -> PyArrow): {avg_cust*1000:7.1f} ms  |  {rps_cust:9,.0f} rows/s")
        print(f"  3. Pure-Python PyArrow:        {avg_py_arrow*1000:7.1f} ms  |  {rps_py:9,.0f} rows/s")
        print(f"  4. C-Accelerated PyArrow:      {avg_c_arrow*1000:7.1f} ms  |  {rps_c:9,.0f} rows/s")
        print(f"     ==> Speedup over Traditional: {avg_trad/avg_c_arrow:5.2f}x faster")
        print(f"     ==> Speedup over Customer:    {avg_cust/avg_c_arrow:5.2f}x faster")
        print(f"     ==> Speedup over Pure-Python: {avg_py_arrow/avg_c_arrow:5.2f}x faster")

    # 2. Multi-Threaded Benchmarks
    print("\n" + "=" * 80)
    print(" 2. MULTI-THREADED CONCURRENT BENCHMARKS (4 & 8 Threads)")
    print("=" * 80)

    multi_configs = [
        ("Small Concurrent (8 threads x 2,000 rows = 16,000 rows)", 2000, 8),
        ("Medium Concurrent (4 threads x 10,000 rows = 40,000 rows)", 10000, 4),
        ("Large Concurrent (4 threads x 50,000 rows = 200,000 rows)", 50000, 4),
        ("Large Concurrent (8 threads x 25,000 rows = 200,000 rows)", 25000, 8),
    ]

    for title, rows_per_query, num_threads in multi_configs:
        total_rows = rows_per_query * num_threads
        print(f"\n--- {title} ---")

        times_trad = []
        times_cust = []
        times_py_arrow = []
        times_c_arrow = []

        for it in range(iterations):
            gc.collect()
            t, _ = run_concurrent_workload(database, rows_per_query, num_threads, read_traditional_rows)
            times_trad.append(t)

            gc.collect()
            t, _ = run_concurrent_workload(database, rows_per_query, num_threads, read_customer_to_arrow)
            times_cust.append(t)

            gc.collect()
            t, _ = run_concurrent_workload(database, rows_per_query, num_threads, read_pure_python_arrow)
            times_py_arrow.append(t)

            gc.collect()
            t, _ = run_concurrent_workload(database, rows_per_query, num_threads, read_c_accelerated_arrow)
            times_c_arrow.append(t)

        avg_trad = statistics.mean(times_trad)
        avg_cust = statistics.mean(times_cust)
        avg_py = statistics.mean(times_py_arrow)
        avg_c = statistics.mean(times_c_arrow)

        rps_trad = total_rows / avg_trad
        rps_cust = total_rows / avg_cust
        rps_py = total_rows / avg_py
        rps_c = total_rows / avg_c

        print(f"  1. Traditional Rows:           {avg_trad*1000:7.1f} ms  |  {rps_trad:9,.0f} rows/s (total throughput)")
        print(f"  2. Customer (Rows -> PyArrow): {avg_cust*1000:7.1f} ms  |  {rps_cust:9,.0f} rows/s (total throughput)")
        print(f"  3. Pure-Python PyArrow:        {avg_py*1000:7.1f} ms  |  {rps_py:9,.0f} rows/s (total throughput)")
        print(f"  4. C-Accelerated PyArrow:      {avg_c*1000:7.1f} ms  |  {rps_c:9,.0f} rows/s (total throughput)")
        print(f"     ==> Speedup over Traditional: {avg_trad/avg_c:5.2f}x faster")
        print(f"     ==> Speedup over Customer:    {avg_cust/avg_c:5.2f}x faster")
        print(f"     ==> Speedup over Pure-Python: {avg_py/avg_c:5.2f}x faster")


if __name__ == "__main__":
    run_all_benchmarks()
