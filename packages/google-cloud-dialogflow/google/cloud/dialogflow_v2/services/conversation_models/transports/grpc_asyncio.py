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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.dialogflow_v2.types import (
    conversation_model as gcd_conversation_model,
)
from google.cloud.dialogflow_v2.types import conversation_model

from .base import DEFAULT_CLIENT_INFO, ConversationModelsTransport
from .grpc import ConversationModelsGrpcTransport


class ConversationModelsGrpcAsyncIOTransport(ConversationModelsTransport):
    """gRPC AsyncIO backend transport for ConversationModels.

    Manages a collection of models for human agent assistant.

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
        host: str = "dialogflow.googleapis.com",
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
        host: str = "dialogflow.googleapis.com",
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
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
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

        # Wrap messages. This must be done after self._grpc_channel exists
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
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
    def create_conversation_model(
        self,
    ) -> Callable[
        [gcd_conversation_model.CreateConversationModelRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create conversation model method over gRPC.

        Creates a model.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [CreateConversationModelOperationMetadata][google.cloud.dialogflow.v2.CreateConversationModelOperationMetadata]
        -  ``response``:
           [ConversationModel][google.cloud.dialogflow.v2.ConversationModel]

        Returns:
            Callable[[~.CreateConversationModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_conversation_model" not in self._stubs:
            self._stubs["create_conversation_model"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/CreateConversationModel",
                request_serializer=gcd_conversation_model.CreateConversationModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_conversation_model"]

    @property
    def get_conversation_model(
        self,
    ) -> Callable[
        [conversation_model.GetConversationModelRequest],
        Awaitable[conversation_model.ConversationModel],
    ]:
        r"""Return a callable for the get conversation model method over gRPC.

        Gets conversation model.

        Returns:
            Callable[[~.GetConversationModelRequest],
                    Awaitable[~.ConversationModel]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_conversation_model" not in self._stubs:
            self._stubs["get_conversation_model"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/GetConversationModel",
                request_serializer=conversation_model.GetConversationModelRequest.serialize,
                response_deserializer=conversation_model.ConversationModel.deserialize,
            )
        return self._stubs["get_conversation_model"]

    @property
    def list_conversation_models(
        self,
    ) -> Callable[
        [conversation_model.ListConversationModelsRequest],
        Awaitable[conversation_model.ListConversationModelsResponse],
    ]:
        r"""Return a callable for the list conversation models method over gRPC.

        Lists conversation models.

        Returns:
            Callable[[~.ListConversationModelsRequest],
                    Awaitable[~.ListConversationModelsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_conversation_models" not in self._stubs:
            self._stubs["list_conversation_models"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/ListConversationModels",
                request_serializer=conversation_model.ListConversationModelsRequest.serialize,
                response_deserializer=conversation_model.ListConversationModelsResponse.deserialize,
            )
        return self._stubs["list_conversation_models"]

    @property
    def delete_conversation_model(
        self,
    ) -> Callable[
        [conversation_model.DeleteConversationModelRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete conversation model method over gRPC.

        Deletes a model.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [DeleteConversationModelOperationMetadata][google.cloud.dialogflow.v2.DeleteConversationModelOperationMetadata]
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        Returns:
            Callable[[~.DeleteConversationModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_conversation_model" not in self._stubs:
            self._stubs["delete_conversation_model"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/DeleteConversationModel",
                request_serializer=conversation_model.DeleteConversationModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_conversation_model"]

    @property
    def deploy_conversation_model(
        self,
    ) -> Callable[
        [conversation_model.DeployConversationModelRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the deploy conversation model method over gRPC.

        Deploys a model. If a model is already deployed, deploying it
        has no effect. A model can only serve prediction requests after
        it gets deployed. For article suggestion, custom model will not
        be used unless it is deployed.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [DeployConversationModelOperationMetadata][google.cloud.dialogflow.v2.DeployConversationModelOperationMetadata]
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        Returns:
            Callable[[~.DeployConversationModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "deploy_conversation_model" not in self._stubs:
            self._stubs["deploy_conversation_model"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/DeployConversationModel",
                request_serializer=conversation_model.DeployConversationModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["deploy_conversation_model"]

    @property
    def undeploy_conversation_model(
        self,
    ) -> Callable[
        [conversation_model.UndeployConversationModelRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the undeploy conversation model method over gRPC.

        Undeploys a model. If the model is not deployed this method has
        no effect. If the model is currently being used:

        -  For article suggestion, article suggestion will fallback to
           the default model if model is undeployed.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [UndeployConversationModelOperationMetadata][google.cloud.dialogflow.v2.UndeployConversationModelOperationMetadata]
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        Returns:
            Callable[[~.UndeployConversationModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "undeploy_conversation_model" not in self._stubs:
            self._stubs["undeploy_conversation_model"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/UndeployConversationModel",
                request_serializer=conversation_model.UndeployConversationModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["undeploy_conversation_model"]

    @property
    def get_conversation_model_evaluation(
        self,
    ) -> Callable[
        [conversation_model.GetConversationModelEvaluationRequest],
        Awaitable[conversation_model.ConversationModelEvaluation],
    ]:
        r"""Return a callable for the get conversation model
        evaluation method over gRPC.

        Gets an evaluation of conversation model.

        Returns:
            Callable[[~.GetConversationModelEvaluationRequest],
                    Awaitable[~.ConversationModelEvaluation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_conversation_model_evaluation" not in self._stubs:
            self._stubs[
                "get_conversation_model_evaluation"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/GetConversationModelEvaluation",
                request_serializer=conversation_model.GetConversationModelEvaluationRequest.serialize,
                response_deserializer=conversation_model.ConversationModelEvaluation.deserialize,
            )
        return self._stubs["get_conversation_model_evaluation"]

    @property
    def list_conversation_model_evaluations(
        self,
    ) -> Callable[
        [conversation_model.ListConversationModelEvaluationsRequest],
        Awaitable[conversation_model.ListConversationModelEvaluationsResponse],
    ]:
        r"""Return a callable for the list conversation model
        evaluations method over gRPC.

        Lists evaluations of a conversation model.

        Returns:
            Callable[[~.ListConversationModelEvaluationsRequest],
                    Awaitable[~.ListConversationModelEvaluationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_conversation_model_evaluations" not in self._stubs:
            self._stubs[
                "list_conversation_model_evaluations"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/ListConversationModelEvaluations",
                request_serializer=conversation_model.ListConversationModelEvaluationsRequest.serialize,
                response_deserializer=conversation_model.ListConversationModelEvaluationsResponse.deserialize,
            )
        return self._stubs["list_conversation_model_evaluations"]

    @property
    def create_conversation_model_evaluation(
        self,
    ) -> Callable[
        [conversation_model.CreateConversationModelEvaluationRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create conversation model
        evaluation method over gRPC.

        Creates evaluation of a conversation model.

        Returns:
            Callable[[~.CreateConversationModelEvaluationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_conversation_model_evaluation" not in self._stubs:
            self._stubs[
                "create_conversation_model_evaluation"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2.ConversationModels/CreateConversationModelEvaluation",
                request_serializer=conversation_model.CreateConversationModelEvaluationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_conversation_model_evaluation"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_conversation_model: self._wrap_method(
                self.create_conversation_model,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_conversation_model: self._wrap_method(
                self.get_conversation_model,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_conversation_models: self._wrap_method(
                self.list_conversation_models,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_conversation_model: self._wrap_method(
                self.delete_conversation_model,
                default_timeout=None,
                client_info=client_info,
            ),
            self.deploy_conversation_model: self._wrap_method(
                self.deploy_conversation_model,
                default_timeout=None,
                client_info=client_info,
            ),
            self.undeploy_conversation_model: self._wrap_method(
                self.undeploy_conversation_model,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_conversation_model_evaluation: self._wrap_method(
                self.get_conversation_model_evaluation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_conversation_model_evaluations: self._wrap_method(
                self.list_conversation_model_evaluations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_conversation_model_evaluation: self._wrap_method(
                self.create_conversation_model_evaluation,
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
        return self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"

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
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
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
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
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
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
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
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
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
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("ConversationModelsGrpcAsyncIOTransport",)
