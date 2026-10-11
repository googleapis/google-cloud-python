"""Comprehensive Cross-FFI CPU Profiler Suite for Google Cloud Spanner (Stock Python vs Go Shared Core).

Measures pure CPU time (excluding I/O wait, socket polling, and network latency) across BOTH:
- Flow A: Without Shared Core (Stock Python SDK: GAPIC + grpcio + Python Protobuf + _parse_value_pb)
- Flow B: With Go Shared Core (Cross-FFI: Python -> C ABI3 Extension -> Go Shared Core libspanner_go.so)

Cross-FFI Profiling Architecture:
1. Yappi (`set_clock_type("cpu")`, `builtins=True`): Captures exact `CLOCK_THREAD_CPUTIME_ID` for all Python
   frames and C-extension entry points (`spanner_go_ext.execute_streaming_sql`, `submit_async`, `pop_completed`).
2. Go Shared Core Deterministic `CLOCK_THREAD_CPUTIME_ID` Phase Counters + `runtime/pprof`:
   Captures exact nanosecond thread CPU time inside `libspanner_go.so` across Request/Auth serialization,
   `ExecuteStreamingSql` stream init, `stream.Recv` + Protobuf unmarshaling, chunked row assembly,
   and zero-copy `CSpannerCell` arena encoding, alongside statistical `runtime/pprof` (`.pprof`) stacks.
3. Linux Kernel Whole-Process & Per-Thread CPU Accounting (`RUSAGE_SELF` + `/proc/self/task/<tid>/stat`):
   Captures 100% of user + system CPU time across all OS threads (including background Go `M` threads
   running HTTP/2 `http2Client.reader`, `loopyWriter`, and `crypto/tls`, as well as `grpcio` C++ executor threads).
4. Cross-FFI `pstats` & Flame Graph Stitching:
   Stitches the C-extension and Go Shared Core call hierarchy directly into the `.prof` (`pstats`) files
   so `pstats` tables and interactive HTML flame graphs display the unified Python -> C FFI -> Go call stack.
"""

import argparse
import asyncio
import concurrent.futures
import io
import json
import marshal
import os
import pstats
import resource
import subprocess
import sys
import threading
import time
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GO_CORE_DIR = os.path.join(SCRIPT_DIR, "spanner_go_core")
if GO_CORE_DIR not in sys.path:
    sys.path.insert(0, GO_CORE_DIR)

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
except ImportError:
    try:
        from google.cloud.spanner_v1 import AsyncClient as HighLevelAsyncClient
    except ImportError:
        HighLevelAsyncClient = None

try:
    from google.cloud.spanner_v1._async.pool import BurstyPool as AsyncBurstyPool
except ImportError:
    try:
        from google.cloud.spanner_v1 import AsyncBurstyPool
    except ImportError:
        AsyncBurstyPool = None

PROJECT = "span-cloud-testing"
INSTANCE = "suvham-testing"
DATABASE = "benchmark_db_async"
TABLE = "AsyncBenchmarkTable"
DB_PATH = f"projects/{PROJECT}/instances/{INSTANCE}/databases/{DATABASE}"
POINT_SELECT_SQL = f"SELECT * FROM {TABLE} WHERE id = @id"
LIMIT_1000_SQL = f"SELECT * FROM {TABLE} LIMIT 1000"

WARMUP_DURATION_SEC = 5.0
PROFILE_DURATION_SEC = 10.0


def ensure_go_shared_core():
    """Imports spanner_go_ext, automatically building it via build_go_core.sh if needed."""
    try:
        import spanner_go_ext
        # Verify dlopen of libspanner_go.so works on this machine's glibc
        fd = spanner_go_ext.get_notify_fd()
        if fd >= 0:
            return spanner_go_ext
    except Exception as first_err:
        build_script = os.path.join(GO_CORE_DIR, "build_go_core.sh")
        if os.path.exists(build_script):
            print(f"[*] Rebuilding Go Shared Core for current host ({first_err})...")
            subprocess.run(["bash", build_script], check=True)
            import importlib
            if "spanner_go_ext" in sys.modules:
                del sys.modules["spanner_go_ext"]
            import spanner_go_ext
            return spanner_go_ext
        raise RuntimeError(f"Failed to load spanner_go_ext: {first_err}") from first_err
    import spanner_go_ext
    return spanner_go_ext


# -----------------------------------------------------------------------------
# Kernel-Level Whole-Process & Per-Thread CPU Accounting (/proc/self/task + rusage)
# -----------------------------------------------------------------------------
CLK_TCK = os.sysconf(os.sysconf_names.get("SC_CLK_TCK", "SC_CLK_TCK")) if hasattr(os, "sysconf") else 100


def snapshot_os_threads():
    """Reads /proc/self/task/<tid>/stat and comm to snapshot exact per-OS-thread CPU jiffies."""
    tasks = {}
    task_dir = "/proc/self/task"
    if not os.path.exists(task_dir):
        return tasks
    for tid_str in os.listdir(task_dir):
        if not tid_str.isdigit():
            continue
        tid = int(tid_str)
        try:
            with open(f"{task_dir}/{tid}/comm", "r", encoding="utf-8", errors="replace") as f:
                comm = f.read().strip()
            with open(f"{task_dir}/{tid}/stat", "r", encoding="utf-8", errors="replace") as f:
                stat_str = f.read()
            rparen = stat_str.rfind(")")
            fields = stat_str[rparen + 2:].split()
            # fields[11] is utime, fields[12] is stime in clock ticks
            utime_ticks = int(fields[11])
            stime_ticks = int(fields[12])
            tasks[tid] = (comm, (utime_ticks + stime_ticks) / float(CLK_TCK))
        except Exception:
            continue
    return tasks


def get_rusage_cpu_sec():
    """Returns exact whole-process (User + System) CPU seconds across all OS threads."""
    ru = resource.getrusage(resource.RUSAGE_SELF)
    return float(ru.ru_utime + ru.ru_stime), float(ru.ru_utime), float(ru.ru_stime)


