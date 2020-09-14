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
import os
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.trace_v1.services.trace_service import pagers
from google.cloud.trace_v1.types import trace

from .transports.base import TraceServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import TraceServiceGrpcTransport
from .transports.grpc_asyncio import TraceServiceGrpcAsyncIOTransport


class TraceServiceClientMeta(type):
    """Metaclass for the TraceService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[TraceServiceTransport]]
    _transport_registry["grpc"] = TraceServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = TraceServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[TraceServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class TraceServiceClient(metaclass=TraceServiceClientMeta):
    """This file describes an API for collecting and viewing traces
    and spans within a trace.  A Trace is a collection of spans
    corresponding to a single operation or set of operations for an
    application. A span is an individual timed event which forms a
    node of the trace tree. Spans for a single trace may span
    multiple services.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "cloudtrace.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, TraceServiceTransport] = None,
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        if client_options.api_endpoint is None:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS", "never")
            if use_mtls_env == "never":
                client_options.api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                client_options.api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                has_client_cert_source = (
                    client_options.client_cert_source is not None
                    or mtls.has_default_client_cert_source()
                )
                client_options.api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if has_client_cert_source
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, TraceServiceTransport):
            # transport is a TraceServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=client_options.api_endpoint,
                scopes=client_options.scopes,
                api_mtls_endpoint=client_options.api_endpoint,
                client_cert_source=client_options.client_cert_source,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def list_traces(
        self,
        request: trace.ListTracesRequest = None,
        *,
        project_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTracesPager:
        r"""Returns of a list of traces that match the specified
        filter conditions.

        Args:
            request (:class:`~.trace.ListTracesRequest`):
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
            ~.pagers.ListTracesPager:
                The response message for the ``ListTraces`` method.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a trace.ListTracesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, trace.ListTracesRequest):
            request = trace.ListTracesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if project_id is not None:
                request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_traces]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTracesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_trace(
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
            request (:class:`~.trace.GetTraceRequest`):
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
            ~.trace.Trace:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a trace.GetTraceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, trace.GetTraceRequest):
            request = trace.GetTraceRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if project_id is not None:
                request.project_id = project_id
            if trace_id is not None:
                request.trace_id = trace_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_trace]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def patch_traces(
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
            request (:class:`~.trace.PatchTracesRequest`):
                The request object. The request message for the
                `PatchTraces` method.
            project_id (:class:`str`):
                Required. ID of the Cloud project
                where the trace data is stored.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            traces (:class:`~.trace.Traces`):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a trace.PatchTracesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, trace.PatchTracesRequest):
            request = trace.PatchTracesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if project_id is not None:
                request.project_id = project_id
            if traces is not None:
                request.traces = traces

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.patch_traces]

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-trace",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TraceServiceClient",)
