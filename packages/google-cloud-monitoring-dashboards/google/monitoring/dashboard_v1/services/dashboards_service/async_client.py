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

from google.monitoring.dashboard_v1.services.dashboards_service import pagers
from google.monitoring.dashboard_v1.types import dashboard
from google.monitoring.dashboard_v1.types import dashboards_service
from google.monitoring.dashboard_v1.types import layouts

from .transports.base import DashboardsServiceTransport
from .transports.grpc_asyncio import DashboardsServiceGrpcAsyncIOTransport
from .client import DashboardsServiceClient


class DashboardsServiceAsyncClient:
    """Manages Stackdriver dashboards. A dashboard is an arrangement
    of data display widgets in a specific layout.
    """

    _client: DashboardsServiceClient

    DEFAULT_ENDPOINT = DashboardsServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DashboardsServiceClient.DEFAULT_MTLS_ENDPOINT

    dashboard_path = staticmethod(DashboardsServiceClient.dashboard_path)

    from_service_account_file = DashboardsServiceClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(DashboardsServiceClient).get_transport_class, type(DashboardsServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, DashboardsServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the dashboards service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DashboardsServiceTransport]): The
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

        self._client = DashboardsServiceClient(
            credentials=credentials, transport=transport, client_options=client_options,
        )

    async def create_dashboard(
        self,
        request: dashboards_service.CreateDashboardRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dashboard.Dashboard:
        r"""Creates a new custom dashboard.

        This method requires the ``monitoring.dashboards.create``
        permission on the specified project. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`~.dashboards_service.CreateDashboardRequest`):
                The request object. The `CreateDashboard` request.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dashboard.Dashboard:
                A Google Stackdriver dashboard.
                Dashboards define the content and layout
                of pages in the Stackdriver web
                application.

        """
        # Create or coerce a protobuf request object.

        request = dashboards_service.CreateDashboardRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_dashboard,
            default_timeout=30.0,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_dashboards(
        self,
        request: dashboards_service.ListDashboardsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDashboardsAsyncPager:
        r"""Lists the existing dashboards.

        This method requires the ``monitoring.dashboards.list``
        permission on the specified project. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`~.dashboards_service.ListDashboardsRequest`):
                The request object. The `ListDashboards` request.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListDashboardsAsyncPager:
                The ``ListDashboards`` request.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.

        request = dashboards_service.ListDashboardsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_dashboards,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListDashboardsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_dashboard(
        self,
        request: dashboards_service.GetDashboardRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dashboard.Dashboard:
        r"""Fetches a specific dashboard.

        This method requires the ``monitoring.dashboards.get``
        permission on the specified dashboard. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`~.dashboards_service.GetDashboardRequest`):
                The request object. The `GetDashboard` request.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dashboard.Dashboard:
                A Google Stackdriver dashboard.
                Dashboards define the content and layout
                of pages in the Stackdriver web
                application.

        """
        # Create or coerce a protobuf request object.

        request = dashboards_service.GetDashboardRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_dashboard,
            default_timeout=None,
            client_info=_client_info,
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

    async def delete_dashboard(
        self,
        request: dashboards_service.DeleteDashboardRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an existing custom dashboard.

        This method requires the ``monitoring.dashboards.delete``
        permission on the specified dashboard. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`~.dashboards_service.DeleteDashboardRequest`):
                The request object. The `DeleteDashboard` request.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.

        request = dashboards_service.DeleteDashboardRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_dashboard,
            default_timeout=30.0,
            client_info=_client_info,
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

    async def update_dashboard(
        self,
        request: dashboards_service.UpdateDashboardRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dashboard.Dashboard:
        r"""Replaces an existing custom dashboard with a new definition.

        This method requires the ``monitoring.dashboards.update``
        permission on the specified dashboard. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`~.dashboards_service.UpdateDashboardRequest`):
                The request object. The `UpdateDashboard` request.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dashboard.Dashboard:
                A Google Stackdriver dashboard.
                Dashboards define the content and layout
                of pages in the Stackdriver web
                application.

        """
        # Create or coerce a protobuf request object.

        request = dashboards_service.UpdateDashboardRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_dashboard,
            default_timeout=30.0,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("dashboard.name", request.dashboard.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-monitoring-dashboard",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("DashboardsServiceAsyncClient",)
