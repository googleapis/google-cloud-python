# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared Showcase client construction, matrix loader, scenario runners, and log capture."""

from __future__ import annotations

import asyncio
import contextlib
import csv
import logging
import os
import time
from collections.abc import Mapping
from collections.abc import Sequence as AbstractSequence
from pathlib import Path
from typing import Any, TypeVar

import grpc
import pytest
import requests.exceptions
from google import showcase
from google.api_core import exceptions
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.protobuf import any_pb2, duration_pb2
from google.rpc import code_pb2, error_details_pb2, status_pb2
from google.showcase import (
    AttemptSequenceRequest,
    CreateSequenceRequest,
    EchoClient,
    Sequence,
    SequenceServiceClient,
)

try:
    from . import conftest
except (ImportError, ValueError):
    import conftest

HAS_ASYNC_CLIENTS = os.environ.get("GAPIC_PYTHON_ASYNC", "true") == "true"
if HAS_ASYNC_CLIENTS:
    from google.api_core import retry_async as retries_async
    from google.showcase import EchoAsyncClient, SequenceServiceAsyncClient
    from grpc.experimental import aio

_ClientT = TypeVar("_ClientT")

# Deterministic timing constants for fast, non-flaky Showcase system tests.
# Use a negative deadline (-1.0s) for gRPC so C-core immediately expires the call
# locally with DEADLINE_EXCEEDED without racing Go Showcase HTTP/2 RST_STREAM CANCEL.
GRPC_CLIENT_TIMEOUT_SECONDS = -1.0
REST_CLIENT_TIMEOUT_SECONDS = 0.2
CLIENT_TIMEOUT_SECONDS = {
    "grpc": GRPC_CLIENT_TIMEOUT_SECONDS,
    "grpc_asyncio": GRPC_CLIENT_TIMEOUT_SECONDS,
    "rest": REST_CLIENT_TIMEOUT_SECONDS,
    "rest_asyncio": REST_CLIENT_TIMEOUT_SECONDS,
}
SERVER_BLOCK_DELAY_SECONDS = 2
FAST_RETRY_BACKOFF_SECONDS = 0.01
CONSTANT_BACKOFF_MULTIPLIER = 1.0
EXHAUSTION_DEADLINE_SECONDS = 0.1
GENEROUS_RECOVERY_DEADLINE_SECONDS = 5.0
EXHAUSTED_RETRY_ATTEMPTS = 2
RECOVERY_FAILED_ATTEMPTS = 2

SERVER_FAILURE_MESSAGE = "Simulated unretryable invalid argument error."
SERVER_FAILURE_REASON = "INVALID_ARGUMENT_REASON"
SERVER_FAILURE_DOMAIN = "showcase.googleapis.com"
SERVER_FAILURE_METADATA = {"zone": "us-east1-a"}

ECHO_SCENARIOS = frozenset(
    {
        "Happy Path",
        "Logging Off",
        "Server Failure",
        "Active Trace",
        "Client Timeout",
    }
)


def load_csv_matrix(csv_path: Path) -> AbstractSequence[Mapping[str, str]]:
    """Loads atomic specification rows from a Tidy Data compliance CSV matrix."""
    with open(csv_path, mode="r", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


class InMemoryLogCapture(logging.Handler):
    """Thread-safe in-memory handler that captures raw `logging.LogRecord` events."""

    def __init__(self, level: int = logging.NOTSET):
        super().__init__(level=level)
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)

    def clear(self) -> None:
        """Clears all captured log records under the handler lock."""
        with self.lock:
            self.records.clear()


def _insecure_channel_factory(host: str, **kwargs: Any) -> grpc.Channel:
    """Callable channel factory preserving `self._host` on sync gRPC transports."""
    del kwargs
    return grpc.insecure_channel(host)


def _async_insecure_channel_factory(host: str, **kwargs: Any) -> Any:
    """Callable channel factory preserving `self._host` on async gRPC transports."""
    del kwargs
    return aio.insecure_channel(host)


def build_server_failure_status(
    *, include_error_info: bool = True
) -> status_pb2.Status:
    """Builds an INVALID_ARGUMENT gRPC Status with optional packed `ErrorInfo`."""
    details = []
    if include_error_info:
        error_info = error_details_pb2.ErrorInfo(
            reason=SERVER_FAILURE_REASON,
            domain=SERVER_FAILURE_DOMAIN,
            metadata=SERVER_FAILURE_METADATA,
        )
        packed_any = any_pb2.Any()
        packed_any.Pack(error_info)
        details.append(packed_any)
    return status_pb2.Status(
        code=code_pb2.INVALID_ARGUMENT,
        message=SERVER_FAILURE_MESSAGE,
        details=details,
    )


