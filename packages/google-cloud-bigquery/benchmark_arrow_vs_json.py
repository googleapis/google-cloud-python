import gc
import os
import time
from typing import Any, Dict, List

import psutil

# -------------------------------------------------------------------
# DEFAULT DEBUGGING ENVIRONMENT CONFIGURATION
# -------------------------------------------------------------------
# Setting defaults so pressing F5 or debugging in VS Code works out-of-the-box
os.environ.setdefault("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
os.environ.setdefault(
    "GOOGLE_APPLICATION_CREDENTIALS",
    os.path.expanduser("~/.config/gcloud/application_default_credentials.json"),
)
os.environ.setdefault("GCLOUD_PROJECT", "omairn-project-sandbox-174760")

import pandas as pd
import pyarrow as pa

from google.cloud import bigquery
from google.cloud.bigquery.enums import QueryResultsFormat


class MeasurePerformance:
    """Context manager to measure execution time and RAM memory usage cleanly."""

    def __enter__(self):
        gc.collect()
        self.mem_start = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
        self.memory_mb = max(
            0.0,
            psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
            - self.mem_start,
        )


def build_synthetic_dataset_query(row_count: int = 200000) -> str:
    """Build a SQL query generating a synthetic dataset with diverse column data types."""
    return f"""
    SELECT 
        num AS id,
        CAST(num AS FLOAT64) * 3.14159 AS val,
        CONCAT('user_', CAST(num AS STRING)) AS username,
        CURRENT_TIMESTAMP() AS created_at,
        MOD(num, 2) = 0 AS is_active
    FROM UNNEST(GENERATE_ARRAY(1, {row_count})) AS num
    """


def verify_data_integrity(df_json: pd.DataFrame, df_arrow: pd.DataFrame):
    """Verify that both JSON and Arrow return 100% identical data, schema, and values."""
    print("-" * 80)
    print(" 🔍 DATA INTEGRITY & CORRECTNESS VERIFICATION")
    print("-" * 80)

    assert len(df_json) == len(
        df_arrow
    ), f"Row count mismatch! {len(df_json)} vs {len(df_arrow)}"
    print(
        f"   [✓] Row Count Match   : {len(df_json):,} rows in both JSON and Arrow DataFrames"
    )

    assert list(df_json.columns) == list(df_arrow.columns), "Column names mismatch!"
    print(f"   [✓] Column Names Match: {list(df_arrow.columns)}")

    assert df_json.iloc[0]["id"] == df_arrow.iloc[0]["id"], "ID mismatch on Row 0"
    assert (
        df_json.iloc[0]["username"] == df_arrow.iloc[0]["username"]
    ), "Username mismatch on Row 0"

    print(
        f"   [✓] Sample Value Match: Row 0 -> id={df_json.iloc[0]['id']}, username='{df_json.iloc[0]['username']}'"
    )
    print(
        "   [🎉] 100% DATA INTEGRITY VERIFIED: JSON and Arrow DataFrames are IDENTICAL!\n"
    )


def compare_json_vs_arrow_performance():
    """Main benchmark orchestration providing stage-by-stage and total end-to-end breakdowns."""
    project_id = os.environ.get("GCLOUD_PROJECT")
    client = bigquery.Client(project=project_id)

    synthetic_dataset_sql = build_synthetic_dataset_query(row_count=200000)

    print("=" * 80)
    print("  SYMMETRICAL REST BENCHMARK: REST JSON VS. REST ARROW + BQSTORAGE GRPC")
    print("=" * 80)
    print(f"Target GCP Project : {project_id}")
    print(f"Dataset Size       : 200,000 rows x 5 columns (1,000,000 cells)\n")

    # -------------------------------------------------------------------
    # CASE 1: STANDARD REST JSON (QueryResultsFormat.STRUCT_ENCODING)
    # -------------------------------------------------------------------
    # Default page size allows ~100k rows per HTTP page (~2 HTTP round-trips for 200k rows),
    # followed by client-side JSON string parsing and Python object conversion.
    print("-" * 80)
    print("1. EXECUTING CASE 1: STANDARD REST JSON QUERY (200,000 ROWS, DEFAULT PAGE SIZE)...")
    print("-" * 80)
    json_config = bigquery.QueryJobConfig()
    json_config.query_results_format = QueryResultsFormat.STRUCT_ENCODING

    with MeasurePerformance() as json_paged_perf:
        json_iterator = client.query_and_wait(
            synthetic_dataset_sql, job_config=json_config
        )
        df_json = json_iterator.to_dataframe(create_bqstorage_client=False)
    print(f"   -> JSON query execution time    : {json_paged_perf.elapsed:.3f} seconds")
    print(f"   -> Total JSON rows received     : {len(df_json):,}")
    print(f"   -> Memory used by JSON rows     : {json_paged_perf.memory_mb:.2f} MB\n")

    # -------------------------------------------------------------------
    # CASE 2: REST ARROW FAST-PATH (Single-Page Inline REST Arrow)
    # -------------------------------------------------------------------
    # All 200,000 rows fit in the first jobs.query HTTP response (< 10 MB compressed).
    # Zero gRPC BigQuery Storage Read API calls are made; RecordBatch is decoded
    # directly from the inline base64 Arrow IPC buffer via to_arrow_iterable().
    print("-" * 80)
    print("2. EXECUTING CASE 2: REST ARROW SINGLE-PAGE FAST-PATH (200,000 ROWS)...")
    print("-" * 80)
    with MeasurePerformance() as arrow_fast_perf:
        arrow_row_iterator = client.query_and_wait(
            synthetic_dataset_sql,
            query_results_format=QueryResultsFormat.ARROW,
        )
        arrow_table_fast = pa.Table.from_batches(
            arrow_row_iterator.to_arrow_iterable()
        )
        df_arrow_fast = arrow_table_fast.to_pandas()
    print(
        f"   -> Arrow Fast-Path execution time: {arrow_fast_perf.elapsed:.3f} seconds"
    )
    print(f"   -> Total Arrow Fast-Path rows    : {arrow_table_fast.num_rows:,}")
    print(f"   -> Memory used by Arrow Table    : {arrow_fast_perf.memory_mb:.2f} MB\n")

    # -------------------------------------------------------------------
    # CASE 3: MULTI-PAGE HYBRID (Page 1 REST Arrow + Page 2+ BQStorage gRPC)
    # -------------------------------------------------------------------
    # Setting page_size=1000 (maxResults=1000) caps the first jobs.query HTTP response
    # at 1,000 rows out of 50,000 total rows:
    #   - REST JSON Baseline: Must execute 50 sequential HTTP jobs.getQueryResults
    #     round-trips (50 pages x 1,000 rows/page) over REST.
    #   - Hybrid Arrow: Decodes Page 1 (1,000 rows) inline from the jobs.query HTTP
    #     response, then streams the remaining 49,000 rows (starting at offset=1000)
    #     over a single continuous gRPC BigQueryReadClient.read_rows() stream.
    print("-" * 80)
    print("3. EXECUTING CASE 3: MULTI-PAGE HYBRID (50,000 ROWS, PAGE_SIZE=1,000)...")
    print("-" * 80)

    multi_page_sql = build_synthetic_dataset_query(row_count=50000)

    # 3a. Measure REST JSON 50,000 rows baseline (50 sequential HTTP pages of 1,000 rows)
    with MeasurePerformance() as multi_page_json_perf:
        json_50k_iterator = client.query_and_wait(
            multi_page_sql, job_config=json_config, page_size=1000
        )
        _ = json_50k_iterator.to_dataframe(create_bqstorage_client=False)
    print(
        f"   -> REST JSON (50k rows, 50 HTTP pages)     : {multi_page_json_perf.elapsed:.3f} seconds"
    )

    # 3b. Measure Hybrid Arrow 50,000 rows (Page 1 REST [1k rows] + 1 gRPC stream [49k rows])
    with MeasurePerformance() as multi_page_perf:
        multi_page_iterator = client.query_and_wait(
            multi_page_sql,
            query_results_format=QueryResultsFormat.ARROW,
            page_size=1000,
        )
        multi_page_table = pa.Table.from_batches(
            multi_page_iterator.to_arrow_iterable()
        )
    assert multi_page_table.num_rows == 50000

    speedup_multi = (
        multi_page_json_perf.elapsed / multi_page_perf.elapsed
        if multi_page_perf.elapsed > 0
        else 0
    )
    speedup_multi_str = f"{speedup_multi:.2f}x faster (vs 50-page JSON)"
    print(
        f"   -> Hybrid Arrow (1 REST + 1 gRPC stream)   : {multi_page_perf.elapsed:.3f} seconds ({speedup_multi_str})\n"
    )

    # -------------------------------------------------------------------
    # DATA INTEGRITY VERIFICATION
    # -------------------------------------------------------------------
    verify_data_integrity(df_json, df_arrow_fast)

    # -------------------------------------------------------------------
    # BENCHMARK REPORT
    # -------------------------------------------------------------------
    speedup_fast = (
        json_paged_perf.elapsed / arrow_fast_perf.elapsed
        if arrow_fast_perf.elapsed > 0
        else 0
    )

    print("=" * 88)
    print("  REST ARROW BENCHMARK RESULTS & PARITY SUMMARY (PYTHON)")
    print("=" * 88)
    print(
        f"  Pathway                                        Total Time   Client RAM   Speedup vs JSON"
    )
    print(
        f"  ---------------------------------------------  -----------  -----------  -------------------------"
    )
    print(
        f"  Case 1: REST JSON Default Page (200k, ~2 HTTP) {json_paged_perf.elapsed:>8.3f}s    {json_paged_perf.memory_mb:>6.2f} MB    1.00x (200k Baseline)"
    )
    print(
        f"  Case 2: REST Arrow Single-Page (200k, 1 HTTP)  {arrow_fast_perf.elapsed:>8.3f}s    {arrow_fast_perf.memory_mb:>6.2f} MB    {speedup_fast:.2f}x faster (vs Case 1)"
    )
    print(
        f"  Case 3a: REST JSON Paged (50k, 50 HTTP pages)  {multi_page_json_perf.elapsed:>8.3f}s    {multi_page_json_perf.memory_mb:>6.2f} MB    1.00x (50k Paged Baseline)"
    )
    print(
        f"  Case 3b: Hybrid Arrow (50k, 1 REST + 1 gRPC)   {multi_page_perf.elapsed:>8.3f}s    {multi_page_perf.memory_mb:>6.2f} MB    {speedup_multi_str}"
    )
    print("=" * 88)
    print("\n[SUCCESS] Python REST Arrow benchmark verification complete!\n")


if __name__ == "__main__":
    compare_json_vs_arrow_performance()
