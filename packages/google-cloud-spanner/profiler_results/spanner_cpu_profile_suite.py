"""Comprehensive CPU Profiler Suite for Google Cloud Spanner.

Scenarios:
1. Point select with single concurrency (Concurrency = 1)
2. Point select with 32 concurrency (Concurrency = 32)
3. LIMIT 1000 read for a 12-column table (AsyncBenchmarkTable)

Includes:
- 5-second connection/runtime warmup before recording
- 5ms mock database/server sleep per RPC
- Output of .prof binary profile files and formatted text summaries
"""

import asyncio
import cProfile
import io
import os
import pstats
import time
from unittest import mock

from google.api_core import gapic_v1
from google.cloud.spanner_v1 import (
    param_types,
    Type,
    TypeCode,
    StructType,
    ResultSetMetadata,
    PartialResultSet,
)
from google.cloud.spanner_v1.snapshot import Snapshot
from google.cloud.spanner_v1._helpers import _make_value_pb

PROJECT = "span-cloud-testing"
INSTANCE = "suvham-testing"
DATABASE = "benchmark_db_async"
TABLE = "AsyncBenchmarkTable"

WARMUP_DURATION_SEC = 5.0
PROFILE_DURATION_SEC = 10.0
DB_SLEEP_SEC = 0.005  # 5ms mock database sleep


