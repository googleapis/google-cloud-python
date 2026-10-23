"""Pure-Python Low-Maintenance IPC client for the Spanner Go Shared Core sidecar.

Why this is the "Low-Maintenance IPC" flow (`ipc_lowmaint`):
  1. ZERO C-Extension (.so) & ZERO C Compiler Required:
     - 100% pure Python using only the Python standard library (`socket`, `struct`, `json`, `threading`, `os`).
     - Ships as a universal `py3-none-any.whl` (0 KB wheel size increase, no `manylinux`/`musllinux`/macOS/Windows
       wheel matrix, no `<Python.h>` or `gcc`, works on CPython 3.9+, PyPy, and free-threaded Python).
  2. ZERO Cross-Runtime Pointer Sharing & ZERO C Memory Management:
     - Calls `ipcOpExecuteLowMaint` (op=11) on the Go sidecar, which executes `ipcExecuteStreamingSqlPureGo` in
       100% memory-safe Go (zero `C.malloc`, zero `C.free`, zero `unsafe` pointers, plain Go goroutines) and
       streams back standard UTF-8 JSON rows (`[[col1, col2, ...], ...]`), supporting NULL, BOOL, NUMBER, STRING,
       ARRAY, and STRUCT without data loss.
     - Decodes rows via Python's built-in `json.loads()` on a reusable `bytearray` (zero C segfaults, zero manual
       `Py_INCREF`/`Py_DECREF`, 100% visible to `tracemalloc`, `pdb`, `cProfile`, and `py-spy`).
  3. Fixes Process Lifecycle, `fork()`, and Resource Leak Hazards:
     - Registers `os.register_at_fork(after_in_child=...)` so forked child workers (`gunicorn`, `Celery`,
       `multiprocessing`) automatically detach inherited parent sockets instead of interleaving/corrupting frames.
     - Tracks all per-thread sockets per client and closes them deterministically in `close_client()` (no 1,024
       `PTHREAD_KEYS_MAX` limit, no leaked FDs or 16 MiB buffers on thread pools).
     - Uses standard Python socket calls (PEP 475), so `Ctrl+C` (`SIGINT`) interrupts blocked reads cleanly.
"""

from __future__ import annotations

import json
import os
import socket
import struct
import threading
import time

IPC_MAGIC = 0x4F475053  # "SPGO"
IPC_VERSION = 1
IPC_INLINE_BUF = 16384
IPC_MAX_PAYLOAD = 1 << 31
IPC_RETAIN_MAX = 2 << 20  # Cap per-thread retained bytearray at 2 MiB (vs 16 MiB in C ext)

OP_EXECUTE = 1
OP_INIT = 2
OP_CLOSE = 3
OP_STATS = 4
OP_RESET_STATS = 5
OP_PING = 6
OP_SHUTDOWN = 7
OP_PROF_START = 8
OP_PROF_STOP = 9
OP_INFO = 10
OP_EXECUTE_LOWMAINT = 11

_REQ_HDR = struct.Struct("<IHHQIIII")
_RESP_HDR = struct.Struct("<IHHiiiiQQII")
_U64 = struct.Struct("<Q")

_stat_lock = threading.Lock()
_stat_requests = 0
_stat_bytes_sent = 0
_stat_bytes_recv = 0
_stat_send_calls = 0
_stat_recv_calls = 0
_stat_decode_ns = 0
_stat_connects = 0
_stat_heap_responses = 0


def _connect_unix(path: str, sockbuf: int = 0) -> socket.socket:
    global _stat_connects
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        if sockbuf > 0:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, sockbuf)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, sockbuf)
        s.connect(path)
    except Exception:
        s.close()
        raise
    with _stat_lock:
        _stat_connects += 1
    return s


class _ThreadConn:
    """Per-thread persistent AF_UNIX connection with bounded buffer reuse."""

    __slots__ = ("sock", "pid", "inline_buf", "inline_mv", "rbuf")

    def __init__(self, sock: socket.socket, pid: int):
        self.sock: socket.socket | None = sock
        self.pid = pid
        self.inline_buf = bytearray(IPC_INLINE_BUF)
        self.inline_mv = memoryview(self.inline_buf)
        self.rbuf = bytearray()

    def close(self) -> None:
        s, self.sock = self.sock, None
        self.rbuf = bytearray()
        if s is not None:
            try:
                s.close()
            except OSError:
                pass

    def detach_in_forked_child(self) -> None:
        """Close the duplicated FD in a forked child without shutting down the parent's socket."""
        s, self.sock = self.sock, None
        self.rbuf = bytearray()
        if s is not None:
            try:
                s.close()
            except OSError:
                pass


