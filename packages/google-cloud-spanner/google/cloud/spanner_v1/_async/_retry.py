# Copyright 2026 Google LLC All rights reserved.
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

"""Centralized unary RPC retry helpers for Cloud Spanner."""

__CROSS_SYNC_OUTPUT__ = "google.cloud.spanner_v1._retry"

from typing import Any, Callable, List, Optional, Tuple, TypeVar

from google.api_core import gapic_v1
from google.api_core.exceptions import (
    InternalServerError,
    ResourceExhausted,
    ServiceUnavailable,
)
from google.api_core.retry import AsyncRetry
from google.api_core.retry.retry_base import _BaseRetry

from google.cloud.aio._cross_sync import CrossSync

ResponseT = TypeVar("ResponseT")
Metadata = Optional[List[Tuple[str, str]]]

if CrossSync.is_async:
    from typing import Awaitable

    UnaryRpcCallable = Callable[[List[Tuple[str, str]]], Awaitable[ResponseT]]
else:  # pragma: NO COVER
    # Only used by CrossSync when generating sync _retry.py; never runs here
    # because CrossSync.is_async is always True in _async/_retry.py.
    UnaryRpcCallable = Callable[[List[Tuple[str, str]]], ResponseT]

# TODO: Deduplicate with the shared list of retryable InternalServerError
# messages from https://github.com/googleapis/google-cloud-python/pull/19175
# once that PR is merged.
_RETRYABLE_INTERNAL_ERROR_MESSAGES = (
    "RST_STREAM",
    "Received unexpected EOS on DATA frame from server",
    "HTTP/2 error code: INTERNAL_ERROR",
    "Connection closed with unknown cause",
    "Authentication backend internal server error. Please retry",
)

_UNSET = object()


def _is_retryable_internal_error(exception: BaseException) -> bool:
    """Return True if ``exception`` is a transient Spanner InternalServerError."""
    if not isinstance(exception, InternalServerError):
        return False
    message = getattr(exception, "message", None)
    if not isinstance(message, str) or not message:
        message = str(exception)
    return any(
        retryable_message in message
        for retryable_message in _RETRYABLE_INTERNAL_ERROR_MESSAGES
    )


def _is_retryable_unary_error(exception: BaseException) -> bool:
    """Predicate matching unary Spanner RPC errors eligible for retry."""
    return isinstance(
        exception, (ServiceUnavailable, ResourceExhausted)
    ) or _is_retryable_internal_error(exception)


def _extend_retry_predicate(
    existing_predicate: Optional[Callable[[Exception], bool]],
) -> Callable[[Exception], bool]:
    """Extend a GAPIC retry predicate with Spanner transient unary errors."""
    if existing_predicate is None or existing_predicate is _is_retryable_unary_error:
        return _is_retryable_unary_error

    def predicate(exception: Exception) -> bool:
        return bool(existing_predicate(exception)) or _is_retryable_unary_error(
            exception
        )

    return predicate


def resolve_unary_retry(
    api: Any,
    method_name: str,
    retry: Any,
) -> Optional[_BaseRetry]:
    """Resolve the effective unary retry policy for a Spanner RPC call.

    When ``retry`` is :data:`google.api_core.gapic_v1.method.DEFAULT`, this
    resolves the transport's wrapped method retry policy (preserving its
    method-specific timeout, backoff configuration, and existing retryable
    error predicate) while extending its predicate to include transient
    Spanner errors. If no wrapped transport method is available (for example,
    in unit tests with mock clients), a default ``AsyncRetry`` instance with
    Spanner's transient error predicate is returned.

    Args:
        api: GAPIC client instance providing ``transport._wrapped_methods``.
        method_name: Transport method name (for example, ``"commit"``).
        retry: Explicit retry object, ``None``, or ``gapic_v1.method.DEFAULT``.

    Returns:
        Effective retry policy, or ``None`` if retries are disabled.
    """
    if retry is None:
        return None
    if retry is not gapic_v1.method.DEFAULT:
        return retry

    transport = getattr(api, "transport", None)
    wrapped_methods = getattr(transport, "_wrapped_methods", None)
    if isinstance(wrapped_methods, dict):
        transport_method = getattr(transport, method_name, None)
        try:
            callable_wrapper = (
                wrapped_methods.get(transport_method)
                if transport_method is not None
                else None
            )
        except TypeError:
            callable_wrapper = None
        if callable_wrapper is not None:
            gapic_retry = getattr(callable_wrapper, "_retry", _UNSET)
            if gapic_retry is None:
                return None
            if isinstance(gapic_retry, _BaseRetry):
                existing_predicate = getattr(gapic_retry, "_predicate", None)
                return gapic_retry.with_predicate(
                    _extend_retry_predicate(existing_predicate)
                )

    return AsyncRetry(predicate=_is_retryable_unary_error)


@CrossSync.convert
async def execute_unary_with_retry(
    database: Any,
    rpc_call: UnaryRpcCallable[ResponseT],
    metadata: Metadata = None,
    span: Any = None,
    retry_policy: Optional[_BaseRetry] = None,
    on_retry: Optional[Callable[[int, Exception], Any]] = None,
) -> ResponseT:
    """Execute a unary RPC with retries and per-attempt request IDs.

    Runs ``rpc_call`` and retries transient failures according to
    ``retry_policy``. Every try shares the same request number while increasing
    the attempt number (1, 2, ...) so request-ID headers and error messages
    record which attempt failed.

    Inside ``rpc_call``, pass ``retry=None`` to the generated API method.
    Otherwise, that method runs its own hidden retry loop and every retry
    stays stuck on attempt 1.

    Args:
        database: Database object providing request-ID numbering
            (``_next_nth_request``) and error augmentation
            (``with_error_augmentation``).
        rpc_call: Function that takes ``call_metadata`` and calls the RPC
            (with ``retry=None`` passed to the generated API method).
        metadata: Optional initial gRPC metadata pairs.
        span: Optional OpenTelemetry span associated with the request.
        retry_policy: Retry policy controlling delays and which errors are
            retried, or ``None`` to run once without retrying.
        on_retry: Optional callback called with ``(attempt, exception)``
            whenever a failed attempt matches ``retry_policy`` (before the
            timeout check). Must be a regular ``def`` function (not
            ``async def``), because the underlying retry helper calls it
            directly without ``await``.

    Returns:
        The return value of ``rpc_call``.
    """
    nth_request = getattr(database, "_next_nth_request", 0)
    attempt = 0

    async def target() -> ResponseT:
        nonlocal attempt
        attempt += 1
        call_metadata, error_augmenter = database.with_error_augmentation(
            nth_request, attempt, metadata, span
        )
        with error_augmenter:
            return await rpc_call(call_metadata)

    if retry_policy is None:
        return await target()

    if on_retry is None:
        return await retry_policy(target)()

    existing_on_error = getattr(retry_policy, "_on_error", None)

    def handle_retry_error(exception: Exception) -> None:
        on_retry(attempt, exception)
        if existing_on_error is not None:
            existing_on_error(exception)

    if existing_on_error is None:
        return await retry_policy(target, on_error=handle_retry_error)()

    # Calling retry_policy(..., on_error=...) ignores the argument if
    # retry_policy was created with its own on_error callback. Make a copy
    # with handle_retry_error so both on_retry and existing_on_error run.
    updated_retry = type(retry_policy)(
        predicate=retry_policy._predicate,
        initial=retry_policy._initial,
        maximum=retry_policy._maximum,
        multiplier=retry_policy._multiplier,
        timeout=retry_policy.timeout,
        on_error=handle_retry_error,
    )
    return await updated_retry(target)()
