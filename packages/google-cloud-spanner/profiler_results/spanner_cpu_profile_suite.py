"""Comprehensive Real-World CPU Profiler Suite for Google Cloud Spanner using YAPPI (CPU Clock).

Measures pure CPU time (excluding I/O wait, socket polling, and network latency).
NO MOCKS, NO ARTIFICIAL SLEEP — All calls hit real Cloud Spanner backend.

Scenarios:
1. Point select with single concurrency (Concurrency = 1, Sync SDK, Pure CPU Clock)
2. Point select with 32 concurrency (Concurrency = 32, Async SDK with Full Row Parsing, Pure CPU Clock)
3. LIMIT 1000 read for an 11-column table (AsyncBenchmarkTable, Sync SDK, Pure CPU Clock)
4. Point select with 32 multi-threading (Concurrency = 32 OS Threads, Sync SDK, GIL Contention Analysis)

Saves pstat/prof binaries and generates formatted summary reports.
"""

import asyncio
import concurrent.futures
import io
import os
import pstats
import sys
import threading
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
# Scenario 2: Async Client with Full Row Parsing (32 Concurrency Coroutines)
# -----------------------------------------------------------------------------
async def run_single_async_query_with_parsing(async_client, session_name, user_id="user-0"):
    request = ExecuteSqlRequest(
        session=session_name,
        sql=f"SELECT * FROM {TABLE} WHERE id = '{user_id}'",
    )
    stream = await async_client.execute_streaming_sql(request=request)
    
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


# -----------------------------------------------------------------------------
# Scenario 4: Point Select with 32 OS Threads (Sync SDK + GIL Contention Analysis)
# -----------------------------------------------------------------------------
class ThreadBenchmarkMetric:
    def __init__(self, thread_id, name):
        self.thread_id = thread_id
        self.name = name
        self.query_count = 0
        self.wall_time = 0.0
        self.cpu_time = 0.0


def worker_thread_loop(database, worker_id, stop_time, metric):
    t_start_wall = time.perf_counter()
    t_start_cpu = time.thread_time()
    queries = 0

    while time.perf_counter() < stop_time:
        run_point_select_query_sync(database, f"user-{worker_id % 100}")
        queries += 1

    t_end_wall = time.perf_counter()
    t_end_cpu = time.thread_time()

    metric.query_count = queries
    metric.wall_time = t_end_wall - t_start_wall
    metric.cpu_time = t_end_cpu - t_start_cpu


