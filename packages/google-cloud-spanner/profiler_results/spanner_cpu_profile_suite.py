"""Comprehensive Real-World CPU Profiler Suite for Google Cloud Spanner using YAPPI (CPU Clock).

Measures pure CPU time (excluding I/O wait, socket polling, and network latency).
NO MOCKS, NO ARTIFICIAL SLEEP — All calls hit real Cloud Spanner backend.

Scenarios:
1. Point select with single concurrency (Concurrency = 1, Sync SDK, Pure CPU Clock)
2. Point select with 32 concurrency (Concurrency = 32, Async SDK with Full Row Parsing, Pure CPU Clock)
3. LIMIT 1000 read for an 11-column table (AsyncBenchmarkTable, Sync SDK, Pure CPU Clock)

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
from google.cloud import spanner_v1
from google.cloud.spanner_v1 import _helpers
from google.cloud.spanner_v1 import param_types
from google.cloud.spanner_v1.services.spanner.async_client import SpannerAsyncClient
from google.cloud.spanner_v1.types import ExecuteSqlRequest
from google.cloud.spanner_v1.types.result_set import PartialResultSet

try:
    from google.cloud.spanner_v1._async.client import Client as HighLevelAsyncClient
    from google.cloud.spanner_v1._async.pool import BurstyPool as AsyncBurstyPool
except ImportError:
    try:
        from google.cloud.spanner_v1 import AsyncClient as HighLevelAsyncClient
        from google.cloud.spanner_v1 import AsyncBurstyPool
    except ImportError:
        HighLevelAsyncClient = None
        AsyncBurstyPool = None

PROJECT = "span-cloud-testing"
INSTANCE = "suvham-testing"
DATABASE = "benchmark_db_async"
TABLE = "AsyncBenchmarkTable"
DB_PATH = f"projects/{PROJECT}/instances/{INSTANCE}/databases/{DATABASE}"

WARMUP_DURATION_SEC = 5.0
PROFILE_DURATION_SEC = 10.0


# -----------------------------------------------------------------------------
# Scenario 1 & 3: Synchronous Client Queries (High-Level SDK)
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
# Scenario 2: Async Client with Full Row Parsing (32 Concurrency)
# -----------------------------------------------------------------------------
async def run_single_async_query_with_parsing(async_client, session_name, user_id="user-0"):
    request = ExecuteSqlRequest(
        session=session_name,
        sql=f"SELECT * FROM {TABLE} WHERE id = '{user_id}'",
    )
    stream = await async_client.execute_streaming_sql(request=request)
    
    # Fully decode rows into Python objects (measuring real customer row deserialization)
    rows = []
    metadata = None
    width = 0
    current_row = []
    
    async for partial_result_set in stream:
        pb = PartialResultSet.pb(partial_result_set)
        if metadata is None and pb.metadata.row_type.fields:
            metadata = pb.metadata
            fields = metadata.row_type.fields
            width = len(fields)
        
        if metadata and pb.values:
            fields = metadata.row_type.fields
            index = len(current_row)
            for val in pb.values:
                f = fields[index]
                parsed_val = _helpers._parse_value_pb(val, f.type_, f.name)
                current_row.append(parsed_val)
                index += 1
                if index == width:
                    rows.append(current_row)
                    current_row = []
                    index = 0
    return len(rows)


async def async_worker_loop_gapic(async_client, session_name, worker_id, stop_time):
    count = 0
    while time.time() < stop_time:
        await run_single_async_query_with_parsing(async_client, session_name, f"user-{worker_id % 100}")
        count += 1
    return count


async def run_single_async_query_high_level(async_database, user_id="user-0"):
    async with async_database.snapshot() as snapshot:
        results = await snapshot.execute_sql(
            f"SELECT * FROM {TABLE} WHERE id = @id",
            params={"id": user_id},
            param_types={"id": param_types.STRING},
        )
        rows = [row async for row in results]
        return len(rows)


async def async_worker_loop_high_level(async_database, worker_id, stop_time):
    count = 0
    while time.time() < stop_time:
        await run_single_async_query_high_level(async_database, f"user-{worker_id % 100}")
        count += 1
    return count


async def execute_async_scenario_2(output_prof_path, concurrency=32):
    print("\n" + "=" * 80)
    print(f"SCENARIO 2: Real Spanner Async Client with {concurrency} Concurrency (C={concurrency}, Full Row Parsing, Pure CPU Clock)")
    print("=" * 80)

    use_high_level = HighLevelAsyncClient is not None
    if use_high_level:
        print(f"[*] Initializing high-level spanner_v1.AsyncClient for {PROJECT} / {INSTANCE} / {DATABASE}...")
        async_client = HighLevelAsyncClient(project=PROJECT)
        async_instance = async_client.instance(INSTANCE)
        pool = AsyncBurstyPool(target_size=concurrency) if AsyncBurstyPool else None
        async_database = async_instance.database(DATABASE, pool=pool) if pool else async_instance.database(DATABASE)
        worker_fn = lambda wid, st: async_worker_loop_high_level(async_database, wid, st)
    else:
        print(f"[*] Initializing SpannerAsyncClient (grpc.aio transport) for {DB_PATH}...")
        async_client = SpannerAsyncClient()
        print(f"[*] Creating async sessions for {concurrency} workers...")
        sessions = await asyncio.gather(*[async_client.create_session(database=DB_PATH) for _ in range(concurrency)])
        session_names = [s.name for s in sessions]
        print(f"[+] Successfully created {len(session_names)} async sessions.")
        worker_fn = lambda wid, st: async_worker_loop_gapic(async_client, session_names[wid], wid, st)

    # 1. Warmup for 5 seconds across 32 concurrent coroutines
    print(f"[*] Warming up {concurrency} concurrent coroutines on event loop for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC
    warmup_tasks = [worker_fn(i, warmup_end) for i in range(concurrency)]
    warmup_results = await asyncio.gather(*warmup_tasks)
    print(f"[+] Warmup completed: {sum(warmup_results)} total requests executed across {concurrency} coroutines.")

    # 2. Profile pure CPU time across all 32 coroutines
    print(f"[*] Profiling pure CPU time across all {concurrency} coroutines for {PROFILE_DURATION_SEC} seconds...")
    yappi.set_clock_type("cpu")
    yappi.clear_stats()
    yappi.start()

    prof_end = time.time() + PROFILE_DURATION_SEC
    profile_tasks = [worker_fn(i, prof_end) for i in range(concurrency)]
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
# Scenario 3: LIMIT 1000 Read (Sync SDK, CPU Clock)
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

    print(f"Initializing Sync Spanner Client for {PROJECT} / {INSTANCE} / {DATABASE}...")
    client = spanner.Client(project=PROJECT)
    instance = client.instance(INSTANCE)
    database = instance.database(DATABASE)

    f1 = os.path.join(output_dir, "spanner_point_select_c1.prof")
    ps1, cnt1 = run_scenario_1_point_select_c1(database, f1)
    print_summary_table(ps1, "Scenario 1: Point Select C=1 (Real Spanner, Pure CPU)", cnt1)

    f2 = os.path.join(output_dir, "spanner_point_select_c32.prof")
    ps2, cnt2 = run_scenario_2_point_select_c32_async(f2, concurrency=32)
    print_summary_table(ps2, "Scenario 2: Point Select C=32 (Real Spanner, Async Full Row Parsing)", cnt2)

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