def _roundtrip(
    sock: socket.socket,
    op: int,
    handle: int,
    aux: int,
    b1: bytes,
    b2: bytes,
    b3: bytes,
    tconn: _ThreadConn | None,
):
    """Send 1 framed request and receive 1 framed response."""
    global _stat_bytes_sent, _stat_send_calls
    hdr = _REQ_HDR.pack(IPC_MAGIC, IPC_VERSION, op, handle, len(b1), len(b2), len(b3), aux)
    req = hdr + b1 + b2 + b3 if (b1 or b2 or b3) else hdr
    sock.sendall(req)

    if tconn is not None:
        inline_buf = tconn.inline_buf
        inline_mv = tconn.inline_mv
    else:
        inline_buf = bytearray(IPC_INLINE_BUF)
        inline_mv = memoryview(inline_buf)

    have = sock.recv_into(inline_buf)
    if have == 0:
        raise RuntimeError("Spanner Go IPC sidecar closed connection (ECONNRESET)")
    recv_calls = 1
    while have < 48:
        n = sock.recv_into(inline_mv[have:])
        if n == 0:
            raise RuntimeError("Spanner Go IPC sidecar closed connection mid-header")
        have += n
        recv_calls += 1

    magic, ver, r_op, status, row_count, col_count, attempts, cells_b, arena_b, extra_b, cell_sz = (
        _RESP_HDR.unpack_from(inline_buf, 0)
    )
    if magic != IPC_MAGIC or ver != IPC_VERSION:
        raise RuntimeError(f"Spanner Go IPC protocol mismatch (magic={magic:#x}, ver={ver})")
    total = cells_b + arena_b + extra_b
    if total > IPC_MAX_PAYLOAD:
        raise RuntimeError(f"Spanner Go IPC response payload too large ({total} bytes)")

    got = have - 48
    if got > total:
        raise RuntimeError("Spanner Go IPC framing error: received more bytes than response length")

    heap_alloc = 0
    if total <= IPC_INLINE_BUF - 48:
        target_mv = inline_mv[48 : 48 + total]
        while got < total:
            n = sock.recv_into(target_mv[got:])
            if n == 0:
                raise RuntimeError("Spanner Go IPC sidecar closed connection mid-payload")
            got += n
            recv_calls += 1
        payload_buf = target_mv.tobytes() if total > 0 else b""
    elif tconn is not None and total <= IPC_RETAIN_MAX:
        rbuf = tconn.rbuf
        if len(rbuf) < total:
            rbuf.extend(b"\x00" * (total - len(rbuf)))
        elif len(rbuf) > total:
            del rbuf[total:]
        with memoryview(rbuf) as rmv:
            if got > 0:
                rmv[:got] = inline_mv[48:have]
            while got < total:
                n = sock.recv_into(rmv[got:total])
                if n == 0:
                    raise RuntimeError("Spanner Go IPC sidecar closed connection mid-payload")
                got += n
                recv_calls += 1
        payload_buf = rbuf
    else:
        heap_alloc = 1
        oneoff = bytearray(total)
        with memoryview(oneoff) as omv:
            if got > 0:
                omv[:got] = inline_mv[48:have]
            while got < total:
                n = sock.recv_into(omv[got:total])
                if n == 0:
                    raise RuntimeError("Spanner Go IPC sidecar closed connection mid-payload")
                got += n
                recv_calls += 1
        payload_buf = oneoff

    return len(req), status, row_count, col_count, attempts, cells_b, arena_b, extra_b, payload_buf, recv_calls, heap_alloc


