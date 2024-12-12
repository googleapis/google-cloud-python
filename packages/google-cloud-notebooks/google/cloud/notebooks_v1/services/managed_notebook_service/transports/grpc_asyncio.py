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

from google.cloud.notebooks_v1.types import managed_service, runtime

from .base import DEFAULT_CLIENT_INFO, ManagedNotebookServiceTransport
from .grpc import ManagedNotebookServiceGrpcTransport

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
                    "serviceName": "google.cloud.notebooks.v1.ManagedNotebookService",
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
                    "serviceName": "google.cloud.notebooks.v1.ManagedNotebookService",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class ManagedNotebookServiceGrpcAsyncIOTransport(ManagedNotebookServiceTransport):
    """gRPC AsyncIO backend transport for ManagedNotebookService.

    API v1 service for Managed Notebooks.

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
        host: str = "notebooks.googleapis.com",
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
        host: str = "notebooks.googleapis.com",
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
                 The hostname to connect to (default: 'notebooks.googleapis.com').
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
    def list_runtimes(
        self,
    ) -> Callable[
        [managed_service.ListRuntimesRequest],
        Awaitable[managed_service.ListRuntimesResponse],
    ]:
        r"""Return a callable for the list runtimes method over gRPC.

        Lists Runtimes in a given project and location.

        Returns:
            Callable[[~.ListRuntimesRequest],
                    Awaitable[~.ListRuntimesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_runtimes" not in self._stubs:
            self._stubs["list_runtimes"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/ListRuntimes",
                request_serializer=managed_service.ListRuntimesRequest.serialize,
                response_deserializer=managed_service.ListRuntimesResponse.deserialize,
            )
        return self._stubs["list_runtimes"]

    @property
    def get_runtime(
        self,
    ) -> Callable[[managed_service.GetRuntimeRequest], Awaitable[runtime.Runtime]]:
        r"""Return a callable for the get runtime method over gRPC.

        Gets details of a single Runtime. The location must
        be a regional endpoint rather than zonal.

        Returns:
            Callable[[~.GetRuntimeRequest],
                    Awaitable[~.Runtime]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_runtime" not in self._stubs:
            self._stubs["get_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/GetRuntime",
                request_serializer=managed_service.GetRuntimeRequest.serialize,
                response_deserializer=runtime.Runtime.deserialize,
            )
        return self._stubs["get_runtime"]

    @property
    def create_runtime(
        self,
    ) -> Callable[
        [managed_service.CreateRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create runtime method over gRPC.

        Creates a new Runtime in a given project and
        location.

        Returns:
            Callable[[~.CreateRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_runtime" not in self._stubs:
            self._stubs["create_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/CreateRuntime",
                request_serializer=managed_service.CreateRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_runtime"]

    @property
    def update_runtime(
        self,
    ) -> Callable[
        [managed_service.UpdateRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update runtime method over gRPC.

        Update Notebook Runtime configuration.

        Returns:
            Callable[[~.UpdateRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_runtime" not in self._stubs:
            self._stubs["update_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/UpdateRuntime",
                request_serializer=managed_service.UpdateRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_runtime"]

    @property
    def delete_runtime(
        self,
    ) -> Callable[
        [managed_service.DeleteRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete runtime method over gRPC.

        Deletes a single Runtime.

        Returns:
            Callable[[~.DeleteRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_runtime" not in self._stubs:
            self._stubs["delete_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/DeleteRuntime",
                request_serializer=managed_service.DeleteRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_runtime"]

    @property
    def start_runtime(
        self,
    ) -> Callable[
        [managed_service.StartRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the start runtime method over gRPC.

        Starts a Managed Notebook Runtime.
        Perform "Start" on GPU instances; "Resume" on CPU
        instances See:

        https://cloud.google.com/compute/docs/instances/stop-start-instance
        https://cloud.google.com/compute/docs/instances/suspend-resume-instance

        Returns:
            Callable[[~.StartRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_runtime" not in self._stubs:
            self._stubs["start_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/StartRuntime",
                request_serializer=managed_service.StartRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_runtime"]

    @property
    def stop_runtime(
        self,
    ) -> Callable[
        [managed_service.StopRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the stop runtime method over gRPC.

        Stops a Managed Notebook Runtime.
        Perform "Stop" on GPU instances; "Suspend" on CPU
        instances See:

        https://cloud.google.com/compute/docs/instances/stop-start-instance
        https://cloud.google.com/compute/docs/instances/suspend-resume-instance

        Returns:
            Callable[[~.StopRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_runtime" not in self._stubs:
            self._stubs["stop_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/StopRuntime",
                request_serializer=managed_service.StopRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_runtime"]

    @property
    def switch_runtime(
        self,
    ) -> Callable[
        [managed_service.SwitchRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the switch runtime method over gRPC.

        Switch a Managed Notebook Runtime.

        Returns:
            Callable[[~.SwitchRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "switch_runtime" not in self._stubs:
            self._stubs["switch_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/SwitchRuntime",
                request_serializer=managed_service.SwitchRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["switch_runtime"]

    @property
    def reset_runtime(
        self,
    ) -> Callable[
        [managed_service.ResetRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the reset runtime method over gRPC.

        Resets a Managed Notebook Runtime.

        Returns:
            Callable[[~.ResetRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reset_runtime" not in self._stubs:
            self._stubs["reset_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/ResetRuntime",
                request_serializer=managed_service.ResetRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["reset_runtime"]

    @property
    def upgrade_runtime(
        self,
    ) -> Callable[
        [managed_service.UpgradeRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the upgrade runtime method over gRPC.

        Upgrades a Managed Notebook Runtime to the latest
        version.

        Returns:
            Callable[[~.UpgradeRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "upgrade_runtime" not in self._stubs:
            self._stubs["upgrade_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/UpgradeRuntime",
                request_serializer=managed_service.UpgradeRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["upgrade_runtime"]

    @property
    def report_runtime_event(
        self,
    ) -> Callable[
        [managed_service.ReportRuntimeEventRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the report runtime event method over gRPC.

        Report and process a runtime event.

        Returns:
            Callable[[~.ReportRuntimeEventRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "report_runtime_event" not in self._stubs:
            self._stubs["report_runtime_event"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/ReportRuntimeEvent",
                request_serializer=managed_service.ReportRuntimeEventRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["report_runtime_event"]

    @property
    def refresh_runtime_token_internal(
        self,
    ) -> Callable[
        [managed_service.RefreshRuntimeTokenInternalRequest],
        Awaitable[managed_service.RefreshRuntimeTokenInternalResponse],
    ]:
        r"""Return a callable for the refresh runtime token internal method over gRPC.

        Gets an access token for the consumer service account
        that the customer attached to the runtime. Only
        accessible from the tenant instance.

        Returns:
            Callable[[~.RefreshRuntimeTokenInternalRequest],
                    Awaitable[~.RefreshRuntimeTokenInternalResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "refresh_runtime_token_internal" not in self._stubs:
            self._stubs[
                "refresh_runtime_token_internal"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/RefreshRuntimeTokenInternal",
                request_serializer=managed_service.RefreshRuntimeTokenInternalRequest.serialize,
                response_deserializer=managed_service.RefreshRuntimeTokenInternalResponse.deserialize,
            )
        return self._stubs["refresh_runtime_token_internal"]

    @property
    def diagnose_runtime(
        self,
    ) -> Callable[
        [managed_service.DiagnoseRuntimeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the diagnose runtime method over gRPC.

        Creates a Diagnostic File and runs Diagnostic Tool
        given a Runtime.

        Returns:
            Callable[[~.DiagnoseRuntimeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "diagnose_runtime" not in self._stubs:
            self._stubs["diagnose_runtime"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.ManagedNotebookService/DiagnoseRuntime",
                request_serializer=managed_service.DiagnoseRuntimeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["diagnose_runtime"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_runtimes: self._wrap_method(
                self.list_runtimes,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_runtime: self._wrap_method(
                self.get_runtime,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_runtime: self._wrap_method(
                self.create_runtime,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_runtime: self._wrap_method(
                self.update_runtime,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_runtime: self._wrap_method(
                self.delete_runtime,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.start_runtime: self._wrap_method(
                self.start_runtime,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.stop_runtime: self._wrap_method(
                self.stop_runtime,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.switch_runtime: self._wrap_method(
                self.switch_runtime,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.reset_runtime: self._wrap_method(
                self.reset_runtime,
                default_timeout=None,
                client_info=client_info,
            ),
            self.upgrade_runtime: self._wrap_method(
                self.upgrade_runtime,
                default_timeout=None,
                client_info=client_info,
            ),
            self.report_runtime_event: self._wrap_method(
                self.report_runtime_event,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.refresh_runtime_token_internal: self._wrap_method(
                self.refresh_runtime_token_internal,
                default_timeout=None,
                client_info=client_info,
            ),
            self.diagnose_runtime: self._wrap_method(
                self.diagnose_runtime,
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


__all__ = ("ManagedNotebookServiceGrpcAsyncIOTransport",)
