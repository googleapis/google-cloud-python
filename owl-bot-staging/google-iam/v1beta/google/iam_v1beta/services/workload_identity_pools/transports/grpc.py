# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers
from google.api_core import operations_v1
from google.api_core import gapic_v1
import google.auth                         # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message

import grpc  # type: ignore
import proto  # type: ignore

from google.iam_v1beta.types import workload_identity_pool
from google.iam_v1beta.types import workload_identity_pool as gi_workload_identity_pool
from google.longrunning import operations_pb2 # type: ignore
from .base import WorkloadIdentityPoolsTransport, DEFAULT_CLIENT_INFO

try:
    from google.api_core import client_logging  # type: ignore
    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(std_logging.DEBUG)
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
                extra = {
                    "serviceName": "google.iam.v1beta.WorkloadIdentityPools",
                    "rpcName": client_call_details.method,
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )

        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = dict([(k, str(v)) for k, v in response_metadata]) if response_metadata else None
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
                extra = {
                    "serviceName": "google.iam.v1beta.WorkloadIdentityPools",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class WorkloadIdentityPoolsGrpcTransport(WorkloadIdentityPoolsTransport):
    """gRPC backend transport for WorkloadIdentityPools.

    Manages WorkloadIdentityPools.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    _stubs: Dict[str, Callable]

    def __init__(self, *,
            host: str = 'iam.googleapis.com',
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
                 The hostname to connect to (default: 'iam.googleapis.com').
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
        self._logged_channel =  grpc.intercept_channel(self._grpc_channel, self._interceptor)

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(cls,
                       host: str = 'iam.googleapis.com',
                       credentials: Optional[ga_credentials.Credentials] = None,
                       credentials_file: Optional[str] = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> grpc.Channel:
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
            **kwargs
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
            self._operations_client = operations_v1.OperationsClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_workload_identity_pools(self) -> Callable[
            [workload_identity_pool.ListWorkloadIdentityPoolsRequest],
            workload_identity_pool.ListWorkloadIdentityPoolsResponse]:
        r"""Return a callable for the list workload identity pools method over gRPC.

        Lists all non-deleted
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool]s
        in a project. If ``show_deleted`` is set to ``true``, then
        deleted pools are also listed.

        Returns:
            Callable[[~.ListWorkloadIdentityPoolsRequest],
                    ~.ListWorkloadIdentityPoolsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_workload_identity_pools' not in self._stubs:
            self._stubs['list_workload_identity_pools'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/ListWorkloadIdentityPools',
                request_serializer=workload_identity_pool.ListWorkloadIdentityPoolsRequest.serialize,
                response_deserializer=workload_identity_pool.ListWorkloadIdentityPoolsResponse.deserialize,
            )
        return self._stubs['list_workload_identity_pools']

    @property
    def get_workload_identity_pool(self) -> Callable[
            [workload_identity_pool.GetWorkloadIdentityPoolRequest],
            workload_identity_pool.WorkloadIdentityPool]:
        r"""Return a callable for the get workload identity pool method over gRPC.

        Gets an individual
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        Returns:
            Callable[[~.GetWorkloadIdentityPoolRequest],
                    ~.WorkloadIdentityPool]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_workload_identity_pool' not in self._stubs:
            self._stubs['get_workload_identity_pool'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/GetWorkloadIdentityPool',
                request_serializer=workload_identity_pool.GetWorkloadIdentityPoolRequest.serialize,
                response_deserializer=workload_identity_pool.WorkloadIdentityPool.deserialize,
            )
        return self._stubs['get_workload_identity_pool']

    @property
    def create_workload_identity_pool(self) -> Callable[
            [gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the create workload identity pool method over gRPC.

        Creates a new
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot reuse the name of a deleted pool until 30 days after
        deletion.

        Returns:
            Callable[[~.CreateWorkloadIdentityPoolRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_workload_identity_pool' not in self._stubs:
            self._stubs['create_workload_identity_pool'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/CreateWorkloadIdentityPool',
                request_serializer=gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_workload_identity_pool']

    @property
    def update_workload_identity_pool(self) -> Callable[
            [gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update workload identity pool method over gRPC.

        Updates an existing
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        Returns:
            Callable[[~.UpdateWorkloadIdentityPoolRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_workload_identity_pool' not in self._stubs:
            self._stubs['update_workload_identity_pool'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/UpdateWorkloadIdentityPool',
                request_serializer=gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_workload_identity_pool']

    @property
    def delete_workload_identity_pool(self) -> Callable[
            [workload_identity_pool.DeleteWorkloadIdentityPoolRequest],
            operations_pb2.Operation]:
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
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_workload_identity_pool' not in self._stubs:
            self._stubs['delete_workload_identity_pool'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/DeleteWorkloadIdentityPool',
                request_serializer=workload_identity_pool.DeleteWorkloadIdentityPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_workload_identity_pool']

    @property
    def undelete_workload_identity_pool(self) -> Callable[
            [workload_identity_pool.UndeleteWorkloadIdentityPoolRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the undelete workload identity
        pool method over gRPC.

        Undeletes a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool],
        as long as it was deleted fewer than 30 days ago.

        Returns:
            Callable[[~.UndeleteWorkloadIdentityPoolRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'undelete_workload_identity_pool' not in self._stubs:
            self._stubs['undelete_workload_identity_pool'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/UndeleteWorkloadIdentityPool',
                request_serializer=workload_identity_pool.UndeleteWorkloadIdentityPoolRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['undelete_workload_identity_pool']

    @property
    def list_workload_identity_pool_providers(self) -> Callable[
            [workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest],
            workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse]:
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
                    ~.ListWorkloadIdentityPoolProvidersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_workload_identity_pool_providers' not in self._stubs:
            self._stubs['list_workload_identity_pool_providers'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/ListWorkloadIdentityPoolProviders',
                request_serializer=workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest.serialize,
                response_deserializer=workload_identity_pool.ListWorkloadIdentityPoolProvidersResponse.deserialize,
            )
        return self._stubs['list_workload_identity_pool_providers']

    @property
    def get_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.GetWorkloadIdentityPoolProviderRequest],
            workload_identity_pool.WorkloadIdentityPoolProvider]:
        r"""Return a callable for the get workload identity pool
        provider method over gRPC.

        Gets an individual
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityPoolProvider].

        Returns:
            Callable[[~.GetWorkloadIdentityPoolProviderRequest],
                    ~.WorkloadIdentityPoolProvider]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_workload_identity_pool_provider' not in self._stubs:
            self._stubs['get_workload_identity_pool_provider'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/GetWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.GetWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=workload_identity_pool.WorkloadIdentityPoolProvider.deserialize,
            )
        return self._stubs['get_workload_identity_pool_provider']

    @property
    def create_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest],
            operations_pb2.Operation]:
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
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_workload_identity_pool_provider' not in self._stubs:
            self._stubs['create_workload_identity_pool_provider'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/CreateWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_workload_identity_pool_provider']

    @property
    def update_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update workload identity pool
        provider method over gRPC.

        Updates an existing
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider].

        Returns:
            Callable[[~.UpdateWorkloadIdentityPoolProviderRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_workload_identity_pool_provider' not in self._stubs:
            self._stubs['update_workload_identity_pool_provider'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/UpdateWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_workload_identity_pool_provider']

    @property
    def delete_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest],
            operations_pb2.Operation]:
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
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_workload_identity_pool_provider' not in self._stubs:
            self._stubs['delete_workload_identity_pool_provider'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/DeleteWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_workload_identity_pool_provider']

    @property
    def undelete_workload_identity_pool_provider(self) -> Callable[
            [workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the undelete workload identity
        pool provider method over gRPC.

        Undeletes a
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider],
        as long as it was deleted fewer than 30 days ago.

        Returns:
            Callable[[~.UndeleteWorkloadIdentityPoolProviderRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'undelete_workload_identity_pool_provider' not in self._stubs:
            self._stubs['undelete_workload_identity_pool_provider'] = self._logged_channel.unary_unary(
                '/google.iam.v1beta.WorkloadIdentityPools/UndeleteWorkloadIdentityPoolProvider',
                request_serializer=workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['undelete_workload_identity_pool_provider']

    def close(self):
        self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = (
    'WorkloadIdentityPoolsGrpcTransport',
)
