#!/usr/bin/env python3
"""Open-loop benchmark: Spanner Go Shared Core over FFI vs IPC vs the pure-Python client.

All clients are driven through the SAME high-level SDK call and the SAME open-loop harness, each
run in a fresh process:

    with database.snapshot() as snapshot:
        rows = list(snapshot.execute_sql(...))

  python           : stock Python client (GAPIC + grpcio + proto-plus + StreamedResultSet), N channels
  python_nometrics : same, with SPANNER_DISABLE_BUILTIN_METRICS=true (optional)
  ffi              : Snapshot.execute_sql -> spanner_go_ext (UNCHANGED in-process cgo FFI flow)
  ipc              : Snapshot.execute_sql -> spanner_ipc_ext (AF_UNIX) -> Go Shared Core sidecar whose
                     calls run on locked OS threads, like the FFI cgo callback (default IPC client)
  ipc_goroutine    : same sidecar using plain goroutines (optional)
  null             : harness-overhead baseline, no Spanner (optional)

FFI and IPC run byte-identical Go Shared Core code (same sources, toolchain and module versions; see
spanner_go_core/build_ipc_core.sh), receive the same CSpannerCell batches and materialize rows with
the same per-cell CPython calls; they differ only in the boundary (in-process pointer hand-off vs.
request + writev()/recv() copy of the batch through the kernel, several recv() hops for heavy reads).

Open-loop methodology (no coordinated omission):
  * Requests follow a fixed schedule (uniform or Poisson) independent of completions; latency is
    measured from the *scheduled* send time. Warmup ramps the rate from 20% to 100%.
  * One continuous stream per run: [warmup | measurement window]; CPU sampled at the window edges.
  * Requests never started when the window closes are cancelled (`dropped`) and counted in latency
    percentiles as censored at the window close (lower bound), so saturated cells do not look good.
  * Flags: S = saturated (dropped / achieved < 95% offered), P = worker-pool cap hit (partly closed
    loop), N = non-stationary (achieved off by >5% or latency drifting inside the window).
  * CPU = client RUSAGE_SELF (+ sidecar getrusage for IPC): whole-process, both sides of the boundary,
    plus per-thread attribution (CPU and voluntary context switches) from /proc for both processes.
  * Channels: identical static count for every client per (workload, QPS); --channels auto sizes it
    from concurrency (Little's law) and bandwidth-delay product (RTT/response size from the parity run).
  * --repeats N interleaves N repetitions; reports show medians and [min-max] ranges.

Usage:
  python3 spanner_open_loop_benchmark.py                 # python, ffi, ipc x point, heavy x 10/50/100/500 QPS
  python3 spanner_open_loop_benchmark.py --smoke         # few-second sanity run
  python3 spanner_open_loop_benchmark.py --repeats 3 --clients python,ffi,ipc,ipc_goroutine
"""

import argparse
import contextlib
import copy
import functools
import hashlib
import itertools
import json
import math
import os
import platform
import random
import resource
import shutil
import socket
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
import warnings
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait as futures_wait

