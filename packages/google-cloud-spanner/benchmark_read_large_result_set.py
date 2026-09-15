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

"""Benchmark comparing traditional row reading vs direct PyArrow conversion.

Reuses the read-large-result-set query from spanner-client-benchmarks.
Measures rows 2...N to exclude initial query execution latency on Spanner.
"""

import gc
import statistics
import time
import pyarrow as pa
from google.cloud import spanner

PROJECT_ID = "appdev-soda-spanner-staging"
INSTANCE_ID = "knut-test-ycsb"
DATABASE_ID = "spring-data-jpa"

# Query generating random query results on the fly without inserting data
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


def benchmark_traditional_rows(database, num_rows):
    """Traditional row iteration measuring rows 2...N."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        row_iterator = iter(results)
        try:
            first_row = next(row_iterator)
            for cell in first_row:
                pass
        except StopIteration:
            return 0.0

        # Measure iteration and decoding of remaining rows (rows 2...N)
        start_time = time.perf_counter()
        count = 1
        for row in row_iterator:
            for cell in row:
                pass
            count += 1
        end_time = time.perf_counter()
        return (end_time - start_time), count


def benchmark_rows_to_pyarrow_customer_way(database, num_rows):
    """Customer's current path: traditional rows -> PyArrow Table (measuring 2...N)."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        row_iterator = iter(results)
        try:
            first_row = next(row_iterator)
            for cell in first_row:
                pass
        except StopIteration:
            return 0.0

        col_names = [col.name for col in results.fields]
        start_time = time.perf_counter()
        rows_list = []
        for row in row_iterator:
            row_dict = {}
            for col_name, cell in zip(col_names, row):
                if hasattr(cell, "months"):  # Spanner Interval
                    row_dict[col_name] = str(cell)
                else:
                    row_dict[col_name] = cell
            rows_list.append(row_dict)
        table = pa.Table.from_pylist(rows_list)
        end_time = time.perf_counter()
        return (end_time - start_time), len(table) + 1


def benchmark_direct_arrow_batches(database, num_rows, max_chunk_size=65536):
    """Direct-to-Arrow streaming batches (measuring rows 2...N after initial stream initialization)."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        # Initialize stream with lazy decoding (fetches first PartialResultSet / executes query on Spanner)
        results._lazy_decode = True
        results._consume_next()

        start_time = time.perf_counter()
        total_rows = 0
        for batch in results.to_arrow_batches(max_chunk_size=max_chunk_size):
            total_rows += batch.num_rows
        end_time = time.perf_counter()
        return (end_time - start_time), total_rows


def benchmark_direct_arrow_table(database, num_rows, max_chunk_size=65536):
    """Direct-to-Arrow complete Table materialization (measuring rows 2...N)."""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            SQL,
            params={"num_rows": num_rows},
            param_types={"num_rows": spanner.param_types.INT64},
        )
        # Initialize stream with lazy decoding (fetches first PartialResultSet / executes query on Spanner)
        results._lazy_decode = True
        results._consume_next()

        start_time = time.perf_counter()
        table = results.to_arrow(max_chunk_size=max_chunk_size)
        end_time = time.perf_counter()
        return (end_time - start_time), table.num_rows


def run_benchmarks():
    print(f"Connecting to Cloud Spanner: {PROJECT_ID} / {INSTANCE_ID} / {DATABASE_ID}")
    client = spanner.Client(project=PROJECT_ID)
    instance = client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)

    # Warmup
    print("\nWarming up connection and caches...")
    benchmark_traditional_rows(database, 1000)
    benchmark_direct_arrow_table(database, 1000)

    test_sizes = [10000, 50000, 100000]
    iterations = 3

    for num_rows in test_sizes:
        print(f"\n========================================================")
        print(f"  BENCHMARK: {num_rows:,} ROWS (12 diverse columns)")
        print(f"  Measuring time for rows 2...N (excluding query compile)")
        print(f"========================================================")

        results_trad = []
        results_cust = []
        results_arrow_batch = []
        results_arrow_table = []

        for i in range(iterations):
            gc.collect()
            t_trad, count_trad = benchmark_traditional_rows(database, num_rows)
            results_trad.append(t_trad)

            gc.collect()
            t_cust, count_cust = benchmark_rows_to_pyarrow_customer_way(database, num_rows)
            results_cust.append(t_cust)

            gc.collect()
            t_batch, count_batch = benchmark_direct_arrow_batches(database, num_rows)
            results_arrow_batch.append(t_batch)

            gc.collect()
            t_table, count_table = benchmark_direct_arrow_table(database, num_rows)
            results_arrow_table.append(t_table)

            print(f"  Run {i+1}/{iterations}:")
            print(f"    - Traditional Rows:                 {t_trad*1000:.1f} ms  ({num_rows/t_trad:,.0f} rows/s)")
            print(f"    - Customer (Rows -> PyArrow Table): {t_cust*1000:.1f} ms  ({num_rows/t_cust:,.0f} rows/s)")
            print(f"    - Direct to_arrow_batches():        {t_batch*1000:.1f} ms  ({num_rows/t_batch:,.0f} rows/s)")
            print(f"    - Direct to_arrow() Table:          {t_table*1000:.1f} ms  ({num_rows/t_table:,.0f} rows/s)")

        avg_trad = statistics.mean(results_trad)
        avg_cust = statistics.mean(results_cust)
        avg_batch = statistics.mean(results_arrow_batch)
        avg_table = statistics.mean(results_arrow_table)

        print(f"\n  --- Summary for {num_rows:,} rows (Average of {iterations} runs) ---")
        print(f"    1. Traditional Python Rows:        {avg_trad*1000:7.1f} ms | {num_rows/avg_trad:9,.0f} rows/s")
        print(f"    2. Customer Path (Rows -> PyArrow):{avg_cust*1000:7.1f} ms | {num_rows/avg_cust:9,.0f} rows/s")
        print(f"    3. Direct to_arrow_batches():      {avg_batch*1000:7.1f} ms | {num_rows/avg_batch:9,.0f} rows/s  --> {avg_cust/avg_batch:.2f}x faster than customer")
        print(f"    4. Direct to_arrow() Table:        {avg_table*1000:7.1f} ms | {num_rows/avg_table:9,.0f} rows/s  --> {avg_cust/avg_table:.2f}x faster than customer")


if __name__ == "__main__":
    run_benchmarks()