def construct_showcase_client(
    client_class: type[_ClientT],
    transport_name: str,
    client_options: ClientOptions | None = None,
    use_mtls: bool = False,
) -> _ClientT:
    """Instantiates a sync or async Showcase client for the requested transport."""
    extra_kwargs: dict[str, Any] = {}
    if transport_name == "grpc" and not use_mtls:
        extra_kwargs["channel"] = _insecure_channel_factory
    elif transport_name == "grpc_asyncio" and not use_mtls:
        extra_kwargs["channel"] = _async_insecure_channel_factory
        extra_kwargs["credentials"] = conftest.async_anonymous_credentials()
    elif transport_name == "rest_asyncio":
        extra_kwargs["credentials"] = conftest.async_anonymous_credentials()

    return conftest.construct_client(
        client_class,
        use_mtls=use_mtls,
        transport_name=transport_name,
        client_options=client_options,
        **extra_kwargs,
    )


def _expected_timeout_exceptions() -> tuple[type[BaseException], ...]:
    """Returns genuine transport timeout exception types across sync and async stacks."""
    exc_types: list[type[BaseException]] = [
        exceptions.DeadlineExceeded,
        requests.exceptions.Timeout,
        TimeoutError,
        asyncio.TimeoutError,
    ]
    try:
        import aiohttp

        server_timeout = getattr(aiohttp, "ServerTimeoutError", None)
        if server_timeout is not None:
            exc_types.append(server_timeout)
    except ImportError:
        pass
    try:
        from google.auth import exceptions as auth_exceptions

        # google.auth.exceptions.TimeoutError was introduced after google-auth 2.14.x.
        auth_timeout = getattr(auth_exceptions, "TimeoutError", None)
        if auth_timeout is not None:
            exc_types.append(auth_timeout)
    except ImportError:
        pass
    return tuple(exc_types)


async def _drain_async_inspection_tasks() -> None:
    """Drains `done_callback` scheduling ticks and pending `_inspect_async_call` tasks."""
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    current = asyncio.current_task()
    pending = [
        task
        for task in asyncio.all_tasks()
        if task is not current
        and not task.done()
        and getattr(task.get_coro(), "__name__", "") == "_inspect_async_call"
    ]
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)


def _build_echo_plan(
    scenario: str,
    transport_name: str,
    *,
    include_error_info: bool = True,
) -> tuple[str, Any, dict[str, Any], Any]:
    """Builds RPC method name, request message, call kwargs, and exception expectation."""
    match scenario:
        case "Happy Path":
            return (
                "echo",
                showcase.EchoRequest(content="hello"),
                {},
                contextlib.nullcontext(),
            )
        case "Logging Off" | "Server Failure" | "Active Trace":
            return (
                "echo",
                showcase.EchoRequest(
                    error=build_server_failure_status(
                        include_error_info=include_error_info
                    )
                ),
                {},
                pytest.raises(
                    (exceptions.InvalidArgument, exceptions.BadRequest),
                    match=r"Simulated unretryable invalid argument error\.",
                ),
            )
        case "Client Timeout":
            return (
                "block",
                showcase.BlockRequest(
                    response_delay=duration_pb2.Duration(
                        seconds=SERVER_BLOCK_DELAY_SECONDS
                    )
                ),
                {"timeout": CLIENT_TIMEOUT_SECONDS[transport_name], "retry": None},
                pytest.raises(
                    _expected_timeout_exceptions(),
                    match=r"(?i)deadline exceeded|timed out|timeout",
                ),
            )
        case _:
            raise ValueError(f"Unsupported Echo scenario: {scenario!r}")


def _build_sequence_plan(
    scenario: str,
    *,
    recovery_failed_attempts: int = RECOVERY_FAILED_ATTEMPTS,
) -> tuple[list[Sequence.Response], Any, float, Any]:
    """Builds responses, `on_error` hook, deadline, and context expectation for Sequence RPCs."""
    if scenario == "Retries Exhausted":
        responses = [
            Sequence.Response(
                status=status_pb2.Status(
                    code=code_pb2.UNAVAILABLE,
                    message="Persistent outage",
                )
            )
            for _ in range(EXHAUSTED_RETRY_ATTEMPTS)
        ]
        attempts_seen = 0

        def on_error(_exc: Exception) -> None:
            nonlocal attempts_seen
            attempts_seen += 1
            if attempts_seen >= EXHAUSTED_RETRY_ATTEMPTS:
                time.sleep(EXHAUSTION_DEADLINE_SECONDS)

        return (
            responses,
            on_error,
            EXHAUSTION_DEADLINE_SECONDS,
            pytest.raises(
                exceptions.RetryError,
                match=r"Deadline of .* exceeded|Persistent outage",
            ),
        )

    if scenario == "Retry Recovery":
        responses = [
            Sequence.Response(
                status=status_pb2.Status(
                    code=code_pb2.UNAVAILABLE,
                    message="Temporary glitch",
                )
            )
            for _ in range(recovery_failed_attempts)
        ] + [Sequence.Response(status=status_pb2.Status(code=code_pb2.OK))]
        return (
            responses,
            None,
            GENEROUS_RECOVERY_DEADLINE_SECONDS,
            contextlib.nullcontext(),
        )

    raise ValueError(f"Unsupported Sequence scenario: {scenario!r}")