warnings.filterwarnings("ignore", category=UserWarning)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GO_CORE_DIR = os.path.join(SCRIPT_DIR, "spanner_go_core")
IPC_DIR = os.path.join(GO_CORE_DIR, "ipc")
IPC_SERVER_BIN = os.path.join(IPC_DIR, "spanner_ipc_server")
IPC_EXT_SO = os.path.join(IPC_DIR, "spanner_ipc_ext.so")
IPC_BUILD_SCRIPT = os.path.join(GO_CORE_DIR, "build_ipc_core.sh")
IPC_SOURCES_SHA = os.path.join(IPC_DIR, "ipc_build_sources.sha256")
FFI_LIB = os.path.join(GO_CORE_DIR, "libspanner_go.so")
for _p in (GO_CORE_DIR, IPC_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

PROJECT = os.environ.get("SPANNER_BENCH_PROJECT", "span-cloud-testing")
INSTANCE = os.environ.get("SPANNER_BENCH_INSTANCE", "suvham-testing")
DATABASE = os.environ.get("SPANNER_BENCH_DATABASE", "benchmark_db_async")
TABLE = os.environ.get("SPANNER_BENCH_TABLE", "AsyncBenchmarkTable")
POINT_SELECT_SQL = f"SELECT * FROM {TABLE} WHERE id = @id"

CLIENTS = ("python", "python_nometrics", "ffi", "ipc", "ipc_goroutine", "null")
DEFAULT_CLIENTS = ("python", "ffi", "ipc")
IPC_CLIENTS = ("ipc", "ipc_goroutine")
SPANNER_FREE_CLIENTS = ("null",)
CLIENT_LABELS = {
    "python": "Pure Python (stock client)",
    "python_nometrics": "Pure Python, built-in metrics disabled",
    "ffi": "Go core FFI (unchanged)",
    "ipc": "Go core IPC (sidecar, locked-thread calls)",
    "ipc_goroutine": "Go core IPC (sidecar, plain goroutines)",
    "null": "Harness baseline (sleep only, no Spanner)",
}
WORKLOADS = ("point", "heavy")
WORKLOAD_LABELS = {"point": "Point select", "heavy": "Heavy read"}
DEFAULT_QPS = (10, 50, 100, 500)

# --channels auto. Concurrency term (Little's law): qps * design latency, <= 25 concurrent streams per
# HTTP/2 channel (GFE allows 100). Bandwidth term: the Go core opens every channel with a fixed 16 MiB
# HTTP/2 connection window (client.go), so one channel moves at most window/RTT bytes per second; keep
# it <= 50% utilized. Both terms give the same N to every client.
CHANNEL_DESIGN_LATENCY_S = 0.2
CHANNEL_TARGET_STREAMS = 25
CHANNEL_MAX = 16
GO_CORE_CONN_WINDOW_BYTES = 16 * 1024 * 1024
CHANNEL_BANDWIDTH_UTIL = 0.5
DEFAULT_BYTES_PER_QUERY = {"point": 1300, "heavy": 1_200_000}
# --max-inflight auto: worker threads for qps * 1 s of latency, capped per workload (memory).
INFLIGHT_BUDGET_S = 1.0
INFLIGHT_MIN = 32
INFLIGHT_MAX = {"point": 256, "heavy": 128}


# =============================================================================================
# Small helpers
# =============================================================================================
def heavy_sql_for(limit):
    return f"SELECT * FROM {TABLE} LIMIT {int(limit)}"


def auto_channels(qps, workload, rtt_s=None, bytes_per_query=None):
    streams = math.ceil(qps * CHANNEL_DESIGN_LATENCY_S / CHANNEL_TARGET_STREAMS)
    bandwidth = 0
    if rtt_s:
        per_channel_bytes_s = CHANNEL_BANDWIDTH_UTIL * GO_CORE_CONN_WINDOW_BYTES / max(rtt_s, 1e-4)
        bandwidth = math.ceil(qps * (bytes_per_query or DEFAULT_BYTES_PER_QUERY[workload]) / per_channel_bytes_s)
    return max(1, min(CHANNEL_MAX, max(streams, bandwidth)))


def plan_channels(spec, workloads, qps_list, rtt_s=None, bytes_by_workload=None):
    spec = str(spec).strip().lower()
    bytes_by_workload = bytes_by_workload or {}
    if spec == "auto":
        return {(w, q): auto_channels(q, w, rtt_s, bytes_by_workload.get(w)) for w in workloads for q in qps_list}
    if ":" in spec:
        mapping = {}
        for part in spec.split(","):
            q, n = part.split(":")
            mapping[float(q)] = int(n)
        missing = [q for q in qps_list if float(q) not in mapping]
        if missing:
            raise SystemExit(f"--channels mapping is missing QPS levels: {missing}")
        return {(w, q): mapping[float(q)] for w in workloads for q in qps_list}
    return {(w, q): int(spec) for w in workloads for q in qps_list}


def auto_max_inflight(qps, workload):
    return max(INFLIGHT_MIN, min(INFLIGHT_MAX[workload], math.ceil(qps * INFLIGHT_BUDGET_S)))


def percentiles(values):
    if not values:
        return {"n": 0, "p50": None, "p90": None, "p99": None, "p999": None, "max": None, "mean": None}
    v = sorted(values)

    def q(p):
        k = (len(v) - 1) * p
        lo, hi = math.floor(k), math.ceil(k)
        return v[lo] + (v[hi] - v[lo]) * (k - lo)

    return {"n": len(v), "p50": q(0.50), "p90": q(0.90), "p99": q(0.99), "p999": q(0.999), "max": v[-1],
            "mean": sum(v) / len(v)}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def go_bin():
    for cand in (shutil.which("go"), "/usr/local/go/bin/go", os.path.expanduser("~/go/bin/go")):
        if cand and os.path.exists(cand):
            return cand
    return None


def go_build_fingerprint(path):
    """Go toolchain, module graph (incl. h1 hashes/replacements) and relevant build settings."""
    gb = go_bin()
    if not gb or not os.path.exists(path):
        return None
    try:
        out = subprocess.run([gb, "version", "-m", path], capture_output=True, text=True, timeout=30).stdout
    except Exception:  # noqa: BLE001
        return None
    lines = out.splitlines()
    if not lines:
        return None
    deps, build = [], []
    for line in lines[1:]:
        parts = line.split()
        if not parts:
            continue
        if parts[0] in ("dep", "=>"):
            deps.append(" ".join(parts))
        elif parts[0] == "build":
            key = parts[1].split("=", 1)[0] if len(parts) > 1 else ""
            if key not in ("-buildmode", "-tags") and not key.startswith("vcs"):
                build.append(" ".join(parts[1:]))
    return {"go_version": lines[0].split(":", 1)[-1].strip(), "deps": deps, "build": sorted(build)}


def calibrate_wake_cost(iterations=2000, sleep_s=20e-6):
    """CPU charged per short sleep/wake cycle on this host (Go's sysmon polls with 20 us sleeps)."""
    ru0 = resource.getrusage(resource.RUSAGE_SELF)
    t0 = time.perf_counter()
    for _ in range(iterations):
        time.sleep(sleep_s)
    wall = time.perf_counter() - t0
    ru1 = resource.getrusage(resource.RUSAGE_SELF)
    cpu = (ru1.ru_utime + ru1.ru_stime) - (ru0.ru_utime + ru0.ru_stime)
    return {"sleep_us": sleep_s * 1e6, "cpu_us_per_sleep_wake": cpu * 1e6 / iterations,
            "wall_us_per_sleep_wake": wall * 1e6 / iterations}


_CLK_TCK = os.sysconf("SC_CLK_TCK") if hasattr(os, "sysconf") else 100


def read_thread_stats(pid):
    """{tid: (comm, cpu_ns, voluntary_cs, involuntary_cs)} for every thread of `pid` (from /proc)."""
    out = {}
    base = f"/proc/{pid}/task"
    try:
        tids = os.listdir(base)
    except OSError:
        return out
    for tid in tids:
        try:
            with open(f"{base}/{tid}/comm", "r", encoding="utf-8", errors="replace") as f:
                comm = f.read().strip()
            try:
                with open(f"{base}/{tid}/schedstat", "r", encoding="utf-8") as f:
                    cpu_ns = int(f.read().split()[0])
            except (OSError, ValueError, IndexError):
                with open(f"{base}/{tid}/stat", "r", encoding="utf-8", errors="replace") as f:
                    fields = f.read().rsplit(")", 1)[1].split()
                cpu_ns = (int(fields[11]) + int(fields[12])) * 1_000_000_000 // _CLK_TCK
            vcs = ivcs = 0
            with open(f"{base}/{tid}/status", "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if line.startswith("voluntary_ctxt_switches"):
                        vcs = int(line.split()[1])
                    elif line.startswith("nonvoluntary_ctxt_switches"):
                        ivcs = int(line.split()[1])
            out[int(tid)] = (comm, cpu_ns, vcs, ivcs)
        except (OSError, ValueError, IndexError):
            continue
    return out


def thread_breakdown(before, after, completed, top=5):
    """Per-thread CPU / voluntary-context-switch deltas over the window (threads that exited inside the
    window are not visible here; whole-process totals still come from getrusage)."""
    rows = []
    for tid, (comm, cpu1, v1, i1) in after.items():
        _, cpu0, v0, i0 = before.get(tid, (comm, 0, 0, 0))
        dcpu, dv, di = cpu1 - cpu0, v1 - v0, i1 - i0
        if dcpu <= 0 and dv <= 0:
            continue
        rows.append({"tid": tid, "comm": comm, "cpu_ms": dcpu / 1e6, "vol_cs": dv, "invol_cs": di,
                     "cpu_us_per_vol_cs": (dcpu / 1e3 / dv) if dv else None})
    n = max(1, completed)
    by_cs = sorted(rows, key=lambda r: r["vol_cs"], reverse=True)
    top_waker = by_cs[0] if by_cs else None
    return {
        "threads_active": len(rows),
        "cpu_ms_total": sum(r["cpu_ms"] for r in rows),
        "vol_cs_total": sum(r["vol_cs"] for r in rows),
        "top_waker_vol_cs_per_query": (top_waker["vol_cs"] / n) if top_waker else None,
        "top_waker_cpu_us_per_vol_cs": top_waker["cpu_us_per_vol_cs"] if top_waker else None,
        "top_by_vol_cs": by_cs[:top],
        "top_by_cpu": sorted(rows, key=lambda r: r["cpu_ms"], reverse=True)[:top],
    }


def fmt_ms(v, width=0):
    if v is None:
        s = "-"
    elif v >= 1000:
        s = f"{v:.0f}"
    elif v >= 100:
        s = f"{v:.1f}"
    else:
        s = f"{v:.2f}"
    return s.rjust(width) if width else s


def fmt_num(v, nd=2, width=0):
    s = "-" if v is None else f"{v:.{nd}f}"
    return s.rjust(width) if width else s


# =============================================================================================
# Artifact management (IPC only; the FFI artifacts are never rebuilt by this script)
# =============================================================================================
def ipc_artifacts_fresh():
    """True when the IPC artifacts were built from the current shared-core + IPC sources (sha256)."""
    if not (os.path.exists(IPC_SERVER_BIN) and os.path.exists(IPC_EXT_SO) and os.path.exists(IPC_SOURCES_SHA)):
        return False, "IPC artifacts missing"
    with open(IPC_SOURCES_SHA, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) != 2:
                continue
            digest, name = parts
            src = os.path.join(GO_CORE_DIR, name)
            if not os.path.exists(src) or sha256_file(src) != digest:
                return False, f"source changed since the IPC artifacts were built: {name}"
    return True, "ok"


def ensure_ipc_artifacts(force=False):
    fresh, why = ipc_artifacts_fresh()
    if fresh and not force:
        return
    print(f"[*] (Re)building IPC artifacts ({'forced' if force else why}) via {IPC_BUILD_SCRIPT} ...", flush=True)
    subprocess.run(["bash", IPC_BUILD_SCRIPT], check=True, env=dict(os.environ, PYTHON=sys.executable))


def load_ffi_ext():
    try:
        import spanner_go_ext  # noqa: WPS433 (unchanged FFI extension)
    except Exception as exc:  # pragma: no cover - environment specific
        raise RuntimeError(
            f"Could not import the FFI extension spanner_go_ext ({exc}). "
            f"Build it with: bash {os.path.join(GO_CORE_DIR, 'build_go_core.sh')}"
        ) from exc
    return spanner_go_ext


def load_ipc_ext():
    import spanner_ipc_ext  # noqa: WPS433

    return spanner_ipc_ext


# =============================================================================================
# Workloads (identical for every client)
# =============================================================================================
def run_point_select_query_sync(database, user_id):
    from google.cloud.spanner_v1 import param_types

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            POINT_SELECT_SQL,
            params={"id": user_id},
            param_types={"id": param_types.STRING},
        )
        rows = list(results)
        return len(rows)


def run_heavy_read_query_sync(database, sql):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(sql)
        rows = list(results)
        return len(rows)


def make_request_fn(workload, database, heavy_sql):
    if workload == "point":
        user_ids = [f"user-{i}" for i in range(100)]
        return lambda i: run_point_select_query_sync(database, user_ids[i % 100])
    return lambda i: run_heavy_read_query_sync(database, heavy_sql)


def extract_multiplexed_session_name(database):
    """Creates (via the stock Python path) and returns the multiplexed session name."""
    from google.cloud.spanner_v1 import param_types

    with database.snapshot() as snapshot:
        _ = list(
            snapshot.execute_sql(
                POINT_SELECT_SQL,
                params={"id": "user-0"},
                param_types={"id": param_types.STRING},
            )
        )
        return snapshot._session.name


@contextlib.contextmanager
def go_core_snapshot_hook(execute_fn, fallback_session_name):
    """Plugs a Go Shared Core executor under the sync Snapshot.execute_sql.

    Used verbatim for BOTH ffi and ipc: the Python snapshot checkout / session lifecycle is identical
    and only `execute_fn` differs:
        ffi: functools.partial(spanner_go_ext.execute_streaming_sql, cid)
        ipc: functools.partial(spanner_ipc_ext.execute_streaming_sql, handle)
    (Same logic as patched_sync_snapshot_go_core in spanner_cpu_profile_suite.py.)
    """
    from google.cloud.spanner_v1.snapshot import _SnapshotBase

    orig_execute_sql = _SnapshotBase.execute_sql

    def go_core_sync_execute_sql(
        self,
        sql,
        params=None,
        param_types=None,
        query_mode=None,
        query_options=None,
        request_options=None,
        last_statement=False,
        partition=None,
        retry=None,
        timeout=None,
        data_boost_enabled=False,
        directed_read_options=None,
        column_info=None,
        lazy_decode=False,
    ):
        with self._lock:
            if self._begin_request_sent or self._read_request_count > 0:
                if not self._multi_use:
                    raise ValueError("Cannot re-use single-use snapshot.")
            else:
                self._begin_request_sent = True
        self._execute_sql_request_count += 1
        self._read_request_count += 1
        param_id = params.get("id", "") if params else ""
        sess_name = (
            self._session.name
            if getattr(self, "_session", None) is not None and getattr(self._session, "_session_id", None)
            else fallback_session_name
        )
        return execute_fn(sess_name, sql, param_id)

    _SnapshotBase.execute_sql = go_core_sync_execute_sql
    try:
        yield
    finally:
        _SnapshotBase.execute_sql = orig_execute_sql


# =============================================================================================
# Pure-Python client with the same static number of gRPC channels
# =============================================================================================
def make_round_robin_channel_pool(channels):
    import grpc

    class RoundRobinChannelPool(grpc.Channel):
        """grpc.Channel facade over N independent channels (separate subchannel pools -> separate
        HTTP/2 connections), one channel picked per RPC. The GAPIC MetricsInterceptor re-resolves
        the multicallable on every RPC, so consecutive RPCs land on consecutive channels."""

        def __init__(self, chans):
            self._channels = list(chans)
            self._n = len(self._channels)
            self._rr = itertools.count()
            self._picks = [itertools.count() for _ in self._channels]  # atomic under the GIL

        @property
        def rpc_counts(self):
            return [c.__reduce__()[1][0] for c in self._picks]

        def _pick(self):
            idx = next(self._rr) % self._n
            next(self._picks[idx])
            return self._channels[idx]

        def unary_unary(self, method, request_serializer=None, response_deserializer=None, _registered_method=False):
            ch = self._pick()
            if _registered_method:
                return ch.unary_unary(method, request_serializer, response_deserializer, _registered_method)
            return ch.unary_unary(method, request_serializer, response_deserializer)

        def unary_stream(self, method, request_serializer=None, response_deserializer=None, _registered_method=False):
            ch = self._pick()
            if _registered_method:
                return ch.unary_stream(method, request_serializer, response_deserializer, _registered_method)
            return ch.unary_stream(method, request_serializer, response_deserializer)

        def stream_unary(self, method, request_serializer=None, response_deserializer=None, _registered_method=False):
            ch = self._pick()
            if _registered_method:
                return ch.stream_unary(method, request_serializer, response_deserializer, _registered_method)
            return ch.stream_unary(method, request_serializer, response_deserializer)

        def stream_stream(self, method, request_serializer=None, response_deserializer=None, _registered_method=False):
            ch = self._pick()
            if _registered_method:
                return ch.stream_stream(method, request_serializer, response_deserializer, _registered_method)
            return ch.stream_stream(method, request_serializer, response_deserializer)

        def subscribe(self, callback, try_to_connect=False):
            for ch in self._channels:
                ch.subscribe(callback, try_to_connect)

        def unsubscribe(self, callback):
            for ch in self._channels:
                ch.unsubscribe(callback)

        def close(self):
            for ch in self._channels:
                ch.close()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()
            return False

    return RoundRobinChannelPool(channels)


def attach_pooled_spanner_api(database, channel_count):
    """Builds database.spanner_api exactly like Database.spanner_api does (same credentials, client
    info, client options, MetricsInterceptor and stock channel options) except that the transport's
    channel is a round-robin pool of `channel_count` independent channels."""
    import google.auth.credentials
    from google.cloud.spanner_v1 import database as database_module
    from google.cloud.spanner_v1.services.spanner import SpannerClient
    from google.cloud.spanner_v1.services.spanner.transports.grpc import SpannerGrpcTransport

    spanner_client = database._instance._client
    credentials = spanner_client.credentials
    if isinstance(credentials, google.auth.credentials.Scoped):
        scope = getattr(database_module, "SPANNER_DATA_SCOPE", "https://www.googleapis.com/auth/spanner.data")
        credentials = credentials.with_scopes((scope,))
    holder = {}

    def channel_factory(host, **kwargs):
        base_options = list(kwargs.pop("options", None) or [])
        chans = [
            SpannerGrpcTransport.create_channel(
                host, options=base_options + [("grpc.use_local_subchannel_pool", 1)], **kwargs
            )
            for _ in range(channel_count)
        ]
        holder["pool"] = make_round_robin_channel_pool(chans)
        return holder["pool"]

    def transport_factory(**kwargs):
        return SpannerGrpcTransport(channel=channel_factory, **kwargs)

    database._spanner_api = SpannerClient(
        credentials=credentials,
        client_info=spanner_client._client_info,
        client_options=spanner_client._client_options,
        transport=transport_factory,
    )
    database._channel_id = 1
    return holder["pool"]


# =============================================================================================
# IPC sidecar process
# =============================================================================================
class IpcSidecar:
    def __init__(self, sockbuf, log_path, lock_os_thread=True):
        self.sockbuf = int(sockbuf)
        self.lock_os_thread = bool(lock_os_thread)
        self.log_path = log_path
        self.tmpdir = tempfile.mkdtemp(prefix="spanner_ipc_")
        self.socket_path = os.path.join(self.tmpdir, "core.sock")
        self.proc = None
        self._log = None

    def start(self, ipc_ext, timeout_s=30.0):
        os.makedirs(os.path.dirname(self.log_path) or ".", exist_ok=True)
        self._log = open(self.log_path, "ab")
        cmd = [IPC_SERVER_BIN, "-socket", self.socket_path, "-sockbuf", str(self.sockbuf),
               "-parent-pid", str(os.getpid())]
        if self.lock_os_thread:
            cmd.append("-lock-os-thread")
        self.proc = subprocess.Popen(cmd, stdout=self._log, stderr=subprocess.STDOUT, env=os.environ.copy(),
                                     close_fds=True)
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                raise RuntimeError(f"IPC sidecar exited early (code {self.proc.returncode}); see {self.log_path}")
            if os.path.exists(self.socket_path) and ipc_ext.ping(self.socket_path):
                return
            time.sleep(0.02)
        raise RuntimeError(f"IPC sidecar did not become ready within {timeout_s}s; see {self.log_path}")

    def stop(self, ipc_ext):
        if self.proc is not None and self.proc.poll() is None:
            with contextlib.suppress(Exception):
                ipc_ext.shutdown_server(self.socket_path)
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
        if self._log:
            self._log.close()
        shutil.rmtree(self.tmpdir, ignore_errors=True)


# =============================================================================================
# Client flows (setup / CPU probe / teardown). Every flow measures the same way.
# =============================================================================================
def base_probe():
    ru = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "wall": time.perf_counter(),
        "client_cpu": ru.ru_utime + ru.ru_stime,
        "client_user": ru.ru_utime,
        "client_sys": ru.ru_stime,
        "client_nvcsw": ru.ru_nvcsw,
        "client_nivcsw": ru.ru_nivcsw,
    }


