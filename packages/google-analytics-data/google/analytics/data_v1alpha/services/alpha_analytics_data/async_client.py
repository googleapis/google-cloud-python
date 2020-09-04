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

from google.analytics.data_v1alpha.types import analytics_data_api
from google.analytics.data_v1alpha.types import data

from .transports.base import AlphaAnalyticsDataTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AlphaAnalyticsDataGrpcAsyncIOTransport
from .client import AlphaAnalyticsDataClient


class AlphaAnalyticsDataAsyncClient:
    """Google Analytics reporting data service."""

    _client: AlphaAnalyticsDataClient

    DEFAULT_ENDPOINT = AlphaAnalyticsDataClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AlphaAnalyticsDataClient.DEFAULT_MTLS_ENDPOINT

    from_service_account_file = AlphaAnalyticsDataClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(AlphaAnalyticsDataClient).get_transport_class,
        type(AlphaAnalyticsDataClient),
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, AlphaAnalyticsDataTransport] = "grpc_asyncio",
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

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = AlphaAnalyticsDataClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def run_report(
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

        request = analytics_data_api.RunReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_report,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def run_pivot_report(
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

        request = analytics_data_api.RunPivotReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_pivot_report,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def batch_run_reports(
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

        request = analytics_data_api.BatchRunReportsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_run_reports,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def batch_run_pivot_reports(
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

        request = analytics_data_api.BatchRunPivotReportsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_run_pivot_reports,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_metadata(
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
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_data_api.GetMetadataRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_metadata,
            default_timeout=None,
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
        gapic_version=pkg_resources.get_distribution("google-analytics-data",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AlphaAnalyticsDataAsyncClient",)
