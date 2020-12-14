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

import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.logging_v2.types import logging_metrics
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import MetricsServiceV2Transport, DEFAULT_CLIENT_INFO
from .grpc import MetricsServiceV2GrpcTransport


class MetricsServiceV2GrpcAsyncIOTransport(MetricsServiceV2Transport):
    """gRPC AsyncIO backend transport for MetricsServiceV2.

    Service for configuring logs-based metrics.

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
        host: str = "logging.googleapis.com",
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
        host: str = "logging.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
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
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._ssl_channel_credentials = ssl_channel_credentials

        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        elif api_mtls_endpoint:
            warnings.warn(
                "api_mtls_endpoint and client_cert_source are deprecated",
                DeprecationWarning,
            )

            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
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
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            self._ssl_channel_credentials = ssl_credentials
        else:
            host = host if ":" in host else host + ":443"

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_channel_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_log_metrics(
        self,
    ) -> Callable[
        [logging_metrics.ListLogMetricsRequest],
        Awaitable[logging_metrics.ListLogMetricsResponse],
    ]:
        r"""Return a callable for the list log metrics method over gRPC.

        Lists logs-based metrics.

        Returns:
            Callable[[~.ListLogMetricsRequest],
                    Awaitable[~.ListLogMetricsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_log_metrics" not in self._stubs:
            self._stubs["list_log_metrics"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.MetricsServiceV2/ListLogMetrics",
                request_serializer=logging_metrics.ListLogMetricsRequest.serialize,
                response_deserializer=logging_metrics.ListLogMetricsResponse.deserialize,
            )
        return self._stubs["list_log_metrics"]

    @property
    def get_log_metric(
        self,
    ) -> Callable[
        [logging_metrics.GetLogMetricRequest], Awaitable[logging_metrics.LogMetric]
    ]:
        r"""Return a callable for the get log metric method over gRPC.

        Gets a logs-based metric.

        Returns:
            Callable[[~.GetLogMetricRequest],
                    Awaitable[~.LogMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_log_metric" not in self._stubs:
            self._stubs["get_log_metric"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.MetricsServiceV2/GetLogMetric",
                request_serializer=logging_metrics.GetLogMetricRequest.serialize,
                response_deserializer=logging_metrics.LogMetric.deserialize,
            )
        return self._stubs["get_log_metric"]

    @property
    def create_log_metric(
        self,
    ) -> Callable[
        [logging_metrics.CreateLogMetricRequest], Awaitable[logging_metrics.LogMetric]
    ]:
        r"""Return a callable for the create log metric method over gRPC.

        Creates a logs-based metric.

        Returns:
            Callable[[~.CreateLogMetricRequest],
                    Awaitable[~.LogMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_log_metric" not in self._stubs:
            self._stubs["create_log_metric"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.MetricsServiceV2/CreateLogMetric",
                request_serializer=logging_metrics.CreateLogMetricRequest.serialize,
                response_deserializer=logging_metrics.LogMetric.deserialize,
            )
        return self._stubs["create_log_metric"]

    @property
    def update_log_metric(
        self,
    ) -> Callable[
        [logging_metrics.UpdateLogMetricRequest], Awaitable[logging_metrics.LogMetric]
    ]:
        r"""Return a callable for the update log metric method over gRPC.

        Creates or updates a logs-based metric.

        Returns:
            Callable[[~.UpdateLogMetricRequest],
                    Awaitable[~.LogMetric]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_log_metric" not in self._stubs:
            self._stubs["update_log_metric"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.MetricsServiceV2/UpdateLogMetric",
                request_serializer=logging_metrics.UpdateLogMetricRequest.serialize,
                response_deserializer=logging_metrics.LogMetric.deserialize,
            )
        return self._stubs["update_log_metric"]

    @property
    def delete_log_metric(
        self,
    ) -> Callable[[logging_metrics.DeleteLogMetricRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete log metric method over gRPC.

        Deletes a logs-based metric.

        Returns:
            Callable[[~.DeleteLogMetricRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_log_metric" not in self._stubs:
            self._stubs["delete_log_metric"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.MetricsServiceV2/DeleteLogMetric",
                request_serializer=logging_metrics.DeleteLogMetricRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_log_metric"]


__all__ = ("MetricsServiceV2GrpcAsyncIOTransport",)