def go_core_breakdown(delta7):
    calls = delta7[0]
    if not calls:
        return None
    return {
        "calls": calls,
        "chunks_per_call": delta7[1] / calls,
        "req_build_marshal_us_per_call": delta7[2] / 1e3 / calls,
        "proto_unmarshal_us_per_call": delta7[4] / 1e3 / calls,
        "chunk_assemble_us_per_call": delta7[5] / 1e3 / calls,
        "arena_encode_us_per_call": delta7[6] / 1e3 / calls,
    }


class NullFlow:
    """Harness-overhead baseline: same dispatcher + worker pool, request = sleep(), no Spanner."""

    name = "null"

    def __init__(self, database, channels, null_sleep_s=0.005, **_):
        self.null_sleep_s = null_sleep_s

    def start(self):
        pass

    def probe(self):
        return base_probe()

    def pids(self):
        return {"client": os.getpid()}

    def details(self, p0, p1, completed):
        return {"null_sleep_ms": self.null_sleep_s * 1e3}

    def close(self):
        pass


class PythonFlow:
    name = "python"

    def __init__(self, database, channels, **_):
        self.database = database
        self.channels = channels
        self.pool = None

    def start(self):
        self.pool = attach_pooled_spanner_api(self.database, self.channels)

    def probe(self):
        return base_probe()

    def pids(self):
        return {"client": os.getpid()}

    def details(self, p0, p1, completed):
        return {
            "channel_rpc_counts": self.pool.rpc_counts if self.pool else None,
            "builtin_metrics_disabled": os.environ.get("SPANNER_DISABLE_BUILTIN_METRICS", "").lower() == "true",
        }

    def close(self):
        pass


class FfiFlow:
    name = "ffi"

    def __init__(self, database, channels, **_):
        self.database = database
        self.channels = channels
        self.go_ext = None
        self.cid = None
        self._hook = None

    def start(self):
        self.go_ext = load_ffi_ext()
        session_name = extract_multiplexed_session_name(self.database)
        self.cid = self.go_ext.init_client(self.channels)
        self._hook = go_core_snapshot_hook(functools.partial(self.go_ext.execute_streaming_sql, self.cid), session_name)
        self._hook.__enter__()

    def probe(self):
        d = base_probe()
        d["core"] = tuple(self.go_ext.get_core_stats())  # read-only counters of the unchanged FFI ext
        return d

    def pids(self):
        return {"client": os.getpid()}

    def start_profile(self, path):
        return self.go_ext.start_cpu_profile(path)

    def stop_profile(self):
        self.go_ext.stop_cpu_profile()

    def details(self, p0, p1, completed):
        delta = [b - a for a, b in zip(p0["core"], p1["core"])]
        calls = max(1, delta[0])
        return {
            "go_core": go_core_breakdown(delta[:7]),
            "python_decode_us_per_call": delta[7] / 1e3 / calls if len(delta) > 7 else None,
        }

    def close(self):
        if self._hook:
            self._hook.__exit__(None, None, None)
        if self.go_ext is not None and self.cid:
            self.go_ext.close_client(self.cid)


class IpcFlow:
    """IPC client. lock_os_thread=True (client 'ipc') runs every Go Shared Core call in the sidecar on
    a goroutine locked to its OS thread, like the FFI cgo callback goroutine. lock_os_thread=False
    (client 'ipc_goroutine') is the natural plain-goroutine sidecar."""

    name = "ipc"

    def __init__(self, database, channels, sockbuf=0, log_path=None, lock_os_thread=True, **_):
        self.database = database
        self.channels = channels
        self.sockbuf = sockbuf
        self.lock_os_thread = lock_os_thread
        self.log_path = log_path or os.path.join(tempfile.gettempdir(), "spanner_ipc_server.log")
        self.ipc = None
        self.sidecar = None
        self.handle = None
        self.server_info = None
        self._hook = None

    def start(self):
        self.ipc = load_ipc_ext()
        self.sidecar = IpcSidecar(self.sockbuf, self.log_path, lock_os_thread=self.lock_os_thread)
        self.sidecar.start(self.ipc)
        session_name = extract_multiplexed_session_name(self.database)
        self.handle = self.ipc.open_client(self.sidecar.socket_path, self.channels, self.sockbuf)
        self.server_info = json.loads(self.ipc.server_info(self.handle))
        self._hook = go_core_snapshot_hook(functools.partial(self.ipc.execute_streaming_sql, self.handle), session_name)
        self._hook.__enter__()

    def probe(self):
        d = base_probe()
        s = self.ipc.server_stats(self.handle)
        d.update(
            server_cpu=(s[0] + s[1]) / 1e6,
            server_user=s[0] / 1e6,
            server_sys=s[1] / 1e6,
            server_nvcsw=s[11],
            server_nivcsw=s[12],
            server_goroutines=s[9],
            core=tuple(s[2:9]),
            ipc_client=tuple(self.ipc.client_stats()),
        )
        return d

    def pids(self):
        return {"client": os.getpid(), "sidecar": self.sidecar.proc.pid}

    def start_profile(self, path):
        return self.ipc.server_prof_start(self.handle, path)

    def stop_profile(self):
        self.ipc.server_prof_stop(self.handle)

    def details(self, p0, p1, completed):
        delta = [b - a for a, b in zip(p0["core"], p1["core"])]
        cdelta = [b - a for a, b in zip(p0["ipc_client"], p1["ipc_client"])]
        reqs = max(1, cdelta[0])
        return {
            "go_core": go_core_breakdown(delta),
            "python_decode_us_per_call": cdelta[5] / 1e3 / reqs,
            "ipc": {
                "requests": cdelta[0],
                "bytes_sent_per_query": cdelta[1] / reqs,
                "bytes_recv_per_query": cdelta[2] / reqs,
                "send_calls_per_query": cdelta[3] / reqs,
                "recv_hops_per_query": cdelta[4] / reqs,
                "large_response_ratio": cdelta[7] / reqs,
                "new_connections_in_window": cdelta[6],
                "server_goroutines": p1.get("server_goroutines"),
            },
            "sidecar": {
                k: self.server_info.get(k) for k in ("go_version", "gomaxprocs", "num_cpu", "sockbuf", "lock_os_thread")
            },
        }

    def close(self):
        if self._hook:
            self._hook.__exit__(None, None, None)
        if self.ipc is not None and self.handle:
            with contextlib.suppress(Exception):
                self.ipc.close_client(self.handle)
        if self.sidecar is not None:
            self.sidecar.stop(self.ipc)


