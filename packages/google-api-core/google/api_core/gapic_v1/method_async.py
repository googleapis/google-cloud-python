# Copyright 2020 Google LLC
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
"""AsyncIO helpers for wrapping gRPC and REST methods with common functionality.

This is used by gapic clients to provide common error mapping, retry, timeout,
compression, pagination, and long-running operations to methods.
"""

import asyncio
import contextlib
import functools
import inspect

from google.api_core import _observability, grpc_helpers_async
from google.api_core.gapic_v1 import client_info
from google.api_core.gapic_v1.client_info import METRICS_METADATA_KEY

# Retain _GapicCallable import for backward compatibility with external packages
from google.api_core.gapic_v1.method import (  # noqa: F401
    DEFAULT,
    USE_DEFAULT_METADATA,
    _apply_decorators,
    _deduplicate_metadata_tokens,
    _extract_error_attributes,
    _extract_metrics_header,
    _extract_rpc_identity,
    _extract_status_code,
    _GapicCallable,
)
from google.api_core.timeout import TimeToDeadlineTimeout

_DEFAULT_ASYNC_TRANSPORT_KIND = "grpc_asyncio"


class _AsyncGapicCallable(object):
    """Async callable object that wraps an async RPC method with retry, timeout, metadata, and tracing.

    Args:
        target (Callable): The low-level async RPC method.
        retry (Optional[google.api_core.retry_async.AsyncRetry]): The default retry for the
            callable. If ``None``, this callable will not retry by default.
        timeout (Optional[Union[google.api_core.timeout.Timeout, float]]): The default timeout for the
            callable. If ``None``, this callable will not specify a timeout argument to the
            low-level RPC method.
        compression (Optional[grpc.Compression]): The default compression for the callable.
            If ``None``, this callable will not specify a compression argument to the low-level
            RPC method.
        metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata that is
            provided to the RPC method on every invocation. This is merged with
            any metadata specified during invocation. If ``None``, no
            additional metadata will be passed to the RPC method.
        client_options (Optional[google.api_core.client_options.ClientOptions]):
            Client options used to configure client-level behavior, such as
            custom OpenTelemetry tracer providers. Defaults to None.
        method_name (Optional[str]): The optional explicit full RPC method name
            (e.g. "/google.cloud.secretmanager.v1.SecretManagerService/AccessSecretVersion").
        is_streaming (bool): Whether the RPC method is streaming. Defaults to False.
            Note: Streaming methods do not currently generate Tier 3 observability spans.
        client_info (Optional[google.api_core.gapic_v1.client_info.ClientInfo]):
            Client information used for metadata headers. Defaults to None.
        kind (str): The transport kind for the RPC method. Defaults to "grpc_asyncio".
            Allowed values for OpenTelemetry method tracing are "grpc_asyncio" and "rest_asyncio".
    """

    def __init__(
        self,
        target,
        retry,
        timeout,
        compression,
        metadata=None,
        client_options=None,
        method_name=None,
        is_streaming=False,
        client_info=None,
        kind=_DEFAULT_ASYNC_TRANSPORT_KIND,
    ):
        self._target = target
        self._retry = retry
        self._timeout = timeout
        self._compression = compression

        # Pre-extract the x-goog-api-client header from the initialized metadata.
        self._x_goog_api_client, remaining = _extract_metrics_header(metadata)
        self._static_metadata = tuple(remaining)
        if self._x_goog_api_client:
            self._default_metadata = (
                (METRICS_METADATA_KEY, self._x_goog_api_client),
                *self._static_metadata,
            )
        else:
            self._default_metadata = self._static_metadata

        # Configure the OpenTelemetry span factory once at initialization.
        self._start_span_fn = None
        if (
            not is_streaming
            and kind in ("grpc_asyncio", "rest_asyncio")
            and method_name is not None
            and _observability.is_otel_capabilities_enabled(client_options)
        ):
            try:
                from opentelemetry import trace

                tracer_provider = None
                if isinstance(client_options, dict):
                    tracer_provider = client_options.get("tracer_provider")
                elif client_options is not None:
                    tracer_provider = getattr(client_options, "tracer_provider", None)
                if tracer_provider is not None:
                    tracer = tracer_provider.get_tracer("google.api_core")
                else:
                    tracer = trace.get_tracer("google.api_core")

                span_name, _, _ = _extract_rpc_identity(method_name)
                is_rest = kind in ("rest", "rest_asyncio")
                span_attributes = {
                    "rpc.system.name": "http" if is_rest else "grpc",
                    "rpc.method": span_name,
                }
                self._start_span_fn = functools.partial(
                    tracer.start_as_current_span,
                    span_name,
                    kind=trace.SpanKind.CLIENT,
                    attributes=span_attributes,
                )
            except (ImportError, AttributeError, TypeError):
                # Gracefully disable tracing if OpenTelemetry or custom provider fails
                self._start_span_fn = None

    async def __call__(
        self, *args, timeout=DEFAULT, retry=DEFAULT, compression=DEFAULT, **kwargs
    ):
        """Invoke the low-level async RPC with retry, timeout, compression, and metadata."""
        if retry is DEFAULT:
            retry = self._retry

        if timeout is DEFAULT:
            timeout = self._timeout

        if compression is DEFAULT:
            compression = self._compression

        if isinstance(timeout, (int, float)):
            timeout = TimeToDeadlineTimeout(timeout=timeout)

        # Apply all applicable decorators.
        wrapped_func = _apply_decorators(self._target, [retry, timeout])

        if user_metadata := kwargs.get("metadata"):
            # Add the user agent metadata to the call.
            final_metadata = list(self._static_metadata)
            user_x_goog, remaining = _extract_metrics_header(user_metadata)

            merged_header = _deduplicate_metadata_tokens(
                self._x_goog_api_client, user_x_goog
            )
            if merged_header:
                final_metadata.append((METRICS_METADATA_KEY, merged_header))
            final_metadata.extend(remaining)
            kwargs["metadata"] = final_metadata
        elif self._default_metadata:
            kwargs["metadata"] = self._default_metadata

        if compression is not None:
            kwargs["compression"] = compression

        span_cm = contextlib.nullcontext()
        if self._start_span_fn is not None:
            try:
                span_cm = self._start_span_fn()
            except (
                Exception
            ):  # Fail-open: proceed without span if tracing initialization fails
                span_cm = contextlib.nullcontext()

        with span_cm as span:
            try:
                res = wrapped_func(*args, **kwargs)
                if inspect.isawaitable(res):
                    result = await res
                else:
                    result = res
                if span is not None and hasattr(span, "set_attribute"):
                    span.set_attribute("rpc.response.status_code", "OK")
                return result
            except (Exception, asyncio.CancelledError) as exc:
                if span is not None and hasattr(span, "set_attribute"):
                    span.set_attribute(
                        "rpc.response.status_code", _extract_status_code(exc)
                    )
                    for k, v in _extract_error_attributes(exc).items():
                        span.set_attribute(k, v)
                raise


def wrap_method(
    func,
    default_retry=None,
    default_timeout=None,
    default_compression=None,
    client_info=client_info.DEFAULT_CLIENT_INFO,
    kind=_DEFAULT_ASYNC_TRANSPORT_KIND,
    *,
    client_options=None,
    method_name=None,
    is_streaming=False,
):
    """Wrap an async RPC method with common behavior.

    Returns:
        Callable: A new callable that takes optional ``retry``, ``timeout``,
            and ``compression`` arguments and applies the common error mapping,
            retry, timeout, metadata, and compression behavior to the low-level RPC method.
    """
    if kind == _DEFAULT_ASYNC_TRANSPORT_KIND:
        func = grpc_helpers_async.wrap_errors(func)

    metadata = [client_info.to_grpc_metadata()] if client_info is not None else None

    return functools.wraps(func)(
        _AsyncGapicCallable(
            func,
            default_retry,
            default_timeout,
            default_compression,
            metadata=metadata,
            client_options=client_options,
            method_name=method_name,
            is_streaming=is_streaming,
            client_info=client_info,
            kind=kind,
        )
    )
