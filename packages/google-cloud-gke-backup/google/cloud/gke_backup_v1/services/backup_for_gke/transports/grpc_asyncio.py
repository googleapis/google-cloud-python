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
import inspect
import json
import logging as std_logging
import pickle
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.gke_backup_v1.types import (
    backup,
    backup_plan,
    gkebackup,
    restore,
    restore_plan,
    volume,
)

from .base import DEFAULT_CLIENT_INFO, BackupForGKETransport
from .grpc import BackupForGKEGrpcTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientAIOInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor
):  # pragma: NO COVER
    async def intercept_unary_unary(self, continuation, client_call_details, request):
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
                    "serviceName": "google.cloud.gkebackup.v1.BackupForGKE",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = await continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = await response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = await response
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
                f"Received response to rpc {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.gkebackup.v1.BackupForGKE",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class BackupForGKEGrpcAsyncIOTransport(BackupForGKETransport):
    """gRPC AsyncIO backend transport for BackupForGKE.

    BackupForGKE allows Kubernetes administrators to configure,
    execute, and manage backup and restore operations for their GKE
    clusters.

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
        host: str = "gkebackup.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
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

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "gkebackup.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
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
                 The hostname to connect to (default: 'gkebackup.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
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
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, aio.Channel):
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

        self._interceptor = _LoggingClientAIOInterceptor()
        self._grpc_channel._unary_unary_interceptors.append(self._interceptor)
        self._logged_channel = self._grpc_channel
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_backup_plan(
        self,
    ) -> Callable[
        [gkebackup.CreateBackupPlanRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create backup plan method over gRPC.

        Creates a new BackupPlan in a given location.

        Returns:
            Callable[[~.CreateBackupPlanRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup_plan" not in self._stubs:
            self._stubs["create_backup_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/CreateBackupPlan",
                request_serializer=gkebackup.CreateBackupPlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup_plan"]

    @property
    def list_backup_plans(
        self,
    ) -> Callable[
        [gkebackup.ListBackupPlansRequest], Awaitable[gkebackup.ListBackupPlansResponse]
    ]:
        r"""Return a callable for the list backup plans method over gRPC.

        Lists BackupPlans in a given location.

        Returns:
            Callable[[~.ListBackupPlansRequest],
                    Awaitable[~.ListBackupPlansResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backup_plans" not in self._stubs:
            self._stubs["list_backup_plans"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/ListBackupPlans",
                request_serializer=gkebackup.ListBackupPlansRequest.serialize,
                response_deserializer=gkebackup.ListBackupPlansResponse.deserialize,
            )
        return self._stubs["list_backup_plans"]

    @property
    def get_backup_plan(
        self,
    ) -> Callable[[gkebackup.GetBackupPlanRequest], Awaitable[backup_plan.BackupPlan]]:
        r"""Return a callable for the get backup plan method over gRPC.

        Retrieve the details of a single BackupPlan.

        Returns:
            Callable[[~.GetBackupPlanRequest],
                    Awaitable[~.BackupPlan]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup_plan" not in self._stubs:
            self._stubs["get_backup_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/GetBackupPlan",
                request_serializer=gkebackup.GetBackupPlanRequest.serialize,
                response_deserializer=backup_plan.BackupPlan.deserialize,
            )
        return self._stubs["get_backup_plan"]

    @property
    def update_backup_plan(
        self,
    ) -> Callable[
        [gkebackup.UpdateBackupPlanRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update backup plan method over gRPC.

        Update a BackupPlan.

        Returns:
            Callable[[~.UpdateBackupPlanRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_backup_plan" not in self._stubs:
            self._stubs["update_backup_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/UpdateBackupPlan",
                request_serializer=gkebackup.UpdateBackupPlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_backup_plan"]

    @property
    def delete_backup_plan(
        self,
    ) -> Callable[
        [gkebackup.DeleteBackupPlanRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete backup plan method over gRPC.

        Deletes an existing BackupPlan.

        Returns:
            Callable[[~.DeleteBackupPlanRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup_plan" not in self._stubs:
            self._stubs["delete_backup_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/DeleteBackupPlan",
                request_serializer=gkebackup.DeleteBackupPlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup_plan"]

    @property
    def create_backup(
        self,
    ) -> Callable[[gkebackup.CreateBackupRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create backup method over gRPC.

        Creates a Backup for the given BackupPlan.

        Returns:
            Callable[[~.CreateBackupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup" not in self._stubs:
            self._stubs["create_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/CreateBackup",
                request_serializer=gkebackup.CreateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup"]

    @property
    def list_backups(
        self,
    ) -> Callable[
        [gkebackup.ListBackupsRequest], Awaitable[gkebackup.ListBackupsResponse]
    ]:
        r"""Return a callable for the list backups method over gRPC.

        Lists the Backups for a given BackupPlan.

        Returns:
            Callable[[~.ListBackupsRequest],
                    Awaitable[~.ListBackupsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backups" not in self._stubs:
            self._stubs["list_backups"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/ListBackups",
                request_serializer=gkebackup.ListBackupsRequest.serialize,
                response_deserializer=gkebackup.ListBackupsResponse.deserialize,
            )
        return self._stubs["list_backups"]

    @property
    def get_backup(
        self,
    ) -> Callable[[gkebackup.GetBackupRequest], Awaitable[backup.Backup]]:
        r"""Return a callable for the get backup method over gRPC.

        Retrieve the details of a single Backup.

        Returns:
            Callable[[~.GetBackupRequest],
                    Awaitable[~.Backup]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup" not in self._stubs:
            self._stubs["get_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/GetBackup",
                request_serializer=gkebackup.GetBackupRequest.serialize,
                response_deserializer=backup.Backup.deserialize,
            )
        return self._stubs["get_backup"]

    @property
    def update_backup(
        self,
    ) -> Callable[[gkebackup.UpdateBackupRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update backup method over gRPC.

        Update a Backup.

        Returns:
            Callable[[~.UpdateBackupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_backup" not in self._stubs:
            self._stubs["update_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/UpdateBackup",
                request_serializer=gkebackup.UpdateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_backup"]

    @property
    def delete_backup(
        self,
    ) -> Callable[[gkebackup.DeleteBackupRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete backup method over gRPC.

        Deletes an existing Backup.

        Returns:
            Callable[[~.DeleteBackupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup" not in self._stubs:
            self._stubs["delete_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/DeleteBackup",
                request_serializer=gkebackup.DeleteBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup"]

    @property
    def list_volume_backups(
        self,
    ) -> Callable[
        [gkebackup.ListVolumeBackupsRequest],
        Awaitable[gkebackup.ListVolumeBackupsResponse],
    ]:
        r"""Return a callable for the list volume backups method over gRPC.

        Lists the VolumeBackups for a given Backup.

        Returns:
            Callable[[~.ListVolumeBackupsRequest],
                    Awaitable[~.ListVolumeBackupsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_volume_backups" not in self._stubs:
            self._stubs["list_volume_backups"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/ListVolumeBackups",
                request_serializer=gkebackup.ListVolumeBackupsRequest.serialize,
                response_deserializer=gkebackup.ListVolumeBackupsResponse.deserialize,
            )
        return self._stubs["list_volume_backups"]

    @property
    def get_volume_backup(
        self,
    ) -> Callable[[gkebackup.GetVolumeBackupRequest], Awaitable[volume.VolumeBackup]]:
        r"""Return a callable for the get volume backup method over gRPC.

        Retrieve the details of a single VolumeBackup.

        Returns:
            Callable[[~.GetVolumeBackupRequest],
                    Awaitable[~.VolumeBackup]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_volume_backup" not in self._stubs:
            self._stubs["get_volume_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/GetVolumeBackup",
                request_serializer=gkebackup.GetVolumeBackupRequest.serialize,
                response_deserializer=volume.VolumeBackup.deserialize,
            )
        return self._stubs["get_volume_backup"]

    @property
    def create_restore_plan(
        self,
    ) -> Callable[
        [gkebackup.CreateRestorePlanRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create restore plan method over gRPC.

        Creates a new RestorePlan in a given location.

        Returns:
            Callable[[~.CreateRestorePlanRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_restore_plan" not in self._stubs:
            self._stubs["create_restore_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/CreateRestorePlan",
                request_serializer=gkebackup.CreateRestorePlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_restore_plan"]

    @property
    def list_restore_plans(
        self,
    ) -> Callable[
        [gkebackup.ListRestorePlansRequest],
        Awaitable[gkebackup.ListRestorePlansResponse],
    ]:
        r"""Return a callable for the list restore plans method over gRPC.

        Lists RestorePlans in a given location.

        Returns:
            Callable[[~.ListRestorePlansRequest],
                    Awaitable[~.ListRestorePlansResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_restore_plans" not in self._stubs:
            self._stubs["list_restore_plans"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/ListRestorePlans",
                request_serializer=gkebackup.ListRestorePlansRequest.serialize,
                response_deserializer=gkebackup.ListRestorePlansResponse.deserialize,
            )
        return self._stubs["list_restore_plans"]

    @property
    def get_restore_plan(
        self,
    ) -> Callable[
        [gkebackup.GetRestorePlanRequest], Awaitable[restore_plan.RestorePlan]
    ]:
        r"""Return a callable for the get restore plan method over gRPC.

        Retrieve the details of a single RestorePlan.

        Returns:
            Callable[[~.GetRestorePlanRequest],
                    Awaitable[~.RestorePlan]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_restore_plan" not in self._stubs:
            self._stubs["get_restore_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/GetRestorePlan",
                request_serializer=gkebackup.GetRestorePlanRequest.serialize,
                response_deserializer=restore_plan.RestorePlan.deserialize,
            )
        return self._stubs["get_restore_plan"]

    @property
    def update_restore_plan(
        self,
    ) -> Callable[
        [gkebackup.UpdateRestorePlanRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update restore plan method over gRPC.

        Update a RestorePlan.

        Returns:
            Callable[[~.UpdateRestorePlanRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_restore_plan" not in self._stubs:
            self._stubs["update_restore_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/UpdateRestorePlan",
                request_serializer=gkebackup.UpdateRestorePlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_restore_plan"]

    @property
    def delete_restore_plan(
        self,
    ) -> Callable[
        [gkebackup.DeleteRestorePlanRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete restore plan method over gRPC.

        Deletes an existing RestorePlan.

        Returns:
            Callable[[~.DeleteRestorePlanRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_restore_plan" not in self._stubs:
            self._stubs["delete_restore_plan"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/DeleteRestorePlan",
                request_serializer=gkebackup.DeleteRestorePlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_restore_plan"]

    @property
    def create_restore(
        self,
    ) -> Callable[
        [gkebackup.CreateRestoreRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create restore method over gRPC.

        Creates a new Restore for the given RestorePlan.

        Returns:
            Callable[[~.CreateRestoreRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_restore" not in self._stubs:
            self._stubs["create_restore"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/CreateRestore",
                request_serializer=gkebackup.CreateRestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_restore"]

    @property
    def list_restores(
        self,
    ) -> Callable[
        [gkebackup.ListRestoresRequest], Awaitable[gkebackup.ListRestoresResponse]
    ]:
        r"""Return a callable for the list restores method over gRPC.

        Lists the Restores for a given RestorePlan.

        Returns:
            Callable[[~.ListRestoresRequest],
                    Awaitable[~.ListRestoresResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_restores" not in self._stubs:
            self._stubs["list_restores"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/ListRestores",
                request_serializer=gkebackup.ListRestoresRequest.serialize,
                response_deserializer=gkebackup.ListRestoresResponse.deserialize,
            )
        return self._stubs["list_restores"]

    @property
    def get_restore(
        self,
    ) -> Callable[[gkebackup.GetRestoreRequest], Awaitable[restore.Restore]]:
        r"""Return a callable for the get restore method over gRPC.

        Retrieves the details of a single Restore.

        Returns:
            Callable[[~.GetRestoreRequest],
                    Awaitable[~.Restore]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_restore" not in self._stubs:
            self._stubs["get_restore"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/GetRestore",
                request_serializer=gkebackup.GetRestoreRequest.serialize,
                response_deserializer=restore.Restore.deserialize,
            )
        return self._stubs["get_restore"]

    @property
    def update_restore(
        self,
    ) -> Callable[
        [gkebackup.UpdateRestoreRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update restore method over gRPC.

        Update a Restore.

        Returns:
            Callable[[~.UpdateRestoreRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_restore" not in self._stubs:
            self._stubs["update_restore"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/UpdateRestore",
                request_serializer=gkebackup.UpdateRestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_restore"]

    @property
    def delete_restore(
        self,
    ) -> Callable[
        [gkebackup.DeleteRestoreRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete restore method over gRPC.

        Deletes an existing Restore.

        Returns:
            Callable[[~.DeleteRestoreRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_restore" not in self._stubs:
            self._stubs["delete_restore"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/DeleteRestore",
                request_serializer=gkebackup.DeleteRestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_restore"]

    @property
    def list_volume_restores(
        self,
    ) -> Callable[
        [gkebackup.ListVolumeRestoresRequest],
        Awaitable[gkebackup.ListVolumeRestoresResponse],
    ]:
        r"""Return a callable for the list volume restores method over gRPC.

        Lists the VolumeRestores for a given Restore.

        Returns:
            Callable[[~.ListVolumeRestoresRequest],
                    Awaitable[~.ListVolumeRestoresResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_volume_restores" not in self._stubs:
            self._stubs["list_volume_restores"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/ListVolumeRestores",
                request_serializer=gkebackup.ListVolumeRestoresRequest.serialize,
                response_deserializer=gkebackup.ListVolumeRestoresResponse.deserialize,
            )
        return self._stubs["list_volume_restores"]

    @property
    def get_volume_restore(
        self,
    ) -> Callable[[gkebackup.GetVolumeRestoreRequest], Awaitable[volume.VolumeRestore]]:
        r"""Return a callable for the get volume restore method over gRPC.

        Retrieve the details of a single VolumeRestore.

        Returns:
            Callable[[~.GetVolumeRestoreRequest],
                    Awaitable[~.VolumeRestore]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_volume_restore" not in self._stubs:
            self._stubs["get_volume_restore"] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/GetVolumeRestore",
                request_serializer=gkebackup.GetVolumeRestoreRequest.serialize,
                response_deserializer=volume.VolumeRestore.deserialize,
            )
        return self._stubs["get_volume_restore"]

    @property
    def get_backup_index_download_url(
        self,
    ) -> Callable[
        [gkebackup.GetBackupIndexDownloadUrlRequest],
        Awaitable[gkebackup.GetBackupIndexDownloadUrlResponse],
    ]:
        r"""Return a callable for the get backup index download url method over gRPC.

        Retrieve the link to the backupIndex.

        Returns:
            Callable[[~.GetBackupIndexDownloadUrlRequest],
                    Awaitable[~.GetBackupIndexDownloadUrlResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup_index_download_url" not in self._stubs:
            self._stubs[
                "get_backup_index_download_url"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.gkebackup.v1.BackupForGKE/GetBackupIndexDownloadUrl",
                request_serializer=gkebackup.GetBackupIndexDownloadUrlRequest.serialize,
                response_deserializer=gkebackup.GetBackupIndexDownloadUrlResponse.deserialize,
            )
        return self._stubs["get_backup_index_download_url"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_backup_plan: self._wrap_method(
                self.create_backup_plan,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.list_backup_plans: self._wrap_method(
                self.list_backup_plans,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_backup_plan: self._wrap_method(
                self.get_backup_plan,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_backup_plan: self._wrap_method(
                self.update_backup_plan,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_backup_plan: self._wrap_method(
                self.delete_backup_plan,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_backup: self._wrap_method(
                self.create_backup,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_backups: self._wrap_method(
                self.list_backups,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_backup: self._wrap_method(
                self.get_backup,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_backup: self._wrap_method(
                self.update_backup,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_backup: self._wrap_method(
                self.delete_backup,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.list_volume_backups: self._wrap_method(
                self.list_volume_backups,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_volume_backup: self._wrap_method(
                self.get_volume_backup,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_restore_plan: self._wrap_method(
                self.create_restore_plan,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_restore_plans: self._wrap_method(
                self.list_restore_plans,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_restore_plan: self._wrap_method(
                self.get_restore_plan,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_restore_plan: self._wrap_method(
                self.update_restore_plan,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_restore_plan: self._wrap_method(
                self.delete_restore_plan,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_restore: self._wrap_method(
                self.create_restore,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_restores: self._wrap_method(
                self.list_restores,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_restore: self._wrap_method(
                self.get_restore,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_restore: self._wrap_method(
                self.update_restore,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_restore: self._wrap_method(
                self.delete_restore,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_volume_restores: self._wrap_method(
                self.list_volume_restores,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_volume_restore: self._wrap_method(
                self.get_volume_restore,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_backup_index_download_url: self._wrap_method(
                self.get_backup_index_download_url,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_location: self._wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: self._wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: self._wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: self._wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: self._wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_operation: self._wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_operation: self._wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operations: self._wrap_method(
                self.list_operations,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"

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


__all__ = ("BackupForGKEGrpcAsyncIOTransport",)
