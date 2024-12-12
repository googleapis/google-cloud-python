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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.visionai_v1alpha1.types import warehouse

from .base import DEFAULT_CLIENT_INFO, WarehouseTransport
from .grpc import WarehouseGrpcTransport

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
                    "serviceName": "google.cloud.visionai.v1alpha1.Warehouse",
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
                    "serviceName": "google.cloud.visionai.v1alpha1.Warehouse",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class WarehouseGrpcAsyncIOTransport(WarehouseTransport):
    """gRPC AsyncIO backend transport for Warehouse.

    Service that manages media content + metadata for streaming.

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
    def create_asset(
        self,
    ) -> Callable[[warehouse.CreateAssetRequest], Awaitable[warehouse.Asset]]:
        r"""Return a callable for the create asset method over gRPC.

        Creates an asset inside corpus.

        Returns:
            Callable[[~.CreateAssetRequest],
                    Awaitable[~.Asset]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_asset" not in self._stubs:
            self._stubs["create_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/CreateAsset",
                request_serializer=warehouse.CreateAssetRequest.serialize,
                response_deserializer=warehouse.Asset.deserialize,
            )
        return self._stubs["create_asset"]

    @property
    def update_asset(
        self,
    ) -> Callable[[warehouse.UpdateAssetRequest], Awaitable[warehouse.Asset]]:
        r"""Return a callable for the update asset method over gRPC.

        Updates an asset inside corpus.

        Returns:
            Callable[[~.UpdateAssetRequest],
                    Awaitable[~.Asset]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_asset" not in self._stubs:
            self._stubs["update_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/UpdateAsset",
                request_serializer=warehouse.UpdateAssetRequest.serialize,
                response_deserializer=warehouse.Asset.deserialize,
            )
        return self._stubs["update_asset"]

    @property
    def get_asset(
        self,
    ) -> Callable[[warehouse.GetAssetRequest], Awaitable[warehouse.Asset]]:
        r"""Return a callable for the get asset method over gRPC.

        Reads an asset inside corpus.

        Returns:
            Callable[[~.GetAssetRequest],
                    Awaitable[~.Asset]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_asset" not in self._stubs:
            self._stubs["get_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/GetAsset",
                request_serializer=warehouse.GetAssetRequest.serialize,
                response_deserializer=warehouse.Asset.deserialize,
            )
        return self._stubs["get_asset"]

    @property
    def list_assets(
        self,
    ) -> Callable[
        [warehouse.ListAssetsRequest], Awaitable[warehouse.ListAssetsResponse]
    ]:
        r"""Return a callable for the list assets method over gRPC.

        Lists an list of assets inside corpus.

        Returns:
            Callable[[~.ListAssetsRequest],
                    Awaitable[~.ListAssetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_assets" not in self._stubs:
            self._stubs["list_assets"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/ListAssets",
                request_serializer=warehouse.ListAssetsRequest.serialize,
                response_deserializer=warehouse.ListAssetsResponse.deserialize,
            )
        return self._stubs["list_assets"]

    @property
    def delete_asset(
        self,
    ) -> Callable[[warehouse.DeleteAssetRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete asset method over gRPC.

        Deletes asset inside corpus.

        Returns:
            Callable[[~.DeleteAssetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_asset" not in self._stubs:
            self._stubs["delete_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/DeleteAsset",
                request_serializer=warehouse.DeleteAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_asset"]

    @property
    def create_corpus(
        self,
    ) -> Callable[[warehouse.CreateCorpusRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create corpus method over gRPC.

        Creates a corpus inside a project.

        Returns:
            Callable[[~.CreateCorpusRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_corpus" not in self._stubs:
            self._stubs["create_corpus"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/CreateCorpus",
                request_serializer=warehouse.CreateCorpusRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_corpus"]

    @property
    def get_corpus(
        self,
    ) -> Callable[[warehouse.GetCorpusRequest], Awaitable[warehouse.Corpus]]:
        r"""Return a callable for the get corpus method over gRPC.

        Gets corpus details inside a project.

        Returns:
            Callable[[~.GetCorpusRequest],
                    Awaitable[~.Corpus]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_corpus" not in self._stubs:
            self._stubs["get_corpus"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/GetCorpus",
                request_serializer=warehouse.GetCorpusRequest.serialize,
                response_deserializer=warehouse.Corpus.deserialize,
            )
        return self._stubs["get_corpus"]

    @property
    def update_corpus(
        self,
    ) -> Callable[[warehouse.UpdateCorpusRequest], Awaitable[warehouse.Corpus]]:
        r"""Return a callable for the update corpus method over gRPC.

        Updates a corpus in a project.

        Returns:
            Callable[[~.UpdateCorpusRequest],
                    Awaitable[~.Corpus]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_corpus" not in self._stubs:
            self._stubs["update_corpus"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/UpdateCorpus",
                request_serializer=warehouse.UpdateCorpusRequest.serialize,
                response_deserializer=warehouse.Corpus.deserialize,
            )
        return self._stubs["update_corpus"]

    @property
    def list_corpora(
        self,
    ) -> Callable[
        [warehouse.ListCorporaRequest], Awaitable[warehouse.ListCorporaResponse]
    ]:
        r"""Return a callable for the list corpora method over gRPC.

        Lists all corpora in a project.

        Returns:
            Callable[[~.ListCorporaRequest],
                    Awaitable[~.ListCorporaResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_corpora" not in self._stubs:
            self._stubs["list_corpora"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/ListCorpora",
                request_serializer=warehouse.ListCorporaRequest.serialize,
                response_deserializer=warehouse.ListCorporaResponse.deserialize,
            )
        return self._stubs["list_corpora"]

    @property
    def delete_corpus(
        self,
    ) -> Callable[[warehouse.DeleteCorpusRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete corpus method over gRPC.

        Deletes a corpus only if its empty.
        Returns empty response.

        Returns:
            Callable[[~.DeleteCorpusRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_corpus" not in self._stubs:
            self._stubs["delete_corpus"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/DeleteCorpus",
                request_serializer=warehouse.DeleteCorpusRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_corpus"]

    @property
    def create_data_schema(
        self,
    ) -> Callable[[warehouse.CreateDataSchemaRequest], Awaitable[warehouse.DataSchema]]:
        r"""Return a callable for the create data schema method over gRPC.

        Creates data schema inside corpus.

        Returns:
            Callable[[~.CreateDataSchemaRequest],
                    Awaitable[~.DataSchema]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_data_schema" not in self._stubs:
            self._stubs["create_data_schema"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/CreateDataSchema",
                request_serializer=warehouse.CreateDataSchemaRequest.serialize,
                response_deserializer=warehouse.DataSchema.deserialize,
            )
        return self._stubs["create_data_schema"]

    @property
    def update_data_schema(
        self,
    ) -> Callable[[warehouse.UpdateDataSchemaRequest], Awaitable[warehouse.DataSchema]]:
        r"""Return a callable for the update data schema method over gRPC.

        Updates data schema inside corpus.

        Returns:
            Callable[[~.UpdateDataSchemaRequest],
                    Awaitable[~.DataSchema]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_schema" not in self._stubs:
            self._stubs["update_data_schema"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/UpdateDataSchema",
                request_serializer=warehouse.UpdateDataSchemaRequest.serialize,
                response_deserializer=warehouse.DataSchema.deserialize,
            )
        return self._stubs["update_data_schema"]

    @property
    def get_data_schema(
        self,
    ) -> Callable[[warehouse.GetDataSchemaRequest], Awaitable[warehouse.DataSchema]]:
        r"""Return a callable for the get data schema method over gRPC.

        Gets data schema inside corpus.

        Returns:
            Callable[[~.GetDataSchemaRequest],
                    Awaitable[~.DataSchema]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_schema" not in self._stubs:
            self._stubs["get_data_schema"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/GetDataSchema",
                request_serializer=warehouse.GetDataSchemaRequest.serialize,
                response_deserializer=warehouse.DataSchema.deserialize,
            )
        return self._stubs["get_data_schema"]

    @property
    def delete_data_schema(
        self,
    ) -> Callable[[warehouse.DeleteDataSchemaRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete data schema method over gRPC.

        Deletes data schema inside corpus.

        Returns:
            Callable[[~.DeleteDataSchemaRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_data_schema" not in self._stubs:
            self._stubs["delete_data_schema"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/DeleteDataSchema",
                request_serializer=warehouse.DeleteDataSchemaRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_data_schema"]

    @property
    def list_data_schemas(
        self,
    ) -> Callable[
        [warehouse.ListDataSchemasRequest], Awaitable[warehouse.ListDataSchemasResponse]
    ]:
        r"""Return a callable for the list data schemas method over gRPC.

        Lists a list of data schemas inside corpus.

        Returns:
            Callable[[~.ListDataSchemasRequest],
                    Awaitable[~.ListDataSchemasResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_data_schemas" not in self._stubs:
            self._stubs["list_data_schemas"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/ListDataSchemas",
                request_serializer=warehouse.ListDataSchemasRequest.serialize,
                response_deserializer=warehouse.ListDataSchemasResponse.deserialize,
            )
        return self._stubs["list_data_schemas"]

    @property
    def create_annotation(
        self,
    ) -> Callable[[warehouse.CreateAnnotationRequest], Awaitable[warehouse.Annotation]]:
        r"""Return a callable for the create annotation method over gRPC.

        Creates annotation inside asset.

        Returns:
            Callable[[~.CreateAnnotationRequest],
                    Awaitable[~.Annotation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_annotation" not in self._stubs:
            self._stubs["create_annotation"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/CreateAnnotation",
                request_serializer=warehouse.CreateAnnotationRequest.serialize,
                response_deserializer=warehouse.Annotation.deserialize,
            )
        return self._stubs["create_annotation"]

    @property
    def get_annotation(
        self,
    ) -> Callable[[warehouse.GetAnnotationRequest], Awaitable[warehouse.Annotation]]:
        r"""Return a callable for the get annotation method over gRPC.

        Reads annotation inside asset.

        Returns:
            Callable[[~.GetAnnotationRequest],
                    Awaitable[~.Annotation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_annotation" not in self._stubs:
            self._stubs["get_annotation"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/GetAnnotation",
                request_serializer=warehouse.GetAnnotationRequest.serialize,
                response_deserializer=warehouse.Annotation.deserialize,
            )
        return self._stubs["get_annotation"]

    @property
    def list_annotations(
        self,
    ) -> Callable[
        [warehouse.ListAnnotationsRequest], Awaitable[warehouse.ListAnnotationsResponse]
    ]:
        r"""Return a callable for the list annotations method over gRPC.

        Lists a list of annotations inside asset.

        Returns:
            Callable[[~.ListAnnotationsRequest],
                    Awaitable[~.ListAnnotationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_annotations" not in self._stubs:
            self._stubs["list_annotations"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/ListAnnotations",
                request_serializer=warehouse.ListAnnotationsRequest.serialize,
                response_deserializer=warehouse.ListAnnotationsResponse.deserialize,
            )
        return self._stubs["list_annotations"]

    @property
    def update_annotation(
        self,
    ) -> Callable[[warehouse.UpdateAnnotationRequest], Awaitable[warehouse.Annotation]]:
        r"""Return a callable for the update annotation method over gRPC.

        Updates annotation inside asset.

        Returns:
            Callable[[~.UpdateAnnotationRequest],
                    Awaitable[~.Annotation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_annotation" not in self._stubs:
            self._stubs["update_annotation"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/UpdateAnnotation",
                request_serializer=warehouse.UpdateAnnotationRequest.serialize,
                response_deserializer=warehouse.Annotation.deserialize,
            )
        return self._stubs["update_annotation"]

    @property
    def delete_annotation(
        self,
    ) -> Callable[[warehouse.DeleteAnnotationRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete annotation method over gRPC.

        Deletes annotation inside asset.

        Returns:
            Callable[[~.DeleteAnnotationRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_annotation" not in self._stubs:
            self._stubs["delete_annotation"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/DeleteAnnotation",
                request_serializer=warehouse.DeleteAnnotationRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_annotation"]

    @property
    def ingest_asset(
        self,
    ) -> Callable[
        [warehouse.IngestAssetRequest], Awaitable[warehouse.IngestAssetResponse]
    ]:
        r"""Return a callable for the ingest asset method over gRPC.

        Ingests data for the asset. It is not allowed to
        ingest a data chunk which is already expired according
        to TTL. This method is only available via the gRPC API
        (not HTTP since bi-directional streaming is not
        supported via HTTP).

        Returns:
            Callable[[~.IngestAssetRequest],
                    Awaitable[~.IngestAssetResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "ingest_asset" not in self._stubs:
            self._stubs["ingest_asset"] = self._logged_channel.stream_stream(
                "/google.cloud.visionai.v1alpha1.Warehouse/IngestAsset",
                request_serializer=warehouse.IngestAssetRequest.serialize,
                response_deserializer=warehouse.IngestAssetResponse.deserialize,
            )
        return self._stubs["ingest_asset"]

    @property
    def clip_asset(
        self,
    ) -> Callable[[warehouse.ClipAssetRequest], Awaitable[warehouse.ClipAssetResponse]]:
        r"""Return a callable for the clip asset method over gRPC.

        Generates clips for downloading. The api takes in a time range,
        and generates a clip of the first content available after
        start_time and before end_time, which may overflow beyond these
        bounds. Returned clips are truncated if the total size of the
        clips are larger than 100MB.

        Returns:
            Callable[[~.ClipAssetRequest],
                    Awaitable[~.ClipAssetResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "clip_asset" not in self._stubs:
            self._stubs["clip_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/ClipAsset",
                request_serializer=warehouse.ClipAssetRequest.serialize,
                response_deserializer=warehouse.ClipAssetResponse.deserialize,
            )
        return self._stubs["clip_asset"]

    @property
    def generate_hls_uri(
        self,
    ) -> Callable[
        [warehouse.GenerateHlsUriRequest], Awaitable[warehouse.GenerateHlsUriResponse]
    ]:
        r"""Return a callable for the generate hls uri method over gRPC.

        Generates a uri for an HLS manifest. The api takes in
        a collection of time ranges, and generates a URI for an
        HLS manifest that covers all the requested time ranges.

        Returns:
            Callable[[~.GenerateHlsUriRequest],
                    Awaitable[~.GenerateHlsUriResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_hls_uri" not in self._stubs:
            self._stubs["generate_hls_uri"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/GenerateHlsUri",
                request_serializer=warehouse.GenerateHlsUriRequest.serialize,
                response_deserializer=warehouse.GenerateHlsUriResponse.deserialize,
            )
        return self._stubs["generate_hls_uri"]

    @property
    def create_search_config(
        self,
    ) -> Callable[
        [warehouse.CreateSearchConfigRequest], Awaitable[warehouse.SearchConfig]
    ]:
        r"""Return a callable for the create search config method over gRPC.

        Creates a search configuration inside a corpus.

        Please follow the rules below to create a valid
        CreateSearchConfigRequest. --- General Rules ---

        1. Request.search_config_id must not be associated with an
           existing SearchConfig.
        2. Request must contain at least one non-empty
           search_criteria_property or facet_property.
        3. mapped_fields must not be empty, and must map to existing UGA
           keys.
        4. All mapped_fields must be of the same type.
        5. All mapped_fields must share the same granularity.
        6. All mapped_fields must share the same semantic SearchConfig
           match options. For property-specific rules, please reference
           the comments for FacetProperty and SearchCriteriaProperty.

        Returns:
            Callable[[~.CreateSearchConfigRequest],
                    Awaitable[~.SearchConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_search_config" not in self._stubs:
            self._stubs["create_search_config"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/CreateSearchConfig",
                request_serializer=warehouse.CreateSearchConfigRequest.serialize,
                response_deserializer=warehouse.SearchConfig.deserialize,
            )
        return self._stubs["create_search_config"]

    @property
    def update_search_config(
        self,
    ) -> Callable[
        [warehouse.UpdateSearchConfigRequest], Awaitable[warehouse.SearchConfig]
    ]:
        r"""Return a callable for the update search config method over gRPC.

        Updates a search configuration inside a corpus.

        Please follow the rules below to create a valid
        UpdateSearchConfigRequest. --- General Rules ---

        1. Request.search_configuration.name must already exist.
        2. Request must contain at least one non-empty
           search_criteria_property or facet_property.
        3. mapped_fields must not be empty, and must map to existing UGA
           keys.
        4. All mapped_fields must be of the same type.
        5. All mapped_fields must share the same granularity.
        6. All mapped_fields must share the same semantic SearchConfig
           match options. For property-specific rules, please reference
           the comments for FacetProperty and SearchCriteriaProperty.

        Returns:
            Callable[[~.UpdateSearchConfigRequest],
                    Awaitable[~.SearchConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_search_config" not in self._stubs:
            self._stubs["update_search_config"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/UpdateSearchConfig",
                request_serializer=warehouse.UpdateSearchConfigRequest.serialize,
                response_deserializer=warehouse.SearchConfig.deserialize,
            )
        return self._stubs["update_search_config"]

    @property
    def get_search_config(
        self,
    ) -> Callable[
        [warehouse.GetSearchConfigRequest], Awaitable[warehouse.SearchConfig]
    ]:
        r"""Return a callable for the get search config method over gRPC.

        Gets a search configuration inside a corpus.

        Returns:
            Callable[[~.GetSearchConfigRequest],
                    Awaitable[~.SearchConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_search_config" not in self._stubs:
            self._stubs["get_search_config"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/GetSearchConfig",
                request_serializer=warehouse.GetSearchConfigRequest.serialize,
                response_deserializer=warehouse.SearchConfig.deserialize,
            )
        return self._stubs["get_search_config"]

    @property
    def delete_search_config(
        self,
    ) -> Callable[[warehouse.DeleteSearchConfigRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete search config method over gRPC.

        Deletes a search configuration inside a corpus.

        For a DeleteSearchConfigRequest to be valid,
        Request.search_configuration.name must already exist.

        Returns:
            Callable[[~.DeleteSearchConfigRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_search_config" not in self._stubs:
            self._stubs["delete_search_config"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/DeleteSearchConfig",
                request_serializer=warehouse.DeleteSearchConfigRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_search_config"]

    @property
    def list_search_configs(
        self,
    ) -> Callable[
        [warehouse.ListSearchConfigsRequest],
        Awaitable[warehouse.ListSearchConfigsResponse],
    ]:
        r"""Return a callable for the list search configs method over gRPC.

        Lists all search configurations inside a corpus.

        Returns:
            Callable[[~.ListSearchConfigsRequest],
                    Awaitable[~.ListSearchConfigsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_search_configs" not in self._stubs:
            self._stubs["list_search_configs"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/ListSearchConfigs",
                request_serializer=warehouse.ListSearchConfigsRequest.serialize,
                response_deserializer=warehouse.ListSearchConfigsResponse.deserialize,
            )
        return self._stubs["list_search_configs"]

    @property
    def search_assets(
        self,
    ) -> Callable[
        [warehouse.SearchAssetsRequest], Awaitable[warehouse.SearchAssetsResponse]
    ]:
        r"""Return a callable for the search assets method over gRPC.

        Search media asset.

        Returns:
            Callable[[~.SearchAssetsRequest],
                    Awaitable[~.SearchAssetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_assets" not in self._stubs:
            self._stubs["search_assets"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1alpha1.Warehouse/SearchAssets",
                request_serializer=warehouse.SearchAssetsRequest.serialize,
                response_deserializer=warehouse.SearchAssetsResponse.deserialize,
            )
        return self._stubs["search_assets"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_asset: self._wrap_method(
                self.create_asset,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=120.0,
                    multiplier=2.5,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_asset: self._wrap_method(
                self.update_asset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_asset: self._wrap_method(
                self.get_asset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_assets: self._wrap_method(
                self.list_assets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_asset: self._wrap_method(
                self.delete_asset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_corpus: self._wrap_method(
                self.create_corpus,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=120.0,
                    multiplier=2.5,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.get_corpus: self._wrap_method(
                self.get_corpus,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_corpus: self._wrap_method(
                self.update_corpus,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_corpora: self._wrap_method(
                self.list_corpora,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_corpus: self._wrap_method(
                self.delete_corpus,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_data_schema: self._wrap_method(
                self.create_data_schema,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=120.0,
                    multiplier=2.5,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_data_schema: self._wrap_method(
                self.update_data_schema,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_data_schema: self._wrap_method(
                self.get_data_schema,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_data_schema: self._wrap_method(
                self.delete_data_schema,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_data_schemas: self._wrap_method(
                self.list_data_schemas,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_annotation: self._wrap_method(
                self.create_annotation,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=120.0,
                    multiplier=2.5,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.get_annotation: self._wrap_method(
                self.get_annotation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_annotations: self._wrap_method(
                self.list_annotations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_annotation: self._wrap_method(
                self.update_annotation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_annotation: self._wrap_method(
                self.delete_annotation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.ingest_asset: self._wrap_method(
                self.ingest_asset,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=120.0,
                    multiplier=2.5,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.clip_asset: self._wrap_method(
                self.clip_asset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_hls_uri: self._wrap_method(
                self.generate_hls_uri,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_search_config: self._wrap_method(
                self.create_search_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_search_config: self._wrap_method(
                self.update_search_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_search_config: self._wrap_method(
                self.get_search_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_search_config: self._wrap_method(
                self.delete_search_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_search_configs: self._wrap_method(
                self.list_search_configs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.search_assets: self._wrap_method(
                self.search_assets,
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


__all__ = ("WarehouseGrpcAsyncIOTransport",)