class _LowMaintClient:
    def __init__(self, path: str, channel_count: int, sockbuf: int):
        self.path = path
        self.channel_count = channel_count
        self.sockbuf = sockbuf
        self.closed = False
        self.pid = os.getpid()
        self.lock = threading.Lock()
        self.ctl_lock = threading.Lock()
        self.tls = threading.local()
        self.conns: set[_ThreadConn] = set()
        self.ctl_sock: socket.socket | None = _connect_unix(path, sockbuf)
        try:
            _, status, _, _, _, _, _, _, payload, _, _ = _roundtrip(
                self.ctl_sock, OP_INIT, 0, channel_count, b"", b"", b"", None
            )
            if status != 0 or len(payload) < 8:
                msg = bytes(payload).decode("utf-8", errors="replace") if payload else "INIT failed"
                raise RuntimeError(f"Spanner Go IPC INIT failed ({status}): {msg}")
            (self.server_handle,) = _U64.unpack_from(payload, 0)
        except Exception:
            self.ctl_sock.close()
            self.ctl_sock = None
            raise

    def get_thread_conn(self) -> _ThreadConn:
        if self.closed:
            raise RuntimeError("invalid or closed Spanner Go IPC client handle")
        cur_pid = os.getpid()
        tc: _ThreadConn | None = getattr(self.tls, "conn", None)
        if tc is not None and tc.sock is not None and tc.pid == cur_pid:
            return tc
        if tc is not None:
            tc.detach_in_forked_child()
        sock = _connect_unix(self.path, self.sockbuf)
        tc = _ThreadConn(sock, cur_pid)
        with self.lock:
            if self.closed:
                tc.close()
                raise RuntimeError("invalid or closed Spanner Go IPC client handle")
            self.conns.add(tc)
        self.tls.conn = tc
        return tc

    def drop_thread_conn(self, tc: _ThreadConn) -> None:
        self.tls.conn = None
        with self.lock:
            self.conns.discard(tc)
        tc.close()

    def ctl_call(self, op: int, aux: int = 0, body: bytes = b""):
        with self.ctl_lock:
            if self.closed or self.ctl_sock is None or os.getpid() != self.pid:
                self.ctl_sock = _connect_unix(self.path, self.sockbuf)
                self.pid = os.getpid()
            return _roundtrip(self.ctl_sock, op, self.server_handle, aux, body, b"", b"", None)

    def close(self) -> None:
        with self.lock:
            if self.closed:
                return
            self.closed = True
            conns = list(self.conns)
            self.conns.clear()
        try:
            with self.ctl_lock:
                if self.ctl_sock is not None:
                    try:
                        _roundtrip(self.ctl_sock, OP_CLOSE, self.server_handle, 0, b"", b"", b"", None)
                    finally:
                        self.ctl_sock.close()
                        self.ctl_sock = None
        finally:
            for tc in conns:
                tc.close()

    def reset_after_fork_in_child(self) -> None:
        self.lock = threading.Lock()
        self.ctl_lock = threading.Lock()
        self.tls = threading.local()
        if self.ctl_sock is not None:
            try:
                self.ctl_sock.close()
            except OSError:
                pass
            self.ctl_sock = None
        for tc in list(self.conns):
            tc.detach_in_forked_child()
        self.conns.clear()
        self.pid = os.getpid()


_clients_lock = threading.Lock()
_clients: dict[int, _LowMaintClient] = {}
_next_handle = 1


def _after_fork_in_child() -> None:
    global _clients_lock, _stat_lock
    _clients_lock = threading.Lock()
    _stat_lock = threading.Lock()
    for cl in list(_clients.values()):
        cl.reset_after_fork_in_child()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_after_fork_in_child)


def _get_client(handle: int) -> _LowMaintClient:
    cl = _clients.get(handle)
    if cl is None or cl.closed:
        raise RuntimeError("invalid or closed Spanner Go IPC client handle")
    return cl


def open_client(socket_path: str, channel_count: int = 4, sockbuf: int = 0) -> int:
    global _next_handle
    cl = _LowMaintClient(socket_path, channel_count, sockbuf)
    with _clients_lock:
        h = _next_handle
        _next_handle += 1
        _clients[h] = cl
    return h


def close_client(handle: int) -> None:
    with _clients_lock:
        cl = _clients.pop(handle, None)
    if cl is None:
        raise RuntimeError("invalid or closed Spanner Go IPC client handle")
    cl.close()