class CrossFFIProfileSession:
    """Manages simultaneous Yappi + Kernel RUSAGE_SELF + /proc/self/task + Go Shared Core profiling."""

    def __init__(self, use_go_core=False, go_ext=None, pprof_path=None):
        self.use_go_core = use_go_core
        self.go_ext = go_ext
        self.pprof_path = pprof_path
        self.wall_start = 0.0
        self.wall_elapsed = 0.0
        self.rusage_start = (0.0, 0.0, 0.0)
        self.rusage_end = (0.0, 0.0, 0.0)
        self.threads_start = {}
        self.threads_end = {}
        self.go_core_stats = (0, 0, 0, 0, 0, 0, 0, 0)

    def start(self):
        if self.use_go_core and self.go_ext is not None:
            self.go_ext.reset_core_stats()
            if self.pprof_path:
                self.go_ext.start_cpu_profile(self.pprof_path)
        yappi.set_clock_type("cpu")
        yappi.clear_stats()
        self.threads_start = snapshot_os_threads()
        self.rusage_start = get_rusage_cpu_sec()
        self.wall_start = time.perf_counter()
        yappi.start(builtins=True)

    def stop(self):
        yappi.stop()
        self.wall_elapsed = time.perf_counter() - self.wall_start
        self.rusage_end = get_rusage_cpu_sec()
        self.threads_end = snapshot_os_threads()
        if self.use_go_core and self.go_ext is not None:
            if self.pprof_path:
                self.go_ext.stop_cpu_profile()
            self.go_core_stats = self.go_ext.get_core_stats()

    def save_and_stitch(self, output_prof_path, request_count):
        """Saves Yappi pstats and stitches C-FFI + Go Shared Core (or Native C++ gRPC) CPU frames."""
        stats = yappi.get_func_stats()
        stats.save(output_prof_path, type="pstat")

        ps = pstats.Stats(output_prof_path)
        python_yappi_cpu = float(ps.total_tt)

        total_proc_cpu = max(0.0, self.rusage_end[0] - self.rusage_start[0])
        user_proc_cpu = max(0.0, self.rusage_end[1] - self.rusage_start[1])
        sys_proc_cpu = max(0.0, self.rusage_end[2] - self.rusage_start[2])

        if self.use_go_core:
            calls, chunks, req_ns, init_ns, recv_ns, asm_ns, enc_ns, c_pylist_ns = self.go_core_stats
            n_calls = max(1, int(calls) if calls > 0 else int(request_count))
            n_chunks = max(n_calls, int(chunks))

            req_s = req_ns / 1e9
            init_s = init_ns / 1e9
            recv_s = recv_ns / 1e9
            asm_s = asm_ns / 1e9
            enc_s = enc_ns / 1e9
            c_pylist_s = c_pylist_ns / 1e9

            fg_go_s = req_s + init_s + recv_s + asm_s + enc_s
            # Total CPU outside Python interpreter = max(fg_go_s, total_proc_cpu - python_yappi_cpu)
            off_thread_total_s = max(fg_go_s, total_proc_cpu - python_yappi_cpu)
            bg_go_m_threads_s = max(0.0, off_thread_total_s - fg_go_s)
            go_total_s = fg_go_s + bg_go_m_threads_s

            self._stitch_go_frames(
                output_prof_path,
                n_calls=n_calls,
                n_chunks=n_chunks,
                req_s=req_s,
                init_s=init_s,
                recv_s=recv_s,
                asm_s=asm_s,
                enc_s=enc_s,
                bg_go_s=bg_go_m_threads_s,
                c_pylist_s=c_pylist_s,
            )
            ps = pstats.Stats(output_prof_path)
            true_total_cpu = max(total_proc_cpu, float(ps.total_tt))
            breakdown = {
                "wall_elapsed_sec": round(self.wall_elapsed, 4),
                "request_count": int(request_count),
                "qps": round(request_count / max(0.001, self.wall_elapsed), 2),
                "total_process_cpu_sec": round(true_total_cpu, 4),
                "user_cpu_sec": round(user_proc_cpu, 4),
                "sys_cpu_sec": round(sys_proc_cpu, 4),
                "python_and_c_ext_cpu_sec": round(python_yappi_cpu, 4),
                "c_ext_pylist_decode_cpu_sec": round(c_pylist_s, 4),
                "go_shared_core_total_cpu_sec": round(go_total_s, 4),
                "go_foreground_phases_cpu_sec": round(fg_go_s, 4),
                "go_background_m_threads_cpu_sec": round(bg_go_m_threads_s, 4),
                "go_req_build_auth_cpu_sec": round(req_s, 4),
                "go_stream_init_cpu_sec": round(init_s, 4),
                "go_recv_protobuf_cpu_sec": round(recv_s, 4),
                "go_chunk_assemble_cpu_sec": round(asm_s, 4),
                "go_zero_copy_arena_encode_cpu_sec": round(enc_s, 4),
                "cpu_ms_per_query": round((true_total_cpu / max(1, request_count)) * 1000.0, 3),
                "python_cpu_ms_per_query": round((python_yappi_cpu / max(1, request_count)) * 1000.0, 3),
                "go_core_cpu_ms_per_query": round((go_total_s / max(1, request_count)) * 1000.0, 3),
            }
        else:
            native_grpc_bg_s = max(0.0, total_proc_cpu - python_yappi_cpu)
            true_total_cpu = max(total_proc_cpu, python_yappi_cpu)
            breakdown = {
                "wall_elapsed_sec": round(self.wall_elapsed, 4),
                "request_count": int(request_count),
                "qps": round(request_count / max(0.001, self.wall_elapsed), 2),
                "total_process_cpu_sec": round(true_total_cpu, 4),
                "user_cpu_sec": round(user_proc_cpu, 4),
                "sys_cpu_sec": round(sys_proc_cpu, 4),
                "python_and_c_ext_cpu_sec": round(python_yappi_cpu, 4),
                "native_grpc_bg_threads_cpu_sec": round(native_grpc_bg_s, 4),
                "go_shared_core_total_cpu_sec": 0.0,
                "cpu_ms_per_query": round((true_total_cpu / max(1, request_count)) * 1000.0, 3),
                "python_cpu_ms_per_query": round((python_yappi_cpu / max(1, request_count)) * 1000.0, 3),
                "go_core_cpu_ms_per_query": 0.0,
            }

        return ps, breakdown

    def _stitch_go_frames(
        self,
        prof_path,
        n_calls,
        n_chunks,
        req_s,
        init_s,
        recv_s,
        asm_s,
        enc_s,
        bg_go_s,
        c_pylist_s,
    ):
        """Injects Cross-FFI C-Extension and Go Shared Core nodes into the pstats dictionary."""
        with open(prof_path, "rb") as f:
            raw_stats = marshal.load(f)

        # Locate the FFI boundary caller inside raw_stats:
        # Either <built-in method execute_streaming_sql> / <built-in method submit_async>
        # or our Python wrapper function run_point_select_query_go_core / execute_streaming_sql.
        ffi_Sync_key = None
        ffi_Async_submit_key = None
        ffi_Async_pop_key = None
        wrapper_key = None

        for k in list(raw_stats.keys()):
            fn_name = k[2]
            if "execute_streaming_sql" in fn_name and ("built-in" in fn_name or k[0] == "~"):
                ffi_Sync_key = k
            elif "submit_async" in fn_name:
                ffi_Async_submit_key = k
            elif "pop_completed" in fn_name:
                ffi_Async_pop_key = k
            elif fn_name in (
                "run_point_select_query_go_core_sync",
                "run_limit_1000_query_go_core_sync",
                "execute_streaming_sql_go_async",
            ):
                wrapper_key = k

        parent_key = ffi_Sync_key or ffi_Async_submit_key or wrapper_key
        if parent_key is None and raw_stats:
            # Fallback to highest cumulative function
            parent_key = max(raw_stats.items(), key=lambda x: x[1][3])[0]

        go_total_s = req_s + init_s + recv_s + asm_s + enc_s + bg_go_s

        # Define synthetic pstats keys for the C-Extension and Go Shared Core frames
        k_c_decode = ("c_ext/spanner_go_ext.c", 190, "[C-FFI] batch_to_pylist (CSpannerCell -> PyList)")
        k_go_entry = ("spanner_go_core/main.go", 364, "[Go Shared Core] main.executeStreamingSqlInternal")
        k_go_req = ("spanner_go_core/main.go", 391, "[Go Shared Core] main.buildExecuteSqlRequestAndAuth")
        k_go_init = ("spanner_go_core/client.go", 138, "[Go Shared Core] CoreClient.ExecuteStreamingSql (gRPC Stream Init)")
        k_go_recv = ("spanner_go_core/main.go", 441, "[Go Shared Core] grpc.ClientStream.Recv + proto.Unmarshal(PartialResultSet)")
        k_go_asm = ("spanner_go_core/main.go", 465, "[Go Shared Core] main.assembleStreamingRowChunks")
        k_go_enc = ("spanner_go_core/main.go", 215, "[Go Shared Core] main.buildCBatch (Zero-Copy CSpannerCell Arena)")
        k_go_bg = ("spanner_go_core/runtime", 1, "[Go Shared Core] grpc.http2Client.reader + crypto/tls (Background M-Threads)")

        # Add C-extension batch_to_pylist under pop_completed (async) or parent_key (sync)
        c_decode_parent = ffi_Async_pop_key if ffi_Async_pop_key is not None else parent_key
        if c_decode_parent is not None and c_pylist_s > 0:
            raw_stats[k_c_decode] = (
                n_calls,
                n_calls,
                c_pylist_s,
                c_pylist_s,
                {c_decode_parent: (n_calls, n_calls, c_pylist_s, c_pylist_s)},
            )
            # Reduce self-time of c_decode_parent by c_pylist_s so total time is not double-counted
            p_cc, p_nc, p_tt, p_ct, p_callers = raw_stats[c_decode_parent]
            new_p_tt = max(0.0, p_tt - c_pylist_s)
            raw_stats[c_decode_parent] = (p_cc, p_nc, new_p_tt, max(p_ct, c_pylist_s), p_callers)

        # Add Go Shared Core hierarchy under parent_key
        if parent_key is not None:
            raw_stats[k_go_entry] = (
                n_calls,
                n_calls,
                0.000001,
                go_total_s,
                {parent_key: (n_calls, n_calls, 0.000001, go_total_s)},
            )
            raw_stats[k_go_req] = (
                n_calls,
                n_calls,
                req_s,
                req_s,
                {k_go_entry: (n_calls, n_calls, req_s, req_s)},
            )
            raw_stats[k_go_init] = (
                n_calls,
                n_calls,
                init_s,
                init_s,
                {k_go_entry: (n_calls, n_calls, init_s, init_s)},
            )
            raw_stats[k_go_recv] = (
                n_chunks,
                n_chunks,
                recv_s,
                recv_s,
                {k_go_entry: (n_chunks, n_chunks, recv_s, recv_s)},
            )
            raw_stats[k_go_asm] = (
                n_chunks,
                n_chunks,
                asm_s,
                asm_s,
                {k_go_entry: (n_chunks, n_chunks, asm_s, asm_s)},
            )
            raw_stats[k_go_enc] = (
                n_calls,
                n_calls,
                enc_s,
                enc_s,
                {k_go_entry: (n_calls, n_calls, enc_s, enc_s)},
            )
            if bg_go_s > 0:
                raw_stats[k_go_bg] = (
                    n_chunks,
                    n_chunks,
                    bg_go_s,
                    bg_go_s,
                    {k_go_entry: (n_chunks, n_chunks, bg_go_s, bg_go_s)},
                )

            # Propagate go_total_s up the cumulative time chain from parent_key to root callers
            visited = set()
            stack = [parent_key]
            while stack:
                curr = stack.pop()
                if curr in visited or curr not in raw_stats:
                    continue
                visited.add(curr)
                cc, nc, tt, ct, callers = raw_stats[curr]
                updated_callers = {}
                for caller_k, caller_val in callers.items():
                    if isinstance(caller_val, tuple) and len(caller_val) == 4:
                        c_cc, c_nc, c_tt, c_ct = caller_val
                        updated_callers[caller_k] = (c_cc, c_nc, c_tt, c_ct + go_total_s)
                    else:
                        updated_callers[caller_k] = caller_val
                    stack.append(caller_k)
                raw_stats[curr] = (cc, nc, tt, ct + go_total_s, updated_callers)

        with open(prof_path, "wb") as f:
            marshal.dump(raw_stats, f)


