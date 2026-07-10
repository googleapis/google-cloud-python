# Copyright 2026 Google LLC
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
#
"""Client-side fallback policy for accelerator-routed RPCs.

Mirrors the Go client's ``session.UnimplementedErrorInterceptor``: a daemon that
cannot open any sessions replies ``UNIMPLEMENTED``, and the routing layer
transparently retries the call on the native client. A sticky breaker trips
after enough consecutive ``UNIMPLEMENTED`` replies so a persistently-degraded
daemon stops being dialed at all. A daemon whose subprocess has died mid-flight
trips the breaker immediately — it will never recover.

Any other gRPC error is a real, daemon-served result the native client would
reproduce (the daemon owns retries, so it has already exhausted them), so it is
translated to the matching ``google.api_core`` exception and raised without
falling back.

This module is plain sync-only logic shared verbatim by the async and generated
sync clients; ``grpc.RpcError`` is the common base of both ``grpc.RpcError`` and
``grpc.aio.AioRpcError``, so no CrossSync branching is needed here.
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from grpc import RpcError, StatusCode

from google.api_core import exceptions as core_exceptions

if TYPE_CHECKING:
    from google.cloud.bigtable.data._accelerator._daemon import AcceleratorDaemon

# Consecutive ``UNIMPLEMENTED`` replies that trip the sticky breaker, after which
# the accelerator is bypassed for the lifetime of the Table. Matches the Go
# client's ``session.DefaultUnimplementedThreshold``.
DEFAULT_UNIMPLEMENTED_THRESHOLD = 30


class _AcceleratorFallback(Exception):
    """Internal signal that an accelerator attempt should be retried natively.

    Never escapes the Table method that raises it: the method catches it and
    falls through to the native code path.
    """


class AcceleratorBreaker:
    """Tracks accelerator health and decides when to stop using it.

    One instance per Table. Thread-safe so the generated sync client can share a
    Table across threads. Two triggers permanently bypass the accelerator:

    * ``threshold`` consecutive ``UNIMPLEMENTED`` replies (the daemon understands
      the RPC shape but has no working sessions), and
    * an explicit :meth:`trip` when the daemon subprocess is found dead.

    Any non-``UNIMPLEMENTED`` outcome resets the consecutive count, matching the
    Go interceptor: a normal reply proves the daemon is healthy again.
    """

    def __init__(self, threshold: int = DEFAULT_UNIMPLEMENTED_THRESHOLD):
        self._threshold = threshold
        self._consecutive = 0
        self._tripped = False
        self._lock = threading.Lock()

    def bypass(self) -> bool:
        """Whether the accelerator should be skipped entirely from now on."""
        return self._tripped

    def trip(self) -> None:
        """Permanently bypass the accelerator (e.g. the daemon process died)."""
        with self._lock:
            self._tripped = True

    def record_unimplemented(self) -> None:
        """Note an ``UNIMPLEMENTED`` reply; trip the breaker at the threshold."""
        with self._lock:
            self._consecutive += 1
            if self._consecutive >= self._threshold:
                self._tripped = True

    def record_ok(self) -> None:
        """Note any non-``UNIMPLEMENTED`` outcome; resets the consecutive count."""
        with self._lock:
            self._consecutive = 0


def _grpc_code(exc: BaseException) -> StatusCode | None:
    """Best-effort extraction of a gRPC status code from an exception."""
    code = getattr(exc, "code", None)
    if not callable(code):
        return None
    try:
        return code()
    except Exception:
        return None


def handle_accelerator_error(
    exc: BaseException,
    *,
    daemon: "AcceleratorDaemon | None",
    breaker: AcceleratorBreaker,
) -> None:
    """Classify an exception raised by an accelerator-routed RPC.

    Always raises. Either raises :class:`_AcceleratorFallback` to tell the caller
    to retry on the native path, or raises the translated ``google.api_core``
    exception for the caller to propagate:

    * daemon subprocess dead -> trip the breaker, fall back (it will not recover)
    * ``UNIMPLEMENTED`` -> count toward the breaker, fall back for this call
    * any other gRPC error -> reset the counter, translate and raise
    * a non-gRPC exception -> re-raise unchanged (never masked as a fallback)
    """
    # A dead subprocess can surface as a channel error under any status code, so
    # check liveness first: the "daemon died mid-flight" case always wins and is
    # never recoverable.
    if daemon is not None and not daemon.is_running:
        breaker.trip()
        raise _AcceleratorFallback() from exc
    if not isinstance(exc, RpcError):
        # A bug in our own merge machinery, not a daemon result. Do not mask it
        # as a fallback; let it propagate unchanged.
        raise exc
    if _grpc_code(exc) == StatusCode.UNIMPLEMENTED:
        breaker.record_unimplemented()
        raise _AcceleratorFallback() from exc
    breaker.record_ok()
    raise core_exceptions.from_grpc_error(exc) from exc
