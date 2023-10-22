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

from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.monitoring.dashboard_v1.types import dashboard, dashboards_service

from .base import DashboardsServiceTransport
from .grpc import DashboardsServiceGrpcTransport


class DashboardsServiceGrpcAsyncIOTransport(DashboardsServiceTransport):
    """gRPC AsyncIO backend transport for DashboardsService.

    Manages Stackdriver dashboards. A dashboard is an arrangement
    of data display widgets in a specific layout.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "monitoring.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "monitoring.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host,
                credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_dashboard(
        self,
    ) -> Callable[
        [dashboards_service.CreateDashboardRequest], Awaitable[dashboard.Dashboard]
    ]:
        r"""Return a callable for the create dashboard method over gRPC.

        Creates a new custom dashboard.

        This method requires the ``monitoring.dashboards.create``
        permission on the specified project. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable[[~.CreateDashboardRequest],
                    Awaitable[~.Dashboard]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_dashboard" not in self._stubs:
            self._stubs["create_dashboard"] = self.grpc_channel.unary_unary(
                "/google.monitoring.dashboard.v1.DashboardsService/CreateDashboard",
                request_serializer=dashboards_service.CreateDashboardRequest.serialize,
                response_deserializer=dashboard.Dashboard.deserialize,
            )
        return self._stubs["create_dashboard"]

    @property
    def list_dashboards(
        self,
    ) -> Callable[
        [dashboards_service.ListDashboardsRequest],
        Awaitable[dashboards_service.ListDashboardsResponse],
    ]:
        r"""Return a callable for the list dashboards method over gRPC.

        Lists the existing dashboards.

        This method requires the ``monitoring.dashboards.list``
        permission on the specified project. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable[[~.ListDashboardsRequest],
                    Awaitable[~.ListDashboardsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_dashboards" not in self._stubs:
            self._stubs["list_dashboards"] = self.grpc_channel.unary_unary(
                "/google.monitoring.dashboard.v1.DashboardsService/ListDashboards",
                request_serializer=dashboards_service.ListDashboardsRequest.serialize,
                response_deserializer=dashboards_service.ListDashboardsResponse.deserialize,
            )
        return self._stubs["list_dashboards"]

    @property
    def get_dashboard(
        self,
    ) -> Callable[
        [dashboards_service.GetDashboardRequest], Awaitable[dashboard.Dashboard]
    ]:
        r"""Return a callable for the get dashboard method over gRPC.

        Fetches a specific dashboard.

        This method requires the ``monitoring.dashboards.get``
        permission on the specified dashboard. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable[[~.GetDashboardRequest],
                    Awaitable[~.Dashboard]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_dashboard" not in self._stubs:
            self._stubs["get_dashboard"] = self.grpc_channel.unary_unary(
                "/google.monitoring.dashboard.v1.DashboardsService/GetDashboard",
                request_serializer=dashboards_service.GetDashboardRequest.serialize,
                response_deserializer=dashboard.Dashboard.deserialize,
            )
        return self._stubs["get_dashboard"]

    @property
    def delete_dashboard(
        self,
    ) -> Callable[[dashboards_service.DeleteDashboardRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete dashboard method over gRPC.

        Deletes an existing custom dashboard.

        This method requires the ``monitoring.dashboards.delete``
        permission on the specified dashboard. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable[[~.DeleteDashboardRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_dashboard" not in self._stubs:
            self._stubs["delete_dashboard"] = self.grpc_channel.unary_unary(
                "/google.monitoring.dashboard.v1.DashboardsService/DeleteDashboard",
                request_serializer=dashboards_service.DeleteDashboardRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_dashboard"]

    @property
    def update_dashboard(
        self,
    ) -> Callable[
        [dashboards_service.UpdateDashboardRequest], Awaitable[dashboard.Dashboard]
    ]:
        r"""Return a callable for the update dashboard method over gRPC.

        Replaces an existing custom dashboard with a new definition.

        This method requires the ``monitoring.dashboards.update``
        permission on the specified dashboard. For more information, see
        `Google Cloud IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable[[~.UpdateDashboardRequest],
                    Awaitable[~.Dashboard]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_dashboard" not in self._stubs:
            self._stubs["update_dashboard"] = self.grpc_channel.unary_unary(
                "/google.monitoring.dashboard.v1.DashboardsService/UpdateDashboard",
                request_serializer=dashboards_service.UpdateDashboardRequest.serialize,
                response_deserializer=dashboard.Dashboard.deserialize,
            )
        return self._stubs["update_dashboard"]


__all__ = ("DashboardsServiceGrpcAsyncIOTransport",)