# -----------------------------------------------------------------------------
# Go Shared Core AsyncIO Wrapper (Non-blocking Submit + epoll_wait Pipe Reader)
# -----------------------------------------------------------------------------
class GoCoreAsyncSession:
    """Integrates Go Shared Core with Python's asyncio SelectorEventLoop via a non-blocking OS pipe."""

    def __init__(self, go_ext, cid, loop=None):
        self.go_ext = go_ext
        self.cid = cid
        self.loop = loop or asyncio.get_running_loop()
        self.notify_fd = self.go_ext.get_notify_fd()
        self._pending = {}
        self._next_id = 1
        self.loop.add_reader(self.notify_fd, self._on_go_completion_ready)

    def _on_go_completion_ready(self):
        for req_id, rows, err in self.go_ext.pop_completed():
            fut = self._pending.pop(req_id, None)
            if fut is not None and not fut.done():
                if err is not None:
                    fut.set_exception(RuntimeError(err))
                else:
                    fut.set_result(rows)

    async def execute_streaming_sql_go_async(self, session_name, sql, param_id=""):
        req_id = self._next_id
        self._next_id += 1
        fut = self.loop.create_future()
        self._pending[req_id] = fut
        self.go_ext.submit_async(self.cid, req_id, session_name, sql, param_id)
        rows = await fut
        return len(rows)

    def close(self):
        try:
            self.loop.remove_reader(self.notify_fd)
        except Exception:
            pass


