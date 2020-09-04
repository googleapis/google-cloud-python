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

from google.analytics.data_v1alpha.types import analytics_data_api
from google.analytics.data_v1alpha.types import data

from .transports.base import AlphaAnalyticsDataTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import AlphaAnalyticsDataGrpcTransport
from .transports.grpc_asyncio import AlphaAnalyticsDataGrpcAsyncIOTransport


class AlphaAnalyticsDataClientMeta(type):
    """Metaclass for the AlphaAnalyticsData client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[AlphaAnalyticsDataTransport]]
    _transport_registry["grpc"] = AlphaAnalyticsDataGrpcTransport
    _transport_registry["grpc_asyncio"] = AlphaAnalyticsDataGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[AlphaAnalyticsDataTransport]:
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


class AlphaAnalyticsDataClient(metaclass=AlphaAnalyticsDataClientMeta):
    """Google Analytics reporting data service."""

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

    DEFAULT_ENDPOINT = "analyticsdata.googleapis.com"
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
        transport: Union[str, AlphaAnalyticsDataTransport] = None,
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the alpha analytics data client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AlphaAnalyticsDataTransport]): The
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
        if isinstance(transport, AlphaAnalyticsDataTransport):
            # transport is a AlphaAnalyticsDataTransport instance.
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

    def run_report(
        self,
        request: analytics_data_api.RunReportRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.RunReportResponse:
        r"""Returns a customized report of your Google Analytics
        event data. Reports contain statistics derived from data
        collected by the Google Analytics tracking code. The
        data returned from the API is as a table with columns
        for the requested dimensions and metrics. Metrics are
        individual measurements of user activity on your
        property, such as active users or event count.
        Dimensions break down metrics across some common
        criteria, such as country or event name.

        Args:
            request (:class:`~.analytics_data_api.RunReportRequest`):
                The request object. The request to generate a report.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_data_api.RunReportResponse:
                The response report table
                corresponding to a request.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.RunReportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.RunReportRequest):
            request = analytics_data_api.RunReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_report]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def run_pivot_report(
        self,
        request: analytics_data_api.RunPivotReportRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.RunPivotReportResponse:
        r"""Returns a customized pivot report of your Google
        Analytics event data. Pivot reports are more advanced
        and expressive formats than regular reports. In a pivot
        report, dimensions are only visible if they are included
        in a pivot. Multiple pivots can be specified to further
        dissect your data.

        Args:
            request (:class:`~.analytics_data_api.RunPivotReportRequest`):
                The request object. The request to generate a pivot
                report.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_data_api.RunPivotReportResponse:
                The response pivot report table
                corresponding to a pivot request.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.RunPivotReportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.RunPivotReportRequest):
            request = analytics_data_api.RunPivotReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_pivot_report]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_run_reports(
        self,
        request: analytics_data_api.BatchRunReportsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.BatchRunReportsResponse:
        r"""Returns multiple reports in a batch. All reports must
        be for the same Entity.

        Args:
            request (:class:`~.analytics_data_api.BatchRunReportsRequest`):
                The request object. The batch request containing
                multiple report requests.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_data_api.BatchRunReportsResponse:
                The batch response containing
                multiple reports.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.BatchRunReportsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.BatchRunReportsRequest):
            request = analytics_data_api.BatchRunReportsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_run_reports]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_run_pivot_reports(
        self,
        request: analytics_data_api.BatchRunPivotReportsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.BatchRunPivotReportsResponse:
        r"""Returns multiple pivot reports in a batch. All
        reports must be for the same Entity.

        Args:
            request (:class:`~.analytics_data_api.BatchRunPivotReportsRequest`):
                The request object. The batch request containing
                multiple pivot report requests.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_data_api.BatchRunPivotReportsResponse:
                The batch response containing
                multiple pivot reports.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.BatchRunPivotReportsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.BatchRunPivotReportsRequest):
            request = analytics_data_api.BatchRunPivotReportsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_run_pivot_reports]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_metadata(
        self,
        request: analytics_data_api.GetMetadataRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.Metadata:
        r"""Returns metadata for dimensions and metrics available
        in reporting methods. Used to explore the dimensions and
        metrics. Dimensions and metrics will be mostly added
        over time, but renames and deletions may occur.

        Args:
            request (:class:`~.analytics_data_api.GetMetadataRequest`):
                The request object. Request for dimension and metric
                metadata.
            name (:class:`str`):
                Required. The name of the metadata to
                retrieve. Either has the form 'metadata'
                or 'properties/{property}/metadata'.
                This name field is specified in the URL
                path and not URL parameters. Property is
                a numeric Google Analytics App + Web
                Property Id.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_data_api.Metadata:
                The dimensions and metrics currently
                accepted in reporting methods.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.GetMetadataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.GetMetadataRequest):
            request = analytics_data_api.GetMetadataRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_metadata]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-analytics-data",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AlphaAnalyticsDataClient",)
