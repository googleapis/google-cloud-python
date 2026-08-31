"""Comprehensive Real-World CPU Profiler Suite for Google Cloud Spanner using YAPPI (CPU Clock).

Measures pure CPU time (excluding I/O wait, socket polling, and network latency).
NO MOCKS, NO ARTIFICIAL SLEEP — All calls hit real Cloud Spanner backend.

Scenarios:
1. Point select with single concurrency (Concurrency = 1, Sync, Pure CPU Clock)
2. Point select with 32 concurrency (Concurrency = 32, AsyncIO, Pure CPU Clock)
3. LIMIT 1000 read for an 11-column table (AsyncBenchmarkTable, Sync, Pure CPU Clock)

Saves pstat/prof binaries and generates formatted summary reports.
"""

import asyncio
import io
import os
import pstats
import sys
import time

try:
    from absl import app
    HAS_ABSL = True
except ImportError:
    HAS_ABSL = False

import yappi
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types
from google.cloud.spanner_v1.services.spanner.async_client import SpannerAsyncClient
from google.cloud.spanner_v1.types import ExecuteSqlRequest

PROJECT = "span-cloud-testing"
INSTANCE = "suvham-testing"
DATABASE = "benchmark_db_async"
TABLE = "AsyncBenchmarkTable"
DB_PATH = f"projects/{PROJECT}/instances/{INSTANCE}/databases/{DATABASE}"

WARMUP_DURATION_SEC = 5.0
PROFILE_DURATION_SEC = 10.0


# -----------------------------------------------------------------------------
# Scenario 1 & 3: Synchronous Client Queries
# -----------------------------------------------------------------------------
def run_point_select_query_sync(database, user_id="user-0"):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            f"SELECT * FROM {TABLE} WHERE id = @id",
            params={"id": user_id},
            param_types={"id": param_types.STRING},
        )
        rows = list(results)
        return len(rows)


def run_limit_1000_query_sync(database):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(f"SELECT * FROM {TABLE} LIMIT 1000")
        rows = list(results)
        return len(rows)