# -----------------------------------------------------------------------------
# Scenario 1 & 3: Synchronous Client Queries (Without Shared Core vs With Go Shared Core)
# -----------------------------------------------------------------------------
def run_point_select_query_sync(database, user_id="user-0"):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            POINT_SELECT_SQL,
            params={"id": user_id},
            param_types={"id": param_types.STRING},
        )
        rows = list(results)
        return len(rows)


def run_point_select_query_go_core_sync(go_ext, cid, session_name, user_id="user-0"):
    rows = go_ext.execute_streaming_sql(cid, session_name, POINT_SELECT_SQL, user_id)
    return len(rows)


def run_limit_1000_query_sync(database):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(LIMIT_1000_SQL)
        rows = list(results)
        return len(rows)


def run_limit_1000_query_go_core_sync(go_ext, cid, session_name):
    rows = go_ext.execute_streaming_sql(cid, session_name, LIMIT_1000_SQL, "")
    return len(rows)


def extract_multiplexed_session_name(database):
    """Obtains the active multiplexed session name from the Spanner database client."""
    with database.snapshot() as snapshot:
        _ = list(
            snapshot.execute_sql(
                POINT_SELECT_SQL,
                params={"id": "user-0"},
                param_types={"id": param_types.STRING},
            )
        )
        return snapshot._session.name


def run_scenario_1_point_select_c1(
    database,
    output_prof_path,
    use_go_core=False,
    go_ext=None,
    cid=None,
    session_name=None,
    warmup_sec=WARMUP_DURATION_SEC,
    profile_sec=PROFILE_DURATION_SEC,
):
    label = "WITH GO SHARED CORE (Cross-FFI)" if use_go_core else "WITHOUT SHARED CORE (Stock Python SDK)"
    print("\n" + "=" * 88)
    print(f"SCENARIO 1 [{'1B' if use_go_core else '1A'}]: Point Select C=1 (Sync) — {label}")
    print("=" * 88)

    print(f"[*] Warming up for {warmup_sec} seconds...")
    warmup_end = time.perf_counter() + warmup_sec
    warmup_count = 0
    while time.perf_counter() < warmup_end:
        uid = f"user-{warmup_count % 100}"
        if use_go_core:
            run_point_select_query_go_core_sync(go_ext, cid, session_name, uid)
        else:
            run_point_select_query_sync(database, uid)
        warmup_count += 1
    print(f"[+] Warmup completed: {warmup_count} requests executed.")

    pprof_path = output_prof_path.replace(".prof", ".pprof") if use_go_core else None
    print(f"[*] Profiling pure CPU time (Cross-FFI enabled={use_go_core}) for {profile_sec} seconds...")
    prof_session = CrossFFIProfileSession(use_go_core=use_go_core, go_ext=go_ext, pprof_path=pprof_path)
    prof_session.start()

    prof_end = time.perf_counter() + profile_sec
    recorded_count = 0
    while time.perf_counter() < prof_end:
        uid = f"user-{recorded_count % 100}"
        if use_go_core:
            run_point_select_query_go_core_sync(go_ext, cid, session_name, uid)
        else:
            run_point_select_query_sync(database, uid)
        recorded_count += 1

    prof_session.stop()
    ps, breakdown = prof_session.save_and_stitch(output_prof_path, recorded_count)
    print(f"[+] Profiling finished: {recorded_count} requests ({breakdown['qps']} QPS) | Total CPU: {breakdown['total_process_cpu_sec']:.4f}s ({breakdown['cpu_ms_per_query']:.3f} ms/query)")
    print(f"[+] Saved profile stats to: {output_prof_path}")
    return ps, recorded_count, breakdown


# -----------------------------------------------------------------------------
# Scenario 2: Async Client with 32 Concurrency Coroutines (Without vs With Go Shared Core)
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
    while time.perf_counter() < stop_time:
        await run_single_async_query_with_parsing(async_client, session_name, f"user-{(worker_id + count) % 100}")
        count += 1
    return count


async def run_single_async_query_high_level(async_database, user_id="user-0"):
    async with async_database.snapshot() as snapshot:
        results = await snapshot.execute_sql(
            POINT_SELECT_SQL,
            params={"id": user_id},
            param_types={"id": param_types.STRING},
        )
        rows = [row async for row in results]
        return len(rows)


async def async_worker_loop_high_level(async_database, worker_id, stop_time):
    count = 0
    while time.perf_counter() < stop_time:
        await run_single_async_query_high_level(async_database, f"user-{(worker_id + count) % 100}")
        count += 1
    return count


async def async_worker_loop_go_core(go_async_session, session_name, worker_id, stop_time):
    count = 0
    while time.perf_counter() < stop_time:
        await go_async_session.execute_streaming_sql_go_async(
            session_name, POINT_SELECT_SQL, f"user-{(worker_id + count) % 100}"
        )
        count += 1
    return count