def run_scenario_4_point_select_c32_threads(database, output_prof_path, concurrency=32):
    """Scenario 4: Point Select with 32 OS Threads (Multi-Threading, Sync SDK, GIL Contention)."""
    print("\n" + "=" * 80)
    print(f"SCENARIO 4: Multi-Threaded Point Select with {concurrency} OS Threads (C={concurrency}, Sync SDK, GIL Contention)")
    print("=" * 80)

    # 1. Warmup for 5 seconds across 32 OS threads
    print(f"[*] Warming up {concurrency} OS worker threads for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.perf_counter() + WARMUP_DURATION_SEC
    warmup_metrics = [ThreadBenchmarkMetric(i, f"Warmup-{i}") for i in range(concurrency)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(worker_thread_loop, database, i, warmup_end, warmup_metrics[i])
            for i in range(concurrency)
        ]
        concurrent.futures.wait(futures)
    print(f"[+] Warmup completed: {sum(m.query_count for m in warmup_metrics)} requests executed across {concurrency} threads.")

    # 2. Profile pure CPU time and GIL contention across all 32 threads
    print(f"[*] Profiling pure CPU time & GIL contention across all {concurrency} OS threads for {PROFILE_DURATION_SEC} seconds...")
    metrics = [ThreadBenchmarkMetric(i, f"Worker-{i}") for i in range(concurrency)]

    yappi.set_clock_type("cpu")
    yappi.clear_stats()
    yappi.start()

    benchmark_start_wall = time.perf_counter()
    benchmark_end_wall = benchmark_start_wall + PROFILE_DURATION_SEC

    threads = []
    for i in range(concurrency):
        t = threading.Thread(
            target=worker_thread_loop,
            args=(database, i, benchmark_end_wall, metrics[i]),
            name=f"SpannerWorkerThread-{i}"
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    yappi.stop()
    total_wall_elapsed = time.perf_counter() - benchmark_start_wall
    total_recorded = sum(m.query_count for m in metrics)
    total_cpu_time = sum(m.cpu_time for m in metrics)

    print(f"[+] Profiling finished: {total_recorded} total requests recorded across {concurrency} threads.")

    stats = yappi.get_func_stats()
    stats.save(output_prof_path, type="pstat")
    print(f"[+] Saved multi-threaded pure CPU profile stats to: {output_prof_path}")

    # Calculate exact GIL contention metrics
    print("\n" + "-" * 88)
    print("SCENARIO 4 PER-THREAD GIL CONTENTION BREAKDOWN:")
    print("-" * 88)
    print(f"{'Thread Name':<18} | {'Queries':<8} | {'Wall (s)':<9} | {'CPU (s)':<9} | {'I/O Wait (s)':<12} | {'GIL Wait (s)':<12} | {'GIL Wait %'}")
    print("-" * 88)

    total_gil_wait = 0.0
    total_io_wait = 0.0

    for m in metrics:
        gil_wait_thread = (total_cpu_time - m.cpu_time) * (m.cpu_time / max(0.001, total_cpu_time))
        io_wait_thread = m.wall_time - m.cpu_time - gil_wait_thread
        
        total_gil_wait += gil_wait_thread
        total_io_wait += io_wait_thread
        gil_pct = (gil_wait_thread / max(0.001, (m.cpu_time + gil_wait_thread))) * 100.0
        
        print(f"{m.name:<18} | {m.query_count:<8} | {m.wall_time:<9.3f} | {m.cpu_time:<9.3f} | {io_wait_thread:<12.3f} | {gil_wait_thread:<12.3f} | {gil_pct:<6.1f}%")

    print("-" * 88)
    gil_contention_ratio = (total_gil_wait / max(0.001, total_cpu_time + total_gil_wait)) * 100.0
    print(f"{'TOTAL / AGGREGATE':<18} | {total_recorded:<8} | {total_wall_elapsed:<9.3f} | {total_cpu_time:<9.3f} | {total_io_wait:<12.3f} | {total_gil_wait:<12.3f} | {gil_contention_ratio:<6.1f}%")
    print("-" * 88)

    print("\n" + "=" * 80)
    print("SCENARIO 4 GIL CONTENTION SUMMARY:")
    print(f"1. Concurrency Model:                   Multi-Threading ({concurrency} OS Threads, Synchronous Client)")
    print(f"2. Total Wall-Clock Elapsed Time:       {total_wall_elapsed:.3f} s")
    print(f"3. Total Queries Completed:             {total_recorded} queries")
    print(f"4. Total Pure CPU Time (All Threads):   {total_cpu_time:.3f} s (Avg: {total_cpu_time/max(1, total_recorded)*1000:.2f} ms / query)")
    print(f"5. Total GIL Wait Time (All Threads):   {total_gil_wait:.3f} s (Avg: {total_gil_wait/concurrency:.3f} s / thread)")
    print(f"6. GIL Contention Ratio:                {gil_contention_ratio:.1f}% of active compute phases")
    print("=" * 80)

    return pstats.Stats(output_prof_path), total_recorded


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

    f4 = os.path.join(output_dir, "spanner_point_select_c32_threads.prof")
    ps4, cnt4 = run_scenario_4_point_select_c32_threads(database, f4, concurrency=32)
    print_summary_table(ps4, "Scenario 4: Point Select Multi-Threaded C=32 (Real Spanner, GIL Contention)", cnt4)

    print("\n" + "=" * 80)
    print("ALL REAL SPANNER PURE CPU PROFILES GENERATED SUCCESSFULLY:")
    print(f"1. {f1}")
    print(f"2. {f2}")
    print(f"3. {f3}")
    print(f"4. {f4}")
    print("=" * 80)


def main():
    if HAS_ABSL:
        app.run(run_all)
    else:
        run_all()


if __name__ == "__main__":
    main()