FLOWS = {
    "python": PythonFlow,
    "python_nometrics": PythonFlow,
    "ffi": FfiFlow,
    "ipc": functools.partial(IpcFlow, lock_os_thread=True),
    "ipc_goroutine": functools.partial(IpcFlow, lock_os_thread=False),
    "null": NullFlow,
}


# =============================================================================================
# Open-loop driver
# =============================================================================================
def build_schedule(qps, warmup_s, duration_s, arrival, seed):
    """Arrival offsets: the rate ramps 20% -> 100% over the first half of the warmup, then stays at qps."""
    rng = random.Random(seed)
    ramp_s = min(warmup_s * 0.5, 5.0)
    total_s = warmup_s + duration_s
    offsets = []
    if arrival == "uniform":
        t = 0.0
        while t < ramp_s:
            offsets.append(t)
            t += 1.0 / (qps * (0.2 + 0.8 * t / ramp_s))
        start = math.ceil(ramp_s * qps) / qps  # steady part on an exact grid (no float drift)
        n_steady = int(round((total_s - start) * qps))
        offsets.extend(start + k / qps for k in range(n_steady))
        return [o for o in offsets if o < total_s]
    t = rng.expovariate(qps * 0.2) if ramp_s > 0 else rng.expovariate(qps)
    while t < total_s:
        offsets.append(t)
        rate = qps if t >= ramp_s else qps * (0.2 + 0.8 * t / ramp_s)
        t += rng.expovariate(rate)
    return offsets


def run_open_loop(request_fn, qps, warmup_s, duration_s, max_inflight, arrival, seed, probe, log=print):
    """One continuous open-loop stream: [ramped warmup | measurement window]."""
    total_s = warmup_s + duration_s
    offsets = build_schedule(qps, warmup_s, duration_s, arrival, seed)
    n = len(offsets)
    intended = [0.0] * n
    submitted = [0.0] * n
    started = [0.0] * n
    ended = [0.0] * n
    rows = [-1] * n
    error_samples = []

    def task(i):
        started[i] = time.perf_counter()
        try:
            rows[i] = request_fn(i)
        except Exception as exc:  # noqa: BLE001 - every failure is reported
            rows[i] = -1
            if len(error_samples) < 10:
                error_samples.append(f"{type(exc).__name__}: {exc}"[:400])
        ended[i] = time.perf_counter()

    executor = ThreadPoolExecutor(max_workers=max_inflight, thread_name_prefix="openloop")
    futures = [None] * n
    submit = executor.submit
    sleep = time.sleep
    perf = time.perf_counter
    try:
        t0 = perf() + 0.05
        window_start = t0 + warmup_s
        window_end = t0 + total_s
        probe_start = None
        sleep(max(0.0, t0 - perf()))
        log(f"    warmup {warmup_s:.1f}s (ramped) + measure {duration_s:.1f}s @ {qps:g} QPS ({n} scheduled requests, "
            f"<= {max_inflight} in flight, {arrival} arrivals)")
        for i in range(n):
            target = t0 + offsets[i]
            if probe_start is None and target >= window_start:
                now = perf()
                if window_start > now:
                    sleep(window_start - now)
                probe_start = probe()  # CPU sample at the window start edge
            now = perf()
            if target > now:
                sleep(target - now)
            intended[i] = target
            submitted[i] = perf()
            futures[i] = submit(task, i)
        if probe_start is None:
            sleep(max(0.0, window_start - perf()))
            probe_start = probe()
        sleep(max(0.0, window_end - perf()))
        probe_end = probe()  # CPU sample at the window end edge
        t_close = perf()
        dropped_idx = [i for i in range(n) if futures[i].cancel()]
        futures_wait([f for f in futures if not f.cancelled()])
        drain_s = perf() - t_close
        threads_peak = len(executor._threads)  # noqa: SLF001 - informational
    finally:
        executor.shutdown(wait=True)

    # Requests are classified against the nominal schedule edges; CPU uses the probe timestamps.
    ws, we = window_start, window_end
    window_idx = [i for i in range(n) if ws <= intended[i] < we]
    done = [i for i in window_idx if ended[i] > 0.0 and rows[i] >= 0]
    failed = [i for i in window_idx if ended[i] > 0.0 and rows[i] < 0]
    dropped = [i for i in dropped_idx if ws <= intended[i] < we]
    completions_in_window = sum(1 for i in range(n) if ws <= ended[i] <= we and rows[i] >= 0)
    lat_done = [(ended[i] - intended[i]) * 1e3 for i in done]
    lat_censored = [(t_close - intended[i]) * 1e3 for i in dropped]  # lower bound for dropped requests
    half = ws + duration_s / 2.0
    first = [(ended[i] - intended[i]) * 1e3 for i in done if intended[i] < half]
    second = [(ended[i] - intended[i]) * 1e3 for i in done if intended[i] >= half]
    return {
        "probe_start": probe_start,
        "probe_end": probe_end,
        "window_s": we - ws,
        "cpu_window_s": probe_end["wall"] - probe_start["wall"],
        "scheduled_in_window": len(window_idx),
        "completed": len(done),
        "errors": len(failed),
        "error_samples": error_samples,
        "dropped_unstarted": len(dropped),
        "completions_in_window": completions_in_window,
        "latency_ms": percentiles(lat_done + lat_censored),
        "latency_completed_ms": percentiles(lat_done),
        "service_ms": percentiles([(ended[i] - started[i]) * 1e3 for i in done]),
        "queue_ms": percentiles([(started[i] - intended[i]) * 1e3 for i in done]),
        "dispatch_lag_ms": percentiles([(submitted[i] - intended[i]) * 1e3 for i in window_idx if submitted[i]]),
        "pool_wait_ms": percentiles([(started[i] - submitted[i]) * 1e3 for i in done]),
        "latency_p50_first_half_ms": statistics.median(first) if first else None,
        "latency_p50_second_half_ms": statistics.median(second) if second else None,
        "rows_per_query": (sum(rows[i] for i in done) / len(done)) if done else None,
        "drain_s": drain_s,
        "threads_peak": threads_peak,
    }


