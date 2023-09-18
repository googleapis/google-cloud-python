# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials   # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc                        # type: ignore
from grpc.experimental import aio  # type: ignore

from google.iam_v1beta.types import workload_identity_pool
from google.iam_v1beta.types import workload_identity_pool as gi_workload_identity_pool
from google.longrunning import operations_pb2 # type: ignore
from .base import WorkloadIdentityPoolsTransport, DEFAULT_CLIENT_INFO
from .grpc import WorkloadIdentityPoolsGrpcTransport


class WorkloadIdentityPoolsGrpcAsyncIOTransport(WorkloadIdentityPoolsTransport):
    """gRPC AsyncIO backend transport for WorkloadIdentityPools.

    Manages WorkloadIdentityPools.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(cls,
                       host: str = 'iam.googleapis.com',
                       credentials: Optional[ga_credentials.Credentials] = None,
                       credentials_file: Optional[str] = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> aio.Channel:
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

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs
        )

    def __init__(self, *,
            host: str = 'iam.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            channel: Optional[aio.Channel] = None,
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
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
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
            api_audience=api_audience,
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
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_workload_identity_pools(self) -> Callable[
            [workload_identity_pool.ListWorkloadIdentityPoolsRequest],
            Awaitable[workload_identity_pool.ListWorkloadIdentityPoolsResponse]]:
        r"""Return a callable for the list workload identity pools method over gRPC.

        Lists all non-deleted
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool]s
        in a project. If ``show_deleted`` is set to ``true``, then
        deleted pools are also listed.

        Returns:
            Callable[[~.ListWorkloadIdentityPoolsRequest],
                    Awaitable[~.ListWorkloadIdentityPoolsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_workload_identity_pools' not in self._stubs:
            self._stubs['list_workload_identity_pools'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/ListWorkloadIdentityPools',
                request_serializer=workload_identity_pool.ListWorkloadIdentityPoolsRequest.serialize,
                response_deserializer=workload_identity_pool.ListWorkloadIdentityPoolsResponse.deserialize,
            )
        return self._stubs['list_workload_identity_pools']

    @property
    def get_workload_identity_pool(self) -> Callable[
            [workload_identity_pool.GetWorkloadIdentityPoolRequest],
            Awaitable[workload_identity_pool.WorkloadIdentityPool]]:
        r"""Return a callable for the get workload identity pool method over gRPC.

        Gets an individual
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        Returns:
            Callable[[~.GetWorkloadIdentityPoolRequest],
                    Awaitable[~.WorkloadIdentityPool]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_workload_identity_pool' not in self._stubs:
            self._stubs['get_workload_identity_pool'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/GetWorkloadIdentityPool',
                request_serializer=workload_identity_pool.GetWorkloadIdentityPoolRequest.serialize,
                response_deserializer=workload_identity_pool.WorkloadIdentityPool.deserialize,
            )
        return self._stubs['get_workload_identity_pool']

    @property
    def create_workload_identity_pool(self) -> Callable[
            [gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create workload identity pool method over gRPC.

        Creates a new
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot reuse the name of a deleted pool until 30 days after
        deletion.

        Returns:
            Callable[[~.CreateWorkloadIdentityPoolRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_workload_identity_pool' not in self._stubs:
            self._stubs['create_workload_identity_pool'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/CreateWorkloadIdentityPool',
                request_serializer=gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_workload_identity_pool']

    @property
    def update_workload_identity_pool(self) -> Callable[
            [gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update workload identity pool method over gRPC.

        Updates an existing
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        Returns:
            Callable[[~.UpdateWorkloadIdentityPoolRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_workload_identity_pool' not in self._stubs:
            self._stubs['update_workload_identity_pool'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/UpdateWorkloadIdentityPool',
                request_serializer=gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_workload_identity_pool']

    @property
    def delete_workload_identity_pool(self) -> Callable[
            [workload_identity_pool.DeleteWorkloadIdentityPoolRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete workload identity pool method over gRPC.

        Deletes a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot use a deleted pool to exchange external credentials
        for Google Cloud credentials. However, deletion does not revoke
        credentials that have already been issued. Credentials issued
        for a deleted pool do not grant access to resources. If the pool
        is undeleted, and the credentials are not expired, they grant
        access again. You can undelete a pool for 30 days. After 30
        days, deletion is permanent. You cannot update deleted pools.
        However, you can view and list them.

        Returns:
            Callable[[~.DeleteWorkloadIdentityPoolRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_workload_identity_pool' not in self._stubs:
            self._stubs['delete_workload_identity_pool'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/DeleteWorkloadIdentityPool',
                request_serializer=workload_identity_pool.DeleteWorkloadIdentityPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_workload_identity_pool']

    @property
    def undelete_workload_identity_pool(self) -> Callable[
            [workload_identity_pool.UndeleteWorkloadIdentityPoolRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the undelete workload identity
        pool method over gRPC.

        Undeletes a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool],
        as long as it was deleted fewer than 30 days ago.

        Returns:
            Callable[[~.UndeleteWorkloadIdentityPoolRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'undelete_workload_identity_pool' not in self._stubs:
            self._stubs['undelete_workload_identity_pool'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/UndeleteWorkloadIdentityPool',
                request_serializer=workload_identity_pool.UndeleteWorkloadIdentityPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['undelete_workload_identity_pool']

    @property
    def list_workload_identity_pool_providers(self) -> Callable[
            [workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest],
            Awaitable[workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse]]:
        r"""Return a callable for the list workload identity pool
        providers method over gRPC.

        Lists all non-deleted
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityPoolProvider]s
        in a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].
        If ``show_deleted`` is set to ``true``, then deleted providers
        are also listed.

        Returns:
            Callable[[~.ListWorkloadIdentityPoolProvidersRequest],
                    Awaitable[~.ListWorkloadIdentityPoolProvidersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_workload_identity_pool_providers' not in self._stubs:
            self._stubs['list_workload_identity_pool_providers'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/ListWorkloadIdentityPoolProviders',
                request_serializer=workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest.serialize,
                response_deserializer=workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse.deserialize,
            )
        return self._stubs['list_workload_identity_pool_providers']

    @property
    def get_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.GetWorkloadIdentityPoolProviderRequest],
            Awaitable[workload_identity_pool.WorkloadIdentityPoolProvider]]:
        r"""Return a callable for the get workload identity pool
        provider method over gRPC.

        Gets an individual
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityPoolProvider].

        Returns:
            Callable[[~.GetWorkloadIdentityPoolProviderRequest],
                    Awaitable[~.WorkloadIdentityPoolProvider]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_workload_identity_pool_provider' not in self._stubs:
            self._stubs['get_workload_identity_pool_provider'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/GetWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.GetWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=workload_identity_pool.WorkloadIdentityPoolProvider.deserialize,
            )
        return self._stubs['get_workload_identity_pool_provider']

    @property
    def create_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create workload identity pool
        provider method over gRPC.

        Creates a new
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider]
        in a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot reuse the name of a deleted provider until 30 days
        after deletion.

        Returns:
            Callable[[~.CreateWorkloadIdentityPoolProviderRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_workload_identity_pool_provider' not in self._stubs:
            self._stubs['create_workload_identity_pool_provider'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/CreateWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_workload_identity_pool_provider']

    @property
    def update_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update workload identity pool
        provider method over gRPC.

        Updates an existing
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider].

        Returns:
            Callable[[~.UpdateWorkloadIdentityPoolProviderRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_workload_identity_pool_provider' not in self._stubs:
            self._stubs['update_workload_identity_pool_provider'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/UpdateWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_workload_identity_pool_provider']

    @property
    def delete_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete workload identity pool
        provider method over gRPC.

        Deletes a
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider].
        Deleting a provider does not revoke credentials that have
        already been issued; they continue to grant access. You can
        undelete a provider for 30 days. After 30 days, deletion is
        permanent. You cannot update deleted providers. However, you can
        view and list them.

        Returns:
            Callable[[~.DeleteWorkloadIdentityPoolProviderRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_workload_identity_pool_provider' not in self._stubs:
            self._stubs['delete_workload_identity_pool_provider'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/DeleteWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_workload_identity_pool_provider']

    @property
    def undelete_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the undelete workload identity
        pool provider method over gRPC.

        Undeletes a
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider],
        as long as it was deleted fewer than 30 days ago.

        Returns:
            Callable[[~.UndeleteWorkloadIdentityPoolProviderRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'undelete_workload_identity_pool_provider' not in self._stubs:
            self._stubs['undelete_workload_identity_pool_provider'] = self.grpc_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/UndeleteWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['undelete_workload_identity_pool_provider']

    def close(self):
        return self.grpc_channel.close()


__all__ = (
    'WorkloadIdentityPoolsGrpcAsyncIOTransport',
)
