# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.api_core import grpc_helpers
from google.api_core import operations_v1
from google.api_core import gapic_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.storage_transfer_v1.types import transfer
from google.cloud.storage_transfer_v1.types import transfer_types
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from .base import StorageTransferServiceTransport, DEFAULT_CLIENT_INFO


class StorageTransferServiceGrpcTransport(StorageTransferServiceTransport):
    """gRPC backend transport for StorageTransferService.

    Storage Transfer Service and its protos.
    Transfers data between between Google Cloud Storage buckets or
    from a data source external to Google to a Cloud Storage bucket.

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
        host: str = "storagetransfer.googleapis.com",
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
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
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
        self._operations_client: Optional[operations_v1.OperationsClient] = None

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

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "storagetransfer.googleapis.com",
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
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def get_google_service_account(
        self,
    ) -> Callable[
        [transfer.GetGoogleServiceAccountRequest], transfer_types.GoogleServiceAccount
    ]:
        r"""Return a callable for the get google service account method over gRPC.

        Returns the Google service account that is used by
        Storage Transfer Service to access buckets in the
        project where transfers run or in other projects. Each
        Google service account is associated with one Google
        Cloud Platform Console project. Users should add this
        service account to the Google Cloud Storage bucket ACLs
        to grant access to Storage Transfer Service. This
        service account is created and owned by Storage Transfer
        Service and can only be used by Storage Transfer
        Service.

        Returns:
            Callable[[~.GetGoogleServiceAccountRequest],
                    ~.GoogleServiceAccount]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_google_service_account" not in self._stubs:
            self._stubs["get_google_service_account"] = self.grpc_channel.unary_unary(
                "/google.storagetransfer.v1.StorageTransferService/GetGoogleServiceAccount",
                request_serializer=transfer.GetGoogleServiceAccountRequest.serialize,
                response_deserializer=transfer_types.GoogleServiceAccount.deserialize,
            )
        return self._stubs["get_google_service_account"]

    @property
    def create_transfer_job(
        self,
    ) -> Callable[[transfer.CreateTransferJobRequest], transfer_types.TransferJob]:
        r"""Return a callable for the create transfer job method over gRPC.

        Creates a transfer job that runs periodically.

        Returns:
            Callable[[~.CreateTransferJobRequest],
                    ~.TransferJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_transfer_job" not in self._stubs:
            self._stubs["create_transfer_job"] = self.grpc_channel.unary_unary(
                "/google.storagetransfer.v1.StorageTransferService/CreateTransferJob",
                request_serializer=transfer.CreateTransferJobRequest.serialize,
                response_deserializer=transfer_types.TransferJob.deserialize,
            )
        return self._stubs["create_transfer_job"]

    @property
    def update_transfer_job(
        self,
    ) -> Callable[[transfer.UpdateTransferJobRequest], transfer_types.TransferJob]:
        r"""Return a callable for the update transfer job method over gRPC.

        Updates a transfer job. Updating a job's transfer spec does not
        affect transfer operations that are running already.

        **Note:** The job's
        [status][google.storagetransfer.v1.TransferJob.status] field can
        be modified using this RPC (for example, to set a job's status
        to
        [DELETED][google.storagetransfer.v1.TransferJob.Status.DELETED],
        [DISABLED][google.storagetransfer.v1.TransferJob.Status.DISABLED],
        or
        [ENABLED][google.storagetransfer.v1.TransferJob.Status.ENABLED]).

        Returns:
            Callable[[~.UpdateTransferJobRequest],
                    ~.TransferJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_transfer_job" not in self._stubs:
            self._stubs["update_transfer_job"] = self.grpc_channel.unary_unary(
                "/google.storagetransfer.v1.StorageTransferService/UpdateTransferJob",
                request_serializer=transfer.UpdateTransferJobRequest.serialize,
                response_deserializer=transfer_types.TransferJob.deserialize,
            )
        return self._stubs["update_transfer_job"]

    @property
    def get_transfer_job(
        self,
    ) -> Callable[[transfer.GetTransferJobRequest], transfer_types.TransferJob]:
        r"""Return a callable for the get transfer job method over gRPC.

        Gets a transfer job.

        Returns:
            Callable[[~.GetTransferJobRequest],
                    ~.TransferJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_transfer_job" not in self._stubs:
            self._stubs["get_transfer_job"] = self.grpc_channel.unary_unary(
                "/google.storagetransfer.v1.StorageTransferService/GetTransferJob",
                request_serializer=transfer.GetTransferJobRequest.serialize,
                response_deserializer=transfer_types.TransferJob.deserialize,
            )
        return self._stubs["get_transfer_job"]

    @property
    def list_transfer_jobs(
        self,
    ) -> Callable[
        [transfer.ListTransferJobsRequest], transfer.ListTransferJobsResponse
    ]:
        r"""Return a callable for the list transfer jobs method over gRPC.

        Lists transfer jobs.

        Returns:
            Callable[[~.ListTransferJobsRequest],
                    ~.ListTransferJobsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_transfer_jobs" not in self._stubs:
            self._stubs["list_transfer_jobs"] = self.grpc_channel.unary_unary(
                "/google.storagetransfer.v1.StorageTransferService/ListTransferJobs",
                request_serializer=transfer.ListTransferJobsRequest.serialize,
                response_deserializer=transfer.ListTransferJobsResponse.deserialize,
            )
        return self._stubs["list_transfer_jobs"]

    @property
    def pause_transfer_operation(
        self,
    ) -> Callable[[transfer.PauseTransferOperationRequest], empty_pb2.Empty]:
        r"""Return a callable for the pause transfer operation method over gRPC.

        Pauses a transfer operation.

        Returns:
            Callable[[~.PauseTransferOperationRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "pause_transfer_operation" not in self._stubs:
            self._stubs["pause_transfer_operation"] = self.grpc_channel.unary_unary(
                "/google.storagetransfer.v1.StorageTransferService/PauseTransferOperation",
                request_serializer=transfer.PauseTransferOperationRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["pause_transfer_operation"]

    @property
    def resume_transfer_operation(
        self,
    ) -> Callable[[transfer.ResumeTransferOperationRequest], empty_pb2.Empty]:
        r"""Return a callable for the resume transfer operation method over gRPC.

        Resumes a transfer operation that is paused.

        Returns:
            Callable[[~.ResumeTransferOperationRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "resume_transfer_operation" not in self._stubs:
            self._stubs["resume_transfer_operation"] = self.grpc_channel.unary_unary(
                "/google.storagetransfer.v1.StorageTransferService/ResumeTransferOperation",
                request_serializer=transfer.ResumeTransferOperationRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["resume_transfer_operation"]

    @property
    def run_transfer_job(
        self,
    ) -> Callable[[transfer.RunTransferJobRequest], operations_pb2.Operation]:
        r"""Return a callable for the run transfer job method over gRPC.

        Attempts to start a new TransferOperation for the
        current TransferJob. A TransferJob has a maximum of one
        active TransferOperation. If this method is called while
        a TransferOperation is active, an error wil be returned.

        Returns:
            Callable[[~.RunTransferJobRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_transfer_job" not in self._stubs:
            self._stubs["run_transfer_job"] = self.grpc_channel.unary_unary(
                "/google.storagetransfer.v1.StorageTransferService/RunTransferJob",
                request_serializer=transfer.RunTransferJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["run_transfer_job"]

    def close(self):
        self.grpc_channel.close()


__all__ = ("StorageTransferServiceGrpcTransport",)
