# -*- coding: utf-8 -*-

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
#

from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.trace_v2.types import trace
from google.cloud.trace_v2.types import tracing
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore

from .transports.base import TraceServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import TraceServiceGrpcAsyncIOTransport
from .client import TraceServiceClient


class TraceServiceAsyncClient:
    """This file describes an API for collecting and viewing traces
    and spans within a trace.  A Trace is a collection of spans
    corresponding to a single operation or set of operations for an
    application. A span is an individual timed event which forms a
    node of the trace tree. A single trace may contain span(s) from
    multiple services.
    """

    _client: TraceServiceClient

    DEFAULT_ENDPOINT = TraceServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TraceServiceClient.DEFAULT_MTLS_ENDPOINT

    span_path = staticmethod(TraceServiceClient.span_path)

    from_service_account_file = TraceServiceClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(TraceServiceClient).get_transport_class, type(TraceServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, TraceServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the trace service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TraceServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = TraceServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def batch_write_spans(
        self,
        request: tracing.BatchWriteSpansRequest = None,
        *,
        name: str = None,
        spans: Sequence[trace.Span] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Sends new spans to new or existing traces. You cannot
        update existing spans.

        Args:
            request (:class:`~.tracing.BatchWriteSpansRequest`):
                The request object. The request message for the
                `BatchWriteSpans` method.
            name (:class:`str`):
                Required. The name of the project where the spans
                belong. The format is ``projects/[PROJECT_ID]``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            spans (:class:`Sequence[~.trace.Span]`):
                Required. A list of new spans. The
                span names must not match existing
                spans, or the results are undefined.
                This corresponds to the ``spans`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, spans]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = tracing.BatchWriteSpansRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name
        if spans is not None:
            request.spans = spans

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_write_spans,
            default_timeout=120.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def create_span(
        self,
        request: trace.Span = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> trace.Span:
        r"""Creates a new span.

        Args:
            request (:class:`~.trace.Span`):
                The request object. A span represents a single operation
                within a trace. Spans can be nested to form a trace
                tree. Often, a trace contains a root span that describes
                the end-to-end latency, and one or more subspans for its
                sub-operations. A trace can also contain multiple root
                spans, or none at all. Spans do not need to be
                contiguous&mdash;there may be gaps or overlaps between
                spans in a trace.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.trace.Span:
                A span represents a single operation
                within a trace. Spans can be nested to
                form a trace tree. Often, a trace
                contains a root span that describes the
                end-to-end latency, and one or more
                subspans for its sub-operations. A trace
                can also contain multiple root spans, or
                none at all. Spans do not need to be
                contiguous&mdash;there may be gaps or
                overlaps between spans in a trace.

        """
        # Create or coerce a protobuf request object.

        request = trace.Span(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_span,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=1.0,
                multiplier=1.2,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
            default_timeout=120.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-trace",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TraceServiceAsyncClient",)
