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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import gapic_v1  # type: ignore
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.bigquery_datatransfer_v1.types import datatransfer
from google.cloud.bigquery_datatransfer_v1.types import transfer
from google.protobuf import empty_pb2  # type: ignore
from .base import DataTransferServiceTransport, DEFAULT_CLIENT_INFO


class DataTransferServiceGrpcTransport(DataTransferServiceTransport):
    """gRPC backend transport for DataTransferService.

    The Google BigQuery Data Transfer Service API enables
    BigQuery users to configure the transfer of their data from
    other Google Products into BigQuery. This service contains
    methods that are end user exposed. It backs up the frontend.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "bigquerydatatransfer.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
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
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "bigquerydatatransfer.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def get_data_source(
        self,
    ) -> Callable[[datatransfer.GetDataSourceRequest], datatransfer.DataSource]:
        r"""Return a callable for the get data source method over gRPC.

        Retrieves a supported data source and returns its
        settings, which can be used for UI rendering.

        Returns:
            Callable[[~.GetDataSourceRequest],
                    ~.DataSource]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_source" not in self._stubs:
            self._stubs["get_data_source"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/GetDataSource",
                request_serializer=datatransfer.GetDataSourceRequest.serialize,
                response_deserializer=datatransfer.DataSource.deserialize,
            )
        return self._stubs["get_data_source"]

    @property
    def list_data_sources(
        self,
    ) -> Callable[
        [datatransfer.ListDataSourcesRequest], datatransfer.ListDataSourcesResponse
    ]:
        r"""Return a callable for the list data sources method over gRPC.

        Lists supported data sources and returns their
        settings, which can be used for UI rendering.

        Returns:
            Callable[[~.ListDataSourcesRequest],
                    ~.ListDataSourcesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_data_sources" not in self._stubs:
            self._stubs["list_data_sources"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/ListDataSources",
                request_serializer=datatransfer.ListDataSourcesRequest.serialize,
                response_deserializer=datatransfer.ListDataSourcesResponse.deserialize,
            )
        return self._stubs["list_data_sources"]

    @property
    def create_transfer_config(
        self,
    ) -> Callable[[datatransfer.CreateTransferConfigRequest], transfer.TransferConfig]:
        r"""Return a callable for the create transfer config method over gRPC.

        Creates a new data transfer configuration.

        Returns:
            Callable[[~.CreateTransferConfigRequest],
                    ~.TransferConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_transfer_config" not in self._stubs:
            self._stubs["create_transfer_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/CreateTransferConfig",
                request_serializer=datatransfer.CreateTransferConfigRequest.serialize,
                response_deserializer=transfer.TransferConfig.deserialize,
            )
        return self._stubs["create_transfer_config"]

    @property
    def update_transfer_config(
        self,
    ) -> Callable[[datatransfer.UpdateTransferConfigRequest], transfer.TransferConfig]:
        r"""Return a callable for the update transfer config method over gRPC.

        Updates a data transfer configuration.
        All fields must be set, even if they are not updated.

        Returns:
            Callable[[~.UpdateTransferConfigRequest],
                    ~.TransferConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_transfer_config" not in self._stubs:
            self._stubs["update_transfer_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/UpdateTransferConfig",
                request_serializer=datatransfer.UpdateTransferConfigRequest.serialize,
                response_deserializer=transfer.TransferConfig.deserialize,
            )
        return self._stubs["update_transfer_config"]

    @property
    def delete_transfer_config(
        self,
    ) -> Callable[[datatransfer.DeleteTransferConfigRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete transfer config method over gRPC.

        Deletes a data transfer configuration,
        including any associated transfer runs and logs.

        Returns:
            Callable[[~.DeleteTransferConfigRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_transfer_config" not in self._stubs:
            self._stubs["delete_transfer_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/DeleteTransferConfig",
                request_serializer=datatransfer.DeleteTransferConfigRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_transfer_config"]

    @property
    def get_transfer_config(
        self,
    ) -> Callable[[datatransfer.GetTransferConfigRequest], transfer.TransferConfig]:
        r"""Return a callable for the get transfer config method over gRPC.

        Returns information about a data transfer config.

        Returns:
            Callable[[~.GetTransferConfigRequest],
                    ~.TransferConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_transfer_config" not in self._stubs:
            self._stubs["get_transfer_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/GetTransferConfig",
                request_serializer=datatransfer.GetTransferConfigRequest.serialize,
                response_deserializer=transfer.TransferConfig.deserialize,
            )
        return self._stubs["get_transfer_config"]

    @property
    def list_transfer_configs(
        self,
    ) -> Callable[
        [datatransfer.ListTransferConfigsRequest],
        datatransfer.ListTransferConfigsResponse,
    ]:
        r"""Return a callable for the list transfer configs method over gRPC.

        Returns information about all data transfers in the
        project.

        Returns:
            Callable[[~.ListTransferConfigsRequest],
                    ~.ListTransferConfigsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_transfer_configs" not in self._stubs:
            self._stubs["list_transfer_configs"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/ListTransferConfigs",
                request_serializer=datatransfer.ListTransferConfigsRequest.serialize,
                response_deserializer=datatransfer.ListTransferConfigsResponse.deserialize,
            )
        return self._stubs["list_transfer_configs"]

    @property
    def schedule_transfer_runs(
        self,
    ) -> Callable[
        [datatransfer.ScheduleTransferRunsRequest],
        datatransfer.ScheduleTransferRunsResponse,
    ]:
        r"""Return a callable for the schedule transfer runs method over gRPC.

        Creates transfer runs for a time range [start_time, end_time].
        For each date - or whatever granularity the data source supports
        - in the range, one transfer run is created. Note that runs are
        created per UTC time in the time range. DEPRECATED: use
        StartManualTransferRuns instead.

        Returns:
            Callable[[~.ScheduleTransferRunsRequest],
                    ~.ScheduleTransferRunsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "schedule_transfer_runs" not in self._stubs:
            self._stubs["schedule_transfer_runs"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/ScheduleTransferRuns",
                request_serializer=datatransfer.ScheduleTransferRunsRequest.serialize,
                response_deserializer=datatransfer.ScheduleTransferRunsResponse.deserialize,
            )
        return self._stubs["schedule_transfer_runs"]

    @property
    def start_manual_transfer_runs(
        self,
    ) -> Callable[
        [datatransfer.StartManualTransferRunsRequest],
        datatransfer.StartManualTransferRunsResponse,
    ]:
        r"""Return a callable for the start manual transfer runs method over gRPC.

        Start manual transfer runs to be executed now with schedule_time
        equal to current time. The transfer runs can be created for a
        time range where the run_time is between start_time (inclusive)
        and end_time (exclusive), or for a specific run_time.

        Returns:
            Callable[[~.StartManualTransferRunsRequest],
                    ~.StartManualTransferRunsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_manual_transfer_runs" not in self._stubs:
            self._stubs["start_manual_transfer_runs"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/StartManualTransferRuns",
                request_serializer=datatransfer.StartManualTransferRunsRequest.serialize,
                response_deserializer=datatransfer.StartManualTransferRunsResponse.deserialize,
            )
        return self._stubs["start_manual_transfer_runs"]

    @property
    def get_transfer_run(
        self,
    ) -> Callable[[datatransfer.GetTransferRunRequest], transfer.TransferRun]:
        r"""Return a callable for the get transfer run method over gRPC.

        Returns information about the particular transfer
        run.

        Returns:
            Callable[[~.GetTransferRunRequest],
                    ~.TransferRun]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_transfer_run" not in self._stubs:
            self._stubs["get_transfer_run"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/GetTransferRun",
                request_serializer=datatransfer.GetTransferRunRequest.serialize,
                response_deserializer=transfer.TransferRun.deserialize,
            )
        return self._stubs["get_transfer_run"]

    @property
    def delete_transfer_run(
        self,
    ) -> Callable[[datatransfer.DeleteTransferRunRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete transfer run method over gRPC.

        Deletes the specified transfer run.

        Returns:
            Callable[[~.DeleteTransferRunRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_transfer_run" not in self._stubs:
            self._stubs["delete_transfer_run"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/DeleteTransferRun",
                request_serializer=datatransfer.DeleteTransferRunRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_transfer_run"]

    @property
    def list_transfer_runs(
        self,
    ) -> Callable[
        [datatransfer.ListTransferRunsRequest], datatransfer.ListTransferRunsResponse
    ]:
        r"""Return a callable for the list transfer runs method over gRPC.

        Returns information about running and completed jobs.

        Returns:
            Callable[[~.ListTransferRunsRequest],
                    ~.ListTransferRunsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_transfer_runs" not in self._stubs:
            self._stubs["list_transfer_runs"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/ListTransferRuns",
                request_serializer=datatransfer.ListTransferRunsRequest.serialize,
                response_deserializer=datatransfer.ListTransferRunsResponse.deserialize,
            )
        return self._stubs["list_transfer_runs"]

    @property
    def list_transfer_logs(
        self,
    ) -> Callable[
        [datatransfer.ListTransferLogsRequest], datatransfer.ListTransferLogsResponse
    ]:
        r"""Return a callable for the list transfer logs method over gRPC.

        Returns user facing log messages for the data
        transfer run.

        Returns:
            Callable[[~.ListTransferLogsRequest],
                    ~.ListTransferLogsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_transfer_logs" not in self._stubs:
            self._stubs["list_transfer_logs"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/ListTransferLogs",
                request_serializer=datatransfer.ListTransferLogsRequest.serialize,
                response_deserializer=datatransfer.ListTransferLogsResponse.deserialize,
            )
        return self._stubs["list_transfer_logs"]

    @property
    def check_valid_creds(
        self,
    ) -> Callable[
        [datatransfer.CheckValidCredsRequest], datatransfer.CheckValidCredsResponse
    ]:
        r"""Return a callable for the check valid creds method over gRPC.

        Returns true if valid credentials exist for the given
        data source and requesting user.
        Some data sources doesn't support service account, so we
        need to talk to them on behalf of the end user. This API
        just checks whether we have OAuth token for the
        particular user, which is a pre-requisite before user
        can create a transfer config.

        Returns:
            Callable[[~.CheckValidCredsRequest],
                    ~.CheckValidCredsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "check_valid_creds" not in self._stubs:
            self._stubs["check_valid_creds"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.datatransfer.v1.DataTransferService/CheckValidCreds",
                request_serializer=datatransfer.CheckValidCredsRequest.serialize,
                response_deserializer=datatransfer.CheckValidCredsResponse.deserialize,
            )
        return self._stubs["check_valid_creds"]


__all__ = ("DataTransferServiceGrpcTransport",)
