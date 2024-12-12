# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.cloud.backupdr_v1.types import (
    backupdr,
    backupplan,
    backupplanassociation,
    backupvault,
)

from .base import DEFAULT_CLIENT_INFO, BackupDRTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.cloud.backupdr.v1.BackupDR",
                    "rpcName": client_call_details.method,
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )

        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.backupdr.v1.BackupDR",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class BackupDRGrpcTransport(BackupDRTransport):
    """gRPC backend transport for BackupDR.

    The BackupDR Service

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
        host: str = "backupdr.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'backupdr.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
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
        self._operations_client: Optional[operations_v1.OperationsClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
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
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "backupdr.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
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
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_management_servers(
        self,
    ) -> Callable[
        [backupdr.ListManagementServersRequest], backupdr.ListManagementServersResponse
    ]:
        r"""Return a callable for the list management servers method over gRPC.

        Lists ManagementServers in a given project and
        location.

        Returns:
            Callable[[~.ListManagementServersRequest],
                    ~.ListManagementServersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_management_servers" not in self._stubs:
            self._stubs["list_management_servers"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/ListManagementServers",
                request_serializer=backupdr.ListManagementServersRequest.serialize,
                response_deserializer=backupdr.ListManagementServersResponse.deserialize,
            )
        return self._stubs["list_management_servers"]

    @property
    def get_management_server(
        self,
    ) -> Callable[[backupdr.GetManagementServerRequest], backupdr.ManagementServer]:
        r"""Return a callable for the get management server method over gRPC.

        Gets details of a single ManagementServer.

        Returns:
            Callable[[~.GetManagementServerRequest],
                    ~.ManagementServer]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_management_server" not in self._stubs:
            self._stubs["get_management_server"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/GetManagementServer",
                request_serializer=backupdr.GetManagementServerRequest.serialize,
                response_deserializer=backupdr.ManagementServer.deserialize,
            )
        return self._stubs["get_management_server"]

    @property
    def create_management_server(
        self,
    ) -> Callable[[backupdr.CreateManagementServerRequest], operations_pb2.Operation]:
        r"""Return a callable for the create management server method over gRPC.

        Creates a new ManagementServer in a given project and
        location.

        Returns:
            Callable[[~.CreateManagementServerRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_management_server" not in self._stubs:
            self._stubs["create_management_server"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/CreateManagementServer",
                request_serializer=backupdr.CreateManagementServerRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_management_server"]

    @property
    def delete_management_server(
        self,
    ) -> Callable[[backupdr.DeleteManagementServerRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete management server method over gRPC.

        Deletes a single ManagementServer.

        Returns:
            Callable[[~.DeleteManagementServerRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_management_server" not in self._stubs:
            self._stubs["delete_management_server"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/DeleteManagementServer",
                request_serializer=backupdr.DeleteManagementServerRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_management_server"]

    @property
    def create_backup_vault(
        self,
    ) -> Callable[[backupvault.CreateBackupVaultRequest], operations_pb2.Operation]:
        r"""Return a callable for the create backup vault method over gRPC.

        Creates a new BackupVault in a given project and
        location.

        Returns:
            Callable[[~.CreateBackupVaultRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup_vault" not in self._stubs:
            self._stubs["create_backup_vault"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/CreateBackupVault",
                request_serializer=backupvault.CreateBackupVaultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup_vault"]

    @property
    def list_backup_vaults(
        self,
    ) -> Callable[
        [backupvault.ListBackupVaultsRequest], backupvault.ListBackupVaultsResponse
    ]:
        r"""Return a callable for the list backup vaults method over gRPC.

        Lists BackupVaults in a given project and location.

        Returns:
            Callable[[~.ListBackupVaultsRequest],
                    ~.ListBackupVaultsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backup_vaults" not in self._stubs:
            self._stubs["list_backup_vaults"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/ListBackupVaults",
                request_serializer=backupvault.ListBackupVaultsRequest.serialize,
                response_deserializer=backupvault.ListBackupVaultsResponse.deserialize,
            )
        return self._stubs["list_backup_vaults"]

    @property
    def fetch_usable_backup_vaults(
        self,
    ) -> Callable[
        [backupvault.FetchUsableBackupVaultsRequest],
        backupvault.FetchUsableBackupVaultsResponse,
    ]:
        r"""Return a callable for the fetch usable backup vaults method over gRPC.

        FetchUsableBackupVaults lists usable BackupVaults in
        a given project and location. Usable BackupVault are the
        ones that user has backupdr.backupVaults.get permission.

        Returns:
            Callable[[~.FetchUsableBackupVaultsRequest],
                    ~.FetchUsableBackupVaultsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_usable_backup_vaults" not in self._stubs:
            self._stubs[
                "fetch_usable_backup_vaults"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/FetchUsableBackupVaults",
                request_serializer=backupvault.FetchUsableBackupVaultsRequest.serialize,
                response_deserializer=backupvault.FetchUsableBackupVaultsResponse.deserialize,
            )
        return self._stubs["fetch_usable_backup_vaults"]

    @property
    def get_backup_vault(
        self,
    ) -> Callable[[backupvault.GetBackupVaultRequest], backupvault.BackupVault]:
        r"""Return a callable for the get backup vault method over gRPC.

        Gets details of a BackupVault.

        Returns:
            Callable[[~.GetBackupVaultRequest],
                    ~.BackupVault]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup_vault" not in self._stubs:
            self._stubs["get_backup_vault"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/GetBackupVault",
                request_serializer=backupvault.GetBackupVaultRequest.serialize,
                response_deserializer=backupvault.BackupVault.deserialize,
            )
        return self._stubs["get_backup_vault"]

    @property
    def update_backup_vault(
        self,
    ) -> Callable[[backupvault.UpdateBackupVaultRequest], operations_pb2.Operation]:
        r"""Return a callable for the update backup vault method over gRPC.

        Updates the settings of a BackupVault.

        Returns:
            Callable[[~.UpdateBackupVaultRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_backup_vault" not in self._stubs:
            self._stubs["update_backup_vault"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/UpdateBackupVault",
                request_serializer=backupvault.UpdateBackupVaultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_backup_vault"]

    @property
    def delete_backup_vault(
        self,
    ) -> Callable[[backupvault.DeleteBackupVaultRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete backup vault method over gRPC.

        Deletes a BackupVault.

        Returns:
            Callable[[~.DeleteBackupVaultRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup_vault" not in self._stubs:
            self._stubs["delete_backup_vault"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/DeleteBackupVault",
                request_serializer=backupvault.DeleteBackupVaultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup_vault"]

    @property
    def list_data_sources(
        self,
    ) -> Callable[
        [backupvault.ListDataSourcesRequest], backupvault.ListDataSourcesResponse
    ]:
        r"""Return a callable for the list data sources method over gRPC.

        Lists DataSources in a given project and location.

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
            self._stubs["list_data_sources"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/ListDataSources",
                request_serializer=backupvault.ListDataSourcesRequest.serialize,
                response_deserializer=backupvault.ListDataSourcesResponse.deserialize,
            )
        return self._stubs["list_data_sources"]

    @property
    def get_data_source(
        self,
    ) -> Callable[[backupvault.GetDataSourceRequest], backupvault.DataSource]:
        r"""Return a callable for the get data source method over gRPC.

        Gets details of a DataSource.

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
            self._stubs["get_data_source"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/GetDataSource",
                request_serializer=backupvault.GetDataSourceRequest.serialize,
                response_deserializer=backupvault.DataSource.deserialize,
            )
        return self._stubs["get_data_source"]

    @property
    def update_data_source(
        self,
    ) -> Callable[[backupvault.UpdateDataSourceRequest], operations_pb2.Operation]:
        r"""Return a callable for the update data source method over gRPC.

        Updates the settings of a DataSource.

        Returns:
            Callable[[~.UpdateDataSourceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_source" not in self._stubs:
            self._stubs["update_data_source"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/UpdateDataSource",
                request_serializer=backupvault.UpdateDataSourceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_data_source"]

    @property
    def list_backups(
        self,
    ) -> Callable[[backupvault.ListBackupsRequest], backupvault.ListBackupsResponse]:
        r"""Return a callable for the list backups method over gRPC.

        Lists Backups in a given project and location.

        Returns:
            Callable[[~.ListBackupsRequest],
                    ~.ListBackupsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backups" not in self._stubs:
            self._stubs["list_backups"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/ListBackups",
                request_serializer=backupvault.ListBackupsRequest.serialize,
                response_deserializer=backupvault.ListBackupsResponse.deserialize,
            )
        return self._stubs["list_backups"]

    @property
    def get_backup(
        self,
    ) -> Callable[[backupvault.GetBackupRequest], backupvault.Backup]:
        r"""Return a callable for the get backup method over gRPC.

        Gets details of a Backup.

        Returns:
            Callable[[~.GetBackupRequest],
                    ~.Backup]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup" not in self._stubs:
            self._stubs["get_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/GetBackup",
                request_serializer=backupvault.GetBackupRequest.serialize,
                response_deserializer=backupvault.Backup.deserialize,
            )
        return self._stubs["get_backup"]

    @property
    def update_backup(
        self,
    ) -> Callable[[backupvault.UpdateBackupRequest], operations_pb2.Operation]:
        r"""Return a callable for the update backup method over gRPC.

        Updates the settings of a Backup.

        Returns:
            Callable[[~.UpdateBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_backup" not in self._stubs:
            self._stubs["update_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/UpdateBackup",
                request_serializer=backupvault.UpdateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_backup"]

    @property
    def delete_backup(
        self,
    ) -> Callable[[backupvault.DeleteBackupRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete backup method over gRPC.

        Deletes a Backup.

        Returns:
            Callable[[~.DeleteBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup" not in self._stubs:
            self._stubs["delete_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/DeleteBackup",
                request_serializer=backupvault.DeleteBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup"]

    @property
    def restore_backup(
        self,
    ) -> Callable[[backupvault.RestoreBackupRequest], operations_pb2.Operation]:
        r"""Return a callable for the restore backup method over gRPC.

        Restore from a Backup

        Returns:
            Callable[[~.RestoreBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_backup" not in self._stubs:
            self._stubs["restore_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/RestoreBackup",
                request_serializer=backupvault.RestoreBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_backup"]

    @property
    def create_backup_plan(
        self,
    ) -> Callable[[backupplan.CreateBackupPlanRequest], operations_pb2.Operation]:
        r"""Return a callable for the create backup plan method over gRPC.

        Create a BackupPlan

        Returns:
            Callable[[~.CreateBackupPlanRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup_plan" not in self._stubs:
            self._stubs["create_backup_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/CreateBackupPlan",
                request_serializer=backupplan.CreateBackupPlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup_plan"]

    @property
    def get_backup_plan(
        self,
    ) -> Callable[[backupplan.GetBackupPlanRequest], backupplan.BackupPlan]:
        r"""Return a callable for the get backup plan method over gRPC.

        Gets details of a single BackupPlan.

        Returns:
            Callable[[~.GetBackupPlanRequest],
                    ~.BackupPlan]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup_plan" not in self._stubs:
            self._stubs["get_backup_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/GetBackupPlan",
                request_serializer=backupplan.GetBackupPlanRequest.serialize,
                response_deserializer=backupplan.BackupPlan.deserialize,
            )
        return self._stubs["get_backup_plan"]

    @property
    def list_backup_plans(
        self,
    ) -> Callable[
        [backupplan.ListBackupPlansRequest], backupplan.ListBackupPlansResponse
    ]:
        r"""Return a callable for the list backup plans method over gRPC.

        Lists BackupPlans in a given project and location.

        Returns:
            Callable[[~.ListBackupPlansRequest],
                    ~.ListBackupPlansResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backup_plans" not in self._stubs:
            self._stubs["list_backup_plans"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/ListBackupPlans",
                request_serializer=backupplan.ListBackupPlansRequest.serialize,
                response_deserializer=backupplan.ListBackupPlansResponse.deserialize,
            )
        return self._stubs["list_backup_plans"]

    @property
    def delete_backup_plan(
        self,
    ) -> Callable[[backupplan.DeleteBackupPlanRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete backup plan method over gRPC.

        Deletes a single BackupPlan.

        Returns:
            Callable[[~.DeleteBackupPlanRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup_plan" not in self._stubs:
            self._stubs["delete_backup_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/DeleteBackupPlan",
                request_serializer=backupplan.DeleteBackupPlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup_plan"]

    @property
    def create_backup_plan_association(
        self,
    ) -> Callable[
        [backupplanassociation.CreateBackupPlanAssociationRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the create backup plan association method over gRPC.

        Create a BackupPlanAssociation

        Returns:
            Callable[[~.CreateBackupPlanAssociationRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup_plan_association" not in self._stubs:
            self._stubs[
                "create_backup_plan_association"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/CreateBackupPlanAssociation",
                request_serializer=backupplanassociation.CreateBackupPlanAssociationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup_plan_association"]

    @property
    def get_backup_plan_association(
        self,
    ) -> Callable[
        [backupplanassociation.GetBackupPlanAssociationRequest],
        backupplanassociation.BackupPlanAssociation,
    ]:
        r"""Return a callable for the get backup plan association method over gRPC.

        Gets details of a single BackupPlanAssociation.

        Returns:
            Callable[[~.GetBackupPlanAssociationRequest],
                    ~.BackupPlanAssociation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup_plan_association" not in self._stubs:
            self._stubs[
                "get_backup_plan_association"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/GetBackupPlanAssociation",
                request_serializer=backupplanassociation.GetBackupPlanAssociationRequest.serialize,
                response_deserializer=backupplanassociation.BackupPlanAssociation.deserialize,
            )
        return self._stubs["get_backup_plan_association"]

    @property
    def list_backup_plan_associations(
        self,
    ) -> Callable[
        [backupplanassociation.ListBackupPlanAssociationsRequest],
        backupplanassociation.ListBackupPlanAssociationsResponse,
    ]:
        r"""Return a callable for the list backup plan associations method over gRPC.

        Lists BackupPlanAssociations in a given project and
        location.

        Returns:
            Callable[[~.ListBackupPlanAssociationsRequest],
                    ~.ListBackupPlanAssociationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backup_plan_associations" not in self._stubs:
            self._stubs[
                "list_backup_plan_associations"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/ListBackupPlanAssociations",
                request_serializer=backupplanassociation.ListBackupPlanAssociationsRequest.serialize,
                response_deserializer=backupplanassociation.ListBackupPlanAssociationsResponse.deserialize,
            )
        return self._stubs["list_backup_plan_associations"]

    @property
    def delete_backup_plan_association(
        self,
    ) -> Callable[
        [backupplanassociation.DeleteBackupPlanAssociationRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the delete backup plan association method over gRPC.

        Deletes a single BackupPlanAssociation.

        Returns:
            Callable[[~.DeleteBackupPlanAssociationRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup_plan_association" not in self._stubs:
            self._stubs[
                "delete_backup_plan_association"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/DeleteBackupPlanAssociation",
                request_serializer=backupplanassociation.DeleteBackupPlanAssociationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup_plan_association"]

    @property
    def trigger_backup(
        self,
    ) -> Callable[
        [backupplanassociation.TriggerBackupRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the trigger backup method over gRPC.

        Triggers a new Backup.

        Returns:
            Callable[[~.TriggerBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "trigger_backup" not in self._stubs:
            self._stubs["trigger_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.backupdr.v1.BackupDR/TriggerBackup",
                request_serializer=backupplanassociation.TriggerBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["trigger_backup"]

    def close(self):
        self._logged_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.
        Sets the IAM access control policy on the specified
        function. Replaces any existing policy.
        Returns:
            Callable[[~.SetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self._logged_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.
        Gets the IAM access control policy for a function.
        Returns an empty policy if the function exists and does
        not have a policy set.
        Returns:
            Callable[[~.GetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self._logged_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.
        Tests the specified permissions against the IAM access control
        policy for a function. If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.
        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    ~.TestIamPermissionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self._logged_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("BackupDRGrpcTransport",)