# =============================================================================================
# Worker: one (client, workload, qps, rep) run in a fresh process
# =============================================================================================
def run_worker(args):
    if args.client == "python_nometrics":
        os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = "true"  # before the Spanner client is imported
    tag = f"[{args.client}/{args.workload}/{args.qps:g}qps/{args.channels}ch/rep{args.rep}]"
    log = lambda msg: print(f"{tag} {msg}", flush=True)  # noqa: E731
    heavy_sql = heavy_sql_for(args.heavy_limit)
    database = None
    if args.client not in SPANNER_FREE_CLIENTS:
        from google.cloud import spanner

        database = spanner.Client(project=PROJECT).instance(INSTANCE).database(DATABASE)
    run_name = f"{args.workload}_{args.qps:g}qps_{args.client}_rep{args.rep}"
    flow = FLOWS[args.client](
        database,
        args.channels,
        sockbuf=args.ipc_sockbuf,
        log_path=os.path.join(args.output_dir, "runs", f"sidecar_{run_name}.log"),
        null_sleep_s=args.null_sleep_ms / 1e3,
    )
    result = {
        "client": args.client,
        "workload": args.workload,
        "offered_qps": args.qps,
        "channels": args.channels,
        "max_inflight": args.max_inflight,
        "arrival": args.arrival,
        "warmup_s": args.warmup,
        "duration_s": args.duration,
        "rep": args.rep,
        "sql": POINT_SELECT_SQL if args.workload == "point" else heavy_sql,
        "pid": os.getpid(),
    }
    try:
        flow.start()
        if args.client in SPANNER_FREE_CLIENTS:
            sleep_s = args.null_sleep_ms / 1e3
            request_fn = lambda i: (time.sleep(sleep_s), 1)[1]  # noqa: E731
        else:
            request_fn = make_request_fn(args.workload, database, heavy_sql)
            prewarm = max(4, 2 * args.channels)
            log(f"pre-warming {prewarm} sequential requests (connects all {args.channels} channel(s))")
            for i in range(prewarm):
                request_fn(i)

        pprof_path = None
        if args.go_pprof and hasattr(flow, "start_profile"):
            # Diagnostic only: Go runtime/pprof CPU profile of the window (in-process for FFI, inside the
            # sidecar for IPC). Off by default: SIGPROF sampling adds overhead and cannot see sysmon.
            pprof_path = os.path.join(args.output_dir, "runs", f"{run_name}.pprof")
            result["go_pprof"] = pprof_path
        edges = {"n": 0, "threads0": None, "threads1": None}

        def probe():
            # Window start: [pprof start] -> CPU sample -> per-thread snapshot.
            # Window end:   CPU sample -> per-thread snapshot -> [pprof stop].
            if edges["n"] == 0:
                if pprof_path:
                    flow.start_profile(pprof_path)
                sample = flow.probe()
                if args.thread_stats:
                    edges["threads0"] = {k: read_thread_stats(pid) for k, pid in flow.pids().items()}
            else:
                sample = flow.probe()
                if args.thread_stats:
                    edges["threads1"] = {k: read_thread_stats(pid) for k, pid in flow.pids().items()}
                if pprof_path:
                    flow.stop_profile()
            edges["n"] += 1
            return sample

        phase = run_open_loop(request_fn, args.qps, args.warmup, args.duration, args.max_inflight, args.arrival,
                              args.seed, probe, log=log)
        p0, p1 = phase.pop("probe_start"), phase.pop("probe_end")
        window, cpu_window = phase["window_s"], phase["cpu_window_s"]
        client_cpu = p1["client_cpu"] - p0["client_cpu"]
        server_cpu = (p1["server_cpu"] - p0["server_cpu"]) if "server_cpu" in p0 else 0.0
        total_cpu = client_cpu + server_cpu
        completions = phase["completions_in_window"]
        achieved = completions / window if window > 0 else 0.0
        offered_rate = phase["scheduled_in_window"] / window if window > 0 else 0.0
        goodput = phase["completed"] / window if window > 0 else 0.0
        h1, h2 = phase["latency_p50_first_half_ms"], phase["latency_p50_second_half_ms"]
        drift = (h2 / h1) if h1 and h2 else None
        result.update(phase)
        result["achieved_qps"] = achieved  # completions that landed inside the window
        result["goodput_qps"] = goodput  # window-scheduled requests that eventually succeeded
        result["offered_rate_in_window"] = offered_rate
        result["latency_drift_ratio"] = drift
        result["saturated"] = bool(phase["dropped_unstarted"] > 0 or achieved < 0.95 * offered_rate)
        result["pool_cap_hit"] = bool(phase["threads_peak"] >= args.max_inflight)
        result["non_stationary"] = bool(
            (offered_rate > 0 and abs(achieved - offered_rate) / offered_rate > 0.05)
            or (drift is not None and (drift > 1.25 or drift < 0.8) and abs(h2 - h1) > 5.0)
        )
        result["flags"] = ("S" if result["saturated"] else "") + ("P" if result["pool_cap_hit"] else "") + (
            "N" if result["non_stationary"] else "")
        cvcs = p1["client_nvcsw"] - p0["client_nvcsw"]
        svcs = (p1["server_nvcsw"] - p0["server_nvcsw"]) if "server_nvcsw" in p0 else 0
        result["cpu"] = {
            "client_s": client_cpu,
            "server_s": server_cpu,
            "total_s": total_cpu,
            "client_user_s": p1["client_user"] - p0["client_user"],
            "client_sys_s": p1["client_sys"] - p0["client_sys"],
            "server_user_s": (p1["server_user"] - p0["server_user"]) if "server_user" in p0 else 0.0,
            "server_sys_s": (p1["server_sys"] - p0["server_sys"]) if "server_sys" in p0 else 0.0,
            "cores_used": total_cpu / cpu_window if cpu_window > 0 else None,
            "client_cores": client_cpu / cpu_window if cpu_window > 0 else None,
            "server_cores": server_cpu / cpu_window if cpu_window > 0 else None,
            "util_pct_of_machine": (total_cpu / cpu_window) / (os.cpu_count() or 1) * 100.0 if cpu_window > 0 else None,
            "ms_per_query": total_cpu * 1e3 / completions if completions else None,
            "client_ms_per_query": client_cpu * 1e3 / completions if completions else None,
            "server_ms_per_query": server_cpu * 1e3 / completions if completions else None,
            "client_vol_ctx_switches": cvcs,
            "client_invol_ctx_switches": p1["client_nivcsw"] - p0["client_nivcsw"],
            "server_vol_ctx_switches": svcs,
            "server_invol_ctx_switches": (p1["server_nivcsw"] - p0["server_nivcsw"]) if "server_nivcsw" in p0 else 0,
            "vol_ctx_switches_per_query": (cvcs + svcs) / completions if completions else None,
            "client_vol_ctx_switches_per_query": cvcs / completions if completions else None,
            "server_vol_ctx_switches_per_query": svcs / completions if completions else None,
        }
        if edges["threads0"] is not None and edges["threads1"] is not None:
            result["threads"] = {
                k: thread_breakdown(edges["threads0"].get(k, {}), edges["threads1"].get(k, {}), completions)
                for k in edges["threads1"]
            }
        result.update(flow.details(p0, p1, completions))
        result["ok"] = True
        lat = result["latency_ms"]
        log(
            f"done: goodput {goodput:.1f} / achieved {achieved:.1f} / offered {offered_rate:.1f} QPS | "
            f"p50 {fmt_ms(lat['p50'])} p99 {fmt_ms(lat['p99'])} ms | CPU {result['cpu']['cores_used']:.3f} cores, "
            f"{fmt_ms(result['cpu']['ms_per_query'])} ms/q | errors {phase['errors']} dropped {phase['dropped_unstarted']} "
            f"flags [{result['flags']}]"
        )
    except Exception as exc:  # noqa: BLE001
        result["ok"] = False
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["traceback"] = traceback.format_exc()
        log(f"FAILED: {result['error']}")
    finally:
        with contextlib.suppress(Exception):
            flow.close()
    with open(args.result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)
    return 0 if result.get("ok") else 1


