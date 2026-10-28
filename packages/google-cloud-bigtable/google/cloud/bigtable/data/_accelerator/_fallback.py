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

A daemon that cannot open any sessions replies ``UNIMPLEMENTED``, and the routing
layer transparently retries the call on the native client. The first
``UNIMPLEMENTED`` reply trips a sticky breaker so a persistently-degraded daemon
stops being dialed at all. A daemon whose subprocess has died mid-flight trips
the breaker immediately — it will never recover.

The same breaker also carries a reversible "degraded" flag, set by the health
monitor when the daemon is up but too starved to answer its own health check;
see :class:`AcceleratorBreaker`.

Any other gRPC error is a real, daemon-served result the native client would
reproduce (the daemon owns retries, so it has already exhausted them), so it is
translated to the corresponding ``google.api_core`` exception and raised without
falling back.

This module is plain sync-only logic shared verbatim by the async and generated
sync clients; ``grpc.RpcError`` is the common base of both ``grpc.RpcError`` and
``grpc.aio.AioRpcError``, so no CrossSync branching is needed here.
"""

from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING

from google.api_core import exceptions as core_exceptions
from grpc import RpcError, StatusCode

from google.cloud.bigtable.data._helpers import (
    RetryFailureReason,
    _retry_exception_factory,
)
from google.cloud.bigtable.data.exceptions import InvalidChunk

if TYPE_CHECKING:
    from google.cloud.bigtable.data._accelerator._daemon import AcceleratorDaemon

_LOGGER = logging.getLogger(__name__)

# Prefixes and explicit shape markers in gRPC status details that indicate the
# Go accelerator sidecar rejected a specific request shape (e.g. multi-row
# ReadRowsRequest or nil RowRange) rather than reporting a backend/session
# UNIMPLEMENTED. Backend session errors do not carry the "accelerator:" prefix.
_PER_REQUEST_UNIMPLEMENTED_PREFIXES = (
    "accelerator:",
    "accelerator fallback:",
)
_PER_REQUEST_UNIMPLEMENTED_MARKERS = (
    "single-row accelerator",
    "unsupported row range shape",
)


class _AcceleratorFallback(Exception):
    """Internal signal that an accelerator attempt should be retried natively.

    Never escapes the data target method that raises it: the method catches it
    and falls through to the native code path.
    """


class AcceleratorBreaker:
    """Tracks accelerator health and decides when to stop using it.

    One instance per Table. Thread-safe so the generated sync client can share a
    Table across threads. There are two independent reasons to bypass, and they
    differ in whether they can be undone:

    * **Tripped** — permanent. The first ``UNIMPLEMENTED`` reply (the daemon
      understands the RPC shape but has no working sessions), or an explicit
      :meth:`trip` when the daemon subprocess is found dead. Neither condition
      recovers, so the accelerator is abandoned for the life of the Table.
    * **Degraded** — reversible. Set by the health monitor when the daemon stops
      answering its own health check promptly (see
      ``_async/_accelerator_health.py``). A daemon starved of CPU recovers when
      the load that starved it goes away, so this must clear again — routing
      permanently away from the accelerator on one bad minute would be a far
      worse outcome than the slow calls it avoided.

    Keeping the two flags separate is what makes that safe: :meth:`set_degraded`
    can never resurrect an accelerator that :meth:`trip` has given up on. Each
    flag is its own :class:`threading.Event`, so :meth:`bypass` — which runs on
    every routed RPC — stays a pair of lock-free reads. The two are never read
    as a pair: either one being set already means bypass.
    """

    def __init__(self):
        self._tripped = threading.Event()
        self._degraded = threading.Event()

    def bypass(self) -> bool:
        """Whether the accelerator should be skipped for calls made right now."""
        return self._tripped.is_set() or self._degraded.is_set()

    def trip(self) -> None:
        """Permanently bypass the accelerator (e.g. the daemon process died)."""
        self._tripped.set()

    @property
    def is_tripped(self) -> bool:
        """Whether the accelerator has been permanently abandoned."""
        return self._tripped.is_set()

    @property
    def is_degraded(self) -> bool:
        """Whether the accelerator is currently being skipped for poor health."""
        return self._degraded.is_set()

    def set_degraded(self, degraded: bool) -> None:
        """Start or stop bypassing the accelerator for poor health.

        Reversible, and orthogonal to :meth:`trip`: clearing it does not undo a
        permanent trip.
        """
        if degraded:
            self._degraded.set()
        else:
            self._degraded.clear()


def _grpc_code(exc: BaseException) -> StatusCode | None:
    """Best-effort extraction of a gRPC status code from an exception.

    Handles both ``grpc.RpcError`` (status via a ``code()`` method) and
    ``google.api_core.exceptions.GoogleAPICallError`` (status stored on the
    ``grpc_status_code`` attribute), returning ``None`` for anything else.
    """
    code = getattr(exc, "code", None)
    if callable(code):
        try:
            return code()
        except Exception:
            return None
    grpc_status = getattr(exc, "grpc_status_code", None)
    if isinstance(grpc_status, StatusCode):
        return grpc_status
    return None


def _is_per_request_unimplemented(exc: BaseException) -> bool:
    """Return True if an UNIMPLEMENTED error is a per-request shape rejection
    rather than a persistent session/instance unavailability."""
    details_fn = getattr(exc, "details", None)
    if not callable(details_fn):
        return False
    try:
        details = details_fn()
    except Exception:
        return False
    if not isinstance(details, str):
        return False
    lower = details.strip().lower()
    if lower.startswith(_PER_REQUEST_UNIMPLEMENTED_PREFIXES):
        return True
    return any(marker in lower for marker in _PER_REQUEST_UNIMPLEMENTED_MARKERS)


def _raise_translated_rpc_error(
    exc: RpcError,
    operation_timeout: float | None = None,
) -> None:
    """Translate a gRPC RpcError to a google.api_core exception and raise it.

    For DEADLINE_EXCEEDED, chains a RetryExceptionGroup([translated]) as
    __cause__ to match the native client's timeout exception contract.
    """
    translated = core_exceptions.from_grpc_error(exc)
    if _grpc_code(exc) == StatusCode.DEADLINE_EXCEEDED:
        source_exc, cause_exc = _retry_exception_factory(
            [translated], RetryFailureReason.TIMEOUT, operation_timeout
        )
        raise source_exc from cause_exc
    raise translated from exc


def handle_accelerator_error(
    exc: BaseException,
    *,
    daemon: "AcceleratorDaemon | None",
    breaker: AcceleratorBreaker,
    is_idempotent: bool = True,
    is_closed: bool = False,
    operation_timeout: float | None = None,
) -> None:
    """Classify an exception raised by an accelerator-routed RPC.

    Always raises. Either raises :class:`_AcceleratorFallback` to tell the caller
    to retry on the native path, or raises the translated ``google.api_core``
    exception for the caller to propagate:

    * closed table/daemon -> translate and raise without tripping or falling back
    * daemon subprocess dead -> trip the breaker; fall back only if idempotent
    * ``UNIMPLEMENTED`` -> fall back immediately (trip breaker unless per-request shape error)
    * ``InvalidChunk`` -> trip the breaker and fall back
    * any other gRPC error -> translate and raise (with ``RetryExceptionGroup`` cause on timeout)
    * any other non-gRPC exception -> re-raise unchanged (never masked as a fallback)
    """
    if is_closed or getattr(daemon, "_closed", False) is True:
        if isinstance(exc, RpcError):
            _raise_translated_rpc_error(exc, operation_timeout=operation_timeout)
        raise exc

    # A dead subprocess can surface as a channel error under any status code, so
    # check liveness first: the "daemon died mid-flight" case always wins and is
    # never recoverable.
    if daemon is not None and not daemon.is_running:
        if not breaker.is_tripped:
            _LOGGER.warning(
                "Accelerator daemon is no longer running; permanently falling back "
                "to the native Bigtable client for this table.",
                exc_info=exc,
            )
            breaker.trip()
        if not is_idempotent:
            if isinstance(exc, RpcError):
                _raise_translated_rpc_error(exc, operation_timeout=operation_timeout)
            raise exc
        raise _AcceleratorFallback() from exc

    if isinstance(exc, InvalidChunk):
        if not breaker.is_tripped:
            _LOGGER.warning(
                "Accelerator daemon returned an invalid ReadRows chunk (%s); "
                "permanently falling back to the native Bigtable client for this table.",
                exc,
            )
            breaker.trip()
        raise _AcceleratorFallback() from exc

    if not isinstance(exc, RpcError):
        # A bug in our own merge machinery, not a daemon result. Do not mask it
        # as a fallback; let it propagate unchanged.
        raise exc

    if _grpc_code(exc) == StatusCode.UNIMPLEMENTED:
        if _is_per_request_unimplemented(exc):
            raise _AcceleratorFallback() from exc
        # The daemon only replies UNIMPLEMENTED once it has no working sessions,
        # a persistent condition, so trip the breaker and fall back immediately
        # rather than re-dialing on every subsequent call.
        if not breaker.is_tripped:
            _LOGGER.warning(
                "Accelerator daemon replied UNIMPLEMENTED; permanently falling back "
                "to the native Bigtable client for this table."
            )
            breaker.trip()
        raise _AcceleratorFallback() from exc

    _raise_translated_rpc_error(exc, operation_timeout=operation_timeout)