def execute_showcase_scenario(
    scenario: str,
    transport_name: str,
    client_options: ClientOptions | None = None,
    *,
    span_exporter: Any = None,
    log_capture: InMemoryLogCapture | None = None,
    include_error_info: bool = True,
    recovery_failed_attempts: int = RECOVERY_FAILED_ATTEMPTS,
) -> None:
    """Executes a Showcase Echo or Sequence compliance scenario synchronously."""
    if scenario in ECHO_SCENARIOS:
        method_name, request, call_kwargs, expectation = _build_echo_plan(
            scenario,
            transport_name,
            include_error_info=include_error_info,
        )
        with construct_showcase_client(
            EchoClient, transport_name, client_options=client_options
        ) as client:
            with expectation:
                getattr(client, method_name)(request, **call_kwargs)
        return

    responses, on_error, deadline, expectation = _build_sequence_plan(
        scenario,
        recovery_failed_attempts=recovery_failed_attempts,
    )
    with construct_showcase_client(
        SequenceServiceClient, transport_name, client_options=client_options
    ) as client:
        seq = client.create_sequence(
            CreateSequenceRequest(sequence=Sequence(responses=responses))
        )
        if span_exporter is not None:
            span_exporter.clear()
        if log_capture is not None:
            log_capture.clear()

        retry_policy = retries.Retry(
            predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
            initial=FAST_RETRY_BACKOFF_SECONDS,
            maximum=FAST_RETRY_BACKOFF_SECONDS,
            multiplier=CONSTANT_BACKOFF_MULTIPLIER,
            deadline=deadline,
            on_error=on_error,
        )
        with expectation:
            client.attempt_sequence(
                AttemptSequenceRequest(name=seq.name),
                retry=retry_policy,
            )


async def execute_showcase_scenario_async(
    scenario: str,
    transport_name: str,
    client_options: ClientOptions | None = None,
    *,
    span_exporter: Any = None,
    log_capture: InMemoryLogCapture | None = None,
    include_error_info: bool = True,
    recovery_failed_attempts: int = RECOVERY_FAILED_ATTEMPTS,
) -> None:
    """Executes a Showcase Echo or Sequence compliance scenario asynchronously."""
    if transport_name == "rest_asyncio" and not conftest.HAS_ASYNC_REST_ECHO_TRANSPORT:
        pytest.skip("Async REST transport is not generated in this session.")

    if scenario in ECHO_SCENARIOS:
        method_name, request, call_kwargs, expectation = _build_echo_plan(
            scenario,
            transport_name,
            include_error_info=include_error_info,
        )
        client = construct_showcase_client(
            EchoAsyncClient, transport_name, client_options=client_options
        )
        async with client:
            try:
                with expectation:
                    await getattr(client, method_name)(request, **call_kwargs)
            finally:
                await _drain_async_inspection_tasks()
        return

    responses, on_error, deadline, expectation = _build_sequence_plan(
        scenario,
        recovery_failed_attempts=recovery_failed_attempts,
    )
    client = construct_showcase_client(
        SequenceServiceAsyncClient, transport_name, client_options=client_options
    )
    async with client:
        seq = await client.create_sequence(
            CreateSequenceRequest(sequence=Sequence(responses=responses))
        )
        await _drain_async_inspection_tasks()
        if span_exporter is not None:
            span_exporter.clear()
        if log_capture is not None:
            log_capture.clear()

        retry_policy = retries_async.AsyncRetry(
            predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
            initial=FAST_RETRY_BACKOFF_SECONDS,
            maximum=FAST_RETRY_BACKOFF_SECONDS,
            multiplier=CONSTANT_BACKOFF_MULTIPLIER,
            deadline=deadline,
            on_error=on_error,
        )
        try:
            with expectation:
                await client.attempt_sequence(
                    AttemptSequenceRequest(name=seq.name),
                    retry=retry_policy,
                )
        finally:
            await _drain_async_inspection_tasks()