def run_scenario_1_point_select_c1(database, output_prof_path):
    """Scenario 1: Point select with Concurrency = 1 (Real Spanner, Sync, CPU Clock)."""
    print("\n" + "=" * 80)
    print("SCENARIO 1: Real Point Select with Single Concurrency (C=1, Sync, Pure CPU Clock)")
    print("=" * 80)

    # 1. Warmup for 5 seconds
    print(f"[*] Warming up connection to Spanner for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC
    warmup_count = 0
    while time.time() < warmup_end:
        run_point_select_query_sync(database, "user-0")
        warmup_count += 1
    print(f"[+] Warmup completed: {warmup_count} requests executed.")

    # 2. Profile with Yappi (Pure CPU Time)
    print(f"[*] Profiling pure CPU time for {PROFILE_DURATION_SEC} seconds...")
    yappi.set_clock_type("cpu")
    yappi.clear_stats()
    yappi.start()

    prof_end = time.time() + PROFILE_DURATION_SEC
    recorded_count = 0
    while time.time() < prof_end:
        run_point_select_query_sync(database, "user-0")
        recorded_count += 1

    yappi.stop()
    print(f"[+] Profiling finished: {recorded_count} requests recorded.")

    stats = yappi.get_func_stats()
    stats.save(output_prof_path, type="pstat")
    print(f"[+] Saved pure CPU profile stats to: {output_prof_path}")
    return pstats.Stats(output_prof_path), recorded_count


# -----------------------------------------------------------------------------
# Scenario 2: Spanner Async Client (32 Concurrent Coroutines on Event Loop, CPU Clock)
# -----------------------------------------------------------------------------
async def run_single_async_query(async_client, session_name, user_id="user-0"):
    request = ExecuteSqlRequest(
        session=session_name,
        sql=f"SELECT * FROM {TABLE} WHERE id = '{user_id}'",
    )
    stream = await async_client.execute_streaming_sql(request=request)
    chunk_count = 0
    async for partial_result_set in stream:
        chunk_count += len(partial_result_set.values)
    return chunk_count


async def async_worker_loop(async_client, session_name, worker_id, stop_time):
    count = 0
    while time.time() < stop_time:
        await run_single_async_query(async_client, session_name, f"user-{worker_id % 100}")
        count += 1
    return count


async def execute_async_scenario_2(output_prof_path, concurrency=32):
    print("\n" + "=" * 80)
    print(f"SCENARIO 2: Real Spanner Async Client with {concurrency} Concurrency (C={concurrency}, AsyncIO, Pure CPU Clock)")
    print("=" * 80)

    print(f"[*] Initializing SpannerAsyncClient (grpc.aio transport) for {DB_PATH}...")
    async_client = SpannerAsyncClient()
    
    print(f"[*] Creating async sessions for {concurrency} workers...")
    sessions = await asyncio.gather(*[async_client.create_session(database=DB_PATH) for _ in range(concurrency)])
    session_names = [s.name for s in sessions]
    print(f"[+] Successfully created {len(session_names)} async sessions.")

    # 1. Warmup for 5 seconds across 32 concurrent coroutines
    print(f"[*] Warming up 32 concurrent coroutines on event loop for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC
    warmup_tasks = [
        async_worker_loop(async_client, session_names[i], i, warmup_end)
        for i in range(concurrency)
    ]
    warmup_results = await asyncio.gather(*warmup_tasks)
    print(f"[+] Warmup completed: {sum(warmup_results)} total requests executed across 32 coroutines.")

    # 2. Profile pure CPU time across all 32 coroutines
    print(f"[*] Profiling pure CPU time across all {concurrency} coroutines for {PROFILE_DURATION_SEC} seconds...")
    yappi.set_clock_type("cpu")
    yappi.clear_stats()
    yappi.start()

    prof_end = time.time() + PROFILE_DURATION_SEC
    profile_tasks = [
        async_worker_loop(async_client, session_names[i], i, prof_end)
        for i in range(concurrency)
    ]
    profile_results = await asyncio.gather(*profile_tasks)
    yappi.stop()

    total_recorded = sum(profile_results)
    print(f"[+] Profiling finished: {total_recorded} total requests recorded across all {concurrency} coroutines.")
    
    stats = yappi.get_func_stats()
    stats.save(output_prof_path, type="pstat")
    print(f"[+] Saved pure CPU profile stats to: {output_prof_path}")
    return pstats.Stats(output_prof_path), total_recorded


def run_scenario_2_point_select_c32_async(output_prof_path, concurrency=32):
    return asyncio.run(execute_async_scenario_2(output_prof_path, concurrency))


# -----------------------------------------------------------------------------
# Scenario 3: LIMIT 1000 Read (Sync, CPU Clock)
# -----------------------------------------------------------------------------
def run_scenario_3_limit_1000_c1(database, output_prof_path):
    """Scenario 3: LIMIT 1000 Read for 11-column table (Real Spanner, CPU Clock)."""
    print("\n" + "=" * 80)
    print("SCENARIO 3: Real LIMIT 1000 Read for AsyncBenchmarkTable (Sync, Pure CPU Clock)")
    print("=" * 80)

    # 1. Warmup for 5 seconds
    print(f"[*] Warming up LIMIT 1000 stream for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC
    warmup_count = 0
    while time.time() < warmup_end:
        rows_read = run_limit_1000_query_sync(database)
        warmup_count += 1
    print(f"[+] Warmup completed: {warmup_count} queries ({warmup_count * 1000} rows) executed.")

    # 2. Profile pure CPU time
    print(f"[*] Profiling LIMIT 1000 pure CPU time for {PROFILE_DURATION_SEC} seconds...")
    yappi.set_clock_type("cpu")
    yappi.clear_stats()
    yappi.start()

    prof_end = time.time() + PROFILE_DURATION_SEC
    recorded_count = 0
    while time.time() < prof_end:
        rows_read = run_limit_1000_query_sync(database)
        recorded_count += 1

    yappi.stop()
    print(f"[+] Profiling finished: {recorded_count} queries ({recorded_count * 1000} rows) recorded.")

    stats = yappi.get_func_stats()
    stats.save(output_prof_path, type="pstat")
    print(f"[+] Saved pure CPU profile stats to: {output_prof_path}")
    return pstats.Stats(output_prof_path), recorded_count


def print_summary_table(ps, title, request_count):
    s = io.StringIO()
    ps.stream = s
    ps.strip_dirs()
    print("\n" + "-" * 80)
    print(f"SUMMARY FOR: {title}")
    print(f"Total Requests: {request_count} | Total Pure CPU Time: {ps.total_tt:.4f} s | Avg CPU/Query: {(ps.total_tt / max(1, request_count)) * 1000:.3f} ms")
    print("-" * 80)
    ps.sort_stats("cumulative").print_stats(15)
    print(s.getvalue())


def run_all(argv=None):
    repo_dir = "/usr/local/google/home/suvham/workspace/cloudPython/google-cloud-python/packages/google-cloud-spanner/profiler_results"
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.exists(os.path.join(os.getcwd(), "packages/google-cloud-spanner/profiler_results/README.md")):
        output_dir = os.path.join(os.getcwd(), "packages/google-cloud-spanner/profiler_results")
    elif os.path.exists(os.path.join(os.getcwd(), "README.md")) and "profiler_results" in os.getcwd():
        output_dir = os.getcwd()
    elif os.path.exists(repo_dir):
        output_dir = repo_dir
    else:
        output_dir = script_dir

    os.makedirs(output_dir, exist_ok=True)

    print(f"Initializing Spanner Client for {PROJECT} / {INSTANCE} / {DATABASE}...")
    client = spanner.Client(project=PROJECT)
    instance = client.instance(INSTANCE)
    database = instance.database(DATABASE)

    f1 = os.path.join(output_dir, "spanner_point_select_c1.prof")
    ps1, cnt1 = run_scenario_1_point_select_c1(database, f1)
    print_summary_table(ps1, "Scenario 1: Point Select C=1 (Real Spanner, Pure CPU)", cnt1)

    f2 = os.path.join(output_dir, "spanner_point_select_c32.prof")
    ps2, cnt2 = run_scenario_2_point_select_c32_async(f2, concurrency=32)
    print_summary_table(ps2, "Scenario 2: Point Select C=32 (Real Spanner, AsyncIO Pure CPU)", cnt2)

    f3 = os.path.join(output_dir, "spanner_limit1000_c1.prof")
    ps3, cnt3 = run_scenario_3_limit_1000_c1(database, f3)
    print_summary_table(ps3, "Scenario 3: LIMIT 1000 Read (Real Spanner, Pure CPU)", cnt3)

    print("\n" + "=" * 80)
    print("ALL REAL SPANNER PURE CPU PROFILES GENERATED SUCCESSFULLY:")
    print(f"1. {f1}")
    print(f"2. {f2}")
    print(f"3. {f3}")
    print("=" * 80)


def main():
    if HAS_ABSL:
        app.run(run_all)
    else:
        run_all()


if __name__ == "__main__":
    main()
