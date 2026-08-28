"""Comprehensive Real-World CPU Profiler Suite for Google Cloud Spanner.

Makes actual network calls against Cloud Spanner (NO MOCKS, NO ARTIFICIAL SLEEP).

Scenarios:
1. Point select with single concurrency (Concurrency = 1)
2. Point select with 32 concurrency (Concurrency = 32)
3. LIMIT 1000 read for a >10 column table (AsyncBenchmarkTable)

Includes:
- 5-second connection/runtime warmup before recording
- Real GAPIC, gRPC, network, and auth execution
- Output of .prof binary profile files and formatted text summaries
"""

import concurrent.futures
import cProfile
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

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

PROJECT = "span-cloud-testing"
INSTANCE = "suvham-testing"
DATABASE = "benchmark_db_async"
TABLE = "AsyncBenchmarkTable"

WARMUP_DURATION_SEC = 5.0
PROFILE_DURATION_SEC = 10.0


def run_point_select_query(database, user_id="user-0"):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            f"SELECT * FROM {TABLE} WHERE id = @id",
            params={"id": user_id},
            param_types={"id": param_types.STRING},
        )
        rows = list(results)
        return len(rows)


def run_limit_1000_query(database):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(f"SELECT * FROM {TABLE} LIMIT 1000")
        rows = list(results)
        return len(rows)


def run_scenario_1_point_select_c1(database, output_prof_path):
    """Scenario 1: Point select with Concurrency = 1 (Real Spanner)."""
    print("\n" + "=" * 80)
    print("SCENARIO 1: Real Point Select with Single Concurrency (C=1)")
    print("=" * 80)

    # 1. Warmup for 5 seconds
    print(f"[*] Warming up connection to Spanner for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC
    warmup_count = 0
    while time.time() < warmup_end:
        run_point_select_query(database, "user-0")
        warmup_count += 1
    print(f"[+] Warmup completed: {warmup_count} requests executed.")

    # 2. Profile for PROFILE_DURATION_SEC
    print(f"[*] Profiling for {PROFILE_DURATION_SEC} seconds...")
    pr = cProfile.Profile()
    pr.enable()

    prof_end = time.time() + PROFILE_DURATION_SEC
    recorded_count = 0
    while time.time() < prof_end:
        run_point_select_query(database, "user-0")
        recorded_count += 1

    pr.disable()
    print(f"[+] Profiling finished: {recorded_count} requests recorded.")

    pr.dump_stats(output_prof_path)
    print(f"[+] Saved profile stats to: {output_prof_path}")
    return pstats.Stats(pr), recorded_count


def run_scenario_2_point_select_c32(database, output_prof_path, concurrency=32):
    """Scenario 2: Point select with Concurrency = 32 (Real Spanner)."""
    print("\n" + "=" * 80)
    print(f"SCENARIO 2: Real Point Select with {concurrency} Concurrency (C={concurrency})")
    print("=" * 80)

    # 1. Warmup for 5 seconds
    print(f"[*] Warming up across {concurrency} workers for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC

    def worker_warmup(worker_id):
        count = 0
        while time.time() < warmup_end:
            run_point_select_query(database, f"user-{worker_id % 100}")
            count += 1
        return count

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(worker_warmup, i) for i in range(concurrency)]
        warmup_count = sum(f.result() for f in futures)
    print(f"[+] Warmup completed: {warmup_count} requests executed.")

    # 2. Profile for PROFILE_DURATION_SEC
    print(f"[*] Profiling across {concurrency} workers for {PROFILE_DURATION_SEC} seconds...")
    pr = cProfile.Profile()
    prof_end = time.time() + PROFILE_DURATION_SEC

    def worker_profile(worker_id):
        count = 0
        while time.time() < prof_end:
            run_point_select_query(database, f"user-{worker_id % 100}")
            count += 1
        return count

    pr.enable()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(worker_profile, i) for i in range(concurrency)]
        recorded_count = sum(f.result() for f in futures)
    pr.disable()

    print(f"[+] Profiling finished: {recorded_count} requests recorded across {concurrency} workers.")
    pr.dump_stats(output_prof_path)
    print(f"[+] Saved profile stats to: {output_prof_path}")
    return pstats.Stats(pr), recorded_count


def run_scenario_3_limit_1000_c1(database, output_prof_path):
    """Scenario 3: LIMIT 1000 Read for 11-column table (Real Spanner)."""
    print("\n" + "=" * 80)
    print("SCENARIO 3: Real LIMIT 1000 Read for AsyncBenchmarkTable")
    print("=" * 80)

    # 1. Warmup for 5 seconds
    print(f"[*] Warming up LIMIT 1000 stream for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC
    warmup_count = 0
    while time.time() < warmup_end:
        rows_read = run_limit_1000_query(database)
        warmup_count += 1
    print(f"[+] Warmup completed: {warmup_count} queries ({warmup_count * 1000} rows) executed.")

    # 2. Profile for PROFILE_DURATION_SEC
    print(f"[*] Profiling LIMIT 1000 for {PROFILE_DURATION_SEC} seconds...")
    pr = cProfile.Profile()
    pr.enable()

    prof_end = time.time() + PROFILE_DURATION_SEC
    recorded_count = 0
    while time.time() < prof_end:
        rows_read = run_limit_1000_query(database)
        recorded_count += 1

    pr.disable()
    print(f"[+] Profiling finished: {recorded_count} queries ({recorded_count * 1000} rows) recorded.")

    pr.dump_stats(output_prof_path)
    print(f"[+] Saved profile stats to: {output_prof_path}")
    return pstats.Stats(pr), recorded_count


def print_summary_table(ps, title, request_count):
    s = io.StringIO()
    ps.stream = s
    ps.strip_dirs()
    print("\n" + "-" * 80)
    print(f"SUMMARY FOR: {title}")
    print(f"Total Requests: {request_count} | Total CPU Time: {ps.total_tt:.4f} s | Avg CPU/Query: {(ps.total_tt / max(1, request_count)) * 1000:.3f} ms")
    print("-" * 80)
    ps.sort_stats("cumulative").print_stats(15)
    print(s.getvalue())


def run_all(argv=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = script_dir if os.path.exists(os.path.join(script_dir, "README.md")) else "/usr/local/google/home/suvham/workspace/cloudPython/google-cloud-python/packages/google-cloud-spanner/profiler_results"
    os.makedirs(output_dir, exist_ok=True)

    print(f"Initializing Spanner Client for {PROJECT} / {INSTANCE} / {DATABASE}...")
    client = spanner.Client(project=PROJECT)
    instance = client.instance(INSTANCE)
    database = instance.database(DATABASE)

    f1 = os.path.join(output_dir, "spanner_point_select_c1.prof")
    ps1, cnt1 = run_scenario_1_point_select_c1(database, f1)
    print_summary_table(ps1, "Scenario 1: Point Select C=1 (Real Spanner)", cnt1)

    f2 = os.path.join(output_dir, "spanner_point_select_c32.prof")
    ps2, cnt2 = run_scenario_2_point_select_c32(database, f2)
    print_summary_table(ps2, "Scenario 2: Point Select C=32 (Real Spanner)", cnt2)

    f3 = os.path.join(output_dir, "spanner_limit1000_c1.prof")
    ps3, cnt3 = run_scenario_3_limit_1000_c1(database, f3)
    print_summary_table(ps3, "Scenario 3: LIMIT 1000 Read (Real Spanner)", cnt3)

    print("\n" + "=" * 80)
    print("ALL REAL SPANNER PROFILES GENERATED SUCCESSFULLY:")
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
