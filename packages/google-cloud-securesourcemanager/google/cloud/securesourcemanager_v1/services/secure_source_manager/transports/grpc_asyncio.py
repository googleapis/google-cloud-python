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

from google.cloud.securesourcemanager_v1.types import secure_source_manager

from .base import DEFAULT_CLIENT_INFO, SecureSourceManagerTransport
from .grpc import SecureSourceManagerGrpcTransport

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
                    "serviceName": "google.cloud.securesourcemanager.v1.SecureSourceManager",
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
                    "serviceName": "google.cloud.securesourcemanager.v1.SecureSourceManager",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class SecureSourceManagerGrpcAsyncIOTransport(SecureSourceManagerTransport):
    """gRPC AsyncIO backend transport for SecureSourceManager.

    Secure Source Manager API

    Access Secure Source Manager instances, resources, and
    repositories.

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
        host: str = "securesourcemanager.googleapis.com",
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
        host: str = "securesourcemanager.googleapis.com",
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
                 The hostname to connect to (default: 'securesourcemanager.googleapis.com').
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
    def list_instances(
        self,
    ) -> Callable[
        [secure_source_manager.ListInstancesRequest],
        Awaitable[secure_source_manager.ListInstancesResponse],
    ]:
        r"""Return a callable for the list instances method over gRPC.

        Lists Instances in a given project and location.

        Returns:
            Callable[[~.ListInstancesRequest],
                    Awaitable[~.ListInstancesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_instances" not in self._stubs:
            self._stubs["list_instances"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListInstances",
                request_serializer=secure_source_manager.ListInstancesRequest.serialize,
                response_deserializer=secure_source_manager.ListInstancesResponse.deserialize,
            )
        return self._stubs["list_instances"]

    @property
    def get_instance(
        self,
    ) -> Callable[
        [secure_source_manager.GetInstanceRequest],
        Awaitable[secure_source_manager.Instance],
    ]:
        r"""Return a callable for the get instance method over gRPC.

        Gets details of a single instance.

        Returns:
            Callable[[~.GetInstanceRequest],
                    Awaitable[~.Instance]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_instance" not in self._stubs:
            self._stubs["get_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetInstance",
                request_serializer=secure_source_manager.GetInstanceRequest.serialize,
                response_deserializer=secure_source_manager.Instance.deserialize,
            )
        return self._stubs["get_instance"]

    @property
    def create_instance(
        self,
    ) -> Callable[
        [secure_source_manager.CreateInstanceRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create instance method over gRPC.

        Creates a new instance in a given project and
        location.

        Returns:
            Callable[[~.CreateInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_instance" not in self._stubs:
            self._stubs["create_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CreateInstance",
                request_serializer=secure_source_manager.CreateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_instance"]

    @property
    def delete_instance(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteInstanceRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete instance method over gRPC.

        Deletes a single instance.

        Returns:
            Callable[[~.DeleteInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_instance" not in self._stubs:
            self._stubs["delete_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/DeleteInstance",
                request_serializer=secure_source_manager.DeleteInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_instance"]

    @property
    def list_repositories(
        self,
    ) -> Callable[
        [secure_source_manager.ListRepositoriesRequest],
        Awaitable[secure_source_manager.ListRepositoriesResponse],
    ]:
        r"""Return a callable for the list repositories method over gRPC.

        Lists Repositories in a given project and location.

        The instance field is required in the query parameter
        for requests using the
        securesourcemanager.googleapis.com endpoint.

        Returns:
            Callable[[~.ListRepositoriesRequest],
                    Awaitable[~.ListRepositoriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_repositories" not in self._stubs:
            self._stubs["list_repositories"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListRepositories",
                request_serializer=secure_source_manager.ListRepositoriesRequest.serialize,
                response_deserializer=secure_source_manager.ListRepositoriesResponse.deserialize,
            )
        return self._stubs["list_repositories"]

    @property
    def get_repository(
        self,
    ) -> Callable[
        [secure_source_manager.GetRepositoryRequest],
        Awaitable[secure_source_manager.Repository],
    ]:
        r"""Return a callable for the get repository method over gRPC.

        Gets metadata of a repository.

        Returns:
            Callable[[~.GetRepositoryRequest],
                    Awaitable[~.Repository]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_repository" not in self._stubs:
            self._stubs["get_repository"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetRepository",
                request_serializer=secure_source_manager.GetRepositoryRequest.serialize,
                response_deserializer=secure_source_manager.Repository.deserialize,
            )
        return self._stubs["get_repository"]

    @property
    def create_repository(
        self,
    ) -> Callable[
        [secure_source_manager.CreateRepositoryRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create repository method over gRPC.

        Creates a new repository in a given project and
        location.
        The Repository.Instance field is required in the request
        body for requests using the
        securesourcemanager.googleapis.com endpoint.

        Returns:
            Callable[[~.CreateRepositoryRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_repository" not in self._stubs:
            self._stubs["create_repository"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CreateRepository",
                request_serializer=secure_source_manager.CreateRepositoryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_repository"]

    @property
    def update_repository(
        self,
    ) -> Callable[
        [secure_source_manager.UpdateRepositoryRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update repository method over gRPC.

        Updates the metadata of a repository.

        Returns:
            Callable[[~.UpdateRepositoryRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_repository" not in self._stubs:
            self._stubs["update_repository"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/UpdateRepository",
                request_serializer=secure_source_manager.UpdateRepositoryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_repository"]

    @property
    def delete_repository(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteRepositoryRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete repository method over gRPC.

        Deletes a Repository.

        Returns:
            Callable[[~.DeleteRepositoryRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_repository" not in self._stubs:
            self._stubs["delete_repository"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/DeleteRepository",
                request_serializer=secure_source_manager.DeleteRepositoryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_repository"]

    @property
    def list_hooks(
        self,
    ) -> Callable[
        [secure_source_manager.ListHooksRequest],
        Awaitable[secure_source_manager.ListHooksResponse],
    ]:
        r"""Return a callable for the list hooks method over gRPC.

        Lists hooks in a given repository.

        Returns:
            Callable[[~.ListHooksRequest],
                    Awaitable[~.ListHooksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_hooks" not in self._stubs:
            self._stubs["list_hooks"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListHooks",
                request_serializer=secure_source_manager.ListHooksRequest.serialize,
                response_deserializer=secure_source_manager.ListHooksResponse.deserialize,
            )
        return self._stubs["list_hooks"]

    @property
    def get_hook(
        self,
    ) -> Callable[
        [secure_source_manager.GetHookRequest], Awaitable[secure_source_manager.Hook]
    ]:
        r"""Return a callable for the get hook method over gRPC.

        Gets metadata of a hook.

        Returns:
            Callable[[~.GetHookRequest],
                    Awaitable[~.Hook]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_hook" not in self._stubs:
            self._stubs["get_hook"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetHook",
                request_serializer=secure_source_manager.GetHookRequest.serialize,
                response_deserializer=secure_source_manager.Hook.deserialize,
            )
        return self._stubs["get_hook"]

    @property
    def create_hook(
        self,
    ) -> Callable[
        [secure_source_manager.CreateHookRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create hook method over gRPC.

        Creates a new hook in a given repository.

        Returns:
            Callable[[~.CreateHookRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_hook" not in self._stubs:
            self._stubs["create_hook"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CreateHook",
                request_serializer=secure_source_manager.CreateHookRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_hook"]

    @property
    def update_hook(
        self,
    ) -> Callable[
        [secure_source_manager.UpdateHookRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update hook method over gRPC.

        Updates the metadata of a hook.

        Returns:
            Callable[[~.UpdateHookRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_hook" not in self._stubs:
            self._stubs["update_hook"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/UpdateHook",
                request_serializer=secure_source_manager.UpdateHookRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_hook"]

    @property
    def delete_hook(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteHookRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete hook method over gRPC.

        Deletes a Hook.

        Returns:
            Callable[[~.DeleteHookRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_hook" not in self._stubs:
            self._stubs["delete_hook"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/DeleteHook",
                request_serializer=secure_source_manager.DeleteHookRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_hook"]

    @property
    def get_iam_policy_repo(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the get iam policy repo method over gRPC.

        Get IAM policy for a repository.

        Returns:
            Callable[[~.GetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy_repo" not in self._stubs:
            self._stubs["get_iam_policy_repo"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetIamPolicyRepo",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy_repo"]

    @property
    def set_iam_policy_repo(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the set iam policy repo method over gRPC.

        Set IAM policy on a repository.

        Returns:
            Callable[[~.SetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy_repo" not in self._stubs:
            self._stubs["set_iam_policy_repo"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/SetIamPolicyRepo",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy_repo"]

    @property
    def test_iam_permissions_repo(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
    ]:
        r"""Return a callable for the test iam permissions repo method over gRPC.

        Test IAM permissions on a repository.
        IAM permission checks are not required on this method.

        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    Awaitable[~.TestIamPermissionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions_repo" not in self._stubs:
            self._stubs["test_iam_permissions_repo"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/TestIamPermissionsRepo",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions_repo"]

    @property
    def create_branch_rule(
        self,
    ) -> Callable[
        [secure_source_manager.CreateBranchRuleRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create branch rule method over gRPC.

        CreateBranchRule creates a branch rule in a given
        repository.

        Returns:
            Callable[[~.CreateBranchRuleRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_branch_rule" not in self._stubs:
            self._stubs["create_branch_rule"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CreateBranchRule",
                request_serializer=secure_source_manager.CreateBranchRuleRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_branch_rule"]

    @property
    def list_branch_rules(
        self,
    ) -> Callable[
        [secure_source_manager.ListBranchRulesRequest],
        Awaitable[secure_source_manager.ListBranchRulesResponse],
    ]:
        r"""Return a callable for the list branch rules method over gRPC.

        ListBranchRules lists branch rules in a given
        repository.

        Returns:
            Callable[[~.ListBranchRulesRequest],
                    Awaitable[~.ListBranchRulesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_branch_rules" not in self._stubs:
            self._stubs["list_branch_rules"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListBranchRules",
                request_serializer=secure_source_manager.ListBranchRulesRequest.serialize,
                response_deserializer=secure_source_manager.ListBranchRulesResponse.deserialize,
            )
        return self._stubs["list_branch_rules"]

    @property
    def get_branch_rule(
        self,
    ) -> Callable[
        [secure_source_manager.GetBranchRuleRequest],
        Awaitable[secure_source_manager.BranchRule],
    ]:
        r"""Return a callable for the get branch rule method over gRPC.

        GetBranchRule gets a branch rule.

        Returns:
            Callable[[~.GetBranchRuleRequest],
                    Awaitable[~.BranchRule]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_branch_rule" not in self._stubs:
            self._stubs["get_branch_rule"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetBranchRule",
                request_serializer=secure_source_manager.GetBranchRuleRequest.serialize,
                response_deserializer=secure_source_manager.BranchRule.deserialize,
            )
        return self._stubs["get_branch_rule"]

    @property
    def update_branch_rule(
        self,
    ) -> Callable[
        [secure_source_manager.UpdateBranchRuleRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update branch rule method over gRPC.

        UpdateBranchRule updates a branch rule.

        Returns:
            Callable[[~.UpdateBranchRuleRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_branch_rule" not in self._stubs:
            self._stubs["update_branch_rule"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/UpdateBranchRule",
                request_serializer=secure_source_manager.UpdateBranchRuleRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_branch_rule"]

    @property
    def delete_branch_rule(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteBranchRuleRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete branch rule method over gRPC.

        DeleteBranchRule deletes a branch rule.

        Returns:
            Callable[[~.DeleteBranchRuleRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_branch_rule" not in self._stubs:
            self._stubs["delete_branch_rule"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/DeleteBranchRule",
                request_serializer=secure_source_manager.DeleteBranchRuleRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_branch_rule"]

    @property
    def create_pull_request(
        self,
    ) -> Callable[
        [secure_source_manager.CreatePullRequestRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create pull request method over gRPC.

        Creates a pull request.

        Returns:
            Callable[[~.CreatePullRequestRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_pull_request" not in self._stubs:
            self._stubs["create_pull_request"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CreatePullRequest",
                request_serializer=secure_source_manager.CreatePullRequestRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_pull_request"]

    @property
    def get_pull_request(
        self,
    ) -> Callable[
        [secure_source_manager.GetPullRequestRequest],
        Awaitable[secure_source_manager.PullRequest],
    ]:
        r"""Return a callable for the get pull request method over gRPC.

        Gets a pull request.

        Returns:
            Callable[[~.GetPullRequestRequest],
                    Awaitable[~.PullRequest]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_pull_request" not in self._stubs:
            self._stubs["get_pull_request"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetPullRequest",
                request_serializer=secure_source_manager.GetPullRequestRequest.serialize,
                response_deserializer=secure_source_manager.PullRequest.deserialize,
            )
        return self._stubs["get_pull_request"]

    @property
    def list_pull_requests(
        self,
    ) -> Callable[
        [secure_source_manager.ListPullRequestsRequest],
        Awaitable[secure_source_manager.ListPullRequestsResponse],
    ]:
        r"""Return a callable for the list pull requests method over gRPC.

        Lists pull requests in a repository.

        Returns:
            Callable[[~.ListPullRequestsRequest],
                    Awaitable[~.ListPullRequestsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_pull_requests" not in self._stubs:
            self._stubs["list_pull_requests"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListPullRequests",
                request_serializer=secure_source_manager.ListPullRequestsRequest.serialize,
                response_deserializer=secure_source_manager.ListPullRequestsResponse.deserialize,
            )
        return self._stubs["list_pull_requests"]

    @property
    def update_pull_request(
        self,
    ) -> Callable[
        [secure_source_manager.UpdatePullRequestRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update pull request method over gRPC.

        Updates a pull request.

        Returns:
            Callable[[~.UpdatePullRequestRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_pull_request" not in self._stubs:
            self._stubs["update_pull_request"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/UpdatePullRequest",
                request_serializer=secure_source_manager.UpdatePullRequestRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_pull_request"]

    @property
    def merge_pull_request(
        self,
    ) -> Callable[
        [secure_source_manager.MergePullRequestRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the merge pull request method over gRPC.

        Merges a pull request.

        Returns:
            Callable[[~.MergePullRequestRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "merge_pull_request" not in self._stubs:
            self._stubs["merge_pull_request"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/MergePullRequest",
                request_serializer=secure_source_manager.MergePullRequestRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["merge_pull_request"]

    @property
    def open_pull_request(
        self,
    ) -> Callable[
        [secure_source_manager.OpenPullRequestRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the open pull request method over gRPC.

        Opens a pull request.

        Returns:
            Callable[[~.OpenPullRequestRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "open_pull_request" not in self._stubs:
            self._stubs["open_pull_request"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/OpenPullRequest",
                request_serializer=secure_source_manager.OpenPullRequestRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["open_pull_request"]

    @property
    def close_pull_request(
        self,
    ) -> Callable[
        [secure_source_manager.ClosePullRequestRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the close pull request method over gRPC.

        Closes a pull request without merging.

        Returns:
            Callable[[~.ClosePullRequestRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "close_pull_request" not in self._stubs:
            self._stubs["close_pull_request"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ClosePullRequest",
                request_serializer=secure_source_manager.ClosePullRequestRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["close_pull_request"]

    @property
    def list_pull_request_file_diffs(
        self,
    ) -> Callable[
        [secure_source_manager.ListPullRequestFileDiffsRequest],
        Awaitable[secure_source_manager.ListPullRequestFileDiffsResponse],
    ]:
        r"""Return a callable for the list pull request file diffs method over gRPC.

        Lists a pull request's file diffs.

        Returns:
            Callable[[~.ListPullRequestFileDiffsRequest],
                    Awaitable[~.ListPullRequestFileDiffsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_pull_request_file_diffs" not in self._stubs:
            self._stubs[
                "list_pull_request_file_diffs"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListPullRequestFileDiffs",
                request_serializer=secure_source_manager.ListPullRequestFileDiffsRequest.serialize,
                response_deserializer=secure_source_manager.ListPullRequestFileDiffsResponse.deserialize,
            )
        return self._stubs["list_pull_request_file_diffs"]

    @property
    def fetch_tree(
        self,
    ) -> Callable[
        [secure_source_manager.FetchTreeRequest],
        Awaitable[secure_source_manager.FetchTreeResponse],
    ]:
        r"""Return a callable for the fetch tree method over gRPC.

        Fetches a tree from a repository.

        Returns:
            Callable[[~.FetchTreeRequest],
                    Awaitable[~.FetchTreeResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_tree" not in self._stubs:
            self._stubs["fetch_tree"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/FetchTree",
                request_serializer=secure_source_manager.FetchTreeRequest.serialize,
                response_deserializer=secure_source_manager.FetchTreeResponse.deserialize,
            )
        return self._stubs["fetch_tree"]

    @property
    def fetch_blob(
        self,
    ) -> Callable[
        [secure_source_manager.FetchBlobRequest],
        Awaitable[secure_source_manager.FetchBlobResponse],
    ]:
        r"""Return a callable for the fetch blob method over gRPC.

        Fetches a blob from a repository.

        Returns:
            Callable[[~.FetchBlobRequest],
                    Awaitable[~.FetchBlobResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_blob" not in self._stubs:
            self._stubs["fetch_blob"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/FetchBlob",
                request_serializer=secure_source_manager.FetchBlobRequest.serialize,
                response_deserializer=secure_source_manager.FetchBlobResponse.deserialize,
            )
        return self._stubs["fetch_blob"]

    @property
    def create_issue(
        self,
    ) -> Callable[
        [secure_source_manager.CreateIssueRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create issue method over gRPC.

        Creates an issue.

        Returns:
            Callable[[~.CreateIssueRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_issue" not in self._stubs:
            self._stubs["create_issue"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CreateIssue",
                request_serializer=secure_source_manager.CreateIssueRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_issue"]

    @property
    def get_issue(
        self,
    ) -> Callable[
        [secure_source_manager.GetIssueRequest], Awaitable[secure_source_manager.Issue]
    ]:
        r"""Return a callable for the get issue method over gRPC.

        Gets an issue.

        Returns:
            Callable[[~.GetIssueRequest],
                    Awaitable[~.Issue]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_issue" not in self._stubs:
            self._stubs["get_issue"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetIssue",
                request_serializer=secure_source_manager.GetIssueRequest.serialize,
                response_deserializer=secure_source_manager.Issue.deserialize,
            )
        return self._stubs["get_issue"]

    @property
    def list_issues(
        self,
    ) -> Callable[
        [secure_source_manager.ListIssuesRequest],
        Awaitable[secure_source_manager.ListIssuesResponse],
    ]:
        r"""Return a callable for the list issues method over gRPC.

        Lists issues in a repository.

        Returns:
            Callable[[~.ListIssuesRequest],
                    Awaitable[~.ListIssuesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_issues" not in self._stubs:
            self._stubs["list_issues"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListIssues",
                request_serializer=secure_source_manager.ListIssuesRequest.serialize,
                response_deserializer=secure_source_manager.ListIssuesResponse.deserialize,
            )
        return self._stubs["list_issues"]

    @property
    def update_issue(
        self,
    ) -> Callable[
        [secure_source_manager.UpdateIssueRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update issue method over gRPC.

        Updates a issue.

        Returns:
            Callable[[~.UpdateIssueRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_issue" not in self._stubs:
            self._stubs["update_issue"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/UpdateIssue",
                request_serializer=secure_source_manager.UpdateIssueRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_issue"]

    @property
    def delete_issue(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteIssueRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete issue method over gRPC.

        Deletes an issue.

        Returns:
            Callable[[~.DeleteIssueRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_issue" not in self._stubs:
            self._stubs["delete_issue"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/DeleteIssue",
                request_serializer=secure_source_manager.DeleteIssueRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_issue"]

    @property
    def open_issue(
        self,
    ) -> Callable[
        [secure_source_manager.OpenIssueRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the open issue method over gRPC.

        Opens an issue.

        Returns:
            Callable[[~.OpenIssueRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "open_issue" not in self._stubs:
            self._stubs["open_issue"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/OpenIssue",
                request_serializer=secure_source_manager.OpenIssueRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["open_issue"]

    @property
    def close_issue(
        self,
    ) -> Callable[
        [secure_source_manager.CloseIssueRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the close issue method over gRPC.

        Closes an issue.

        Returns:
            Callable[[~.CloseIssueRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "close_issue" not in self._stubs:
            self._stubs["close_issue"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CloseIssue",
                request_serializer=secure_source_manager.CloseIssueRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["close_issue"]

    @property
    def get_pull_request_comment(
        self,
    ) -> Callable[
        [secure_source_manager.GetPullRequestCommentRequest],
        Awaitable[secure_source_manager.PullRequestComment],
    ]:
        r"""Return a callable for the get pull request comment method over gRPC.

        Gets a pull request comment.

        Returns:
            Callable[[~.GetPullRequestCommentRequest],
                    Awaitable[~.PullRequestComment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_pull_request_comment" not in self._stubs:
            self._stubs["get_pull_request_comment"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetPullRequestComment",
                request_serializer=secure_source_manager.GetPullRequestCommentRequest.serialize,
                response_deserializer=secure_source_manager.PullRequestComment.deserialize,
            )
        return self._stubs["get_pull_request_comment"]

    @property
    def list_pull_request_comments(
        self,
    ) -> Callable[
        [secure_source_manager.ListPullRequestCommentsRequest],
        Awaitable[secure_source_manager.ListPullRequestCommentsResponse],
    ]:
        r"""Return a callable for the list pull request comments method over gRPC.

        Lists pull request comments.

        Returns:
            Callable[[~.ListPullRequestCommentsRequest],
                    Awaitable[~.ListPullRequestCommentsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_pull_request_comments" not in self._stubs:
            self._stubs[
                "list_pull_request_comments"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListPullRequestComments",
                request_serializer=secure_source_manager.ListPullRequestCommentsRequest.serialize,
                response_deserializer=secure_source_manager.ListPullRequestCommentsResponse.deserialize,
            )
        return self._stubs["list_pull_request_comments"]

    @property
    def create_pull_request_comment(
        self,
    ) -> Callable[
        [secure_source_manager.CreatePullRequestCommentRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create pull request comment method over gRPC.

        Creates a pull request comment.

        Returns:
            Callable[[~.CreatePullRequestCommentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_pull_request_comment" not in self._stubs:
            self._stubs[
                "create_pull_request_comment"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CreatePullRequestComment",
                request_serializer=secure_source_manager.CreatePullRequestCommentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_pull_request_comment"]

    @property
    def update_pull_request_comment(
        self,
    ) -> Callable[
        [secure_source_manager.UpdatePullRequestCommentRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update pull request comment method over gRPC.

        Updates a pull request comment.

        Returns:
            Callable[[~.UpdatePullRequestCommentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_pull_request_comment" not in self._stubs:
            self._stubs[
                "update_pull_request_comment"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/UpdatePullRequestComment",
                request_serializer=secure_source_manager.UpdatePullRequestCommentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_pull_request_comment"]

    @property
    def delete_pull_request_comment(
        self,
    ) -> Callable[
        [secure_source_manager.DeletePullRequestCommentRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete pull request comment method over gRPC.

        Deletes a pull request comment.

        Returns:
            Callable[[~.DeletePullRequestCommentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_pull_request_comment" not in self._stubs:
            self._stubs[
                "delete_pull_request_comment"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/DeletePullRequestComment",
                request_serializer=secure_source_manager.DeletePullRequestCommentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_pull_request_comment"]

    @property
    def batch_create_pull_request_comments(
        self,
    ) -> Callable[
        [secure_source_manager.BatchCreatePullRequestCommentsRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch create pull request
        comments method over gRPC.

        Batch creates pull request comments.

        Returns:
            Callable[[~.BatchCreatePullRequestCommentsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_pull_request_comments" not in self._stubs:
            self._stubs[
                "batch_create_pull_request_comments"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/BatchCreatePullRequestComments",
                request_serializer=secure_source_manager.BatchCreatePullRequestCommentsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_create_pull_request_comments"]

    @property
    def resolve_pull_request_comments(
        self,
    ) -> Callable[
        [secure_source_manager.ResolvePullRequestCommentsRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the resolve pull request comments method over gRPC.

        Resolves pull request comments.

        Returns:
            Callable[[~.ResolvePullRequestCommentsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "resolve_pull_request_comments" not in self._stubs:
            self._stubs[
                "resolve_pull_request_comments"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ResolvePullRequestComments",
                request_serializer=secure_source_manager.ResolvePullRequestCommentsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["resolve_pull_request_comments"]

    @property
    def unresolve_pull_request_comments(
        self,
    ) -> Callable[
        [secure_source_manager.UnresolvePullRequestCommentsRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the unresolve pull request
        comments method over gRPC.

        Unresolves pull request comment.

        Returns:
            Callable[[~.UnresolvePullRequestCommentsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "unresolve_pull_request_comments" not in self._stubs:
            self._stubs[
                "unresolve_pull_request_comments"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/UnresolvePullRequestComments",
                request_serializer=secure_source_manager.UnresolvePullRequestCommentsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["unresolve_pull_request_comments"]

    @property
    def create_issue_comment(
        self,
    ) -> Callable[
        [secure_source_manager.CreateIssueCommentRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create issue comment method over gRPC.

        Creates an issue comment.

        Returns:
            Callable[[~.CreateIssueCommentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_issue_comment" not in self._stubs:
            self._stubs["create_issue_comment"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/CreateIssueComment",
                request_serializer=secure_source_manager.CreateIssueCommentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_issue_comment"]

    @property
    def get_issue_comment(
        self,
    ) -> Callable[
        [secure_source_manager.GetIssueCommentRequest],
        Awaitable[secure_source_manager.IssueComment],
    ]:
        r"""Return a callable for the get issue comment method over gRPC.

        Gets an issue comment.

        Returns:
            Callable[[~.GetIssueCommentRequest],
                    Awaitable[~.IssueComment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_issue_comment" not in self._stubs:
            self._stubs["get_issue_comment"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/GetIssueComment",
                request_serializer=secure_source_manager.GetIssueCommentRequest.serialize,
                response_deserializer=secure_source_manager.IssueComment.deserialize,
            )
        return self._stubs["get_issue_comment"]

    @property
    def list_issue_comments(
        self,
    ) -> Callable[
        [secure_source_manager.ListIssueCommentsRequest],
        Awaitable[secure_source_manager.ListIssueCommentsResponse],
    ]:
        r"""Return a callable for the list issue comments method over gRPC.

        Lists comments in an issue.

        Returns:
            Callable[[~.ListIssueCommentsRequest],
                    Awaitable[~.ListIssueCommentsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_issue_comments" not in self._stubs:
            self._stubs["list_issue_comments"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/ListIssueComments",
                request_serializer=secure_source_manager.ListIssueCommentsRequest.serialize,
                response_deserializer=secure_source_manager.ListIssueCommentsResponse.deserialize,
            )
        return self._stubs["list_issue_comments"]

    @property
    def update_issue_comment(
        self,
    ) -> Callable[
        [secure_source_manager.UpdateIssueCommentRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update issue comment method over gRPC.

        Updates an issue comment.

        Returns:
            Callable[[~.UpdateIssueCommentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_issue_comment" not in self._stubs:
            self._stubs["update_issue_comment"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/UpdateIssueComment",
                request_serializer=secure_source_manager.UpdateIssueCommentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_issue_comment"]

    @property
    def delete_issue_comment(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteIssueCommentRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete issue comment method over gRPC.

        Deletes an issue comment.

        Returns:
            Callable[[~.DeleteIssueCommentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_issue_comment" not in self._stubs:
            self._stubs["delete_issue_comment"] = self._logged_channel.unary_unary(
                "/google.cloud.securesourcemanager.v1.SecureSourceManager/DeleteIssueComment",
                request_serializer=secure_source_manager.DeleteIssueCommentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_issue_comment"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_instances: self._wrap_method(
                self.list_instances,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_instance: self._wrap_method(
                self.get_instance,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_instance: self._wrap_method(
                self.create_instance,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_instance: self._wrap_method(
                self.delete_instance,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_repositories: self._wrap_method(
                self.list_repositories,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_repository: self._wrap_method(
                self.get_repository,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_repository: self._wrap_method(
                self.create_repository,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_repository: self._wrap_method(
                self.update_repository,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_repository: self._wrap_method(
                self.delete_repository,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_hooks: self._wrap_method(
                self.list_hooks,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_hook: self._wrap_method(
                self.get_hook,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_hook: self._wrap_method(
                self.create_hook,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_hook: self._wrap_method(
                self.update_hook,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_hook: self._wrap_method(
                self.delete_hook,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy_repo: self._wrap_method(
                self.get_iam_policy_repo,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.set_iam_policy_repo: self._wrap_method(
                self.set_iam_policy_repo,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions_repo: self._wrap_method(
                self.test_iam_permissions_repo,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_branch_rule: self._wrap_method(
                self.create_branch_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_branch_rules: self._wrap_method(
                self.list_branch_rules,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_branch_rule: self._wrap_method(
                self.get_branch_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_branch_rule: self._wrap_method(
                self.update_branch_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_branch_rule: self._wrap_method(
                self.delete_branch_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_pull_request: self._wrap_method(
                self.create_pull_request,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_pull_request: self._wrap_method(
                self.get_pull_request,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_pull_requests: self._wrap_method(
                self.list_pull_requests,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_pull_request: self._wrap_method(
                self.update_pull_request,
                default_timeout=None,
                client_info=client_info,
            ),
            self.merge_pull_request: self._wrap_method(
                self.merge_pull_request,
                default_timeout=None,
                client_info=client_info,
            ),
            self.open_pull_request: self._wrap_method(
                self.open_pull_request,
                default_timeout=None,
                client_info=client_info,
            ),
            self.close_pull_request: self._wrap_method(
                self.close_pull_request,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_pull_request_file_diffs: self._wrap_method(
                self.list_pull_request_file_diffs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_tree: self._wrap_method(
                self.fetch_tree,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_blob: self._wrap_method(
                self.fetch_blob,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_issue: self._wrap_method(
                self.create_issue,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_issue: self._wrap_method(
                self.get_issue,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_issues: self._wrap_method(
                self.list_issues,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_issue: self._wrap_method(
                self.update_issue,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_issue: self._wrap_method(
                self.delete_issue,
                default_timeout=None,
                client_info=client_info,
            ),
            self.open_issue: self._wrap_method(
                self.open_issue,
                default_timeout=None,
                client_info=client_info,
            ),
            self.close_issue: self._wrap_method(
                self.close_issue,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_pull_request_comment: self._wrap_method(
                self.get_pull_request_comment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_pull_request_comments: self._wrap_method(
                self.list_pull_request_comments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_pull_request_comment: self._wrap_method(
                self.create_pull_request_comment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_pull_request_comment: self._wrap_method(
                self.update_pull_request_comment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_pull_request_comment: self._wrap_method(
                self.delete_pull_request_comment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.batch_create_pull_request_comments: self._wrap_method(
                self.batch_create_pull_request_comments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.resolve_pull_request_comments: self._wrap_method(
                self.resolve_pull_request_comments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.unresolve_pull_request_comments: self._wrap_method(
                self.unresolve_pull_request_comments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_issue_comment: self._wrap_method(
                self.create_issue_comment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_issue_comment: self._wrap_method(
                self.get_issue_comment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_issue_comments: self._wrap_method(
                self.list_issue_comments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_issue_comment: self._wrap_method(
                self.update_issue_comment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_issue_comment: self._wrap_method(
                self.delete_issue_comment,
                default_timeout=None,
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


__all__ = ("SecureSourceManagerGrpcAsyncIOTransport",)
