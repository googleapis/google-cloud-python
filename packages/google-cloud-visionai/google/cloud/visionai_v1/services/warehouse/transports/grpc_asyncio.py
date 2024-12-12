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

from google.cloud.visionai_v1.types import warehouse

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
                    "serviceName": "google.cloud.visionai.v1.Warehouse",
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
                    "serviceName": "google.cloud.visionai.v1.Warehouse",
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
                "/google.cloud.visionai.v1.Warehouse/CreateAsset",
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
                "/google.cloud.visionai.v1.Warehouse/UpdateAsset",
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
                "/google.cloud.visionai.v1.Warehouse/GetAsset",
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
                "/google.cloud.visionai.v1.Warehouse/ListAssets",
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
                "/google.cloud.visionai.v1.Warehouse/DeleteAsset",
                request_serializer=warehouse.DeleteAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_asset"]

    @property
    def upload_asset(
        self,
    ) -> Callable[[warehouse.UploadAssetRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the upload asset method over gRPC.

        Upload asset by specifing the asset Cloud Storage
        uri. For video warehouse, it requires users who call
        this API have read access to the cloud storage file.
        Once it is uploaded, it can be retrieved by
        GenerateRetrievalUrl API which by default, only can
        retrieve cloud storage files from the same project of
        the warehouse. To allow retrieval cloud storage files
        that are in a separate project, it requires to find the
        vision ai service account (Go to IAM, check checkbox to
        show "Include Google-provided role grants", search for
        "Cloud Vision AI Service Agent") and grant the read
        access of the cloud storage files to that service
        account.

        Returns:
            Callable[[~.UploadAssetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "upload_asset" not in self._stubs:
            self._stubs["upload_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/UploadAsset",
                request_serializer=warehouse.UploadAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["upload_asset"]

    @property
    def generate_retrieval_url(
        self,
    ) -> Callable[
        [warehouse.GenerateRetrievalUrlRequest],
        Awaitable[warehouse.GenerateRetrievalUrlResponse],
    ]:
        r"""Return a callable for the generate retrieval url method over gRPC.

        Generates a signed url for downloading the asset.
        For video warehouse, please see comment of UploadAsset
        about how to allow retrieval of cloud storage files in a
        different project.

        Returns:
            Callable[[~.GenerateRetrievalUrlRequest],
                    Awaitable[~.GenerateRetrievalUrlResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_retrieval_url" not in self._stubs:
            self._stubs["generate_retrieval_url"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/GenerateRetrievalUrl",
                request_serializer=warehouse.GenerateRetrievalUrlRequest.serialize,
                response_deserializer=warehouse.GenerateRetrievalUrlResponse.deserialize,
            )
        return self._stubs["generate_retrieval_url"]

    @property
    def analyze_asset(
        self,
    ) -> Callable[[warehouse.AnalyzeAssetRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the analyze asset method over gRPC.

        Analyze asset to power search capability.

        Returns:
            Callable[[~.AnalyzeAssetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_asset" not in self._stubs:
            self._stubs["analyze_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/AnalyzeAsset",
                request_serializer=warehouse.AnalyzeAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["analyze_asset"]

    @property
    def index_asset(
        self,
    ) -> Callable[[warehouse.IndexAssetRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the index asset method over gRPC.

        Index one asset for search. Supported corpus type:
        Corpus.Type.VIDEO_ON_DEMAND

        Returns:
            Callable[[~.IndexAssetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "index_asset" not in self._stubs:
            self._stubs["index_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/IndexAsset",
                request_serializer=warehouse.IndexAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["index_asset"]

    @property
    def remove_index_asset(
        self,
    ) -> Callable[
        [warehouse.RemoveIndexAssetRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the remove index asset method over gRPC.

        Remove one asset's index data for search. Supported corpus type:
        Corpus.Type.VIDEO_ON_DEMAND

        Returns:
            Callable[[~.RemoveIndexAssetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_index_asset" not in self._stubs:
            self._stubs["remove_index_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/RemoveIndexAsset",
                request_serializer=warehouse.RemoveIndexAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["remove_index_asset"]

    @property
    def view_indexed_assets(
        self,
    ) -> Callable[
        [warehouse.ViewIndexedAssetsRequest],
        Awaitable[warehouse.ViewIndexedAssetsResponse],
    ]:
        r"""Return a callable for the view indexed assets method over gRPC.

        Lists assets inside an index.

        Returns:
            Callable[[~.ViewIndexedAssetsRequest],
                    Awaitable[~.ViewIndexedAssetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "view_indexed_assets" not in self._stubs:
            self._stubs["view_indexed_assets"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/ViewIndexedAssets",
                request_serializer=warehouse.ViewIndexedAssetsRequest.serialize,
                response_deserializer=warehouse.ViewIndexedAssetsResponse.deserialize,
            )
        return self._stubs["view_indexed_assets"]

    @property
    def create_index(
        self,
    ) -> Callable[[warehouse.CreateIndexRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create index method over gRPC.

        Creates an Index under the corpus.

        Returns:
            Callable[[~.CreateIndexRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_index" not in self._stubs:
            self._stubs["create_index"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/CreateIndex",
                request_serializer=warehouse.CreateIndexRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_index"]

    @property
    def update_index(
        self,
    ) -> Callable[[warehouse.UpdateIndexRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update index method over gRPC.

        Updates an Index under the corpus. Users can perform a
        metadata-only update or trigger a full index rebuild with
        different update_mask values.

        Returns:
            Callable[[~.UpdateIndexRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_index" not in self._stubs:
            self._stubs["update_index"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/UpdateIndex",
                request_serializer=warehouse.UpdateIndexRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_index"]

    @property
    def get_index(
        self,
    ) -> Callable[[warehouse.GetIndexRequest], Awaitable[warehouse.Index]]:
        r"""Return a callable for the get index method over gRPC.

        Gets the details of a single Index under a Corpus.

        Returns:
            Callable[[~.GetIndexRequest],
                    Awaitable[~.Index]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_index" not in self._stubs:
            self._stubs["get_index"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/GetIndex",
                request_serializer=warehouse.GetIndexRequest.serialize,
                response_deserializer=warehouse.Index.deserialize,
            )
        return self._stubs["get_index"]

    @property
    def list_indexes(
        self,
    ) -> Callable[
        [warehouse.ListIndexesRequest], Awaitable[warehouse.ListIndexesResponse]
    ]:
        r"""Return a callable for the list indexes method over gRPC.

        List all Indexes in a given Corpus.

        Returns:
            Callable[[~.ListIndexesRequest],
                    Awaitable[~.ListIndexesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_indexes" not in self._stubs:
            self._stubs["list_indexes"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/ListIndexes",
                request_serializer=warehouse.ListIndexesRequest.serialize,
                response_deserializer=warehouse.ListIndexesResponse.deserialize,
            )
        return self._stubs["list_indexes"]

    @property
    def delete_index(
        self,
    ) -> Callable[[warehouse.DeleteIndexRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete index method over gRPC.

        Delete a single Index. In order to delete an index,
        the caller must make sure that it is not deployed to any
        index endpoint.

        Returns:
            Callable[[~.DeleteIndexRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_index" not in self._stubs:
            self._stubs["delete_index"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/DeleteIndex",
                request_serializer=warehouse.DeleteIndexRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_index"]

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
                "/google.cloud.visionai.v1.Warehouse/CreateCorpus",
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
                "/google.cloud.visionai.v1.Warehouse/GetCorpus",
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
                "/google.cloud.visionai.v1.Warehouse/UpdateCorpus",
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
                "/google.cloud.visionai.v1.Warehouse/ListCorpora",
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
                "/google.cloud.visionai.v1.Warehouse/DeleteCorpus",
                request_serializer=warehouse.DeleteCorpusRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_corpus"]

    @property
    def analyze_corpus(
        self,
    ) -> Callable[
        [warehouse.AnalyzeCorpusRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the analyze corpus method over gRPC.

        Analyzes a corpus.

        Returns:
            Callable[[~.AnalyzeCorpusRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_corpus" not in self._stubs:
            self._stubs["analyze_corpus"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/AnalyzeCorpus",
                request_serializer=warehouse.AnalyzeCorpusRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["analyze_corpus"]

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
                "/google.cloud.visionai.v1.Warehouse/CreateDataSchema",
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
                "/google.cloud.visionai.v1.Warehouse/UpdateDataSchema",
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
                "/google.cloud.visionai.v1.Warehouse/GetDataSchema",
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
                "/google.cloud.visionai.v1.Warehouse/DeleteDataSchema",
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
                "/google.cloud.visionai.v1.Warehouse/ListDataSchemas",
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
                "/google.cloud.visionai.v1.Warehouse/CreateAnnotation",
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
                "/google.cloud.visionai.v1.Warehouse/GetAnnotation",
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
                "/google.cloud.visionai.v1.Warehouse/ListAnnotations",
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
                "/google.cloud.visionai.v1.Warehouse/UpdateAnnotation",
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
                "/google.cloud.visionai.v1.Warehouse/DeleteAnnotation",
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
                "/google.cloud.visionai.v1.Warehouse/IngestAsset",
                request_serializer=warehouse.IngestAssetRequest.serialize,
                response_deserializer=warehouse.IngestAssetResponse.deserialize,
            )
        return self._stubs["ingest_asset"]

    @property
    def clip_asset(
        self,
    ) -> Callable[[warehouse.ClipAssetRequest], Awaitable[warehouse.ClipAssetResponse]]:
        r"""Return a callable for the clip asset method over gRPC.

        Supported by STREAM_VIDEO corpus type. Generates clips for
        downloading. The api takes in a time range, and generates a clip
        of the first content available after start_time and before
        end_time, which may overflow beyond these bounds. Returned clips
        are truncated if the total size of the clips are larger than
        100MB.

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
                "/google.cloud.visionai.v1.Warehouse/ClipAsset",
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
                "/google.cloud.visionai.v1.Warehouse/GenerateHlsUri",
                request_serializer=warehouse.GenerateHlsUriRequest.serialize,
                response_deserializer=warehouse.GenerateHlsUriResponse.deserialize,
            )
        return self._stubs["generate_hls_uri"]

    @property
    def import_assets(
        self,
    ) -> Callable[[warehouse.ImportAssetsRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the import assets method over gRPC.

        Imports assets (images plus annotations) from a meta
        file on cloud storage. Each row in the meta file is
        corresponding to an image (specified by a cloud storage
        uri) and its annotations.

        Returns:
            Callable[[~.ImportAssetsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_assets" not in self._stubs:
            self._stubs["import_assets"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/ImportAssets",
                request_serializer=warehouse.ImportAssetsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_assets"]

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
                "/google.cloud.visionai.v1.Warehouse/CreateSearchConfig",
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
                "/google.cloud.visionai.v1.Warehouse/UpdateSearchConfig",
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
                "/google.cloud.visionai.v1.Warehouse/GetSearchConfig",
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
                "/google.cloud.visionai.v1.Warehouse/DeleteSearchConfig",
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
                "/google.cloud.visionai.v1.Warehouse/ListSearchConfigs",
                request_serializer=warehouse.ListSearchConfigsRequest.serialize,
                response_deserializer=warehouse.ListSearchConfigsResponse.deserialize,
            )
        return self._stubs["list_search_configs"]

    @property
    def create_search_hypernym(
        self,
    ) -> Callable[
        [warehouse.CreateSearchHypernymRequest], Awaitable[warehouse.SearchHypernym]
    ]:
        r"""Return a callable for the create search hypernym method over gRPC.

        Creates a SearchHypernym inside a corpus.

        Returns:
            Callable[[~.CreateSearchHypernymRequest],
                    Awaitable[~.SearchHypernym]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_search_hypernym" not in self._stubs:
            self._stubs["create_search_hypernym"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/CreateSearchHypernym",
                request_serializer=warehouse.CreateSearchHypernymRequest.serialize,
                response_deserializer=warehouse.SearchHypernym.deserialize,
            )
        return self._stubs["create_search_hypernym"]

    @property
    def update_search_hypernym(
        self,
    ) -> Callable[
        [warehouse.UpdateSearchHypernymRequest], Awaitable[warehouse.SearchHypernym]
    ]:
        r"""Return a callable for the update search hypernym method over gRPC.

        Updates a SearchHypernym inside a corpus.

        Returns:
            Callable[[~.UpdateSearchHypernymRequest],
                    Awaitable[~.SearchHypernym]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_search_hypernym" not in self._stubs:
            self._stubs["update_search_hypernym"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/UpdateSearchHypernym",
                request_serializer=warehouse.UpdateSearchHypernymRequest.serialize,
                response_deserializer=warehouse.SearchHypernym.deserialize,
            )
        return self._stubs["update_search_hypernym"]

    @property
    def get_search_hypernym(
        self,
    ) -> Callable[
        [warehouse.GetSearchHypernymRequest], Awaitable[warehouse.SearchHypernym]
    ]:
        r"""Return a callable for the get search hypernym method over gRPC.

        Gets a SearchHypernym inside a corpus.

        Returns:
            Callable[[~.GetSearchHypernymRequest],
                    Awaitable[~.SearchHypernym]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_search_hypernym" not in self._stubs:
            self._stubs["get_search_hypernym"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/GetSearchHypernym",
                request_serializer=warehouse.GetSearchHypernymRequest.serialize,
                response_deserializer=warehouse.SearchHypernym.deserialize,
            )
        return self._stubs["get_search_hypernym"]

    @property
    def delete_search_hypernym(
        self,
    ) -> Callable[[warehouse.DeleteSearchHypernymRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete search hypernym method over gRPC.

        Deletes a SearchHypernym inside a corpus.

        Returns:
            Callable[[~.DeleteSearchHypernymRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_search_hypernym" not in self._stubs:
            self._stubs["delete_search_hypernym"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/DeleteSearchHypernym",
                request_serializer=warehouse.DeleteSearchHypernymRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_search_hypernym"]

    @property
    def list_search_hypernyms(
        self,
    ) -> Callable[
        [warehouse.ListSearchHypernymsRequest],
        Awaitable[warehouse.ListSearchHypernymsResponse],
    ]:
        r"""Return a callable for the list search hypernyms method over gRPC.

        Lists SearchHypernyms inside a corpus.

        Returns:
            Callable[[~.ListSearchHypernymsRequest],
                    Awaitable[~.ListSearchHypernymsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_search_hypernyms" not in self._stubs:
            self._stubs["list_search_hypernyms"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/ListSearchHypernyms",
                request_serializer=warehouse.ListSearchHypernymsRequest.serialize,
                response_deserializer=warehouse.ListSearchHypernymsResponse.deserialize,
            )
        return self._stubs["list_search_hypernyms"]

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
                "/google.cloud.visionai.v1.Warehouse/SearchAssets",
                request_serializer=warehouse.SearchAssetsRequest.serialize,
                response_deserializer=warehouse.SearchAssetsResponse.deserialize,
            )
        return self._stubs["search_assets"]

    @property
    def search_index_endpoint(
        self,
    ) -> Callable[
        [warehouse.SearchIndexEndpointRequest],
        Awaitable[warehouse.SearchIndexEndpointResponse],
    ]:
        r"""Return a callable for the search index endpoint method over gRPC.

        Search a deployed index endpoint (IMAGE corpus type
        only).

        Returns:
            Callable[[~.SearchIndexEndpointRequest],
                    Awaitable[~.SearchIndexEndpointResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_index_endpoint" not in self._stubs:
            self._stubs["search_index_endpoint"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/SearchIndexEndpoint",
                request_serializer=warehouse.SearchIndexEndpointRequest.serialize,
                response_deserializer=warehouse.SearchIndexEndpointResponse.deserialize,
            )
        return self._stubs["search_index_endpoint"]

    @property
    def create_index_endpoint(
        self,
    ) -> Callable[
        [warehouse.CreateIndexEndpointRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create index endpoint method over gRPC.

        Creates an IndexEndpoint.

        Returns:
            Callable[[~.CreateIndexEndpointRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_index_endpoint" not in self._stubs:
            self._stubs["create_index_endpoint"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/CreateIndexEndpoint",
                request_serializer=warehouse.CreateIndexEndpointRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_index_endpoint"]

    @property
    def get_index_endpoint(
        self,
    ) -> Callable[
        [warehouse.GetIndexEndpointRequest], Awaitable[warehouse.IndexEndpoint]
    ]:
        r"""Return a callable for the get index endpoint method over gRPC.

        Gets an IndexEndpoint.

        Returns:
            Callable[[~.GetIndexEndpointRequest],
                    Awaitable[~.IndexEndpoint]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_index_endpoint" not in self._stubs:
            self._stubs["get_index_endpoint"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/GetIndexEndpoint",
                request_serializer=warehouse.GetIndexEndpointRequest.serialize,
                response_deserializer=warehouse.IndexEndpoint.deserialize,
            )
        return self._stubs["get_index_endpoint"]

    @property
    def list_index_endpoints(
        self,
    ) -> Callable[
        [warehouse.ListIndexEndpointsRequest],
        Awaitable[warehouse.ListIndexEndpointsResponse],
    ]:
        r"""Return a callable for the list index endpoints method over gRPC.

        Lists all IndexEndpoints in a project.

        Returns:
            Callable[[~.ListIndexEndpointsRequest],
                    Awaitable[~.ListIndexEndpointsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_index_endpoints" not in self._stubs:
            self._stubs["list_index_endpoints"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/ListIndexEndpoints",
                request_serializer=warehouse.ListIndexEndpointsRequest.serialize,
                response_deserializer=warehouse.ListIndexEndpointsResponse.deserialize,
            )
        return self._stubs["list_index_endpoints"]

    @property
    def update_index_endpoint(
        self,
    ) -> Callable[
        [warehouse.UpdateIndexEndpointRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update index endpoint method over gRPC.

        Updates an IndexEndpoint.

        Returns:
            Callable[[~.UpdateIndexEndpointRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_index_endpoint" not in self._stubs:
            self._stubs["update_index_endpoint"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/UpdateIndexEndpoint",
                request_serializer=warehouse.UpdateIndexEndpointRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_index_endpoint"]

    @property
    def delete_index_endpoint(
        self,
    ) -> Callable[
        [warehouse.DeleteIndexEndpointRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete index endpoint method over gRPC.

        Deletes an IndexEndpoint.

        Returns:
            Callable[[~.DeleteIndexEndpointRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_index_endpoint" not in self._stubs:
            self._stubs["delete_index_endpoint"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/DeleteIndexEndpoint",
                request_serializer=warehouse.DeleteIndexEndpointRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_index_endpoint"]

    @property
    def deploy_index(
        self,
    ) -> Callable[[warehouse.DeployIndexRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the deploy index method over gRPC.

        Deploys an Index to IndexEndpoint.

        Returns:
            Callable[[~.DeployIndexRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "deploy_index" not in self._stubs:
            self._stubs["deploy_index"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/DeployIndex",
                request_serializer=warehouse.DeployIndexRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["deploy_index"]

    @property
    def undeploy_index(
        self,
    ) -> Callable[
        [warehouse.UndeployIndexRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the undeploy index method over gRPC.

        Undeploys an Index from IndexEndpoint.

        Returns:
            Callable[[~.UndeployIndexRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "undeploy_index" not in self._stubs:
            self._stubs["undeploy_index"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/UndeployIndex",
                request_serializer=warehouse.UndeployIndexRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["undeploy_index"]

    @property
    def create_collection(
        self,
    ) -> Callable[
        [warehouse.CreateCollectionRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create collection method over gRPC.

        Creates a collection.

        Returns:
            Callable[[~.CreateCollectionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_collection" not in self._stubs:
            self._stubs["create_collection"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/CreateCollection",
                request_serializer=warehouse.CreateCollectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_collection"]

    @property
    def delete_collection(
        self,
    ) -> Callable[
        [warehouse.DeleteCollectionRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete collection method over gRPC.

        Deletes a collection.

        Returns:
            Callable[[~.DeleteCollectionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_collection" not in self._stubs:
            self._stubs["delete_collection"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/DeleteCollection",
                request_serializer=warehouse.DeleteCollectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_collection"]

    @property
    def get_collection(
        self,
    ) -> Callable[[warehouse.GetCollectionRequest], Awaitable[warehouse.Collection]]:
        r"""Return a callable for the get collection method over gRPC.

        Gets a collection.

        Returns:
            Callable[[~.GetCollectionRequest],
                    Awaitable[~.Collection]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_collection" not in self._stubs:
            self._stubs["get_collection"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/GetCollection",
                request_serializer=warehouse.GetCollectionRequest.serialize,
                response_deserializer=warehouse.Collection.deserialize,
            )
        return self._stubs["get_collection"]

    @property
    def update_collection(
        self,
    ) -> Callable[[warehouse.UpdateCollectionRequest], Awaitable[warehouse.Collection]]:
        r"""Return a callable for the update collection method over gRPC.

        Updates a collection.

        Returns:
            Callable[[~.UpdateCollectionRequest],
                    Awaitable[~.Collection]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_collection" not in self._stubs:
            self._stubs["update_collection"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/UpdateCollection",
                request_serializer=warehouse.UpdateCollectionRequest.serialize,
                response_deserializer=warehouse.Collection.deserialize,
            )
        return self._stubs["update_collection"]

    @property
    def list_collections(
        self,
    ) -> Callable[
        [warehouse.ListCollectionsRequest], Awaitable[warehouse.ListCollectionsResponse]
    ]:
        r"""Return a callable for the list collections method over gRPC.

        Lists collections inside a corpus.

        Returns:
            Callable[[~.ListCollectionsRequest],
                    Awaitable[~.ListCollectionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_collections" not in self._stubs:
            self._stubs["list_collections"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/ListCollections",
                request_serializer=warehouse.ListCollectionsRequest.serialize,
                response_deserializer=warehouse.ListCollectionsResponse.deserialize,
            )
        return self._stubs["list_collections"]

    @property
    def add_collection_item(
        self,
    ) -> Callable[
        [warehouse.AddCollectionItemRequest],
        Awaitable[warehouse.AddCollectionItemResponse],
    ]:
        r"""Return a callable for the add collection item method over gRPC.

        Adds an item into a Collection.

        Returns:
            Callable[[~.AddCollectionItemRequest],
                    Awaitable[~.AddCollectionItemResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_collection_item" not in self._stubs:
            self._stubs["add_collection_item"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/AddCollectionItem",
                request_serializer=warehouse.AddCollectionItemRequest.serialize,
                response_deserializer=warehouse.AddCollectionItemResponse.deserialize,
            )
        return self._stubs["add_collection_item"]

    @property
    def remove_collection_item(
        self,
    ) -> Callable[
        [warehouse.RemoveCollectionItemRequest],
        Awaitable[warehouse.RemoveCollectionItemResponse],
    ]:
        r"""Return a callable for the remove collection item method over gRPC.

        Removes an item from a collection.

        Returns:
            Callable[[~.RemoveCollectionItemRequest],
                    Awaitable[~.RemoveCollectionItemResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_collection_item" not in self._stubs:
            self._stubs["remove_collection_item"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/RemoveCollectionItem",
                request_serializer=warehouse.RemoveCollectionItemRequest.serialize,
                response_deserializer=warehouse.RemoveCollectionItemResponse.deserialize,
            )
        return self._stubs["remove_collection_item"]

    @property
    def view_collection_items(
        self,
    ) -> Callable[
        [warehouse.ViewCollectionItemsRequest],
        Awaitable[warehouse.ViewCollectionItemsResponse],
    ]:
        r"""Return a callable for the view collection items method over gRPC.

        View items inside a collection.

        Returns:
            Callable[[~.ViewCollectionItemsRequest],
                    Awaitable[~.ViewCollectionItemsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "view_collection_items" not in self._stubs:
            self._stubs["view_collection_items"] = self._logged_channel.unary_unary(
                "/google.cloud.visionai.v1.Warehouse/ViewCollectionItems",
                request_serializer=warehouse.ViewCollectionItemsRequest.serialize,
                response_deserializer=warehouse.ViewCollectionItemsResponse.deserialize,
            )
        return self._stubs["view_collection_items"]

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
            self.upload_asset: self._wrap_method(
                self.upload_asset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_retrieval_url: self._wrap_method(
                self.generate_retrieval_url,
                default_timeout=None,
                client_info=client_info,
            ),
            self.analyze_asset: self._wrap_method(
                self.analyze_asset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.index_asset: self._wrap_method(
                self.index_asset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.remove_index_asset: self._wrap_method(
                self.remove_index_asset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.view_indexed_assets: self._wrap_method(
                self.view_indexed_assets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_index: self._wrap_method(
                self.create_index,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_index: self._wrap_method(
                self.update_index,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_index: self._wrap_method(
                self.get_index,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_indexes: self._wrap_method(
                self.list_indexes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_index: self._wrap_method(
                self.delete_index,
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
            self.analyze_corpus: self._wrap_method(
                self.analyze_corpus,
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
            self.import_assets: self._wrap_method(
                self.import_assets,
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
            self.create_search_hypernym: self._wrap_method(
                self.create_search_hypernym,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_search_hypernym: self._wrap_method(
                self.update_search_hypernym,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_search_hypernym: self._wrap_method(
                self.get_search_hypernym,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_search_hypernym: self._wrap_method(
                self.delete_search_hypernym,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_search_hypernyms: self._wrap_method(
                self.list_search_hypernyms,
                default_timeout=None,
                client_info=client_info,
            ),
            self.search_assets: self._wrap_method(
                self.search_assets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.search_index_endpoint: self._wrap_method(
                self.search_index_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_index_endpoint: self._wrap_method(
                self.create_index_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_index_endpoint: self._wrap_method(
                self.get_index_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_index_endpoints: self._wrap_method(
                self.list_index_endpoints,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_index_endpoint: self._wrap_method(
                self.update_index_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_index_endpoint: self._wrap_method(
                self.delete_index_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.deploy_index: self._wrap_method(
                self.deploy_index,
                default_timeout=None,
                client_info=client_info,
            ),
            self.undeploy_index: self._wrap_method(
                self.undeploy_index,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_collection: self._wrap_method(
                self.create_collection,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_collection: self._wrap_method(
                self.delete_collection,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_collection: self._wrap_method(
                self.get_collection,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_collection: self._wrap_method(
                self.update_collection,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_collections: self._wrap_method(
                self.list_collections,
                default_timeout=None,
                client_info=client_info,
            ),
            self.add_collection_item: self._wrap_method(
                self.add_collection_item,
                default_timeout=None,
                client_info=client_info,
            ),
            self.remove_collection_item: self._wrap_method(
                self.remove_collection_item,
                default_timeout=None,
                client_info=client_info,
            ),
            self.view_collection_items: self._wrap_method(
                self.view_collection_items,
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


__all__ = ("WarehouseGrpcAsyncIOTransport",)