# =============================================================================================
# Parity check (FFI vs IPC rows identical; Python rows equal after str normalization) + RTT probe
# =============================================================================================
def run_parity(args):
    from google.cloud import spanner
    from google.cloud.spanner_v1 import param_types

    print("[parity] verifying FFI vs IPC vs pure-Python results ...", flush=True)
    database = spanner.Client(project=PROJECT).instance(INSTANCE).database(DATABASE)
    go_ext = load_ffi_ext()
    ipc = load_ipc_ext()
    sidecar = IpcSidecar(args.ipc_sockbuf, os.path.join(args.output_dir, "runs", "sidecar_parity.log"), lock_os_thread=True)
    sidecar.start(ipc)
    report = {"ok": False}
    cid = handle = None
    try:
        session_name = extract_multiplexed_session_name(database)
        cid = go_ext.init_client(1)
        handle = ipc.open_client(sidecar.socket_path, 1, args.ipc_sockbuf)
        report["sidecar_info"] = json.loads(ipc.server_info(handle))

        ids = [f"user-{i}" for i in range(20)]
        point_mismatch, rtts = [], []
        for uid in ids:
            t = time.perf_counter()
            a = go_ext.execute_streaming_sql(cid, session_name, POINT_SELECT_SQL, uid)
            rtts.append(time.perf_counter() - t)
            if a != ipc.execute_streaming_sql(handle, session_name, POINT_SELECT_SQL, uid):
                point_mismatch.append(uid)
        ordered_heavy = f"SELECT * FROM {TABLE} ORDER BY id LIMIT {int(args.heavy_limit)}"
        ffi_heavy = go_ext.execute_streaming_sql(cid, session_name, ordered_heavy, "")
        ipc.reset_client_stats()
        ipc_heavy = ipc.execute_streaming_sql(handle, session_name, ordered_heavy, "")
        heavy_stats = ipc.client_stats()
        ipc.reset_client_stats()
        ipc_point = ipc.execute_streaming_sql(handle, session_name, POINT_SELECT_SQL, "user-1")
        point_stats = ipc.client_stats()

        def norm(rows):
            return [[None if v is None else str(v) for v in row] for row in rows]

        with database.snapshot() as snap:
            py_heavy = [list(r) for r in snap.execute_sql(ordered_heavy)]
        with database.snapshot() as snap:
            py_point = [list(r) for r in snap.execute_sql(POINT_SELECT_SQL, params={"id": "user-1"},
                                                            param_types={"id": param_types.STRING})]
        with go_core_snapshot_hook(functools.partial(go_ext.execute_streaming_sql, cid), session_name):
            hooked_ffi = run_heavy_read_query_sync(database, ordered_heavy)
        with go_core_snapshot_hook(functools.partial(ipc.execute_streaming_sql, handle), session_name):
            hooked_ipc = run_heavy_read_query_sync(database, ordered_heavy)

        report.update(
            {
                "point_ids_checked": len(ids),
                "point_ffi_vs_ipc_mismatches": point_mismatch,
                "heavy_rows": {"ffi": len(ffi_heavy), "ipc": len(ipc_heavy), "python": len(py_heavy)},
                "heavy_ffi_equals_ipc": ffi_heavy == ipc_heavy,
                "heavy_python_equals_go_core_str_normalized": norm(py_heavy) == norm(ffi_heavy),
                "point_python_equals_go_core_str_normalized": norm(py_point) == norm(ipc_point),
                "hooked_snapshot_rows": {"ffi": hooked_ffi, "ipc": hooked_ipc},
                "ipc_heavy_bytes": heavy_stats[2],
                "ipc_heavy_recv_hops": heavy_stats[4],
                "ipc_point_bytes": point_stats[2],
                "ipc_point_recv_hops": point_stats[4],
                "point_rtt_ms_min": min(rtts) * 1e3,
                "point_rtt_ms_median": statistics.median(rtts) * 1e3,
            }
        )
        report["ok"] = bool(
            not point_mismatch
            and report["heavy_ffi_equals_ipc"]
            and report["heavy_python_equals_go_core_str_normalized"]
            and report["point_python_equals_go_core_str_normalized"]
            and hooked_ffi == hooked_ipc == len(ffi_heavy) == len(py_heavy)
        )
    except Exception as exc:  # noqa: BLE001
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()
    finally:
        with contextlib.suppress(Exception):
            if handle:
                ipc.close_client(handle)
        with contextlib.suppress(Exception):
            if cid:
                go_ext.close_client(cid)
        sidecar.stop(ipc)
    print(f"[parity] {json.dumps({k: v for k, v in report.items() if k not in ('traceback', 'sidecar_info')})}", flush=True)
    with open(args.result_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    return 0 if report.get("ok") else 1


def run_rtt_probe(args):
    """RTT estimate with the stock Python client (used for channel sizing when parity is skipped)."""
    from google.cloud import spanner

    database = spanner.Client(project=PROJECT).instance(INSTANCE).database(DATABASE)
    rtts = []
    for i in range(12):
        t = time.perf_counter()
        run_point_select_query_sync(database, f"user-{i}")
        rtts.append(time.perf_counter() - t)
    out = {"ok": True, "point_rtt_ms_min": min(rtts[2:]) * 1e3, "point_rtt_ms_median": statistics.median(rtts[2:]) * 1e3}
    with open(args.result_path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    return 0


# =============================================================================================
# Orchestrator + reporting
# =============================================================================================
def build_plan(clients, workloads, qps_list, repeats):
    plan, step = [], 0
    for rep in range(repeats):
        for w in workloads:
            for q in qps_list:
                k = step % len(clients)
                for c in list(clients[k:]) + list(clients[:k]):  # rotate client order to spread drift
                    plan.append((rep, w, q, c))
                step += 1
    return plan


def spawn(args_list, log_path, timeout_s):
    cmd = [sys.executable, os.path.abspath(__file__)] + args_list
    with open(log_path, "ab") as logf:
        try:
            return subprocess.run(cmd, stdout=None, stderr=logf, timeout=timeout_s).returncode
        except subprocess.TimeoutExpired:
            return -999


def _median(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None


def _get(d, path):
    for k in path.split("."):
        if d is None:
            return None
        d = d.get(k) if isinstance(d, dict) else None
    return d


AGG_FIELDS = [
    "achieved_qps", "goodput_qps", "latency_ms.p50", "latency_ms.p90", "latency_ms.p99", "latency_ms.p999",
    "latency_ms.max", "cpu.cores_used", "cpu.client_cores", "cpu.server_cores", "cpu.ms_per_query",
    "cpu.client_ms_per_query", "cpu.server_ms_per_query", "cpu.vol_ctx_switches_per_query",
    "cpu.client_vol_ctx_switches_per_query", "cpu.server_vol_ctx_switches_per_query", "ipc.bytes_recv_per_query",
    "ipc.recv_hops_per_query", "go_core.proto_unmarshal_us_per_call", "python_decode_us_per_call", "rows_per_query",
    "threads.client.top_waker_vol_cs_per_query", "threads.client.top_waker_cpu_us_per_vol_cs",
    "threads.sidecar.top_waker_vol_cs_per_query", "threads.sidecar.top_waker_cpu_us_per_vol_cs",
]


def aggregate_runs(runs):
    """Median across repetitions per (workload, qps, client); counts are summed, flags OR-ed."""
    groups = defaultdict(list)
    for r in runs:
        groups[(r["workload"], r["offered_qps"], r["client"])].append(r)
    out = []
    for (w, q, c), rs in groups.items():
        ok = [r for r in rs if r.get("ok")]
        if not ok:
            out.append(dict(rs[0], reps=len(rs), reps_ok=0))
            continue
        a = copy.deepcopy(ok[0])
        for path in AGG_FIELDS:
            med = _median([_get(r, path) for r in ok])
            node, keys = a, path.split(".")
            for k in keys[:-1]:
                node = node.get(k) if isinstance(node, dict) else None
                if node is None:
                    break
            if isinstance(node, dict):
                node[keys[-1]] = med
        a["errors"] = sum(r["errors"] for r in ok)
        a["dropped_unstarted"] = sum(r["dropped_unstarted"] for r in ok)
        a["flags"] = "".join(f for f in "SPN" if any(f in (r.get("flags") or "") for r in ok))
        a["reps"], a["reps_ok"] = len(rs), len(ok)
        p50s = [_get(r, "latency_ms.p50") for r in ok]
        cpus = [_get(r, "cpu.ms_per_query") for r in ok]
        a["p50_range"] = (min(p50s), max(p50s)) if all(v is not None for v in p50s) else None
        a["cpu_ms_range"] = (min(cpus), max(cpus)) if all(v is not None for v in cpus) else None
        out.append(a)
    out.sort(key=lambda r: (WORKLOADS.index(r["workload"]), r["offered_qps"], CLIENTS.index(r["client"])))
    return out


def _ok(r):
    return r.get("ok", False) and r.get("reps_ok", 1) > 0


def cpu_split(r):
    if r["client"] in IPC_CLIENTS and r.get("cpu"):
        return f"{r['cpu']['client_cores']:.3f}+{r['cpu']['server_cores']:.3f}"
    return ""


def ffi_ipc_rows(agg):
    idx = {(r["workload"], r["offered_qps"], r["client"]): r for r in agg if _ok(r)}
    rows = []
    for w in WORKLOADS:
        for q in sorted({k[1] for k in idx if k[0] == w}):
            r_ffi = idx.get((w, q, "ffi"))
            if not r_ffi:
                continue
            for ic in IPC_CLIENTS:
                r_ipc = idx.get((w, q, ic))
                if not r_ipc:
                    continue
                cf, ci = r_ffi["cpu"]["ms_per_query"], r_ipc["cpu"]["ms_per_query"]
                rows.append({
                    "workload": w, "qps": q, "ipc_client": ic,
                    "p50_ffi": r_ffi["latency_ms"]["p50"], "p50_ipc": r_ipc["latency_ms"]["p50"],
                    "p99_ffi": r_ffi["latency_ms"]["p99"], "p99_ipc": r_ipc["latency_ms"]["p99"],
                    "cpu_ffi": cf, "cpu_ipc": ci,
                    "cpu_overhead_pct": ((ci - cf) / cf * 100.0) if cf and ci else None,
                    "vcs_ffi": r_ffi["cpu"].get("vol_ctx_switches_per_query"),
                    "vcs_ipc": r_ipc["cpu"].get("vol_ctx_switches_per_query"),
                    "waker_ffi": _get(r_ffi, "threads.client.top_waker_vol_cs_per_query"),
                    "waker_ipc": _get(r_ipc, "threads.sidecar.top_waker_vol_cs_per_query"),
                    "bytes": _get(r_ipc, "ipc.bytes_recv_per_query"), "hops": _get(r_ipc, "ipc.recv_hops_per_query"),
                    "unm_ffi": _get(r_ffi, "go_core.proto_unmarshal_us_per_call"),
                    "unm_ipc": _get(r_ipc, "go_core.proto_unmarshal_us_per_call"),
                    "flags": (r_ffi.get("flags") or "-") + "/" + (r_ipc.get("flags") or "-"),
                })
    return rows


def vs_python_rows(agg):
    idx = {(r["workload"], r["offered_qps"], r["client"]): r for r in agg if _ok(r)}
    rows = []
    for w in WORKLOADS:
        for q in sorted({k[1] for k in idx if k[0] == w}):
            base = idx.get((w, q, "python"))
            if not base:
                continue
            row = {"workload": w, "qps": q, "python": base}
            for c in ("python_nometrics", "ffi", "ipc", "ipc_goroutine"):
                row[c] = idx.get((w, q, c))
            rows.append(row)
    return rows


def print_report(agg, repeats):
    width = 176
    print("\n" + "=" * width)
    print(f"OPEN-LOOP RESULTS (median of {repeats} rep(s); latency from scheduled send time, dropped requests censored "
          "at window close; CPU = client process + IPC sidecar)")
    print("Flags: S=saturated  P=worker-pool cap hit  N=non-stationary")
    print("=" * width)
    print(
        f"{'Workload':<8} {'QPS':>5} {'Ch':>3} {'Client':<16} {'Goodput':>8} {'Achieved':>8} {'p50 ms':>9} {'p90 ms':>9} "
        f"{'p99 ms':>9} {'p99.9 ms':>9} {'CPU cores':>9} {'(cli+side)':>12} {'CPU ms/q':>9} {'vcs/q':>7} {'Err':>4} "
        f"{'Drop':>6} {'Flags':>5} {'p50 range':>15} {'CPU ms/q range':>15}"
    )
    print("-" * width)
    for r in agg:
        if not _ok(r):
            print(f"{r['workload']:<8} {r['offered_qps']:>5g} {str(r.get('channels')):>3} {r['client']:<16} "
                  f"FAILED: {str(r.get('error', ''))[:100]}")
            continue
        lat, cpu = r["latency_ms"], r["cpu"]
        pr, cr, multi = r.get("p50_range"), r.get("cpu_ms_range"), r.get("reps", 1) > 1
        print(
            f"{r['workload']:<8} {r['offered_qps']:>5g} {r['channels']:>3} {r['client']:<16} {r['goodput_qps']:>8.1f} "
            f"{r['achieved_qps']:>8.1f} {fmt_ms(lat['p50'], 9)} {fmt_ms(lat['p90'], 9)} {fmt_ms(lat['p99'], 9)} "
            f"{fmt_ms(lat['p999'], 9)} {cpu['cores_used']:>9.3f} {cpu_split(r):>12} {fmt_ms(cpu['ms_per_query'], 9)} "
            f"{fmt_num(cpu.get('vol_ctx_switches_per_query'), 1, 7)} {r['errors']:>4} {r['dropped_unstarted']:>6} "
            f"{r.get('flags') or '-':>5} {(fmt_ms(pr[0]) + '-' + fmt_ms(pr[1])) if pr and multi else '':>15} "
            f"{(fmt_ms(cr[0]) + '-' + fmt_ms(cr[1])) if cr and multi else '':>15}"
        )
    rows = ffi_ipc_rows(agg)
    if rows:
        print("\n" + "-" * width)
        print("FFI vs IPC (identical Go Shared Core; only the boundary differs).  top-waker = busiest-waking thread "
              "(FFI: client process; IPC: sidecar), voluntary context switches per query")
        print("-" * width)
        print(
            f"{'Workload':<8} {'QPS':>5} {'IPC client':<14} {'p50 FFI':>9} {'p50 IPC':>9} {'p99 FFI':>9} {'p99 IPC':>9} "
            f"{'CPU/q FFI':>10} {'CPU/q IPC':>10} {'IPC CPU ovh':>12} {'vcs/q FFI':>10} {'vcs/q IPC':>10} "
            f"{'top-waker F/I':>14} {'IPC B/q':>10} {'hops/q':>7} {'unmarshal us F/I':>17} {'flags':>8}"
        )
        for row in rows:
            print(
                f"{row['workload']:<8} {row['qps']:>5g} {row['ipc_client']:<14} {fmt_ms(row['p50_ffi'], 9)} "
                f"{fmt_ms(row['p50_ipc'], 9)} {fmt_ms(row['p99_ffi'], 9)} {fmt_ms(row['p99_ipc'], 9)} "
                f"{fmt_ms(row['cpu_ffi'], 10)} {fmt_ms(row['cpu_ipc'], 10)} {fmt_num(row['cpu_overhead_pct'], 1, 11)}% "
                f"{fmt_num(row['vcs_ffi'], 1, 10)} {fmt_num(row['vcs_ipc'], 1, 10)} "
                f"{(fmt_num(row['waker_ffi'], 1) + '/' + fmt_num(row['waker_ipc'], 1)):>14} {fmt_num(row['bytes'], 0, 10)} "
                f"{fmt_num(row['hops'], 2, 7)} {(fmt_num(row['unm_ffi'], 1) + '/' + fmt_num(row['unm_ipc'], 1)):>17} "
                f"{row['flags']:>8}"
            )
    vrows = vs_python_rows(agg)
    if vrows:
        print("\n" + "-" * width)
        print("vs pure Python (CPU ms/query; speedup = python CPU / client CPU; p50 latency)")
        print("-" * width)
        for row in vrows:
            parts = []
            for c in ("python_nometrics", "ffi", "ipc", "ipc_goroutine"):
                r = row.get(c)
                if r:
                    cp, cc = row["python"]["cpu"]["ms_per_query"], r["cpu"]["ms_per_query"]
                    parts.append(f"{c} {fmt_ms(cc)} ms/q ({(cp / cc) if cp and cc else 0:.1f}x) p50 {fmt_ms(r['latency_ms']['p50'])}")
            print(f"{row['workload']:<8} {row['qps']:>5g}  python {fmt_ms(row['python']['cpu']['ms_per_query'])} ms/q "
                  f"p50 {fmt_ms(row['python']['latency_ms']['p50'])}  |  " + "  |  ".join(parts))
    print("=" * width)


def summarize_markdown(meta, parity, agg, repeats):
    L = ["# Open-loop benchmark: Go Shared Core FFI vs IPC vs pure-Python client\n"]
    L.append(f"* Host: `{meta['host']}` ({meta['cpu_count']} vCPU), Python {meta['python']}, started {meta['started_at']}")
    wc = meta.get("host_wake_cost") or {}
    L.append(f"* Host wake cost: {fmt_num(wc.get('cpu_us_per_sleep_wake'), 1)} µs CPU per 20 µs sleep/wake cycle "
             "(drives the cost of Go's sysmon polling after cgo callbacks)")
    L.append(f"* Target: `{meta['target']}`; heavy read: `{meta['heavy_sql']}`; RTT estimate: {fmt_ms(meta.get('rtt_ms'))} ms")
    L.append(f"* Open loop: {meta['arrival']} arrivals, warmup {meta['warmup_s']} s (ramped) + window {meta['duration_s']} s, "
             f"{repeats} interleaved rep(s), fresh process per run, client order rotated")
    L.append(f"* Channels per workload/QPS (same for all clients): `{meta['channels']}`")
    L.append(f"* Max in-flight per workload/QPS: `{meta['max_inflight']}`")
    L.append(f"* FFI/IPC build parity: {meta.get('build_parity')}")
    L.append("* Clients: " + "; ".join(f"`{c}` = {CLIENT_LABELS[c]}" for c in meta.get("clients", [])))
    if parity:
        L.append(f"* Result parity: **{'PASS' if parity.get('ok') else 'FAIL'}** (heavy rows ffi/ipc/python = "
                 f"{parity.get('heavy_rows')}; IPC heavy response {parity.get('ipc_heavy_bytes')} B in "
                 f"{parity.get('ipc_heavy_recv_hops')} recv hops; point {parity.get('ipc_point_bytes')} B in "
                 f"{parity.get('ipc_point_recv_hops')} hop(s))")
    L.append("* Flags: S = saturated, P = worker-pool cap hit, N = non-stationary. Latency percentiles include dropped "
             "requests censored at window close.\n")
    L.append("| Workload | QPS | Ch | Client | Goodput | Achieved | p50 ms | p90 ms | p99 ms | p99.9 ms | CPU cores (client+sidecar) | CPU ms/query | vol. ctx sw/query | Err | Drop | Flags |")
    L.append("| :-- | --: | --: | :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | :-: |")
    for r in agg:
        if not _ok(r):
            L.append(f"| {r['workload']} | {r['offered_qps']:g} | {r.get('channels')} | {r['client']} | FAILED: "
                     f"{str(r.get('error', ''))[:80]} |||||||||||")
            continue
        lat, cpu = r["latency_ms"], r["cpu"]
        split = cpu_split(r)
        L.append(
            f"| {r['workload']} | {r['offered_qps']:g} | {r['channels']} | {r['client']} | {r['goodput_qps']:.1f} | "
            f"{r['achieved_qps']:.1f} | {fmt_ms(lat['p50'])} | {fmt_ms(lat['p90'])} | {fmt_ms(lat['p99'])} | "
            f"{fmt_ms(lat['p999'])} | {cpu['cores_used']:.3f}{(' (' + split + ')') if split else ''} | "
            f"{fmt_ms(cpu['ms_per_query'])} | {fmt_num(cpu.get('vol_ctx_switches_per_query'), 1)} | {r['errors']} | "
            f"{r['dropped_unstarted']} | {r.get('flags') or '-'} |"
        )
    rows = ffi_ipc_rows(agg)
    if rows:
        L.append("\n## FFI vs IPC (same Go Shared Core, different boundary)\n")
        L.append("| Workload | QPS | IPC client | p50 FFI → IPC (ms) | p99 FFI → IPC (ms) | CPU ms/q FFI → IPC | IPC CPU overhead | vol. ctx sw/q FFI → IPC | top-waker thread cs/q FFI → IPC sidecar | IPC bytes/query | IPC recv hops/query | Go unmarshal µs/call FFI → IPC | Flags FFI/IPC |")
        L.append("| :-- | --: | :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | :-: |")
        for row in rows:
            L.append(
                f"| {row['workload']} | {row['qps']:g} | {row['ipc_client']} | {fmt_ms(row['p50_ffi'])} → {fmt_ms(row['p50_ipc'])} | "
                f"{fmt_ms(row['p99_ffi'])} → {fmt_ms(row['p99_ipc'])} | {fmt_ms(row['cpu_ffi'])} → {fmt_ms(row['cpu_ipc'])} | "
                f"{fmt_num(row['cpu_overhead_pct'], 1)}% | {fmt_num(row['vcs_ffi'], 1)} → {fmt_num(row['vcs_ipc'], 1)} | "
                f"{fmt_num(row['waker_ffi'], 1)} → {fmt_num(row['waker_ipc'], 1)} | {fmt_num(row['bytes'], 0)} | "
                f"{fmt_num(row['hops'], 2)} | {fmt_num(row['unm_ffi'], 1)} → {fmt_num(row['unm_ipc'], 1)} | {row['flags']} |"
            )
    L.append("\nNotes: CPU is whole-process (client `RUSAGE_SELF` + sidecar `getrusage`) and includes the harness's own "
             "dispatcher/worker-pool cost (measure it with `--clients null`). The top-waker column is the thread with the "
             "most voluntary context switches in the window; for FFI at low QPS this is typically Go's sysmon polling "
             "every 20 µs after each cgo callback returns (an FFI-only boundary cost). The Go unmarshal column is a "
             "thread-CPU phase timer that is only reliable when calls stay on one OS thread (`ffi`, `ipc`).")
    return "\n".join(L)


def run_orchestrator(args):
    clients = [c.strip() for c in args.clients.split(",") if c.strip()]
    workloads = [w.strip() for w in args.workloads.split(",") if w.strip()]
    qps_list = [float(q) if "." in q else int(q) for q in args.qps.split(",") if q.strip()]
    for c in clients:
        if c not in CLIENTS:
            raise SystemExit(f"unknown client {c!r}; choose from {CLIENTS}")
    for w in workloads:
        if w not in WORKLOADS:
            raise SystemExit(f"unknown workload {w!r}; choose from {WORKLOADS}")
    inflight = {(w, q): (auto_max_inflight(q, w) if str(args.max_inflight).lower() == "auto" else int(args.max_inflight))
                for w in workloads for q in qps_list}
    os.makedirs(args.output_dir, exist_ok=True)
    runs_dir = os.path.join(args.output_dir, "runs")
    os.makedirs(runs_dir, exist_ok=True)

    if any(c in IPC_CLIENTS for c in clients):
        ensure_ipc_artifacts(force=args.rebuild_ipc)
    if "ffi" in clients and not os.path.exists(FFI_LIB):
        raise SystemExit(f"FFI library missing: {FFI_LIB} (build with spanner_go_core/build_go_core.sh)")
    ffi_fp, ipc_fp = go_build_fingerprint(FFI_LIB), go_build_fingerprint(IPC_SERVER_BIN)
    if ffi_fp and ipc_fp:
        build_parity = "OK (same Go toolchain, module graph and build settings)" if ffi_fp == ipc_fp else "MISMATCH"
        if ffi_fp != ipc_fp:
            print("[!] WARNING: FFI library and IPC sidecar differ in Go toolchain/modules/build settings:")
            print(f"    FFI: {ffi_fp['go_version']} build={ffi_fp['build']}\n    IPC: {ipc_fp['go_version']} build={ipc_fp['build']}")
            print("    Rebuild both on this machine: bash spanner_go_core/build_go_core.sh && bash spanner_go_core/build_ipc_core.sh")
    else:
        build_parity = "unverified here ('go' not found); artifacts carry ipc_build_sources.sha256"

    common = ["--heavy-limit", str(args.heavy_limit), "--ipc-sockbuf", str(args.ipc_sockbuf), "--output-dir",
              args.output_dir, "--arrival", args.arrival, "--null-sleep-ms", str(args.null_sleep_ms)]
    if args.go_pprof:
        common.append("--go-pprof")
    if not args.thread_stats:
        common.append("--no-thread-stats")

    print("=" * 110)
    print("Spanner Go Shared Core open-loop benchmark: FFI vs IPC vs pure Python")
    print(f"  clients={clients} workloads={workloads} qps={qps_list} arrival={args.arrival} repeats={args.repeats}")
    print(f"  warmup={args.warmup}s (ramped) window={args.duration}s build parity: {build_parity}")
    print(f"  output: {args.output_dir}")
    print("=" * 110, flush=True)

    wake = calibrate_wake_cost()
    print(f"[*] host wake cost: {wake['cpu_us_per_sleep_wake']:.1f} us CPU per 20 us sleep/wake cycle", flush=True)

    # Parity check (also measures RTT and response sizes used for channel sizing).
    parity, rtt_ms, bytes_by_workload = None, None, {}
    spanner_clients = [c for c in clients if c not in SPANNER_FREE_CLIENTS]
    if not args.list_plan and spanner_clients:
        if args.parity_check and "ffi" in clients and any(c in IPC_CLIENTS for c in clients):
            ppath = os.path.join(runs_dir, "parity.json")
            rc = spawn(["--_parity", "--_result-path", ppath] + common, os.path.join(runs_dir, "parity.log"), 600)
            if os.path.exists(ppath):
                with open(ppath, "r", encoding="utf-8") as f:
                    parity = json.load(f)
            if rc != 0 or not (parity or {}).get("ok"):
                print(f"[!] PARITY CHECK FAILED (rc={rc}); see {ppath} / {os.path.join(runs_dir, 'parity.log')}")
                if not args.ignore_parity_failure:
                    return 2
            if parity:
                rtt_ms = parity.get("point_rtt_ms_min")
                bytes_by_workload = {"point": parity.get("ipc_point_bytes"), "heavy": parity.get("ipc_heavy_bytes")}
        else:
            rpath = os.path.join(runs_dir, "rtt_probe.json")
            spawn(["--_probe", "--_result-path", rpath] + common, os.path.join(runs_dir, "rtt_probe.log"), 300)
            if os.path.exists(rpath):
                with open(rpath, "r", encoding="utf-8") as f:
                    rtt_ms = json.load(f).get("point_rtt_ms_min")
    channels = plan_channels(args.channels, workloads, qps_list, (rtt_ms / 1e3) if rtt_ms else None, bytes_by_workload)
    print(f"[*] RTT estimate: {fmt_ms(rtt_ms)} ms -> channels per (workload, QPS): "
          + ", ".join(f"{w}@{q:g}={n}" for (w, q), n in channels.items()))
    print("[*] max in-flight per (workload, QPS): " + ", ".join(f"{w}@{q:g}={n}" for (w, q), n in inflight.items()),
          flush=True)

    plan = build_plan(clients, workloads, qps_list, args.repeats)
    meta = {
        "host": socket.gethostname(),
        "cpu_count": os.cpu_count(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "clients": clients,
        "target": f"projects/{PROJECT}/instances/{INSTANCE}/databases/{DATABASE}",
        "heavy_sql": heavy_sql_for(args.heavy_limit),
        "arrival": args.arrival,
        "warmup_s": args.warmup,
        "duration_s": args.duration,
        "repeats": args.repeats,
        "rtt_ms": rtt_ms,
        "host_wake_cost": wake,
        "channels": {f"{w}/{q:g}": n for (w, q), n in channels.items()},
        "max_inflight": {f"{w}/{q:g}": n for (w, q), n in inflight.items()},
        "ipc_sockbuf": args.ipc_sockbuf,
        "build_parity": build_parity,
        "ffi_build": ffi_fp,
        "ipc_build": ipc_fp,
        "plan": [f"rep{rep}/{w}/{q:g}/{c}" for rep, w, q, c in plan],
    }
    if args.list_plan:
        for item in meta["plan"]:
            print("  ", item)
        return 0

    runs = []
    for n_run, (rep, w, q, c) in enumerate(plan, 1):
        name = f"{w}_{q:g}qps_{c}_rep{rep}"
        rpath = os.path.join(runs_dir, f"{name}.json")
        ch = channels[(w, q)]
        print(f"\n[{n_run}/{len(plan)}] rep {rep + 1}/{args.repeats}: {WORKLOAD_LABELS[w]} @ {q:g} QPS — {CLIENT_LABELS[c]} "
              f"({ch} channel(s))", flush=True)
        worker_args = [
            "--_worker", "--client", c, "--workload", w, "--qps", str(q), "--channels", str(ch),
            "--max-inflight", str(inflight[(w, q)]), "--warmup", str(args.warmup), "--duration", str(args.duration),
            "--seed", str(args.seed + int(q) + 1000 * rep), "--rep", str(rep), "--_result-path", rpath,
        ] + common
        rc = spawn(worker_args, os.path.join(runs_dir, f"{name}.log"), args.warmup + args.duration + args.run_timeout)
        if os.path.exists(rpath):
            with open(rpath, "r", encoding="utf-8") as f:
                res = json.load(f)
        else:
            res = {"client": c, "workload": w, "offered_qps": q, "channels": ch, "rep": rep, "ok": False,
                   "error": f"worker exited rc={rc} without results (see {name}.log)"}
        runs.append(res)
        if args.cooldown > 0 and n_run < len(plan):
            time.sleep(args.cooldown)

    agg = aggregate_runs(runs)
    meta["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    json_path = os.path.join(args.output_dir, "open_loop_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "parity": parity, "aggregated": agg, "runs": runs}, f, indent=2, default=str)
    md_path = os.path.join(args.output_dir, "open_loop_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(summarize_markdown(meta, parity, agg, args.repeats))
    print_report(agg, args.repeats)
    print(f"\n[+] Results: {json_path}\n[+] Summary: {md_path}")
    return 0 if all(r.get("ok") for r in runs) else 1


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--clients", default=",".join(DEFAULT_CLIENTS),
                   help="Comma list of " + ",".join(CLIENTS) + " (default: python,ffi,ipc)")
    p.add_argument("--workloads", default=",".join(WORKLOADS), help="Comma list of point,heavy (default: both)")
    p.add_argument("--qps", default=",".join(str(q) for q in DEFAULT_QPS), help="Offered QPS levels (default: 10,50,100,500)")
    p.add_argument("--duration", type=float, default=20.0, help="Measurement window per run in seconds (default 20)")
    p.add_argument("--warmup", type=float, default=8.0, help="Ramped open-loop warmup before the window (default 8)")
    p.add_argument("--repeats", type=int, default=1, help="Interleaved repetitions per cell; reports medians (default 1)")
    p.add_argument("--channels", default="auto",
                   help="gRPC channels for ALL clients: 'auto' (concurrency + bandwidth-delay), an int, or '10:1,50:1,100:2,500:4'")
    p.add_argument("--max-inflight", default="auto", help="Worker threads (max in-flight requests): 'auto' or an int")
    p.add_argument("--arrival", choices=("uniform", "poisson"), default="uniform", help="Open-loop arrival process")
    p.add_argument("--heavy-limit", type=int, default=1000, help="Rows returned by the heavy read (default 1000)")
    p.add_argument("--ipc-sockbuf", type=int, default=0, help="SO_SNDBUF/SO_RCVBUF for IPC sockets (0 = OS default)")
    p.add_argument("--null-sleep-ms", type=float, default=5.0, help="Request duration of the 'null' harness baseline")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--cooldown", type=float, default=2.0, help="Pause between runs in seconds")
    p.add_argument("--run-timeout", type=float, default=900.0, help="Extra seconds allowed per run beyond warmup+window")
    p.add_argument("--output-dir", default=os.path.join(SCRIPT_DIR, "open_loop_results"))
    p.add_argument("--no-parity-check", dest="parity_check", action="store_false")
    p.add_argument("--ignore-parity-failure", action="store_true")
    p.add_argument("--rebuild-ipc", action="store_true", help="Force rebuilding the IPC sidecar + extension")
    p.add_argument("--go-pprof", action="store_true",
                   help="Diagnostic: write a Go CPU profile of each FFI/IPC measurement window to runs/*.pprof")
    p.add_argument("--no-thread-stats", dest="thread_stats", action="store_false",
                   help="Skip per-thread /proc attribution at the window edges")
    p.add_argument("--list-plan", action="store_true")
    p.add_argument("--smoke", action="store_true", help="Quick sanity run: qps 10,50, warmup 2 s, window 4 s")
    # Internal (worker / parity / probe subprocess) flags.
    p.add_argument("--_worker", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--_parity", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--_probe", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--_result-path", dest="result_path", help=argparse.SUPPRESS)
    p.add_argument("--client", help=argparse.SUPPRESS)
    p.add_argument("--workload", help=argparse.SUPPRESS)
    p.add_argument("--rep", type=int, default=0, help=argparse.SUPPRESS)
    args = p.parse_args()

    if args._worker:  # noqa: SLF001
        args.qps = float(args.qps)
        args.channels = int(args.channels)
        args.max_inflight = int(args.max_inflight)
        return run_worker(args)
    if args._parity:  # noqa: SLF001
        return run_parity(args)
    if args._probe:  # noqa: SLF001
        return run_rtt_probe(args)
    if args.smoke:
        args.qps = "10,50"
        args.warmup = 2.0
        args.duration = 4.0
        args.cooldown = 0.5
    return run_orchestrator(args)


if __name__ == "__main__":
    sys.exit(main())