def execute_streaming_sql(handle: int, session: str, sql: str, param_id: str = "") -> list:
    global _stat_requests, _stat_bytes_sent, _stat_bytes_recv, _stat_send_calls, _stat_recv_calls, _stat_decode_ns, _stat_heap_responses
    cl = _get_client(handle)
    tc = cl.get_thread_conn()
    s_b = session.encode("utf-8")
    q_b = sql.encode("utf-8")
    p_b = param_id.encode("utf-8") if param_id else b""
    try:
        assert tc.sock is not None
        req_len, status, _, _, _, cells_b, arena_b, extra_b, payload, recv_calls, heap_alloc = _roundtrip(
            tc.sock, OP_EXECUTE_LOWMAINT, cl.server_handle, 0, s_b, q_b, p_b, tc
        )
    except Exception as exc:
        cl.drop_thread_conn(tc)
        raise RuntimeError(f"Spanner Go IPC request failed: {exc}") from exc

    total_recv = 48 + cells_b + arena_b + extra_b
    if status != 0:
        msg = bytes(payload).decode("utf-8", errors="replace") if payload else ""
        if status > 0:
            raise RuntimeError(f"Spanner Go Shared Core RPC error ({status}): {msg}")
        raise RuntimeError(f"Spanner Go IPC server error ({status}): {msg}")

    t0 = time.thread_time_ns()
    rows = json.loads(payload) if arena_b > 0 else []
    dt = max(0, time.thread_time_ns() - t0)

    with _stat_lock:
        _stat_requests += 1
        _stat_bytes_sent += req_len
        _stat_bytes_recv += total_recv
        _stat_send_calls += 1
        _stat_recv_calls += recv_calls
        _stat_decode_ns += dt
        _stat_heap_responses += heap_alloc
    return rows


def server_stats(handle: int) -> tuple[int, ...]:
    cl = _get_client(handle)
    _, status, _, _, _, _, _, _, payload, _, _ = cl.ctl_call(OP_STATS)
    if status != 0:
        raise RuntimeError(f"Spanner Go IPC STATS failed ({status})")
    n = len(payload) // 8
    return struct.unpack(f"<{n}Q", bytes(payload[: n * 8]))


def reset_server_stats(handle: int) -> None:
    cl = _get_client(handle)
    cl.ctl_call(OP_RESET_STATS)


def server_info(handle: int) -> str:
    cl = _get_client(handle)
    _, status, _, _, _, _, _, _, payload, _, _ = cl.ctl_call(OP_INFO)
    if status != 0:
        raise RuntimeError(f"Spanner Go IPC INFO failed ({status})")
    return bytes(payload).decode("utf-8", errors="replace")


def server_prof_start(handle: int, path: str) -> int:
    cl = _get_client(handle)
    _, status, _, _, _, _, _, _, _, _, _ = cl.ctl_call(OP_PROF_START, body=path.encode("utf-8"))
    return status


def server_prof_stop(handle: int) -> None:
    cl = _get_client(handle)
    cl.ctl_call(OP_PROF_STOP)


def _oneshot(socket_path: str, op: int) -> bool:
    try:
        s = _connect_unix(socket_path, 0)
        try:
            _, status, _, _, _, _, _, _, _, _, _ = _roundtrip(s, op, 0, 0, b"", b"", b"", None)
            return status == 0
        finally:
            s.close()
    except Exception:
        return False


def ping(socket_path: str) -> bool:
    return _oneshot(socket_path, OP_PING)


def shutdown_server(socket_path: str) -> bool:
    return _oneshot(socket_path, OP_SHUTDOWN)


def client_stats() -> tuple[int, int, int, int, int, int, int, int]:
    with _stat_lock:
        return (
            _stat_requests,
            _stat_bytes_sent,
            _stat_bytes_recv,
            _stat_send_calls,
            _stat_recv_calls,
            _stat_decode_ns,
            _stat_connects,
            _stat_heap_responses,
        )


def reset_client_stats() -> None:
    global _stat_requests, _stat_bytes_sent, _stat_bytes_recv, _stat_send_calls, _stat_recv_calls, _stat_decode_ns, _stat_connects, _stat_heap_responses
    with _stat_lock:
        _stat_requests = 0
        _stat_bytes_sent = 0
        _stat_bytes_recv = 0
        _stat_send_calls = 0
        _stat_recv_calls = 0
        _stat_decode_ns = 0
        _stat_connects = 0
        _stat_heap_responses = 0
