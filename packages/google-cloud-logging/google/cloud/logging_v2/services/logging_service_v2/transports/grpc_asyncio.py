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

from google.cloud.logging_v2.types import logging
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import LoggingServiceV2Transport, DEFAULT_CLIENT_INFO
from .grpc import LoggingServiceV2GrpcTransport


class LoggingServiceV2GrpcAsyncIOTransport(LoggingServiceV2Transport):
    """gRPC AsyncIO backend transport for LoggingServiceV2.

    Service for ingesting and querying logs.

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
    def delete_log(
        self,
    ) -> Callable[[logging.DeleteLogRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete log method over gRPC.

        Deletes all the log entries in a log. The log
        reappears if it receives new entries. Log entries
        written shortly before the delete operation might not be
        deleted. Entries received after the delete operation
        with a timestamp before the operation will be deleted.

        Returns:
            Callable[[~.DeleteLogRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_log" not in self._stubs:
            self._stubs["delete_log"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.LoggingServiceV2/DeleteLog",
                request_serializer=logging.DeleteLogRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_log"]

    @property
    def write_log_entries(
        self,
    ) -> Callable[
        [logging.WriteLogEntriesRequest], Awaitable[logging.WriteLogEntriesResponse]
    ]:
        r"""Return a callable for the write log entries method over gRPC.

        Writes log entries to Logging. This API method is the
        only way to send log entries to Logging. This method is
        used, directly or indirectly, by the Logging agent
        (fluentd) and all logging libraries configured to use
        Logging. A single request may contain log entries for a
        maximum of 1000 different resources (projects,
        organizations, billing accounts or folders)

        Returns:
            Callable[[~.WriteLogEntriesRequest],
                    Awaitable[~.WriteLogEntriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "write_log_entries" not in self._stubs:
            self._stubs["write_log_entries"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.LoggingServiceV2/WriteLogEntries",
                request_serializer=logging.WriteLogEntriesRequest.serialize,
                response_deserializer=logging.WriteLogEntriesResponse.deserialize,
            )
        return self._stubs["write_log_entries"]

    @property
    def list_log_entries(
        self,
    ) -> Callable[
        [logging.ListLogEntriesRequest], Awaitable[logging.ListLogEntriesResponse]
    ]:
        r"""Return a callable for the list log entries method over gRPC.

        Lists log entries. Use this method to retrieve log entries that
        originated from a project/folder/organization/billing account.
        For ways to export log entries, see `Exporting
        Logs <https://cloud.google.com/logging/docs/export>`__.

        Returns:
            Callable[[~.ListLogEntriesRequest],
                    Awaitable[~.ListLogEntriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_log_entries" not in self._stubs:
            self._stubs["list_log_entries"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.LoggingServiceV2/ListLogEntries",
                request_serializer=logging.ListLogEntriesRequest.serialize,
                response_deserializer=logging.ListLogEntriesResponse.deserialize,
            )
        return self._stubs["list_log_entries"]

    @property
    def list_monitored_resource_descriptors(
        self,
    ) -> Callable[
        [logging.ListMonitoredResourceDescriptorsRequest],
        Awaitable[logging.ListMonitoredResourceDescriptorsResponse],
    ]:
        r"""Return a callable for the list monitored resource
        descriptors method over gRPC.

        Lists the descriptors for monitored resource types
        used by Logging.

        Returns:
            Callable[[~.ListMonitoredResourceDescriptorsRequest],
                    Awaitable[~.ListMonitoredResourceDescriptorsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_monitored_resource_descriptors" not in self._stubs:
            self._stubs[
                "list_monitored_resource_descriptors"
            ] = self.grpc_channel.unary_unary(
                "/google.logging.v2.LoggingServiceV2/ListMonitoredResourceDescriptors",
                request_serializer=logging.ListMonitoredResourceDescriptorsRequest.serialize,
                response_deserializer=logging.ListMonitoredResourceDescriptorsResponse.deserialize,
            )
        return self._stubs["list_monitored_resource_descriptors"]

    @property
    def list_logs(
        self,
    ) -> Callable[[logging.ListLogsRequest], Awaitable[logging.ListLogsResponse]]:
        r"""Return a callable for the list logs method over gRPC.

        Lists the logs in projects, organizations, folders,
        or billing accounts. Only logs that have entries are
        listed.

        Returns:
            Callable[[~.ListLogsRequest],
                    Awaitable[~.ListLogsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_logs" not in self._stubs:
            self._stubs["list_logs"] = self.grpc_channel.unary_unary(
                "/google.logging.v2.LoggingServiceV2/ListLogs",
                request_serializer=logging.ListLogsRequest.serialize,
                response_deserializer=logging.ListLogsResponse.deserialize,
            )
        return self._stubs["list_logs"]

    @property
    def tail_log_entries(
        self,
    ) -> Callable[
        [logging.TailLogEntriesRequest], Awaitable[logging.TailLogEntriesResponse]
    ]:
        r"""Return a callable for the tail log entries method over gRPC.

        Streaming read of log entries as they are ingested.
        Until the stream is terminated, it will continue reading
        logs.

        Returns:
            Callable[[~.TailLogEntriesRequest],
                    Awaitable[~.TailLogEntriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "tail_log_entries" not in self._stubs:
            self._stubs["tail_log_entries"] = self.grpc_channel.stream_stream(
                "/google.logging.v2.LoggingServiceV2/TailLogEntries",
                request_serializer=logging.TailLogEntriesRequest.serialize,
                response_deserializer=logging.TailLogEntriesResponse.deserialize,
            )
        return self._stubs["tail_log_entries"]


__all__ = ("LoggingServiceV2GrpcAsyncIOTransport",)
