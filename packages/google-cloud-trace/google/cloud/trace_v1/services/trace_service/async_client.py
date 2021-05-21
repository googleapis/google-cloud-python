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
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.trace_v1.services.trace_service import pagers
from google.cloud.trace_v1.types import trace
from .transports.base import TraceServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import TraceServiceGrpcAsyncIOTransport
from .client import TraceServiceClient


class TraceServiceAsyncClient:
    """This file describes an API for collecting and viewing traces
    and spans within a trace.  A Trace is a collection of spans
    corresponding to a single operation or set of operations for an
    application. A span is an individual timed event which forms a
    node of the trace tree. Spans for a single trace may span
    multiple services.
    """

    _client: TraceServiceClient

    DEFAULT_ENDPOINT = TraceServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TraceServiceClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        TraceServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        TraceServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TraceServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(TraceServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(TraceServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        TraceServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TraceServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        TraceServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(TraceServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        TraceServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TraceServiceAsyncClient: The constructed client.
        """
        return TraceServiceClient.from_service_account_info.__func__(TraceServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TraceServiceAsyncClient: The constructed client.
        """
        return TraceServiceClient.from_service_account_file.__func__(TraceServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> TraceServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            TraceServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(TraceServiceClient).get_transport_class, type(TraceServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, TraceServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the trace service client.

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
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

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

    async def list_traces(
        self,
        request: trace.ListTracesRequest = None,
        *,
        project_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTracesAsyncPager:
        r"""Returns of a list of traces that match the specified
        filter conditions.

        Args:
            request (:class:`google.cloud.trace_v1.types.ListTracesRequest`):
                The request object. The request message for the
                `ListTraces` method. All fields are required unless
                specified.
            project_id (:class:`str`):
                Required. ID of the Cloud project
                where the trace data is stored.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.trace_v1.services.trace_service.pagers.ListTracesAsyncPager:
                The response message for the ListTraces method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = trace.ListTracesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_traces,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=1.0,
                multiplier=1.2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=45.0,
            ),
            default_timeout=45.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTracesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_trace(
        self,
        request: trace.GetTraceRequest = None,
        *,
        project_id: str = None,
        trace_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> trace.Trace:
        r"""Gets a single trace by its ID.

        Args:
            request (:class:`google.cloud.trace_v1.types.GetTraceRequest`):
                The request object. The request message for the
                `GetTrace` method.
            project_id (:class:`str`):
                Required. ID of the Cloud project
                where the trace data is stored.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trace_id (:class:`str`):
                Required. ID of the trace to return.
                This corresponds to the ``trace_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.trace_v1.types.Trace:
                A trace describes how long it takes
                for an application to perform an
                operation. It consists of a set of
                spans, each of which represent a single
                timed event within the operation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trace_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = trace.GetTraceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if trace_id is not None:
            request.trace_id = trace_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_trace,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=1.0,
                multiplier=1.2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=45.0,
            ),
            default_timeout=45.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def patch_traces(
        self,
        request: trace.PatchTracesRequest = None,
        *,
        project_id: str = None,
        traces: trace.Traces = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Sends new traces to Stackdriver Trace or updates
        existing traces. If the ID of a trace that you send
        matches that of an existing trace, any fields in the
        existing trace and its spans are overwritten by the
        provided values, and any new fields provided are merged
        with the existing trace data. If the ID does not match,
        a new trace is created.

        Args:
            request (:class:`google.cloud.trace_v1.types.PatchTracesRequest`):
                The request object. The request message for the
                `PatchTraces` method.
            project_id (:class:`str`):
                Required. ID of the Cloud project
                where the trace data is stored.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            traces (:class:`google.cloud.trace_v1.types.Traces`):
                Required. The body of the message.
                This corresponds to the ``traces`` field
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
        has_flattened_params = any([project_id, traces])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = trace.PatchTracesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if traces is not None:
            request.traces = traces

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.patch_traces,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=1.0,
                multiplier=1.2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=45.0,
            ),
            default_timeout=45.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-trace",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TraceServiceAsyncClient",)
