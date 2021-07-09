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

from google.cloud.monitoring_dashboard_v1.services.dashboards_service import pagers
from google.cloud.monitoring_dashboard_v1.types import dashboard
from google.cloud.monitoring_dashboard_v1.types import dashboards_service
from google.cloud.monitoring_dashboard_v1.types import layouts
from .transports.base import DashboardsServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import DashboardsServiceGrpcAsyncIOTransport
from .client import DashboardsServiceClient


class DashboardsServiceAsyncClient:
    """Manages Stackdriver dashboards. A dashboard is an arrangement
    of data display widgets in a specific layout.
    """

    _client: DashboardsServiceClient

    DEFAULT_ENDPOINT = DashboardsServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DashboardsServiceClient.DEFAULT_MTLS_ENDPOINT

    alert_policy_path = staticmethod(DashboardsServiceClient.alert_policy_path)
    parse_alert_policy_path = staticmethod(
        DashboardsServiceClient.parse_alert_policy_path
    )
    dashboard_path = staticmethod(DashboardsServiceClient.dashboard_path)
    parse_dashboard_path = staticmethod(DashboardsServiceClient.parse_dashboard_path)
    common_billing_account_path = staticmethod(
        DashboardsServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DashboardsServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DashboardsServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        DashboardsServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        DashboardsServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        DashboardsServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DashboardsServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        DashboardsServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(DashboardsServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        DashboardsServiceClient.parse_common_location_path
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
            DashboardsServiceAsyncClient: The constructed client.
        """
        return DashboardsServiceClient.from_service_account_info.__func__(DashboardsServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            DashboardsServiceAsyncClient: The constructed client.
        """
        return DashboardsServiceClient.from_service_account_file.__func__(DashboardsServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DashboardsServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            DashboardsServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DashboardsServiceClient).get_transport_class, type(DashboardsServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, DashboardsServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the dashboards service client.

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
        self._client = DashboardsServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_dashboard(
        self,
        request: dashboards_service.CreateDashboardRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dashboard.Dashboard:
        r"""Creates a new custom dashboard. For examples on how you can use
        this API to create dashboards, see `Managing dashboards by
        API </monitoring/dashboards/api-dashboard>`__. This method
        requires the ``monitoring.dashboards.create`` permission on the
        specified project. For more information about permissions, see
        `Cloud Identity and Access Management </iam>`__.

        Args:
            request (:class:`google.cloud.monitoring_dashboard_v1.types.CreateDashboardRequest`):
                The request object. The `CreateDashboard` request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_dashboard_v1.types.Dashboard:
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
            client_info=DEFAULT_CLIENT_INFO,
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
        `Cloud Identity and Access
        Management <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`google.cloud.monitoring_dashboard_v1.types.ListDashboardsRequest`):
                The request object. The `ListDashboards` request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_dashboard_v1.services.dashboards_service.pagers.ListDashboardsAsyncPager:
                The ListDashboards request.

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
            client_info=DEFAULT_CLIENT_INFO,
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
        `Cloud Identity and Access
        Management <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`google.cloud.monitoring_dashboard_v1.types.GetDashboardRequest`):
                The request object. The `GetDashboard` request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_dashboard_v1.types.Dashboard:
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
        `Cloud Identity and Access
        Management <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`google.cloud.monitoring_dashboard_v1.types.DeleteDashboardRequest`):
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
        `Cloud Identity and Access
        Management <https://cloud.google.com/iam>`__.

        Args:
            request (:class:`google.cloud.monitoring_dashboard_v1.types.UpdateDashboardRequest`):
                The request object. The `UpdateDashboard` request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_dashboard_v1.types.Dashboard:
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
            client_info=DEFAULT_CLIENT_INFO,
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
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-monitoring-dashboard",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DashboardsServiceAsyncClient",)