async def execute_async_scenario_2(
    output_prof_path,
    concurrency=32,
    use_go_core=False,
    go_ext=None,
    cid=None,
    session_name=None,
    warmup_sec=WARMUP_DURATION_SEC,
    profile_sec=PROFILE_DURATION_SEC,
):
    label = "WITH GO SHARED CORE (Cross-FFI Async Pipe)" if use_go_core else "WITHOUT SHARED CORE (Stock Python Async SDK)"
    print("\n" + "=" * 88)
    print(f"SCENARIO 2 [{'2B' if use_go_core else '2A'}]: Point Select C={concurrency} (AsyncIO) — {label}")
    print("=" * 88)

    go_async_session = None
    if use_go_core:
        go_async_session = GoCoreAsyncSession(go_ext, cid, loop=asyncio.get_running_loop())
        worker_fn = lambda wid, st: async_worker_loop_go_core(go_async_session, session_name, wid, st)
    else:
        use_high_level = HighLevelAsyncClient is not None
        if use_high_level:
            print(f"[*] Initializing high-level spanner_v1.AsyncClient for {PROJECT} / {INSTANCE} / {DATABASE}...")
            async_client = HighLevelAsyncClient(project=PROJECT)
            async_instance = async_client.instance(INSTANCE)
            pool = AsyncBurstyPool(target_size=concurrency) if AsyncBurstyPool else None
            # Important: async_instance.database() is a coroutine whether pool is passed or not
            if pool is not None:
                async_database = await async_instance.database(DATABASE, pool=pool)
            else:
                async_database = await async_instance.database(DATABASE)
            worker_fn = lambda wid, st: async_worker_loop_high_level(async_database, wid, st)
        else:
            print(f"[*] Initializing SpannerAsyncClient (grpc.aio transport) for {DB_PATH}...")
            async_client = SpannerAsyncClient()
            sessions = await asyncio.gather(*[async_client.create_session(database=DB_PATH) for _ in range(concurrency)])
            session_names = [s.name for s in sessions]
            worker_fn = lambda wid, st: async_worker_loop_gapic(async_client, session_names[wid], wid, st)

    print(f"[*] Warming up {concurrency} concurrent coroutines on event loop for {warmup_sec} seconds...")
    warmup_end = time.perf_counter() + warmup_sec
    warmup_tasks = [worker_fn(i, warmup_end) for i in range(concurrency)]
    warmup_results = await asyncio.gather(*warmup_tasks)
    print(f"[+] Warmup completed: {sum(warmup_results)} total requests executed across {concurrency} coroutines.")

    pprof_path = output_prof_path.replace(".prof", ".pprof") if use_go_core else None
    print(f"[*] Profiling pure CPU time across all {concurrency} coroutines for {profile_sec} seconds...")
    prof_session = CrossFFIProfileSession(use_go_core=use_go_core, go_ext=go_ext, pprof_path=pprof_path)
    prof_session.start()

    prof_end = time.perf_counter() + profile_sec
    profile_tasks = [worker_fn(i, prof_end) for i in range(concurrency)]
    profile_results = await asyncio.gather(*profile_tasks)

    prof_session.stop()
    if go_async_session is not None:
        go_async_session.close()

    total_recorded = sum(profile_results)
    ps, breakdown = prof_session.save_and_stitch(output_prof_path, total_recorded)
    print(
        f"[+] Profiling finished: {total_recorded} requests ({breakdown['qps']} QPS) | "
        f"Total CPU: {breakdown['total_process_cpu_sec']:.4f}s ({breakdown['cpu_ms_per_query']:.3f} ms/query)"
    )
    print(f"[+] Saved profile stats to: {output_prof_path}")
    return ps, total_recorded, breakdown


def run_scenario_2_point_select_c32_async(
    output_prof_path,
    concurrency=32,
    use_go_core=False,
    go_ext=None,
    cid=None,
    session_name=None,
    warmup_sec=WARMUP_DURATION_SEC,
    profile_sec=PROFILE_DURATION_SEC,
):
    return asyncio.run(
        execute_async_scenario_2(
            output_prof_path,
            concurrency=concurrency,
            use_go_core=use_go_core,
            go_ext=go_ext,
            cid=cid,
            session_name=session_name,
            warmup_sec=warmup_sec,
            profile_sec=profile_sec,
        )
    )


# -----------------------------------------------------------------------------
# Scenario 3: LIMIT 1000 Read (Without Shared Core vs With Go Shared Core)
# -----------------------------------------------------------------------------
def run_scenario_3_limit_1000_c1(
    database,
    output_prof_path,
    use_go_core=False,
    go_ext=None,
    cid=None,
    session_name=None,
    warmup_sec=WARMUP_DURATION_SEC,
    profile_sec=PROFILE_DURATION_SEC,
):
    label = "WITH GO SHARED CORE (Cross-FFI)" if use_go_core else "WITHOUT SHARED CORE (Stock Python SDK)"
    print("\n" + "=" * 88)
    print(f"SCENARIO 3 [{'3B' if use_go_core else '3A'}]: LIMIT 1000 Read (11-Col Table) — {label}")
    print("=" * 88)

    print(f"[*] Warming up LIMIT 1000 stream for {warmup_sec} seconds...")
    warmup_end = time.perf_counter() + warmup_sec
    warmup_count = 0
    while time.perf_counter() < warmup_end:
        if use_go_core:
            run_limit_1000_query_go_core_sync(go_ext, cid, session_name)
        else:
            run_limit_1000_query_sync(database)
        warmup_count += 1
    print(f"[+] Warmup completed: {warmup_count} queries ({warmup_count * 1000} rows) executed.")

    pprof_path = output_prof_path.replace(".prof", ".pprof") if use_go_core else None
    print(f"[*] Profiling LIMIT 1000 pure CPU time for {profile_sec} seconds...")
    prof_session = CrossFFIProfileSession(use_go_core=use_go_core, go_ext=go_ext, pprof_path=pprof_path)
    prof_session.start()

    prof_end = time.perf_counter() + profile_sec
    recorded_count = 0
    while time.perf_counter() < prof_end:
        if use_go_core:
            run_limit_1000_query_go_core_sync(go_ext, cid, session_name)
        else:
            run_limit_1000_query_sync(database)
        recorded_count += 1

    prof_session.stop()
    ps, breakdown = prof_session.save_and_stitch(output_prof_path, recorded_count)
    print(
        f"[+] Profiling finished: {recorded_count} queries ({recorded_count * 1000} rows) | "
        f"Total CPU: {breakdown['total_process_cpu_sec']:.4f}s ({breakdown['cpu_ms_per_query']:.3f} ms/query)"
    )
    print(f"[+] Saved profile stats to: {output_prof_path}")
    return ps, recorded_count, breakdown


