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
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.visionai_v1.types import lva_resources, lva_service

from .base import DEFAULT_CLIENT_INFO, LiveVideoAnalyticsTransport
from .grpc import LiveVideoAnalyticsGrpcTransport


class LiveVideoAnalyticsGrpcAsyncIOTransport(LiveVideoAnalyticsTransport):
    """gRPC AsyncIO backend transport for LiveVideoAnalytics.

    Service describing handlers for resources. The service
    enables clients to run Live Video Analytics (LVA) on the
    streaming inputs.

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
        host: str = "visionai.googleapis.com",
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
        host: str = "visionai.googleapis.com",
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
                 The hostname to connect to (default: 'visionai.googleapis.com').
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
    def list_public_operators(
        self,
    ) -> Callable[
        [lva_service.ListPublicOperatorsRequest],
        Awaitable[lva_service.ListPublicOperatorsResponse],
    ]:
        r"""Return a callable for the list public operators method over gRPC.

        ListPublicOperators returns all the operators in
        public registry.

        Returns:
            Callable[[~.ListPublicOperatorsRequest],
                    Awaitable[~.ListPublicOperatorsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_public_operators" not in self._stubs:
            self._stubs["list_public_operators"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/ListPublicOperators",
                request_serializer=lva_service.ListPublicOperatorsRequest.serialize,
                response_deserializer=lva_service.ListPublicOperatorsResponse.deserialize,
            )
        return self._stubs["list_public_operators"]

    @property
    def resolve_operator_info(
        self,
    ) -> Callable[
        [lva_service.ResolveOperatorInfoRequest],
        Awaitable[lva_service.ResolveOperatorInfoResponse],
    ]:
        r"""Return a callable for the resolve operator info method over gRPC.

        ResolveOperatorInfo returns the operator information
        based on the request.

        Returns:
            Callable[[~.ResolveOperatorInfoRequest],
                    Awaitable[~.ResolveOperatorInfoResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "resolve_operator_info" not in self._stubs:
            self._stubs["resolve_operator_info"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/ResolveOperatorInfo",
                request_serializer=lva_service.ResolveOperatorInfoRequest.serialize,
                response_deserializer=lva_service.ResolveOperatorInfoResponse.deserialize,
            )
        return self._stubs["resolve_operator_info"]

    @property
    def list_operators(
        self,
    ) -> Callable[
        [lva_service.ListOperatorsRequest], Awaitable[lva_service.ListOperatorsResponse]
    ]:
        r"""Return a callable for the list operators method over gRPC.

        Lists Operators in a given project and location.

        Returns:
            Callable[[~.ListOperatorsRequest],
                    Awaitable[~.ListOperatorsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operators" not in self._stubs:
            self._stubs["list_operators"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/ListOperators",
                request_serializer=lva_service.ListOperatorsRequest.serialize,
                response_deserializer=lva_service.ListOperatorsResponse.deserialize,
            )
        return self._stubs["list_operators"]

    @property
    def get_operator(
        self,
    ) -> Callable[[lva_service.GetOperatorRequest], Awaitable[lva_resources.Operator]]:
        r"""Return a callable for the get operator method over gRPC.

        Gets details of a single Operator.

        Returns:
            Callable[[~.GetOperatorRequest],
                    Awaitable[~.Operator]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operator" not in self._stubs:
            self._stubs["get_operator"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/GetOperator",
                request_serializer=lva_service.GetOperatorRequest.serialize,
                response_deserializer=lva_resources.Operator.deserialize,
            )
        return self._stubs["get_operator"]

    @property
    def create_operator(
        self,
    ) -> Callable[
        [lva_service.CreateOperatorRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create operator method over gRPC.

        Creates a new Operator in a given project and
        location.

        Returns:
            Callable[[~.CreateOperatorRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_operator" not in self._stubs:
            self._stubs["create_operator"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/CreateOperator",
                request_serializer=lva_service.CreateOperatorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_operator"]

    @property
    def update_operator(
        self,
    ) -> Callable[
        [lva_service.UpdateOperatorRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update operator method over gRPC.

        Updates the parameters of a single Operator.

        Returns:
            Callable[[~.UpdateOperatorRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_operator" not in self._stubs:
            self._stubs["update_operator"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/UpdateOperator",
                request_serializer=lva_service.UpdateOperatorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_operator"]

    @property
    def delete_operator(
        self,
    ) -> Callable[
        [lva_service.DeleteOperatorRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete operator method over gRPC.

        Deletes a single Operator.

        Returns:
            Callable[[~.DeleteOperatorRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operator" not in self._stubs:
            self._stubs["delete_operator"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/DeleteOperator",
                request_serializer=lva_service.DeleteOperatorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_operator"]

    @property
    def list_analyses(
        self,
    ) -> Callable[
        [lva_service.ListAnalysesRequest], Awaitable[lva_service.ListAnalysesResponse]
    ]:
        r"""Return a callable for the list analyses method over gRPC.

        Lists Analyses in a given project and location.

        Returns:
            Callable[[~.ListAnalysesRequest],
                    Awaitable[~.ListAnalysesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_analyses" not in self._stubs:
            self._stubs["list_analyses"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/ListAnalyses",
                request_serializer=lva_service.ListAnalysesRequest.serialize,
                response_deserializer=lva_service.ListAnalysesResponse.deserialize,
            )
        return self._stubs["list_analyses"]

    @property
    def get_analysis(
        self,
    ) -> Callable[[lva_service.GetAnalysisRequest], Awaitable[lva_resources.Analysis]]:
        r"""Return a callable for the get analysis method over gRPC.

        Gets details of a single Analysis.

        Returns:
            Callable[[~.GetAnalysisRequest],
                    Awaitable[~.Analysis]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_analysis" not in self._stubs:
            self._stubs["get_analysis"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/GetAnalysis",
                request_serializer=lva_service.GetAnalysisRequest.serialize,
                response_deserializer=lva_resources.Analysis.deserialize,
            )
        return self._stubs["get_analysis"]

    @property
    def create_analysis(
        self,
    ) -> Callable[
        [lva_service.CreateAnalysisRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create analysis method over gRPC.

        Creates a new Analysis in a given project and
        location.

        Returns:
            Callable[[~.CreateAnalysisRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_analysis" not in self._stubs:
            self._stubs["create_analysis"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/CreateAnalysis",
                request_serializer=lva_service.CreateAnalysisRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_analysis"]

    @property
    def update_analysis(
        self,
    ) -> Callable[
        [lva_service.UpdateAnalysisRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update analysis method over gRPC.

        Updates the parameters of a single Analysis.

        Returns:
            Callable[[~.UpdateAnalysisRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_analysis" not in self._stubs:
            self._stubs["update_analysis"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/UpdateAnalysis",
                request_serializer=lva_service.UpdateAnalysisRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_analysis"]

    @property
    def delete_analysis(
        self,
    ) -> Callable[
        [lva_service.DeleteAnalysisRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete analysis method over gRPC.

        Deletes a single Analysis.

        Returns:
            Callable[[~.DeleteAnalysisRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_analysis" not in self._stubs:
            self._stubs["delete_analysis"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/DeleteAnalysis",
                request_serializer=lva_service.DeleteAnalysisRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_analysis"]

    @property
    def list_processes(
        self,
    ) -> Callable[
        [lva_service.ListProcessesRequest], Awaitable[lva_service.ListProcessesResponse]
    ]:
        r"""Return a callable for the list processes method over gRPC.

        Lists Processes in a given project and location.

        Returns:
            Callable[[~.ListProcessesRequest],
                    Awaitable[~.ListProcessesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_processes" not in self._stubs:
            self._stubs["list_processes"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/ListProcesses",
                request_serializer=lva_service.ListProcessesRequest.serialize,
                response_deserializer=lva_service.ListProcessesResponse.deserialize,
            )
        return self._stubs["list_processes"]

    @property
    def get_process(
        self,
    ) -> Callable[[lva_service.GetProcessRequest], Awaitable[lva_resources.Process]]:
        r"""Return a callable for the get process method over gRPC.

        Gets details of a single Process.

        Returns:
            Callable[[~.GetProcessRequest],
                    Awaitable[~.Process]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_process" not in self._stubs:
            self._stubs["get_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/GetProcess",
                request_serializer=lva_service.GetProcessRequest.serialize,
                response_deserializer=lva_resources.Process.deserialize,
            )
        return self._stubs["get_process"]

    @property
    def create_process(
        self,
    ) -> Callable[
        [lva_service.CreateProcessRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create process method over gRPC.

        Creates a new Process in a given project and
        location.

        Returns:
            Callable[[~.CreateProcessRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_process" not in self._stubs:
            self._stubs["create_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/CreateProcess",
                request_serializer=lva_service.CreateProcessRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_process"]

    @property
    def update_process(
        self,
    ) -> Callable[
        [lva_service.UpdateProcessRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update process method over gRPC.

        Updates the parameters of a single Process.

        Returns:
            Callable[[~.UpdateProcessRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_process" not in self._stubs:
            self._stubs["update_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/UpdateProcess",
                request_serializer=lva_service.UpdateProcessRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_process"]

    @property
    def delete_process(
        self,
    ) -> Callable[
        [lva_service.DeleteProcessRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete process method over gRPC.

        Deletes a single Process.

        Returns:
            Callable[[~.DeleteProcessRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_process" not in self._stubs:
            self._stubs["delete_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/DeleteProcess",
                request_serializer=lva_service.DeleteProcessRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_process"]

    @property
    def batch_run_process(
        self,
    ) -> Callable[
        [lva_service.BatchRunProcessRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the batch run process method over gRPC.

        Run all of the processes to "completion". Max time
        for each process is the LRO time limit.

        Returns:
            Callable[[~.BatchRunProcessRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_run_process" not in self._stubs:
            self._stubs["batch_run_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.visionai.v1.LiveVideoAnalytics/BatchRunProcess",
                request_serializer=lva_service.BatchRunProcessRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_run_process"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_public_operators: gapic_v1.method_async.wrap_method(
                self.list_public_operators,
                default_timeout=None,
                client_info=client_info,
            ),
            self.resolve_operator_info: gapic_v1.method_async.wrap_method(
                self.resolve_operator_info,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operators: gapic_v1.method_async.wrap_method(
                self.list_operators,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_operator: gapic_v1.method_async.wrap_method(
                self.get_operator,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_operator: gapic_v1.method_async.wrap_method(
                self.create_operator,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.update_operator: gapic_v1.method_async.wrap_method(
                self.update_operator,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_operator: gapic_v1.method_async.wrap_method(
                self.delete_operator,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_analyses: gapic_v1.method_async.wrap_method(
                self.list_analyses,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_analysis: gapic_v1.method_async.wrap_method(
                self.get_analysis,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_analysis: gapic_v1.method_async.wrap_method(
                self.create_analysis,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.update_analysis: gapic_v1.method_async.wrap_method(
                self.update_analysis,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_analysis: gapic_v1.method_async.wrap_method(
                self.delete_analysis,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_processes: gapic_v1.method_async.wrap_method(
                self.list_processes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_process: gapic_v1.method_async.wrap_method(
                self.get_process,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_process: gapic_v1.method_async.wrap_method(
                self.create_process,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_process: gapic_v1.method_async.wrap_method(
                self.update_process,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_process: gapic_v1.method_async.wrap_method(
                self.delete_process,
                default_timeout=None,
                client_info=client_info,
            ),
            self.batch_run_process: gapic_v1.method_async.wrap_method(
                self.batch_run_process,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def close(self):
        return self.grpc_channel.close()

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
            self._stubs["delete_operation"] = self.grpc_channel.unary_unary(
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


__all__ = ("LiveVideoAnalyticsGrpcAsyncIOTransport",)
