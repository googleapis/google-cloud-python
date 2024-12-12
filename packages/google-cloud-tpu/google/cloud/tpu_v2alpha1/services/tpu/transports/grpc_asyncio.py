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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.tpu_v2alpha1.types import cloud_tpu

from .base import DEFAULT_CLIENT_INFO, TpuTransport
from .grpc import TpuGrpcTransport

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
                    "serviceName": "google.cloud.tpu.v2alpha1.Tpu",
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
                    "serviceName": "google.cloud.tpu.v2alpha1.Tpu",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class TpuGrpcAsyncIOTransport(TpuTransport):
    """gRPC AsyncIO backend transport for Tpu.

    Manages TPU nodes and other resources

    TPU API v2alpha1

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
        host: str = "tpu.googleapis.com",
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
        host: str = "tpu.googleapis.com",
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
                 The hostname to connect to (default: 'tpu.googleapis.com').
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
    def list_nodes(
        self,
    ) -> Callable[[cloud_tpu.ListNodesRequest], Awaitable[cloud_tpu.ListNodesResponse]]:
        r"""Return a callable for the list nodes method over gRPC.

        Lists nodes.

        Returns:
            Callable[[~.ListNodesRequest],
                    Awaitable[~.ListNodesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_nodes" not in self._stubs:
            self._stubs["list_nodes"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/ListNodes",
                request_serializer=cloud_tpu.ListNodesRequest.serialize,
                response_deserializer=cloud_tpu.ListNodesResponse.deserialize,
            )
        return self._stubs["list_nodes"]

    @property
    def get_node(
        self,
    ) -> Callable[[cloud_tpu.GetNodeRequest], Awaitable[cloud_tpu.Node]]:
        r"""Return a callable for the get node method over gRPC.

        Gets the details of a node.

        Returns:
            Callable[[~.GetNodeRequest],
                    Awaitable[~.Node]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_node" not in self._stubs:
            self._stubs["get_node"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/GetNode",
                request_serializer=cloud_tpu.GetNodeRequest.serialize,
                response_deserializer=cloud_tpu.Node.deserialize,
            )
        return self._stubs["get_node"]

    @property
    def create_node(
        self,
    ) -> Callable[[cloud_tpu.CreateNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create node method over gRPC.

        Creates a node.

        Returns:
            Callable[[~.CreateNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_node" not in self._stubs:
            self._stubs["create_node"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/CreateNode",
                request_serializer=cloud_tpu.CreateNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_node"]

    @property
    def delete_node(
        self,
    ) -> Callable[[cloud_tpu.DeleteNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete node method over gRPC.

        Deletes a node.

        Returns:
            Callable[[~.DeleteNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_node" not in self._stubs:
            self._stubs["delete_node"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/DeleteNode",
                request_serializer=cloud_tpu.DeleteNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_node"]

    @property
    def stop_node(
        self,
    ) -> Callable[[cloud_tpu.StopNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the stop node method over gRPC.

        Stops a node. This operation is only available with
        single TPU nodes.

        Returns:
            Callable[[~.StopNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_node" not in self._stubs:
            self._stubs["stop_node"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/StopNode",
                request_serializer=cloud_tpu.StopNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_node"]

    @property
    def start_node(
        self,
    ) -> Callable[[cloud_tpu.StartNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the start node method over gRPC.

        Starts a node.

        Returns:
            Callable[[~.StartNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_node" not in self._stubs:
            self._stubs["start_node"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/StartNode",
                request_serializer=cloud_tpu.StartNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_node"]

    @property
    def update_node(
        self,
    ) -> Callable[[cloud_tpu.UpdateNodeRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update node method over gRPC.

        Updates the configurations of a node.

        Returns:
            Callable[[~.UpdateNodeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_node" not in self._stubs:
            self._stubs["update_node"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/UpdateNode",
                request_serializer=cloud_tpu.UpdateNodeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_node"]

    @property
    def list_queued_resources(
        self,
    ) -> Callable[
        [cloud_tpu.ListQueuedResourcesRequest],
        Awaitable[cloud_tpu.ListQueuedResourcesResponse],
    ]:
        r"""Return a callable for the list queued resources method over gRPC.

        Lists queued resources.

        Returns:
            Callable[[~.ListQueuedResourcesRequest],
                    Awaitable[~.ListQueuedResourcesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_queued_resources" not in self._stubs:
            self._stubs["list_queued_resources"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/ListQueuedResources",
                request_serializer=cloud_tpu.ListQueuedResourcesRequest.serialize,
                response_deserializer=cloud_tpu.ListQueuedResourcesResponse.deserialize,
            )
        return self._stubs["list_queued_resources"]

    @property
    def get_queued_resource(
        self,
    ) -> Callable[
        [cloud_tpu.GetQueuedResourceRequest], Awaitable[cloud_tpu.QueuedResource]
    ]:
        r"""Return a callable for the get queued resource method over gRPC.

        Gets details of a queued resource.

        Returns:
            Callable[[~.GetQueuedResourceRequest],
                    Awaitable[~.QueuedResource]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_queued_resource" not in self._stubs:
            self._stubs["get_queued_resource"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/GetQueuedResource",
                request_serializer=cloud_tpu.GetQueuedResourceRequest.serialize,
                response_deserializer=cloud_tpu.QueuedResource.deserialize,
            )
        return self._stubs["get_queued_resource"]

    @property
    def create_queued_resource(
        self,
    ) -> Callable[
        [cloud_tpu.CreateQueuedResourceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create queued resource method over gRPC.

        Creates a QueuedResource TPU instance.

        Returns:
            Callable[[~.CreateQueuedResourceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_queued_resource" not in self._stubs:
            self._stubs["create_queued_resource"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/CreateQueuedResource",
                request_serializer=cloud_tpu.CreateQueuedResourceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_queued_resource"]

    @property
    def delete_queued_resource(
        self,
    ) -> Callable[
        [cloud_tpu.DeleteQueuedResourceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete queued resource method over gRPC.

        Deletes a QueuedResource TPU instance.

        Returns:
            Callable[[~.DeleteQueuedResourceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_queued_resource" not in self._stubs:
            self._stubs["delete_queued_resource"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/DeleteQueuedResource",
                request_serializer=cloud_tpu.DeleteQueuedResourceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_queued_resource"]

    @property
    def reset_queued_resource(
        self,
    ) -> Callable[
        [cloud_tpu.ResetQueuedResourceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the reset queued resource method over gRPC.

        Resets a QueuedResource TPU instance

        Returns:
            Callable[[~.ResetQueuedResourceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reset_queued_resource" not in self._stubs:
            self._stubs["reset_queued_resource"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/ResetQueuedResource",
                request_serializer=cloud_tpu.ResetQueuedResourceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["reset_queued_resource"]

    @property
    def generate_service_identity(
        self,
    ) -> Callable[
        [cloud_tpu.GenerateServiceIdentityRequest],
        Awaitable[cloud_tpu.GenerateServiceIdentityResponse],
    ]:
        r"""Return a callable for the generate service identity method over gRPC.

        Generates the Cloud TPU service identity for the
        project.

        Returns:
            Callable[[~.GenerateServiceIdentityRequest],
                    Awaitable[~.GenerateServiceIdentityResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_service_identity" not in self._stubs:
            self._stubs["generate_service_identity"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/GenerateServiceIdentity",
                request_serializer=cloud_tpu.GenerateServiceIdentityRequest.serialize,
                response_deserializer=cloud_tpu.GenerateServiceIdentityResponse.deserialize,
            )
        return self._stubs["generate_service_identity"]

    @property
    def list_accelerator_types(
        self,
    ) -> Callable[
        [cloud_tpu.ListAcceleratorTypesRequest],
        Awaitable[cloud_tpu.ListAcceleratorTypesResponse],
    ]:
        r"""Return a callable for the list accelerator types method over gRPC.

        Lists accelerator types supported by this API.

        Returns:
            Callable[[~.ListAcceleratorTypesRequest],
                    Awaitable[~.ListAcceleratorTypesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_accelerator_types" not in self._stubs:
            self._stubs["list_accelerator_types"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/ListAcceleratorTypes",
                request_serializer=cloud_tpu.ListAcceleratorTypesRequest.serialize,
                response_deserializer=cloud_tpu.ListAcceleratorTypesResponse.deserialize,
            )
        return self._stubs["list_accelerator_types"]

    @property
    def get_accelerator_type(
        self,
    ) -> Callable[
        [cloud_tpu.GetAcceleratorTypeRequest], Awaitable[cloud_tpu.AcceleratorType]
    ]:
        r"""Return a callable for the get accelerator type method over gRPC.

        Gets AcceleratorType.

        Returns:
            Callable[[~.GetAcceleratorTypeRequest],
                    Awaitable[~.AcceleratorType]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_accelerator_type" not in self._stubs:
            self._stubs["get_accelerator_type"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/GetAcceleratorType",
                request_serializer=cloud_tpu.GetAcceleratorTypeRequest.serialize,
                response_deserializer=cloud_tpu.AcceleratorType.deserialize,
            )
        return self._stubs["get_accelerator_type"]

    @property
    def list_runtime_versions(
        self,
    ) -> Callable[
        [cloud_tpu.ListRuntimeVersionsRequest],
        Awaitable[cloud_tpu.ListRuntimeVersionsResponse],
    ]:
        r"""Return a callable for the list runtime versions method over gRPC.

        Lists runtime versions supported by this API.

        Returns:
            Callable[[~.ListRuntimeVersionsRequest],
                    Awaitable[~.ListRuntimeVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_runtime_versions" not in self._stubs:
            self._stubs["list_runtime_versions"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/ListRuntimeVersions",
                request_serializer=cloud_tpu.ListRuntimeVersionsRequest.serialize,
                response_deserializer=cloud_tpu.ListRuntimeVersionsResponse.deserialize,
            )
        return self._stubs["list_runtime_versions"]

    @property
    def get_runtime_version(
        self,
    ) -> Callable[
        [cloud_tpu.GetRuntimeVersionRequest], Awaitable[cloud_tpu.RuntimeVersion]
    ]:
        r"""Return a callable for the get runtime version method over gRPC.

        Gets a runtime version.

        Returns:
            Callable[[~.GetRuntimeVersionRequest],
                    Awaitable[~.RuntimeVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_runtime_version" not in self._stubs:
            self._stubs["get_runtime_version"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/GetRuntimeVersion",
                request_serializer=cloud_tpu.GetRuntimeVersionRequest.serialize,
                response_deserializer=cloud_tpu.RuntimeVersion.deserialize,
            )
        return self._stubs["get_runtime_version"]

    @property
    def get_guest_attributes(
        self,
    ) -> Callable[
        [cloud_tpu.GetGuestAttributesRequest],
        Awaitable[cloud_tpu.GetGuestAttributesResponse],
    ]:
        r"""Return a callable for the get guest attributes method over gRPC.

        Retrieves the guest attributes for the node.

        Returns:
            Callable[[~.GetGuestAttributesRequest],
                    Awaitable[~.GetGuestAttributesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_guest_attributes" not in self._stubs:
            self._stubs["get_guest_attributes"] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/GetGuestAttributes",
                request_serializer=cloud_tpu.GetGuestAttributesRequest.serialize,
                response_deserializer=cloud_tpu.GetGuestAttributesResponse.deserialize,
            )
        return self._stubs["get_guest_attributes"]

    @property
    def simulate_maintenance_event(
        self,
    ) -> Callable[
        [cloud_tpu.SimulateMaintenanceEventRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the simulate maintenance event method over gRPC.

        Simulates a maintenance event.

        Returns:
            Callable[[~.SimulateMaintenanceEventRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "simulate_maintenance_event" not in self._stubs:
            self._stubs[
                "simulate_maintenance_event"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.tpu.v2alpha1.Tpu/SimulateMaintenanceEvent",
                request_serializer=cloud_tpu.SimulateMaintenanceEventRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["simulate_maintenance_event"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_nodes: self._wrap_method(
                self.list_nodes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_node: self._wrap_method(
                self.get_node,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_node: self._wrap_method(
                self.create_node,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_node: self._wrap_method(
                self.delete_node,
                default_timeout=None,
                client_info=client_info,
            ),
            self.stop_node: self._wrap_method(
                self.stop_node,
                default_timeout=None,
                client_info=client_info,
            ),
            self.start_node: self._wrap_method(
                self.start_node,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_node: self._wrap_method(
                self.update_node,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_queued_resources: self._wrap_method(
                self.list_queued_resources,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_queued_resource: self._wrap_method(
                self.get_queued_resource,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_queued_resource: self._wrap_method(
                self.create_queued_resource,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_queued_resource: self._wrap_method(
                self.delete_queued_resource,
                default_timeout=None,
                client_info=client_info,
            ),
            self.reset_queued_resource: self._wrap_method(
                self.reset_queued_resource,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_service_identity: self._wrap_method(
                self.generate_service_identity,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_accelerator_types: self._wrap_method(
                self.list_accelerator_types,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_accelerator_type: self._wrap_method(
                self.get_accelerator_type,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_runtime_versions: self._wrap_method(
                self.list_runtime_versions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_runtime_version: self._wrap_method(
                self.get_runtime_version,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_guest_attributes: self._wrap_method(
                self.get_guest_attributes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.simulate_maintenance_event: self._wrap_method(
                self.simulate_maintenance_event,
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


__all__ = ("TpuGrpcAsyncIOTransport",)