# -----------------------------------------------------------------------------
# Scenario 4: Point Select with 32 OS Threads (Sync SDK vs Go Shared Core + GIL Contention)
# -----------------------------------------------------------------------------
class ThreadBenchmarkMetric:
    def __init__(self, thread_id, name):
        self.thread_id = thread_id
        self.name = name
        self.query_count = 0
        self.wall_time = 0.0
        self.cpu_time = 0.0


def worker_thread_loop(
    database,
    worker_id,
    stop_time,
    metric,
    use_go_core=False,
    go_ext=None,
    cid=None,
    session_name=None,
):
    t_start_wall = time.perf_counter()
    t_start_cpu = time.thread_time()
    queries = 0

    while time.perf_counter() < stop_time:
        uid = f"user-{(worker_id + queries) % 100}"
        if use_go_core:
            run_point_select_query_go_core_sync(go_ext, cid, session_name, uid)
        else:
            run_point_select_query_sync(database, uid)
        queries += 1

    t_end_wall = time.perf_counter()
    t_end_cpu = time.thread_time()

    metric.query_count = queries
    metric.wall_time = t_end_wall - t_start_wall
    metric.cpu_time = t_end_cpu - t_start_cpu


def run_scenario_4_point_select_c32_threads(
    database,
    output_prof_path,
    concurrency=32,
    use_go_core=False,
    go_ext=None,
    cid=None,
    session_name=None,
    warmup_sec=WARMUP_DURATION_SEC,
    profile_sec=PROFILE_DURATION_SEC,
):
    label = "WITH GO SHARED CORE (GIL Released via Py_BEGIN_ALLOW_THREADS)" if use_go_core else "WITHOUT SHARED CORE (Stock Python SDK)"
    print("\n" + "=" * 88)
    print(f"SCENARIO 4 [{'4B' if use_go_core else '4A'}]: Multi-Threaded Point Select C={concurrency} OS Threads — {label}")
    print("=" * 88)

    print(f"[*] Warming up {concurrency} OS worker threads for {warmup_sec} seconds...")
    warmup_end = time.perf_counter() + warmup_sec
    warmup_metrics = [ThreadBenchmarkMetric(i, f"Warmup-{i}") for i in range(concurrency)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(
                worker_thread_loop,
                database,
                i,
                warmup_end,
                warmup_metrics[i],
                use_go_core,
                go_ext,
                cid,
                session_name,
            )
            for i in range(concurrency)
        ]
        concurrent.futures.wait(futures)
    print(f"[+] Warmup completed: {sum(m.query_count for m in warmup_metrics)} requests executed across {concurrency} threads.")

    pprof_path = output_prof_path.replace(".prof", ".pprof") if use_go_core else None
    print(f"[*] Profiling pure CPU time & GIL contention across {concurrency} OS threads for {profile_sec} seconds...")
    metrics = [ThreadBenchmarkMetric(i, f"Worker-{i}") for i in range(concurrency)]

    prof_session = CrossFFIProfileSession(use_go_core=use_go_core, go_ext=go_ext, pprof_path=pprof_path)
    prof_session.start()

    benchmark_start_wall = time.perf_counter()
    benchmark_end_wall = benchmark_start_wall + profile_sec

    threads = []
    for i in range(concurrency):
        t = threading.Thread(
            target=worker_thread_loop,
            args=(database, i, benchmark_end_wall, metrics[i], use_go_core, go_ext, cid, session_name),
            name=f"SpannerWorkerThread-{i}",
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    prof_session.stop()
    total_wall_elapsed = prof_session.wall_elapsed
    total_recorded = sum(m.query_count for m in metrics)
    total_worker_thread_cpu = sum(m.cpu_time for m in metrics)

    ps, breakdown = prof_session.save_and_stitch(output_prof_path, total_recorded)

    # Calculate GIL-held CPU vs GIL-released Native/Go CPU:
    # In Go Shared Core, Py_BEGIN_ALLOW_THREADS releases the GIL for the entire gRPC + Protobuf execution,
    # holding the GIL only during Python call entry and C batch_to_pylist materialization.
    if use_go_core:
        gil_held_cpu_total = breakdown["python_and_c_ext_cpu_sec"]
        gil_released_cpu_total = breakdown["go_shared_core_total_cpu_sec"]
    else:
        gil_held_cpu_total = total_worker_thread_cpu
        gil_released_cpu_total = breakdown.get("native_grpc_bg_threads_cpu_sec", 0.0)

    # True GIL serialization utilization factor rho_gil = min(0.99, gil_held_cpu_total / total_wall_elapsed)
    rho_gil = min(0.99, gil_held_cpu_total / max(0.001, total_wall_elapsed))
    total_gil_wait = gil_held_cpu_total * rho_gil * ((concurrency - 1.0) / concurrency)
    gil_contention_ratio = (total_gil_wait / max(0.0001, breakdown["total_process_cpu_sec"] + total_gil_wait)) * 100.0

    breakdown["gil_held_cpu_sec"] = round(gil_held_cpu_total, 4)
    breakdown["gil_released_native_cpu_sec"] = round(gil_released_cpu_total, 4)
    breakdown["gil_utilization_pct"] = round(rho_gil * 100.0, 2)
    breakdown["total_gil_wait_sec"] = round(total_gil_wait, 4)
    breakdown["gil_contention_ratio_pct"] = round(gil_contention_ratio, 2)

    print("\n" + "=" * 88)
    print(f"SCENARIO 4 [{'4B' if use_go_core else '4A'}] GIL & CROSS-FFI CONTENTION SUMMARY ({label}):")
    print(f"1. Concurrency Model:                   Multi-Threading ({concurrency} OS Threads)")
    print(f"2. Total Wall-Clock Elapsed Time:       {total_wall_elapsed:.3f} s")
    print(f"3. Total Queries Completed:             {total_recorded} queries ({breakdown['qps']:.1f} QPS)")
    print(f"4. Total Process Pure CPU (All Threads):{breakdown['total_process_cpu_sec']:.4f} s ({breakdown['cpu_ms_per_query']:.3f} ms / query)")
    print(f"5. Python GIL-Held CPU Time:            {gil_held_cpu_total:.4f} s ({gil_held_cpu_total/max(1, total_recorded)*1000:.3f} ms / query)")
    print(f"6. GIL-Released Native/Go CPU Time:     {gil_released_cpu_total:.4f} s ({gil_released_cpu_total/max(1, total_recorded)*1000:.3f} ms / query)")
    print(f"7. GIL Serialization Utilization:       {rho_gil*100:.1f}% of wall-clock window")
    print(f"8. Total Estimated GIL Wait Time:       {total_gil_wait:.4f} s (Contention Ratio: {gil_contention_ratio:.1f}%)")
    print("=" * 88)

    return ps, total_recorded, breakdown


def print_summary_table(ps, title, request_count, breakdown=None):
    s = io.StringIO()
    ps.stream = s
    ps.strip_dirs()
    total_cpu = breakdown["total_process_cpu_sec"] if breakdown else ps.total_tt
    cpu_per_q = breakdown["cpu_ms_per_query"] if breakdown else (ps.total_tt / max(1, request_count)) * 1000.0
    print("\n" + "-" * 88)
    print(f"SUMMARY FOR: {title}")
    print(
        f"Total Requests: {request_count} | Total Process Pure CPU: {total_cpu:.4f} s | "
        f"Avg CPU/Query: {cpu_per_q:.3f} ms"
    )
    if breakdown and breakdown.get("go_shared_core_total_cpu_sec", 0.0) > 0:
        print(
            f"Cross-FFI Split -> Python+C-Ext CPU: {breakdown['python_and_c_ext_cpu_sec']:.4f} s "
            f"({breakdown['python_cpu_ms_per_query']:.3f} ms/q) | "
            f"Go Shared Core CPU: {breakdown['go_shared_core_total_cpu_sec']:.4f} s "
            f"({breakdown['go_core_cpu_ms_per_query']:.3f} ms/q)"
        )
    print("-" * 88)
    ps.sort_stats("cumulative").print_stats(15)
    print(s.getvalue())


def print_comparison_report(results):
    """Prints a side-by-side comparison table between Stock Python SDK and Go Shared Core."""
    pairs = [
        ("Scenario 1: Point Select C=1 (Sync)", "s1_stock", "s1_go_core"),
        ("Scenario 2: Point Select C=32 (AsyncIO)", "s2_stock", "s2_go_core"),
        ("Scenario 3: LIMIT 1000 Read C=1 (Sync)", "s3_stock", "s3_go_core"),
        ("Scenario 4: Point Select C=32 (OS Threads)", "s4_stock", "s4_go_core"),
    ]
    print("\n" + "=" * 116)
    print("SIDE-BY-SIDE CROSS-FFI CPU PROFILING COMPARISON: WITHOUT SHARED CORE (STOCK PYTHON) vs WITH GO SHARED CORE")
    print("=" * 116)
    header = (
        f"{'Scenario':<42} | {'Stock CPU/q':<12} | {'GoCore CPU/q':<12} | "
        f"{'Py+C / Go Split (ms/q)':<24} | {'CPU Reduction':<14} | {'QPS Gain'}"
    )
    print(header)
    print("-" * 116)
    for label, k_stock, k_go in pairs:
        if k_stock in results and k_go in results:
            b_stock = results[k_stock]
            b_go = results[k_go]
            s_ms = b_stock["cpu_ms_per_query"]
            g_ms = b_go["cpu_ms_per_query"]
            py_ms = b_go["python_cpu_ms_per_query"]
            go_ms = b_go["go_core_cpu_ms_per_query"]
            reduction_pct = ((s_ms - g_ms) / max(0.001, s_ms)) * 100.0
            speedup_x = s_ms / max(0.001, g_ms)
            qps_ratio = b_go["qps"] / max(0.01, b_stock["qps"])
            print(
                f"{label:<42} | {s_ms:>8.3f} ms | {g_ms:>8.3f} ms | "
                f"{py_ms:>5.3f} Py / {go_ms:>5.3f} Go   | "
                f"-{reduction_pct:>5.1f}% ({speedup_x:>4.1f}x) | {b_stock['qps']:>6.1f} -> {b_go['qps']:>6.1f} ({qps_ratio:.2f}x)"
            )
    print("=" * 116)


def resolve_output_dir():
    repo_dir = "/usr/local/google/home/suvham/workspace/cloudPython/google-cloud-python/packages/google-cloud-spanner/profiler_results"
    if os.path.exists(os.path.join(os.getcwd(), "packages/google-cloud-spanner/profiler_results/README.md")):
        return os.path.join(os.getcwd(), "packages/google-cloud-spanner/profiler_results")
    if os.path.exists(os.path.join(os.getcwd(), "README.md")) and "profiler_results" in os.getcwd():
        return os.getcwd()
    if os.path.exists(repo_dir):
        return repo_dir
    return SCRIPT_DIR


def run_all(flow="all", warmup_sec=WARMUP_DURATION_SEC, profile_sec=PROFILE_DURATION_SEC):
    output_dir = resolve_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "comparison_summary.json")

    if flow == "all":
        script_path = os.path.abspath(__file__)
        print("=" * 100)
        print("[*] PHASE 1/2: Running Flow A (WITHOUT Shared Core — Stock Python SDK) in isolated process...")
        print("=" * 100)
        subprocess.run(
            [
                sys.executable,
                script_path,
                "--flow=without-shared-core",
                f"--warmup={warmup_sec}",
                f"--duration={profile_sec}",
            ],
            check=True,
        )
        print("\n" + "=" * 100)
        print("[*] PHASE 2/2: Running Flow B (WITH Go Shared Core — Cross-FFI C+Go) in isolated process...")
        print("=" * 100)
        subprocess.run(
            [
                sys.executable,
                script_path,
                "--flow=with-shared-core",
                f"--warmup={warmup_sec}",
                f"--duration={profile_sec}",
            ],
            check=True,
        )
        if os.path.exists(summary_path):
            with open(summary_path, "r", encoding="utf-8") as f:
                all_results = json.load(f)
            print_comparison_report(all_results)
        try:
            import export_flamegraph_html
            export_flamegraph_html.main()
        except Exception as e:
            print(f"[!] Warning: Failed to auto-generate HTML flame graphs: {e}")
        return

    run_stock = flow in ("without-shared-core", "baseline", "stock")
    run_go_core = flow in ("with-shared-core", "shared-core", "go-core")

    print(f"[*] Initializing Sync Spanner Client for {PROJECT} / {INSTANCE} / {DATABASE}...")
    client = spanner.Client(project=PROJECT)
    instance = client.instance(INSTANCE)
    database = instance.database(DATABASE)

    go_ext = None
    cid = None
    session_name = None
    if run_go_core:
        go_ext = ensure_go_shared_core()
        session_name = extract_multiplexed_session_name(database)
        cid = go_ext.init_client(4)
        for ch_idx in range(8):
            run_point_select_query_go_core_sync(go_ext, cid, session_name, f"user-{ch_idx}")
        print(f"[+] Initialized & pre-warmed Go Shared Core client pool (4 gRPC channels) on session: {session_name}")

    all_results = {}
    if os.path.exists(summary_path):
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                all_results = json.load(f)
        except Exception:
            all_results = {}

    if run_stock:
        f1 = os.path.join(output_dir, "spanner_point_select_c1.prof")
        ps1, cnt1, b1 = run_scenario_1_point_select_c1(
            database, f1, use_go_core=False, warmup_sec=warmup_sec, profile_sec=profile_sec
        )
        print_summary_table(ps1, "Scenario 1A: Point Select C=1 (Without Shared Core - Stock Python SDK)", cnt1, b1)
        all_results["s1_stock"] = b1

        f2 = os.path.join(output_dir, "spanner_point_select_c32.prof")
        ps2, cnt2, b2 = run_scenario_2_point_select_c32_async(
            f2, concurrency=32, use_go_core=False, warmup_sec=warmup_sec, profile_sec=profile_sec
        )
        print_summary_table(ps2, "Scenario 2A: Point Select C=32 AsyncIO (Without Shared Core - Stock Python SDK)", cnt2, b2)
        all_results["s2_stock"] = b2

        f3 = os.path.join(output_dir, "spanner_limit1000_c1.prof")
        ps3, cnt3, b3 = run_scenario_3_limit_1000_c1(
            database, f3, use_go_core=False, warmup_sec=warmup_sec, profile_sec=profile_sec
        )
        print_summary_table(ps3, "Scenario 3A: LIMIT 1000 Read C=1 (Without Shared Core - Stock Python SDK)", cnt3, b3)
        all_results["s3_stock"] = b3

        f4 = os.path.join(output_dir, "spanner_point_select_c32_threads.prof")
        ps4, cnt4, b4 = run_scenario_4_point_select_c32_threads(
            database, f4, concurrency=32, use_go_core=False, warmup_sec=warmup_sec, profile_sec=profile_sec
        )
        print_summary_table(ps4, "Scenario 4A: Point Select Multi-Threaded C=32 (Without Shared Core - Stock Python SDK)", cnt4, b4)
        all_results["s4_stock"] = b4

    if run_go_core:
        f1_go = os.path.join(output_dir, "spanner_point_select_c1_go_core.prof")
        ps1_go, cnt1_go, b1_go = run_scenario_1_point_select_c1(
            database,
            f1_go,
            use_go_core=True,
            go_ext=go_ext,
            cid=cid,
            session_name=session_name,
            warmup_sec=warmup_sec,
            profile_sec=profile_sec,
        )
        print_summary_table(ps1_go, "Scenario 1B: Point Select C=1 (With Go Shared Core - Cross-FFI)", cnt1_go, b1_go)
        all_results["s1_go_core"] = b1_go

        f2_go = os.path.join(output_dir, "spanner_point_select_c32_go_core.prof")
        ps2_go, cnt2_go, b2_go = run_scenario_2_point_select_c32_async(
            f2_go,
            concurrency=32,
            use_go_core=True,
            go_ext=go_ext,
            cid=cid,
            session_name=session_name,
            warmup_sec=warmup_sec,
            profile_sec=profile_sec,
        )
        print_summary_table(ps2_go, "Scenario 2B: Point Select C=32 AsyncIO (With Go Shared Core - Cross-FFI)", cnt2_go, b2_go)
        all_results["s2_go_core"] = b2_go

        f3_go = os.path.join(output_dir, "spanner_limit1000_c1_go_core.prof")
        ps3_go, cnt3_go, b3_go = run_scenario_3_limit_1000_c1(
            database,
            f3_go,
            use_go_core=True,
            go_ext=go_ext,
            cid=cid,
            session_name=session_name,
            warmup_sec=warmup_sec,
            profile_sec=profile_sec,
        )
        print_summary_table(ps3_go, "Scenario 3B: LIMIT 1000 Read C=1 (With Go Shared Core - Cross-FFI)", cnt3_go, b3_go)
        all_results["s3_go_core"] = b3_go

        f4_go = os.path.join(output_dir, "spanner_point_select_c32_threads_go_core.prof")
        ps4_go, cnt4_go, b4_go = run_scenario_4_point_select_c32_threads(
            database,
            f4_go,
            concurrency=32,
            use_go_core=True,
            go_ext=go_ext,
            cid=cid,
            session_name=session_name,
            warmup_sec=warmup_sec,
            profile_sec=profile_sec,
        )
        print_summary_table(ps4_go, "Scenario 4B: Point Select Multi-Threaded C=32 (With Go Shared Core - Cross-FFI)", cnt4_go, b4_go)
        all_results["s4_go_core"] = b4_go

        go_ext.close_client(cid)

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n[+] Saved structured comparison metrics to: {summary_path}")

    print_comparison_report(all_results)

    # Automatically export standalone interactive HTML flame graphs
    try:
        import export_flamegraph_html
        export_flamegraph_html.main()
    except Exception as e:
        print(f"[!] Warning: Failed to auto-generate HTML flame graphs: {e}")


def main():
    parser = argparse.ArgumentParser(description="Cloud Spanner Cross-FFI CPU Profiler Suite")
    parser.add_argument(
        "--flow",
        choices=["all", "without-shared-core", "with-shared-core", "baseline", "shared-core", "stock", "go-core"],
        default="all",
        help="Which flow(s) to profile: 'without-shared-core', 'with-shared-core', or 'all' (default).",
    )
    parser.add_argument(
        "--warmup",
        type=float,
        default=WARMUP_DURATION_SEC,
        help="Warmup duration in seconds per scenario (default: 5.0).",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=PROFILE_DURATION_SEC,
        help="Profile measurement window in seconds per scenario (default: 10.0).",
    )
    args, _ = parser.parse_known_args()
    run_all(flow=args.flow, warmup_sec=args.warmup, profile_sec=args.duration)


if __name__ == "__main__":
    main()