def create_12_column_metadata():
    """Builds ResultSetMetadata with 12 distinct Spanner column types."""
    return ResultSetMetadata(
        row_type=StructType(
            fields=[
                StructType.Field(name="Id", type_=Type(code=TypeCode.INT64)),
                StructType.Field(name="Name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="Email", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="Age", type_=Type(code=TypeCode.INT64)),
                StructType.Field(name="Score", type_=Type(code=TypeCode.FLOAT64)),
                StructType.Field(name="Balance", type_=Type(code=TypeCode.FLOAT64)),
                StructType.Field(name="IsActive", type_=Type(code=TypeCode.BOOL)),
                StructType.Field(name="Payload", type_=Type(code=TypeCode.BYTES)),
                StructType.Field(
                    name="Tags",
                    type_=Type(
                        code=TypeCode.ARRAY,
                        array_element_type=Type(code=TypeCode.STRING),
                    ),
                ),
                StructType.Field(name="Metadata", type_=Type(code=TypeCode.JSON)),
                StructType.Field(name="CreatedAt", type_=Type(code=TypeCode.TIMESTAMP)),
                StructType.Field(name="UpdatedAt", type_=Type(code=TypeCode.TIMESTAMP)),
            ]
        )
    )


def create_point_select_response():
    """Builds a PartialResultSet for a single 12-column row."""
    metadata = create_12_column_metadata()
    partial_rs = PartialResultSet(
        metadata=metadata,
        resume_token=b"resume-token-point-select",
    )

    values = [
        _make_value_pb(12345),
        _make_value_pb("Alice Smith"),
        _make_value_pb("alice.smith@example.com"),
        _make_value_pb(30),
        _make_value_pb(98.5),
        _make_value_pb(1500.75),
        _make_value_pb(True),
        _make_value_pb(b"sample_payload_bytes_data"),
        _make_value_pb(["admin", "engineering", "us-central"]),
        _make_value_pb('{"tier": "gold", "cluster": "us-central1"}'),
        _make_value_pb("2026-08-25T12:00:00.000000Z"),
        _make_value_pb("2026-08-26T06:00:00.000000Z"),
    ]
    for v in values:
        partial_rs.values.append(v)
    return partial_rs


def create_limit_1000_response(num_rows=1000):
    """Builds PartialResultSet stream for 1000 rows across chunks."""
    metadata = create_12_column_metadata()
    
    chunks = []
    chunk_size = 100
    for chunk_idx in range(num_rows // chunk_size):
        rs = PartialResultSet(
            metadata=metadata if chunk_idx == 0 else None,
            resume_token=f"token-{chunk_idx}".encode("utf-8"),
        )
        for r in range(chunk_size):
            row_id = chunk_idx * chunk_size + r + 1
            values = [
                _make_value_pb(row_id),
                _make_value_pb(f"User_{row_id}"),
                _make_value_pb(f"user_{row_id}@example.com"),
                _make_value_pb(20 + (r % 50)),
                _make_value_pb(75.0 + (r % 25)),
                _make_value_pb(1000.0 + r * 10.5),
                _make_value_pb(r % 2 == 0),
                _make_value_pb(b"payload_bytes_data_block"),
                _make_value_pb(["tag1", "tag2", "tag3"]),
                _make_value_pb('{"tier": "standard", "region": "us-central1"}'),
                _make_value_pb("2026-08-25T12:00:00.000000Z"),
                _make_value_pb("2026-08-26T06:00:00.000000Z"),
            ]
            for v in values:
                rs.values.append(v)
        chunks.append(rs)
    return chunks


class MockGapicClient:
    """Mock GAX client with 5ms database sleep time."""
    def __init__(self, response_chunks):
        self._chunks = response_chunks if isinstance(response_chunks, list) else [response_chunks]

    def execute_streaming_sql(self, request=None, retry=gapic_v1.method.DEFAULT, timeout=gapic_v1.method.DEFAULT, metadata=None):
        time.sleep(DB_SLEEP_SEC)  # 5ms mock server/database latency
        return iter(self._chunks)


class SimpleMockDatabase:
    def __init__(self, spanner_api):
        self.spanner_api = spanner_api
        self._spanner_api = spanner_api
        self.name = f"projects/{PROJECT}/instances/{INSTANCE}/databases/{DATABASE}"
        self.default_query_options = None
        self._default_query_options = None
        self.directed_read_options = None
        self._directed_read_options = None
        self.observability_options = None
        self._observability_options = None
        self.database_role = None
        self._database_role = None
        self.tracing_enabled = False
        self._instance = mock.MagicMock()
        self._instance._client._query_options = None


class SimpleMockSession:
    def __init__(self, database):
        self._database = database
        self.name = f"projects/{PROJECT}/instances/{INSTANCE}/databases/{DATABASE}/sessions/s12345"


def run_single_query(session, sql, params, param_types_dict):
    snapshot = Snapshot(session)
    stream = snapshot.execute_sql(
        sql=sql,
        params=params,
        param_types=param_types_dict,
    )
    rows = list(stream)
    return len(rows)


def run_scenario_1_point_select_c1(output_prof_path):
    """Scenario 1: Point select with Concurrency = 1."""
    print("\n" + "=" * 80)
    print("SCENARIO 1: Point Select with Single Concurrency (C=1)")
    print("=" * 80)

    response_proto = create_point_select_response()
    gapic_client = MockGapicClient(response_proto)
    database = SimpleMockDatabase(gapic_client)
    session = SimpleMockSession(database)

    sql = f"SELECT Id, Name, Email, Age, Score, Balance, IsActive, Payload, Tags, Metadata, CreatedAt, UpdatedAt FROM {TABLE} WHERE Id = @id"
    params = {"id": 12345}
    param_types_dict = {"id": param_types.INT64}

    # 1. Warmup for 5 seconds
    print(f"[*] Warming up connection and client for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC
    warmup_count = 0
    while time.time() < warmup_end:
        run_single_query(session, sql, params, param_types_dict)
        warmup_count += 1
    print(f"[+] Warmup completed: {warmup_count} requests executed.")

    # 2. Profile for PROFILE_DURATION_SEC
    print(f"[*] Profiling for {PROFILE_DURATION_SEC} seconds...")
    pr = cProfile.Profile()
    pr.enable()

    prof_end = time.time() + PROFILE_DURATION_SEC
    recorded_count = 0
    while time.time() < prof_end:
        run_single_query(session, sql, params, param_types_dict)
        recorded_count += 1

    pr.disable()
    print(f"[+] Profiling finished: {recorded_count} requests recorded.")

    pr.dump_stats(output_prof_path)
    print(f"[+] Saved profile stats to: {output_prof_path}")
    return pstats.Stats(pr), recorded_count


async def run_async_benchmark_c32(session, sql, params, param_types_dict, concurrency, duration_sec):
    end_time = time.time() + duration_sec
    total_counts = [0] * concurrency

    async def worker(worker_id):
        count = 0
        while time.time() < end_time:
            # Run query processing
            run_single_query(session, sql, params, param_types_dict)
            # Yield to event loop to simulate async I/O sleep
            await asyncio.sleep(DB_SLEEP_SEC)
            count += 1
        total_counts[worker_id] = count

    tasks = [asyncio.create_task(worker(i)) for i in range(concurrency)]
    await asyncio.gather(*tasks)
    return sum(total_counts)


def run_scenario_2_point_select_c32(output_prof_path, concurrency=32):
    """Scenario 2: Point select with Concurrency = 32."""
    print("\n" + "=" * 80)
    print(f"SCENARIO 2: Point Select with {concurrency} Concurrency (C={concurrency})")
    print("=" * 80)

    # For async concurrency, gapic client returns chunks without blocking sync sleep
    response_proto = create_point_select_response()
    
    class NonBlockingMockGapicClient:
        def __init__(self, response_proto):
            self._proto = response_proto

        def execute_streaming_sql(self, *args, **kwargs):
            return iter([self._proto])

    gapic_client = NonBlockingMockGapicClient(response_proto)
    database = SimpleMockDatabase(gapic_client)
    session = SimpleMockSession(database)

    sql = f"SELECT Id, Name, Email, Age, Score, Balance, IsActive, Payload, Tags, Metadata, CreatedAt, UpdatedAt FROM {TABLE} WHERE Id = @id"
    params = {"id": 12345}
    param_types_dict = {"id": param_types.INT64}

    # 1. Warmup for 5 seconds
    print(f"[*] Warming up across {concurrency} workers for {WARMUP_DURATION_SEC} seconds...")
    warmup_count = asyncio.run(
        run_async_benchmark_c32(session, sql, params, param_types_dict, concurrency, WARMUP_DURATION_SEC)
    )
    print(f"[+] Warmup completed: {warmup_count} requests executed.")

    # 2. Profile for PROFILE_DURATION_SEC
    print(f"[*] Profiling across {concurrency} workers for {PROFILE_DURATION_SEC} seconds...")
    pr = cProfile.Profile()
    pr.enable()

    recorded_count = asyncio.run(
        run_async_benchmark_c32(session, sql, params, param_types_dict, concurrency, PROFILE_DURATION_SEC)
    )

    pr.disable()
    print(f"[+] Profiling finished: {recorded_count} requests recorded across {concurrency} workers.")

    pr.dump_stats(output_prof_path)
    print(f"[+] Saved profile stats to: {output_prof_path}")
    return pstats.Stats(pr), recorded_count


def run_scenario_3_limit_1000_c1(output_prof_path):
    """Scenario 3: LIMIT 1000 Read for 12-column table."""
    print("\n" + "=" * 80)
    print("SCENARIO 3: LIMIT 1000 Read for 12-Column Table (AsyncBenchmarkTable)")
    print("=" * 80)

    chunks = create_limit_1000_response(num_rows=1000)
    gapic_client = MockGapicClient(chunks)
    database = SimpleMockDatabase(gapic_client)
    session = SimpleMockSession(database)

    sql = f"SELECT Id, Name, Email, Age, Score, Balance, IsActive, Payload, Tags, Metadata, CreatedAt, UpdatedAt FROM {TABLE} LIMIT 1000"

    # 1. Warmup for 5 seconds
    print(f"[*] Warming up LIMIT 1000 stream for {WARMUP_DURATION_SEC} seconds...")
    warmup_end = time.time() + WARMUP_DURATION_SEC
    warmup_count = 0
    while time.time() < warmup_end:
        rows_read = run_single_query(session, sql, params={}, param_types_dict={})
        assert rows_read == 1000
        warmup_count += 1
    print(f"[+] Warmup completed: {warmup_count} queries ({warmup_count * 1000} rows) executed.")

    # 2. Profile for PROFILE_DURATION_SEC
    print(f"[*] Profiling LIMIT 1000 for {PROFILE_DURATION_SEC} seconds...")
    pr = cProfile.Profile()
    pr.enable()

    prof_end = time.time() + PROFILE_DURATION_SEC
    recorded_count = 0
    while time.time() < prof_end:
        rows_read = run_single_query(session, sql, params={}, param_types_dict={})
        assert rows_read == 1000
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
    print(f"Total Requests: {request_count} | Total CPU Time: {ps.total_tt:.4f} s | Avg CPU/Query: {(ps.total_tt / request_count) * 1000:.3f} ms")
    print("-" * 80)
    ps.sort_stats("cumulative").print_stats(15)
    print(s.getvalue())


def main():
    output_dir = "/tmp/spanner_profiles"
    os.makedirs(output_dir, exist_ok=True)

    f1 = os.path.join(output_dir, "spanner_point_select_c1.prof")
    ps1, cnt1 = run_scenario_1_point_select_c1(f1)
    print_summary_table(ps1, "Scenario 1: Point Select C=1", cnt1)

    f2 = os.path.join(output_dir, "spanner_point_select_c32.prof")
    ps2, cnt2 = run_scenario_2_point_select_c32(f2)
    print_summary_table(ps2, "Scenario 2: Point Select C=32", cnt2)

    f3 = os.path.join(output_dir, "spanner_limit1000_c1.prof")
    ps3, cnt3 = run_scenario_3_limit_1000_c1(f3)
    print_summary_table(ps3, "Scenario 3: LIMIT 1000 Read (12 columns)", cnt3)

    print("\n" + "=" * 80)
    print("ALL PROFILES GENERATED SUCCESSFULLY:")
    print(f"1. {f1}")
    print(f"2. {f2}")
    print(f"3. {f3}")
    print("=" * 80)


if __name__ == "__main__":
    main()
